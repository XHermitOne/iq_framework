#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Component of historical graphics. The trend.
The component is based on the gnuplot utility.
"""

import os.path
import operator
import wx
import datetime
import time
import uuid

from ...util import log_func
from ...util import file_func
from ...engine.wx import wxbitmap_func

from . import gnuplot_manager

from . import trend_proto

__version__ = (0, 0, 0, 1)

# Gnuplot utility file name
GNUPLOT_FILENAME = 'gnuplot'

# Trend frame placement folder
DEFAULT_GNUPLOT_FRAME_PATH = os.path.join(file_func.getProjectProfilePath(), 'gnuplot')

# Minimum frame sizes
MIN_FRAME_WIDTH = 640
MIN_FRAME_HEIGHT = 480

# Types of frame files
PNG_FILE_TYPE = 'PNG'
PDF_FILE_TYPE = 'PDF'

DATA_FILE_EXT = '.dat'

# Default precision
DEFAULT_X_PRECISION = '01:00:00'
DEFAULT_Y_PRECISION = '1.0'


class iqGnuplotTrendProto(trend_proto.iqTrendProto):
    """
    The base class of historical graphics. The trend.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # wx.Panel.__init__(self, *args, **kwargs)

        # Each trend has its own identifier so that displays
        # do not overlap with other trends
        self.__trend_uuid = str(uuid.uuid4())
        # Frame file name
        self.__frame_filename = None

        self.canvas = wx.StaticBitmap(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        trend_proto.iqTrendProto.__init__(self, *args, **kwargs)

        self.setDefaults()

        # Current Trend Scene - The boundaries of the scene window in the data of the subject area
        # It is represented as a tuple (X1, Y1, X2, Y2)
        self._cur_scene = None

        # Value of division
        self._x_precision = DEFAULT_X_PRECISION
        self._y_precision = DEFAULT_Y_PRECISION
        # Scale num_format
        self._x_format = trend_proto.DEFAULT_X_FORMAT
        self._y_format = trend_proto.DEFAULT_Y_FORMAT

        # Gnuplot utility manager
        self.__gnuplot_manager = gnuplot_manager.iqGnuplotManager()
        self.__gnuplot_manager.enableGrid()
        self.__gnuplot_manager.enableLegend(False)
        self.__gnuplot_manager.enableXTime()
        self.__gnuplot_manager.enableXTextVertical()

        # If you need to remove / free resources when removing control,
        # then you need to use the wx.EVT_WINDOW_DESTROY event
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def _getManager(self):
        """
        Gnuplot utility manager.
        """
        return self.__gnuplot_manager

    def isAdaptScene(self):
        """
        To adapt the trend scene according to the data?
        """
        return False

    def setScene(self, min_x=None, min_y=None, max_x=None, max_y=None):
        """
        Set the current trend scene.

        :param min_x: The minimum value along the x axis.
        :param min_y: The minimum value along the y axis.
        :param max_x: The maximum value on the x axis.
        :param max_y: The maximum value on the y axis.
        :return: The current trend scene.
        """
        # Scene adaptation according to
        if self._cur_scene is None:
            pen_data = self.getPenData(pen_index=0)
            if self.isAdaptScene():
                self._cur_scene = self.adaptScene(pen_data)

        if self._cur_scene is None:
            # Adaptation ended unsuccessfully
            self._cur_scene = (datetime.datetime.now().replace(hour=0, minute=0, second=0), 0.0,
                               datetime.datetime.now().replace(hour=23, minute=59, second=59), 100.0)

        scene = list(self._cur_scene)
        if min_x:
            scene[0] = self._str2dt(min_x, self._x_format) if isinstance(min_x, str) else min_x
        if min_y:
            scene[1] = min_y
        if max_x:
            scene[2] = self._str2dt(max_x, self._x_format) if isinstance(max_x, str) else max_x
        if max_y:
            scene[3] = max_y
        self._cur_scene = tuple(scene)
        return self._cur_scene

    def setStartDT(self, new_dt):
        """
        The start date-time of the trend.

        :param new_dt: New value.
        """
        self.start_datetime = self._convertDate(new_dt)
        self.setScene(min_x=self.start_datetime)

    def setStopDT(self, new_dt):
        """
        The final date and time of the trend.

        :param new_dt: New value.
        """
        self.stop_datetime = self._convertDate(new_dt)
        self.setScene(max_x=self.stop_datetime)

    def setFormats(self, x_format=None, y_format=None):
        """
        Set scale formats.

        :param x_format: X-axis scale num_format.
            If None, then the num_format is not set.
        :param y_format: Y-axis scale num_format.
            If None, then the num_format is not set.
        :return: Tuple (x_format, y_format) of current formats.
        """
        if x_format is not None:
            self._x_format = x_format
        if y_format is not None:
            self._y_format = y_format
        return self._x_format, self._y_format

    def setPrecisions(self, x_precision=None, y_precision=None):
        """
        Set the price of division by axes.

        :param x_precision: The division value of the X axis.
            If None, then the division price is not set.
        :param y_precision: Y axis division value.
            If None, then the division price is not set.
        :return: Tuple (x_precision, y_precision) of the current division prices.
        """
        if x_precision is not None:
            if isinstance(x_precision, str):
                # Цена деления задается строкой. Необходимо правильно преобразовать
                x_precision = self._str2dt(x_precision, self._x_format, bToTimeDelta=True)
            self._x_precision = x_precision
        if y_precision is not None:
            if not isinstance(y_precision, float):
                y_precision = float(y_precision)
            self._y_precision = y_precision
        return self._x_precision, self._y_precision

    def onDestroy(self, event):
        """
        When removing the panel. Event handler.
        If you need to remove / free resources when removing control,
        then you need to use the wx.EVT_WINDOW_DESTROY event.
        """
        frame_filename = self.getFrameFileName(PNG_FILE_TYPE)
        self.delFrameFile(frame_filename)
        frame_filename = self.getFrameFileName(PDF_FILE_TYPE)
        self.delFrameFile(frame_filename)
        dat_filename = os.path.splitext(frame_filename)[0] + DATA_FILE_EXT
        file_func.removeFile(dat_filename)
        event.Skip()

    def getTrendUUID(self):
        """
        The identifier of the trend object.
        Each trend has its own identifier
        so that displays do not overlap with other trends.
        """
        return self.__trend_uuid

    def getFrameFileName(self, file_type=PNG_FILE_TYPE):
        """
        The name of the frame file.

        :param file_type: File Type / File Extension. The default is a PNG file.
        """
        file_ext = '.' + file_type.lower()
        if self.__frame_filename is None or not self.__frame_filename.endswith(file_ext):
            obj_uuid = self.getTrendUUID()
            self.__frame_filename = os.path.join(DEFAULT_GNUPLOT_FRAME_PATH, obj_uuid + file_ext)
        return self.__frame_filename

    def getGraphFileName(self, file_type=DATA_FILE_EXT):
        """
        The name of the chart data file.

        :param file_type: File Type / File Extension.
            The default text file is * .dat.
        """
        frame_filename = self.getFrameFileName()
        graph_filename = os.path.splitext(frame_filename)[0] + DATA_FILE_EXT
        return graph_filename

    def getCurScene(self):
        """
        Current trend scene - The borders of the scene window in the data of the subject area.
        It is represented as a tuple (X1, Y1, X2, Y2)
        """
        return self._cur_scene

    def setDefaults(self):
        """
        Set default options.
        """
        if not os.path.exists(DEFAULT_GNUPLOT_FRAME_PATH):
            try:
                os.makedirs(DEFAULT_GNUPLOT_FRAME_PATH)
                log_func.info(u'Make directory <%s>' % DEFAULT_GNUPLOT_FRAME_PATH)
            except:
                log_func.error(u'Error make directory <%s>' % DEFAULT_GNUPLOT_FRAME_PATH)

    def delFrameFile(self, frame_filename=None):
        """
        Delete frame file.

        :param frame_filename: The name of the trend frame file.
        :return: True/False.
        """
        if frame_filename is None:
            frame_filename = self.getFrameFileName()

        return file_func.removeFile(frame_filename)

    # Scale num_format replacement dictionary
    _FMT2GNUPLOT_TYPE = {'numeric': 'N',
                         'time': 'T',
                         'date': 'D',
                         'datetime': 'DT',
                         'exponent': 'E'}

    def drawFrame(self, size=(0, 0), x_format='time', y_format='numeric',
                  scene=None, points=None):
        """
        Drawing a frame of trend data.

        :param size: Frame size in points.
        :param x_format: Scale num_format X.
        :param y_format: Y scale num_format.
        :param scene: The boundaries of the scene window in the data of the subject area.
        :param points: List of chart points.
            The list of points can also be specified by the name of the data file.
        :return: The file name of the rendered frame or None in case of an error.
        """
        try:
            if scene is None:
                scene = self._cur_scene

            return self._drawFrame(size=size, x_format=x_format, y_format=y_format,
                                   scene=scene, points=points, file_type=PNG_FILE_TYPE)
        except:
            log_func.fatal(u'Frame rendering error')
        return None

    def reportFrame(self, size=(0, 0), x_format='time', y_format='numeric',
                    scene=None, points=None):
        """
        Rendering a trend data frame as a PDF report.

        :param size: Frame size in points.
        :param x_format: Scale num_format X.
        :param y_format: Scale num_format Y.
        :param scene: The boundaries of the scene window in the data of the subject area.
        :param points: List of chart points.
        :return: The file name of the rendered frame or None in case of an error.
        """
        try:
            if scene is None:
                scene = self._cur_scene

            return self._drawFrame(size=size, x_format=x_format, y_format=y_format,
                                   scene=scene, points=points, file_type=PDF_FILE_TYPE)
        except:
            log_func.fatal(u'Report rendering frame error')
        return None

    def _drawFrame(self, size=(0, 0), x_format='time', y_format='numeric', scene=None,
                   points=None, file_type=PNG_FILE_TYPE):
        """
        Drawing a frame of trend data.

        :param size: Frame size in points.
        :param x_format: Scale num_format X.
        :param y_format: Scale num_format Y.
        :param scene: The boundaries of the scene window in the data of the subject area.
        :param points: List of chart points.
            The list of points can also be specified by the name of the data file.
        :return: The file name of the rendered frame or None in case of an error.
        """
        frame_filename = self.getFrameFileName(file_type)

        if isinstance(points, (list, tuple)):
            graph_filename = os.path.splitext(frame_filename)[0] + DATA_FILE_EXT
        elif isinstance(points, str) and os.path.exists(points):
            graph_filename = points
        else:
            log_func.error(u'Invalid type of list of points for drawing a trend frame <%s>' % self.getName())
            return None

        # log_func.debug(u'Frame filename: %s' % frame_filename)
        self.delFrameFile(frame_filename)

        dt_format = self._get_dt_format(x_format)
        self.__gnuplot_manager.setTimeFormat()
        self.__gnuplot_manager.setXFormat(dt_format)

        if scene is None:
            scene = self._cur_scene

        if scene[0] != scene[2] and scene[1] != scene[3]:
            self.__gnuplot_manager.setXRange(self._dt2str(scene[0], gnuplot_manager.DATETIME_GRAPH_DATA_FMT),
                                             self._dt2str(scene[2], gnuplot_manager.DATETIME_GRAPH_DATA_FMT))
            self.__gnuplot_manager.setYRange(float(scene[1]), float(scene[3]))

        if file_type == PNG_FILE_TYPE:
            self.__gnuplot_manager.setOutputPNG(background_color='black')
            self.__gnuplot_manager.setBorderColour('#A9A9A9')  # darkgray
            self.__gnuplot_manager.setGridColour('#A9A9A9')  # darkgray
            self.__gnuplot_manager.setXTextColour('#008B8B')  # darkcyan
            self.__gnuplot_manager.setYTextColour('#008B8B')  # darkcyan
        else:
            self.__gnuplot_manager.setOutputPDF()
            self.__gnuplot_manager.setBorderColour('black')
            self.__gnuplot_manager.setGridColour('black')
            self.__gnuplot_manager.setXTextColour('black')
            self.__gnuplot_manager.setYTextColour('black')
        self.__gnuplot_manager.setOutputFilename(frame_filename)

        if size is not None:
            width, height = size
            width = max(width, MIN_FRAME_WIDTH)
            height = max(height, MIN_FRAME_HEIGHT)
            if width > 0 and height > 0:
                if file_type == PNG_FILE_TYPE:
                    self.__gnuplot_manager.setOutputSizePNG(width, height)
                # else:
                #     self.__gnuplot_manager.setOutputSizePDF(width, height)

        if isinstance(points, (list, tuple)):
            # This is 1 chart
            points_lst = [dict(x=point[0] if isinstance(point[0], datetime.datetime) else float(point[0]),
                               point1=float(point[1])) for point in points]
            self.__gnuplot_manager.saveGraphData(graph_filename, points_lst, ('point1',))
            self.__gnuplot_manager.setPlot(graph_filename, 1)
        else:
            self.__gnuplot_manager.setPlot(graph_filename, len(self.getPens()))

        self.__gnuplot_manager.gen()

        if os.path.exists(frame_filename):
            return frame_filename
        else:
            log_func.error(u'Frame file <%s> Gnuplot trend not found' % frame_filename)
        return None

    def drawEmpty(self, size=None):
        """
        Drawing an empty trend.
        """
        if size is None:
            # size = self.canvas.GetSize()
            size = self.GetSize()
        log_func.debug(u'Drawing an empty trend. Size %s' % str(size))
        frame_filename = self.drawFrame(size=tuple(size))
        self.setFrame(frame_filename)

    def setFrame(self, frame_filename=None):
        """
        Set frame.

        :param frame_filename: The full name of the frame file.
        :return: True/False.
        """
        if frame_filename is None:
            frame_filename = self.getFrameFileName()

        try:
            if frame_filename and os.path.exists(frame_filename) and frame_filename.endswith(PNG_FILE_TYPE.lower()):
                bmp = wxbitmap_func.createBitmap(frame_filename)
                self.canvas.SetBitmap(bmp)
                self.canvas.Refresh()
                return True
        except:
            log_func.fatal(u'Error set frame <%s> in trend <%s>' % (frame_filename, self.getName()))
        return False

    def _saveGraphDataFile(self, graph_filename=None):
        """
        Save pen data in a graphic data file.

        :param graph_filename: The full name of the image file.
            If not defined, then generated.
        :return: True - file saved successfully. False - error saving file.
        """
        if graph_filename is None:
            graph_filename = self.getGraphFileName()

        pens = self.getPens()

        if pens:
            self.setDefaults()

            graph_data = list()
            for i_pen, pen in enumerate(pens):
                try:
                    if pen:
                        # By feathers we form a data file
                        points = pen.getLineData()
                        if points:
                            if not graph_data:
                                graph_data = [dict(x=point[0] if isinstance(point[0],
                                                                            datetime.datetime) else float(point[0]),
                                              pen0=float(point[1])) for point in points]
                            else:
                                for i_point, point in enumerate(points):
                                    point_name = 'pen%d' % i_pen
                                    is_graph_point = False
                                    for i, graph_point in enumerate(graph_data):
                                        if graph_data[i]['x'] == point[0]:
                                            graph_data[i][point_name] = float(point[1])
                                            is_graph_point = True
                                            break
                                    if not is_graph_point:
                                        # There is no such point in the output
                                        # Add to the general list
                                        new_graph_point = dict()
                                        new_graph_point['x'] = point[0] if isinstance(point[0],
                                                                                      datetime.datetime) else float(point[0])
                                        new_graph_point[point_name] = float(point[1])
                                        for i_prev_pen in range(i_pen):
                                            new_graph_point['pen%d' % i_prev_pen] = 0.0
                                        graph_data.append(new_graph_point)
                    else:
                        log_func.error(u'Undefined trend pen <%s>' % self.name)
                except:
                    log_func.fatal(u'Trend rendering error')
                    break

            if graph_data:
                # After filling in the list of graphic data, sort it by time
                graph_data.sort(key=operator.itemgetter('x'))
                # And save it in a file
                self.__gnuplot_manager.saveGraphData(graph_filename, graph_data,
                                                     ['pen%d' % i_pen for i_pen in range(len(pens))])
                return True
        else:
            log_func.error(u'Not defined feathers in the trend <%s>' % self.getName())

        return False

    def draw(self, redraw=True, size=None):
        """
        The main method of plotting a trend.

        :param redraw: Forced drawing.
        :param size: Size.
        """
        if size is None:
            size = self.GetSize()

        # Sign of a non-empty trend
        graph_filename = self.getGraphFileName()
        not_empty = self._saveGraphDataFile(graph_filename)

        if not_empty:
            if redraw:
                self.drawFrame(size=size, points=graph_filename, scene=self._cur_scene)
            self.setFrame()
        else:
            # If the trend is empty, then draw an empty trend
            self.drawEmpty(size=size)

    def adaptScene(self, graph_data=None):
        """
        Adapt the current scene to display according to the graph.

        :param graph_data: List of chart points.
            [(x1, y1), (x2, y2), ... (xN, yN)]
        :return: The current trend scene.
        """
        if graph_data is None:
            graph_data = self.getPenData(pen_index=0)

        if not graph_data:
            log_func.error(u'No chart data for scene adaptation for trend display')
        else:
            time_data = [point[0] for point in graph_data]
            y_data = [point[1] for point in graph_data]
            min_timestamp = time.mktime(min(time_data).timetuple())
            max_timestamp = time.mktime(max(time_data).timetuple())
            x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision, datetime.timedelta) else time.mktime(self._x_precision.timetuple())
            min_y = min(y_data)
            max_y = max(y_data)

            scene_min_time = datetime.datetime.fromtimestamp(int(min_timestamp / x_precision_timestamp) * x_precision_timestamp)
            scene_min_y = int(min_y / self._y_precision) * self._y_precision
            scene_max_time = datetime.datetime.fromtimestamp((int(max_timestamp / x_precision_timestamp) + 1) * x_precision_timestamp)
            scene_max_y = (int(max_y / self._y_precision) + 1) * self._y_precision

            # Trend allows you to view data only within a day
            # Therefore, we limit the maximum value of the timeline
            limit_scene_time_max = scene_min_time.replace(hour=23, minute=59, second=59)
            if scene_max_time > limit_scene_time_max:
                scene_max_time = limit_scene_time_max

            # log_func.debug(u'Scene adaptation:')
            # log_func.debug(u'\tdata x: %s' % str(time_data))
            # log_func.debug(u'\tdata y: %s' % str(y_data))
            # log_func.debug(u'\tmin_value data x: %s' % min_value(time_data))
            # log_func.debug(u'\tmin data y: %s' % min_y)
            # log_func.debug(u'\tmax_value data x: %s' % max_value(time_data))
            # log_func.debug(u'\tmax data y: %s' % max_y)
            # log_func.debug(u'\ttime precision: %s' % str(self._x_precision))
            # log_func.debug(u'\ty precision: %s' % str(self._y_precision))
            # log_func.debug(u'\tmin time: %s' % str(scene_min_time))
            # log_func.debug(u'\tmin y: %s' % str(scene_min_y))
            # log_func.debug(u'\tmax time: %s' % str(scene_max_time))
            # log_func.debug(u'\tmax y: %s' % str(scene_max_y))

            self._cur_scene = (scene_min_time, scene_min_y, scene_max_time, scene_max_y)

            self.setStartDT(scene_min_time)
            self.setStopDT(scene_min_time)

        return self._cur_scene

    def zoomX(self, step=1, redraw=True):
        """
        Increase the X axis graduation value according to the setting scale.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1],
                           max(self._cur_scene[2] + step * self._x_precision,
                               self._cur_scene[0] + self._x_precision),
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True

    def zoomY(self, step=1, redraw=True):
        """
        Increase the Y-axis division price according to the setting scale.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1],
                           self._cur_scene[2],
                           max(self._cur_scene[3] + step * self._y_precision, self._y_precision))

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneX(self, step=1, redraw=True):
        """
        Moving the scene along the X axis by the specified amount of the division price.

        :param step: Number of division prices for movement
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        self._cur_scene = (self._cur_scene[0] + step * self._x_precision,
                           self._cur_scene[1],
                           self._cur_scene[2] + step * self._x_precision,
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneY(self, step=1, redraw=True):
        """
        Moving the scene along the Y axis by the specified amount of the division price.

        :param step: Number of division prices for movement
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        self._cur_scene = (self._cur_scene[0],
                           self._cur_scene[1] + step * self._y_precision,
                           self._cur_scene[2],
                           self._cur_scene[3] + step * self._y_precision)

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneFirst(self, redraw=True):
        """
        The movement of the scene along the X axis by the first value of the trend.

        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        time_width = self._cur_scene[2] - self._cur_scene[0]
        graph_data = self.getPenData(pen_index=0)

        time_data = [point[0] for point in graph_data]
        min_timestamp = time.mktime(min(time_data).timetuple())
        x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision,
                                                                                datetime.timedelta) else time.mktime(self._x_precision.timetuple())

        scene_min_time = datetime.datetime.fromtimestamp(
            int(min_timestamp / x_precision_timestamp) * x_precision_timestamp)

        self._cur_scene = (scene_min_time,
                           self._cur_scene[1],
                           scene_min_time + time_width,
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True

    def moveSceneLast(self, redraw=True):
        """
        Moving the scene along the Y axis by the specified amount of the division price.

        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        time_width = self._cur_scene[2] - self._cur_scene[0]
        graph_data = self.getPenData(pen_index=0)

        time_data = [point[0] for point in graph_data]
        max_timestamp = time.mktime(max(time_data).timetuple())
        x_precision_timestamp = self._x_precision.total_seconds() if isinstance(self._x_precision,
                                                                                datetime.timedelta) else time.mktime(self._x_precision.timetuple())
        scene_max_time = datetime.datetime.fromtimestamp(
            (int(max_timestamp / x_precision_timestamp) + 1) * x_precision_timestamp)

        self._cur_scene = (scene_max_time - time_width,
                           self._cur_scene[1],
                           scene_max_time,
                           self._cur_scene[3])

        if redraw:
            self.draw(redraw=redraw)
        return True
