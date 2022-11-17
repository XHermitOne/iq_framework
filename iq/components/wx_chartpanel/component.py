#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotly-express/Pygal chart wx panel component.
"""

import os.path
import wx

from . import spc
from .. import wx_panel

from ...util import log_func

from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqWxChartPanel(wx_panel.COMPONENT):
    """
    Plotly-express/Pygal chart wx panel component class.
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

        self.datasource = None
        self.chart = None

        self.canvas = wx.StaticBitmap(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.Bind(wx.EVT_SIZE, self.onSize)

    def getChartPsp(self):
        """
        Get chart object passport.
        """
        return self.getAttribute('chart')

    def getDataSourcePsp(self):
        """
        Get datasource object passport.
        """
        return self.getAttribute('datasource')

    def getChart(self):
        """
        Get chart object.
        """
        if self.chart is not None:
            return self.chart

        psp = self.getChartPsp()
        if psp:
            kernel = self.getKernel()
            self.chart = kernel.getObject(psp, register=True)
            return self.chart
        else:
            log_func.warning(u'Not define chart object in <%s>' % self.getName())
        return None

    def getDataSource(self):
        """
        Get datasource object.
        """
        if self.datasource is not None:
            return self.datasource

        psp = self.getDataSourcePsp()
        if psp:
            kernel = self.getKernel()
            self.datasource = kernel.getObject(psp, register=True)
            return self.datasource
        else:
            log_func.warning(u'Not define datasource object in <%s>' % self.getName())
        return None

    def draw(self):
        """
        Draw chart.

        :return: True/False.
        """
        try:
            return self._draw()
        except:
            log_func.fatal(u'Error draw chart in <%s>' % self.getName())
        return False

    def _draw(self):
        """
        Draw chart.

        :return: True/False.
        """
        datasource = self.getDataSource()
        if datasource is None:
            log_func.error(u'Not define datasource object in <%s>' % self.getName())
            return False
        chart = self.getChart()
        if chart is None:
            log_func.error(u'Not define chart object in <%s>' % self.getName())
            return False
        dataset = datasource.getDataset()
        size = self.getSize()
        img_filename = '%s_%dx%d.%s' % (self.getName(), size[0], size[1], chart.getOutputType())
        return chart.draw(dataset, img_filename)

    def _refresh(self):
        """
        Refresh panel.

        :return: True/False.
        """
        result = self.draw()
        chart = self.getChart()
        img_filename = chart.getOutputImageFilename()
        if img_filename and os.path.exists(img_filename):
            bmp = wxbitmap_func.createBitmap(img_filename)
            self.canvas.SetBitmap(bmp)
            self.canvas.Refresh()
        return result

    def refresh(self):
        """
        Refresh panel.

        :return: True/False.
        """
        try:
            return self._refresh()
        except:
            log_func.fatal(u'Error refresh chart panel <%s>' % self.getName())
        return False

    def onSize(self, event):
        """
        Change size handler.
        """
        datasource = self.getDataSource()
        if datasource is not None:
            self.refresh()
        event.Skip()


COMPONENT = iqWxChartPanel
