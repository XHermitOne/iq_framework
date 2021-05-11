#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart component prototype class.
"""

import os
import os.path
import numpy
import matplotlib.pyplot

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)

DEFAULT_BAR_WIDTH = 0.35

HORIZONTAL_ORIENTATION = 'horizontal'
VERTICAL_ORIENTATION = 'vertical'


class iqMatplotlibBarChartProto(object):
    """
    MatPlotLib bar chart component prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self._bar_count = 1
        self._bar_width = DEFAULT_BAR_WIDTH

        self._title = None
        self._x_label = None
        self._y_label = None
        self._legend = tuple()

        self._x_tick_labels = tuple()

        self._orientation = HORIZONTAL_ORIENTATION

        self._bar_data = list()

    def getBarWidth(self):
        """
        Get bar width.
        """
        return self._bar_width

    def setBarWidth(self, bar_width=DEFAULT_BAR_WIDTH):
        """
        Set bar width.
        """
        self._bar_width = bar_width

    def getBarCount(self):
        """
        Get bar count.
        """
        return self._bar_count

    def getTitle(self):
        """
        Get title.
        """
        return self._title

    def setTitle(self, title=None):
        """
        Set title.
        """
        self._title = title

    def getXLabel(self):
        """
        Get X labels.
        """
        return self._x_label

    def setXLabel(self, label=None):
        """
        Set X labels.
        """
        self._x_label = label

    def getYLabel(self):
        """
        Get Y labels.
        """
        return self._y_label

    def setYLabel(self, label=None):
        """
        Set Y label.
        """
        self._y_label = label

    def getLegend(self):
        """
        Get legend list.
        """
        return self._legend

    def setLegend(self, legend=()):
        """
        Set legend list.
        """
        self._legend = legend

    def getOrientation(self):
        """
        Get bar chart orientation.
        """
        return self._orientation

    def setOrientation(self, orientation=HORIZONTAL_ORIENTATION):
        """
        Set bar chart orientation.
        """
        self._orientation = orientation

    def getXTickLabels(self):
        """
        Get X tick labels.
        """
        return self._x_tick_labels

    def setXTickLabels(self,x_tick_labels=()):
        """
        Set X tick labels.

        :param x_tick_labels: X tick label list.
        :return:
        """
        self._x_tick_labels = x_tick_labels

    def addBarData(self, bar_data=()):
        """
        Add bar data.

        :param bar_data: Bar data list.
        :return: True/False.
        """
        if len(self._bar_data) <= self.getBarCount():
            self._bar_data.append(bar_data)
            return True
        else:
            log_func.warning(u'Error limit bar count')
        return False

    def drawPNG(self, png_filename=None, show=False):
        """
        Draw PNG image file.

        :param png_filename: PNG image filename.
        :param show: Show result?
        :return: True/False.
        """
        if png_filename is None:
            png_filename = os.path.join(file_func.getProjectProfilePath(),
                                        self.getGUID() + '.png')
        try:
            orientation = self.getOrientation()
            if orientation == HORIZONTAL_ORIENTATION:
                return self.drawHorizontal(show=show)
            elif orientation == VERTICAL_ORIENTATION:
                return self.drawVertical(show=show)
            else:
                log_func.warning(u'Incorrect orientation value <%s>' % orientation)
        except:
            log_func.fatal(u'Error draw PNG image file <%s>' % png_filename)
        return False

    def drawHorizontal(self, show=False):
        """
        Draw horizontal oriented bar chart.

        :param show: Show result?
        :return:
        """
        fig, ax = matplotlib.pyplot.subplots()

        # Add some text for labels, title and custom x-axis tick labels, etc.
        title = self.getTitle()
        if title:
            ax.set_title(title)

        label = self.getXLabel()
        if label:
            ax.set_xlabel(label)

        label = self.getYLabel()
        if label:
            ax.set_ylabel(label)

        bar_width = self.getBarWidth()
        legend = self.getLegend()
        legend_count = len(legend) if legend else 0

        if self._bar_data:
            point_count = len(self._bar_data[0])

            bar_count = self.getBarCount()
            for i_bar in range(bar_count):
                rects = ax.bar(point_count - bar_width / 2,
                               self._bar_data[i_bar],
                               bar_width,
                               label=legend[i_bar] if legend and i_bar < legend_count else '')

                ax.bar_label(rects, padding=3)

        x_tick_labels = self.getXTickLabels()
        if x_tick_labels:
            ax.set_xticks(numpy.arange(len(x_tick_labels)))
            ax.set_xticklabels(x_tick_labels)

        if legend:
            ax.legend()

        fig.tight_layout()

        if show:
            matplotlib.pyplot.show()
        return True

    def drawVertical(self, show=False):
        """
        Draw vertical oriented bar chart.

        :param show: Show result?
        :return: True/False.
        """
        return False

