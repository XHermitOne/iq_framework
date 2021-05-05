#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart component.
"""

from ... import object

from . import spc
from . import barchart_proto

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqMatplotlibBarChart(object.iqObject, barchart_proto.iqMatplotlibBarChartProto):
    """
    MatPlotLib bar chart component class.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        barchart_proto.iqMatplotlibBarChartProto.__init__(self, *args, **kwargs)


COMPONENT = iqMatplotlibBarChart
