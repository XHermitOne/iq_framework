#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotly-express chart manager component.
"""

from ... import object
from . import spc
from . import chart_manager

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqPlotluExpressChart(chart_manager.iqPlotlyExpressChartProto,
                           object.iqObject):
    """
    Plotly-express chart manager component class.
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
        chart_manager.iqPlotlyExpressChartProto.__init__(self, *args, **kwargs)

        self.setChartType(self.getAttribute('chart_type'))
        self.setSize(self.getAttribute('width'), self.getAttribute('height'))
        self.setOutputType(self.getAttribute('output_type'))
        args = self.getAttribute('args')
        self.setChartArguments(**args)


COMPONENT = iqPlotluExpressChart
