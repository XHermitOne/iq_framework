#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart component prototype class.
"""

import os
import os.path
import numpy
import matplotlib.pyplot
import pandas.plotting._matplotlib

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)

DEFAULT_BAR_WIDTH = 0.35

# HORIZONTAL_ORIENTATION = 'horizontal'
# VERTICAL_ORIENTATION = 'vertical'
DEFAULT_DPI = 150


class iqMatplotlibBarChartProto(object):
    """
    MatPlotLib bar chart component prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self._kind = tuple(pandas.plotting._matplotlib.PLOT_CLASSES.keys())[0]
        self._title = None
        self._x_label = None
        self._y_label = None
        self._legend = tuple()
        self._show_legend = True
        self._grid = False
        self._y = None

        # Current datasource object
        self._current_datasource = None

    def getCurrentDataSource(self):
        """
        Get current datasource object.
        """
        return self._current_datasource

    def setCurrentDataSource(self, datasource=None):
        """
        Set current datasource object.
        """
        if datasource is None:
            self._current_datasource = None
        elif isinstance(datasource, pandas.DataFrame):
            log_func.debug(u'Set data source in <%s>' % self.getName())
            self._current_datasource = datasource
        else:
            log_func.warning(u'Incorrect type bar chart datasource <%s>' % datasource.__class__.__name__)
            self._current_datasource = None

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

    def getShowLegend(self):
        """
        Show legend?
        """
        return self._show_legend

    def setShowLegend(self, show_legend=True):
        """
        Set show legend.
        """
        self._show_legend = show_legend

    def getKind(self):
        """
        Get bar chart kind.
        """
        return self._kind

    def setKind(self, kind=None):
        """
        Set bar chart kind.
        """
        if kind:
            self._kind = kind

    def getGrid(self):
        """
        Get grid.
        """
        return self._grid

    def setGrid(self, grid=True):
        """
        Set grid.

        :param grid: Show grid? True or False.
        :return:
        """
        self._grid = grid

    def getY(self):
        """
        Data column name for pie chart.
        """
        return self._grid

    def setY(self, y=None):
        """
        Data column name for pie chart.
        """
        self._y = y

    def genPNGFilename(self):
        """
        Generate image PNG filename.

        :return:
        """
        base_png_filename = self.getGUID() + '.png'
        return os.path.join(file_func.getProjectProfilePath(), base_png_filename)

    def delPNGFilename(self, png_filename=None):
        """
        Delete image PNG filename.

        :param png_filename: Image PNG filename.
        :return: True/False.
        """
        if png_filename is None:
            png_filename = self.genPNGFilename()
        if os.path.exists(png_filename):
            return file_func.removeFile(png_filename)
        return False

    def getFigureSize(self):
        """
        Get figure size.
        :return:
        """
        return None

    def drawDataFrame(self, dataframe=None, png_filename=None, size=None, show=False):
        """
        Draw DataFrame object.

        :param dataframe: Pandas DataFrame object.
        :param png_filename: Image PNG filename.
        :param size: Image size.
        :param show: Show result?
        :return:
        """
        if dataframe is not None:
            self.setCurrentDataSource(dataframe)

        if self._current_datasource is None:
            log_func.warning(u'Not define datasource object for draw in <%s>' % self.getName())
            return False

        assert isinstance(self._current_datasource, pandas.DataFrame), u'Type error DataFrame for draw'

        try:
            kind = self.getKind()
            if size is None:
                size = self.getFigureSize()

            plot_graph = self._current_datasource.plot(kind=kind,
                                                       legend=self.getShowLegend(),
                                                       figsize=(size[0]/DEFAULT_DPI, size[1]/DEFAULT_DPI) if size else None,
                                                       y=self.getY(),
                                                       backend='wxAgg')

            title = self.getTitle()
            if title:
                plot_graph.set_title(title)

            label = self.getXLabel()
            if label:
                plot_graph.set_xlabel(label)

            label = self.getYLabel()
            if label:
                plot_graph.set_ylabel(label)

            grid = self.getGrid()
            if grid:
                plot_graph.grid()

            matplotlib.pyplot.tight_layout()
            if show:
                matplotlib.pyplot.show()
            else:
                if png_filename is None:
                    png_filename = self.genPNGFilename()
                figure = plot_graph.get_figure()
                figure.savefig(fname=png_filename, dpi=DEFAULT_DPI)

            return True
        except:
            log_func.fatal(u'Error draw DataFrame to png file <%s>' % png_filename)
        return False
