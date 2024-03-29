#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel component.
"""
import wx

from . import spc
from . import matplotlib_barchartpanel_proto
from .. import wx_panel

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqWxMatplotlibBarChartPanel(matplotlib_barchartpanel_proto.iqMatplotlibBarChartPanelProto,
                                  wx_panel.COMPONENT):
    """
    MatPlotLib bar chart wx panel component class.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        matplotlib_barchartpanel_proto.iqMatplotlibBarChartPanelProto.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_SIZE, self.onSize)

    def getFigureSize(self):
        """
        Get size.
        :return:
        """
        return tuple(self.GetSize())

    def onSize(self, event):
        """
        Change size handler.
        """
        current_datasource = self.getCurrentDataSource()
        if current_datasource is not None:
            self.drawDataFrame()
            self.refresh()
        event.Skip()

    def getKind(self):
        """
        Get chart kind.
        """
        self._kind = self.getAttribute('kind')
        return self._kind

    def getTitle(self):
        """
        Get title.
        """
        if not self._title:
            self._title = self.getAttribute('title')
        return self._title

    def getXLabel(self):
        """
        Get X label.
        """
        self._x_label = self.getAttribute('x_label')
        return self._x_label

    def getYLabel(self):
        """
        Get Y label.
        """
        self._y_label = self.getAttribute('y_label')
        return self._y_label

    def getLegend(self):
        """
        Get legend.
        """
        if not self._legend:
            self._legend = self.getAttribute('legend')
        return self._legend

    def getShowLegend(self):
        """
        Show legend?
        """
        self._show_legend = self.getAttribute('show_legend')
        return self._show_legend

    def getGrid(self):
        """
        Get grid.
        """
        self._grid = self.getAttribute('grid')
        return self._grid

    def getY(self):
        """
        Data column name for pie chart.
        """
        y = self.getAttribute('y')
        kind = self.getKind()
        self._y = y if kind == 'pie' else None
        return self._y


COMPONENT = iqWxMatplotlibBarChartPanel
