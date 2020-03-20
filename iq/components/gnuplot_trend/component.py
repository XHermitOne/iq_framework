#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot historical trend component.
"""

# from ... import object
# from ... import passport

from . import spc
from . import gnuplot_trend_proto
from .. import wx_panel

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqGnuplotTrend(gnuplot_trend_proto.iqGnuplotTrendProto, wx_panel.COMPONENT):
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
        gnuplot_trend_proto.iqGnuplotTrendProto.__init__(self)


COMPONENT = iqGnuplotTrend
