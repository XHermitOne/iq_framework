#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart wx panel specification module.
"""

import pandas.plotting._matplotlib

from ...editor import property_editor_id
from .. import wx_panel

# from ..matplotlib_barchart import barchart_proto

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxMatplotlibBarChartPanel'

WXMATPLOTLIBBARCHARTPANEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    # 'bar_count': 1,
    # 'bar_width': barchart_proto.DEFAULT_BAR_WIDTH,

    'kind': tuple(pandas.plotting._matplotlib.PLOT_CLASSES.keys())[0],
    'title': None,
    'x_label': None,
    'y_label': None,
    'legend': None,
    'grid': False,

    # 'orientation': barchart_proto.HORIZONTAL_ORIENTATION,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/barchart',
    '__parent__': wx_panel.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        # 'bar_count': property_editor_id.INTEGER_EDITOR,
        # 'bar_width': property_editor_id.FLOAT_EDITOR,

        'kind': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': tuple(pandas.plotting._matplotlib.PLOT_CLASSES.keys()),
        },
        'title': property_editor_id.STRING_EDITOR,
        'x_label': property_editor_id.STRING_EDITOR,
        'y_label': property_editor_id.STRING_EDITOR,
        'legend': property_editor_id.STRINGLIST_EDITOR,
        'grid': property_editor_id.CHECKBOX_EDITOR,

        # 'orientation': {
        #     'editor': property_editor_id.CHOICE_EDITOR,
        #     'choices': (barchart_proto.HORIZONTAL_ORIENTATION,
        #                 barchart_proto.VERTICAL_ORIENTATION),
        # },
    },
    '__help__': {
        # 'bar_count': u'Bar count',
        # 'bar_width': u'Bar width',

        'kind': u'The kind of plot to produce',
        'title': u'Title',
        'x_label': u'X axis label',
        'y_label': u'Y axis label',
        'legend': u'Bar chart legend',
        'grid': u'Show grid?',

        # 'orientation': u'Bar chart orientation',
    },
}

SPC = WXMATPLOTLIBBARCHARTPANEL_SPC
