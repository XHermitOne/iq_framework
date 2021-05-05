#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel prototype class.
"""

from ..matplotlib_barchart import barchart_proto

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
