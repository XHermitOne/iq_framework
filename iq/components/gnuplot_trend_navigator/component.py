#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot historical trend navigator component.
"""

from . import spc
from . import gnuplot_trend_navigator_proto
from .. import wx_panel

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqGnuplotTrendNavigator(gnuplot_trend_navigator_proto.iqGnuplotTrendNavigatorProto,
                              wx_panel.COMPONENT):
    """
    Gnuplot historical trend component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        gnuplot_trend_navigator_proto.iqGnuplotTrendNavigatorProto.__init__(self)


COMPONENT = iqGnuplotTrendNavigator
