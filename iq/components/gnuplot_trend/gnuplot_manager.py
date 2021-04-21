#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot charting management manager class.

Gnuplot usage command examples:

gnuplot -e "
set xdata time;
set timefmt '%H:%M:%S';
set format x '%H:%M:%S';
set xrange['00:00:00':'00:00:15'];
set terminal png;
set style line 1 lt 1 lw 1 pt 3 linecolor rgb 'red';
set grid;
set nokey;
set xtics rotate;
set term png size 1024,600;
set output 'trend.png';
plot './trend.txt' using 1:2 with lines linestyle 1
"

eog ./trend.png
"""

import os
import os.path
import datetime

import iq
from iq.util import log_func
from iq.util import txtfile_func
from iq.util import sys_func

__version__ = (0, 0, 0, 2)

# Gnuplot command delimiter
COMMAND_DELIMETER = ';'

UNIX_GNUPLOT_RUN = 'gnuplot'
WIN_GNUPLOT_RUN = 'start gnuplot.exe /B'

GNUPLOT_COMMAND_FMT = '%s -e \"%s\"'

DATETIME_GRAPH_DATA_FMT = '%Y-%m-%d %H:%M:%S'


class iqGnuplotManager(object):
    """
    Gnuplot charting management manager class.
    """
    def __init__(self):
        """
        Constructor.
        """
        # List of commands for subsequent
        # generation of gnuplot launch command line
        self.commands = list()

        self.__x_format = None

    def clearCommands(self):
        """
        Clear the list of commands.

        :return: True/False.
        """
        self.commands = list()
        return True

    def _findCommand(self, command_word):
        """
        Search for a team in the list of teams by keyword.

        :param command_word: Keyword.
        :return: Index in the list of commands or -1 if such a command is not found.
        """
        for i, command in enumerate(self.commands):
            if command_word in command:
                return i
        return -1

    def _appendCommand(self, command, command_word=None):
        """
        Add a command to the list of commands.
        If a command is found in the list by keyword, then it is replaced.
        If not found, then just the command is added to the list.

        :param command: Command.
        :param command_word: Keyword.
            If None, then the command is added to the list.
        :return: True/False.
        """
        if command_word is None:
            # Add command to list
            self.commands.append(command)
        else:
            # First, we search for an existing team in the list by keyword
            find_idx = self._findCommand(command_word)
            if find_idx >= 0:
                # If there is such a command, then replace it
                self.commands[find_idx] = command
            else:
                # If the command is not found, then simply replace it
                self.commands.append(command)
        return True

    def _deleteCommand(self, command_word=None):
        """
        Delete a command from the list of commands.
        If a command is found in the list by keyword, then it is deleted.

        :param command_word: Keyword.
            If None, then just adding the command to the list.
        :return: True/False.
        """
        if command_word is None:
            return False
        else:
            # First, we search for an existing team in the list by keyword
            find_idx = self._findCommand(command_word)
            if find_idx >= 0:
                # If there is such a team, then replace it
                del self.commands[find_idx]
                return True
        return False

    def _enableCommand(self, command, enable=True):
        """
        Include / Exclude a command from the list of commands.

        :param command: Gnuplot command.
        :param enable: True - include command/False - exclude command.
        :return: True/False.
        """
        if enable:
            if command not in self.commands:
                self.commands.append(command)
        else:
            if command in self.commands:
                del self.commands[self.commands.index(command)]
        return True

    def enableXTime(self, enable=True):
        """
        On/off. X axis as temporary.

        :param enable: True - on/False - off.
        :return: True/False.
        """
        cmd = 'set xdata time'
        return self._enableCommand(cmd, enable)

    def setTimeFormat(self, dt_format=None):
        """
        Set date-time format.

        :param dt_format: Date-time format.
            If None, then format setting is excluded from the list of commands.
        :return: True/False.
        """
        global DATETIME_GRAPH_DATA_FMT
        if dt_format is None:
            dt_format = DATETIME_GRAPH_DATA_FMT
        else:
            DATETIME_GRAPH_DATA_FMT = dt_format

        cmd_sign = 'set timefmt'
        cmd = 'set timefmt \'%s\'' % dt_format
        return self._appendCommand(cmd, cmd_sign)

    def setXFormat(self, x_format=None):
        """
        Set X axis format.

        :param x_format: X axis format.
            If None, then format setting is excluded from the list of commands.
        :return: True/False.
        """
        cmd_sign = 'set format x'
        cmd = 'set format x \'%s\'' % x_format
        # Remember the X axis format for
        # the correct output of data to the chart data file
        self.__x_format = x_format
        return self._appendCommand(cmd, cmd_sign)

    def setXRange(self, x_start, x_stop):
        """
        Set X axis value range.

        :param x_start: Range start value.
        :param x_stop: End range value.
        :return: True/False.
        """
        cmd_sign = 'set xrange'
        cmd = 'set xrange[\'%s\':\'%s\']' % (x_start, x_stop)
        return self._appendCommand(cmd, cmd_sign)

    def setYRange(self, y_start, y_stop):
        """
        Set the range of y axis values.

        :param y_start: Range start value.
        :param y_stop: End range value.
        :return: True/False.
        """
        cmd_sign = 'set yrange'
        cmd = 'set yrange[%f:%f]' % (float(y_start), float(y_stop))
        return self._appendCommand(cmd, cmd_sign)

    def enableXTextVertical(self, enable=True):
        """
        On/off. X axis text output vertically.

        :param enable: True - on/False - off.
        :return: True/False.
        """
        cmd = 'set xtics rotate'
        return self._enableCommand(cmd, enable)

    def setOutputPNG(self, background_color=None):
        """
        On/off. PNG graphics output.

        :param background_color: PNG color background.
        :return: True/False.
        """
        self._deleteCommand('set terminal pdf')
        cmd_sign = 'set terminal png'
        cmd = 'set terminal png'
        if background_color is not None:
            cmd += ' background rgb \'%s\'' % background_color
        return self._appendCommand(cmd, cmd_sign)

    def setOutputPDF(self, background_color=None):
        """
        On/off. PDF graphics output.

        :param background_color: PDF background color. The default is white.
        :return: True/False.
        """
        self._deleteCommand('set terminal png')
        cmd_sign = 'set terminal pdf'
        cmd = 'set terminal pdf'
        if background_color is not None:
            cmd += ' background rgb \'%s\'' % background_color
        return self._appendCommand(cmd, cmd_sign)

    def setOutputSizePNG(self, width, height):
        """
        Set the size of the resulting PNG image.

        :param width: Width.
        :param height: Height.
        :return: True/False.
        """
        self._deleteCommand('set term pdf monochrome size')
        cmd_sign = 'set term png size'
        cmd = 'set term png size %d, %d' % (int(width), int(height))
        return self._appendCommand(cmd, cmd_sign)

    def setOutputSizePDF(self, width, height):
        """
        Set the size of the resulting PDF image.

        :param width: Width.
        :param height: Height.
        :return: True/False.
        """
        self._deleteCommand('set term png size')
        cmd_sign = 'set term pdf monochrome size'
        cmd = 'set term pdf monochrome size %d, %d' % (int(width), int(height))
        return self._appendCommand(cmd, cmd_sign)

    def setOutputFilename(self, out_filename):
        """
        Set the name of the resulting file.

        :param out_filename: The full name of the resulting file.
        :return: True/False.
        """
        cmd_sign = 'set output'
        cmd = 'set output \'%s\'' % out_filename
        return self._appendCommand(cmd, cmd_sign)

    def enableGrid(self, enable=True):
        """
        On/off the grid.

        :param enable: True - on grid/False - off grid.
        :return: True/False.
        """
        cmd = 'set grid'
        return self._enableCommand(cmd, enable)

    def enableLegend(self, enable=True):
        """
        On/Off the grid.

        :param enable: True - on legend/False - off legend.
        :return: True/False.
        """
        cmd = 'set nokey'
        return self._enableCommand(cmd, not enable)

    def setLineStyle(self, n_line=1, line_type=1, line_width=1, point_type=3, line_color='red'):
        """
        Set line style.

        :param n_line: Line number.
        :param line_type: Line type.
        :param line_width: Line thickness.
        :param point_type: Point type.
        :param line_color: Line colour
        :return: True/False.
        """
        cmd_sign = 'set style line %d' % int(n_line)
        cmd = 'set style line %d linetype %d linewidth %d pointtype %d linecolor rgb \'%s\'' % (int(n_line),
                                                                                                int(line_type),
                                                                                                int(line_width),
                                                                                                int(point_type),
                                                                                                line_color)
        return self._appendCommand(cmd, cmd_sign)

    def setPlot(self, graph_filename, count=1):
        """
        Set charting.

        :param graph_filename: Chart data file full name.
        :param count: The number of graphs.
        :return: True/False.
        """
        global DATETIME_GRAPH_DATA_FMT
        cmd_sign = 'plot '

        if os.path.exists(graph_filename):
            # If time is broken down by date and time, then the number in the using section increases
            params = ['\'%s\' using 1:%d with lines linestyle %d' % (graph_filename,
                                                                     i + 2 + DATETIME_GRAPH_DATA_FMT.count(' '),
                                                                     i + 1) for i in range(count)]
            cmd = cmd_sign + ', '.join(params)
        else:
            # If there is no data, then display an abstract graph
            log_func.warning(u'Graph data file <%s> not found' % graph_filename)
            cmd = 'plot [-pi:pi] sin(x), cos(x)'

        # The chart rendering command can only be the last command.
        if not self.commands:
            self.commands.append(cmd)
        else:
            self._deleteCommand(cmd_sign)

            last_cmd = self.commands[-1]
            if last_cmd.startswith(cmd_sign):
                self.commands[-1] = cmd
            else:
                self.commands.append(cmd)
        return True

    def saveGraphData(self, graph_filename, graph_data=(), fields=()):
        """
        Write graph data to a data file.
        By default, temporary data is written to the file in the format DATETIME_GRAPH_DATA_FMT.

        :param graph_filename: The full name of the chart data file.
        :param graph_data: List of dictionaries for these graphs.
            [
                {
                    'x': X coord value,
                    'Graph name 1': Y coordinate value of graph 1,
                    'Graph name 2': Y coordinate value of graph 2,
                    ...
                    'Graph name N': Y coordinate value of graph N,
                }, ...
            ]
        :param fields: The order of the graphs in the data file.
            ['Graph name 1', 'Graph name 2', ... 'Graph name N']
        :return: True/False.
        """
        global DATETIME_GRAPH_DATA_FMT

        txt = ''
        for record in graph_data:
            x = record.get('x', 0)
            # x_str = str(x) if self.__x_format is None else (x.strftime(self.__x_format) if isinstance(x, datetime.datetime) else str(x))
            x_str = x.strftime(DATETIME_GRAPH_DATA_FMT) if isinstance(x, datetime.datetime) else str(x)
            record_list = [x_str] + [str(record.get(field, 0)) for field in fields]
            record_txt = ' '.join(record_list)
            txt += record_txt + '\n'
        return txtfile_func.saveTextFile(graph_filename, txt)

    def getRunCommand(self):
        """
        Get the resulting command to start the generation.

        :return: The resulting command to generate the chart file.
        """
        commands = COMMAND_DELIMETER.join(self.commands)
        if sys_func.isLinuxPlatform():
            return GNUPLOT_COMMAND_FMT % (UNIX_GNUPLOT_RUN, commands)
        elif sys_func.isWindowsPlatform():
            win_gnuplot_run = iq.KERNEL.settings.THIS.SETTINGS.win_gnuplot_run.get()
            return GNUPLOT_COMMAND_FMT % (win_gnuplot_run if win_gnuplot_run else WIN_GNUPLOT_RUN,
                                          commands)
        else:
            log_func.warning(u'Unsupported <%s> platform' % sys_func.getPlatform())
        return None

    def runCommands(self):
        """
        Start generating.
        Another name for the method is generate

        :return: True/False.
        """
        cmd = self.getRunCommand()
        log_func.info(u'Command execution <%s>' % cmd)
        os.system(cmd)
        return True

    gen = runCommands

    def setBorderColour(self, line_color):
        """
        Set the color of the border of the graph.

        :param line_color: Line colour.
        :return: True/False.
        """
        cmd_sign = 'set border linecolor'
        cmd = 'set border linecolor rgb \'%s\'' % line_color
        return self._appendCommand(cmd, cmd_sign)

    def setGridColour(self, line_color):
        """
        Set graph grid color.

        :param line_color: Line colour.
        :return: True/False.
        """
        cmd_sign = 'set grid linecolor'
        cmd = 'set grid linecolor rgb \'%s\'' % line_color
        return self._appendCommand(cmd, cmd_sign)

    def setXTextColour(self, text_color):
        """
        Set the color of the labels of the scale X of the graph.

        :param text_color: Text colour.
        :return: True/False.
        """
        cmd_sign = 'set xtics textcolor'
        cmd = 'set xtics textcolor rgb \'%s\'' % text_color
        return self._appendCommand(cmd, cmd_sign)

    def setYTextColour(self, text_color):
        """
        Set the color of the labels on the Y scale of the graph.

        :param text_color: Text colour.
        :return: True/False.
        """
        cmd_sign = 'set ytics textcolor'
        cmd = 'set ytics textcolor rgb \'%s\'' % text_color
        return self._appendCommand(cmd, cmd_sign)
