#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel prototype class.
"""

import os.path
import wx

from ..matplotlib_barchart import barchart_proto
from ..gnuplot_trend import gnuplot_trend_proto

from ...util import log_func
from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqMatplotlibBarChartPanelProto(barchart_proto.iqMatplotlibBarChartProto):
    """
    MatPlotLib bar chart wx panel prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        barchart_proto.iqMatplotlibBarChartProto.__init__(self, *args, **kwargs)

        self.canvas = wx.StaticBitmap(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

    def refresh(self):
        """
        Refresh panel.

        :return: True/False.
        """
        png_filename = self.genPNGFilename()

        try:
            if png_filename and os.path.exists(png_filename) and png_filename.endswith(gnuplot_trend_proto.PNG_FILE_TYPE.lower()):
                bmp = wxbitmap_func.createBitmap(png_filename)
                self.canvas.SetBitmap(bmp)
                self.canvas.Refresh()
                return True
            else:
                log_func.warning(u'Image PNG file <%s> not found' % png_filename)
        except:
            log_func.fatal(u'Error refresh bar chart panel')
        return False
