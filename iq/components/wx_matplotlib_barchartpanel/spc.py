#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel specification module.
"""

from ...editor import property_editor_id
from .. import wx_panel
from ..matplotlib_barchart import spc as matplotlib_barchart_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxMatplotlibBarChartPanel'

WXMATPLOTLIBBARCHARTPANEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'kind': matplotlib_barchart_spc.KIND_CHOICES[0],
    'title': None,
    'x_label': None,
    'y_label': None,
    'legend': None,
    'show_legend': True,
    'grid': False,
    'y': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/barchart',
    '__parent__': wx_panel.SPC,
    '__doc__': 'iq.components.wx_matplotlib_barchartpanel.html',
    '__content__': (),
    '__edit__': {
        'kind': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': matplotlib_barchart_spc.KIND_CHOICES,
        },
        'title': property_editor_id.STRING_EDITOR,
        'x_label': property_editor_id.STRING_EDITOR,
        'y_label': property_editor_id.STRING_EDITOR,
        'legend': property_editor_id.STRINGLIST_EDITOR,
        'show_legend': property_editor_id.CHECKBOX_EDITOR,
        'grid': property_editor_id.CHECKBOX_EDITOR,
        'y': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'kind': u'The kind of plot to produce',
        'title': u'Title',
        'x_label': u'X axis label',
        'y_label': u'Y axis label',
        'legend': u'Bar chart legend',
        'show_legend': u'Show legend?',
        'grid': u'Show grid?',
        'y': u'Data column name for pie chart',
    },
}

SPC = WXMATPLOTLIBBARCHARTPANEL_SPC
