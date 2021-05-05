#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel component.
"""

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


COMPONENT = iqWxMatplotlibBarChartPanel
