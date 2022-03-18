#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plotly-express chart wx panel specification module.
"""

from ...editor import property_editor_id
from .. import wx_panel
from ... import passport

from .. import plotly_express_chart
from .. import data_query
from .. import data_model
from .. import transform_datasource

__version__ = (0, 0, 0, 1)

CHART_TYPES = (plotly_express_chart.COMPONENT_TYPE, )


def validChartPsp(psp, *args, **kwargs):
    """
    Validate chart passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in CHART_TYPES


CHART_DATASOURCE_TYPES = (data_query.COMPONENT_TYPE,
                          data_model.COMPONENT_TYPE,
                          transform_datasource.COMPONENT_TYPE)


def validChartDataSourcePsp(psp, *args, **kwargs):
    """
    Validate chart datasource passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in CHART_DATASOURCE_TYPES


COMPONENT_TYPE = 'iqWxPlotlyExpressChartPanel'

WXPLOTLYEXPRESSCHARTPANEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'chart': None,
    'datasource': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/piechart',
    '__parent__': wx_panel.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'chart': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validChartPsp,
        },
        'datasource': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validChartDataSourcePsp,
        },
    },
    '__help__': {
        'chart': u'Plotly-express chart',
        'datasource': u'Datasource pandas.DataFrame or Dataset (list of dictionaries)',
    },
}

SPC = WXPLOTLYEXPRESSCHARTPANEL_SPC
