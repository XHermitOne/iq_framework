#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart specification module.
"""

import pandas.plotting._matplotlib

from ...editor import property_editor_id
from ...object import object_spc

__version__ = (0, 0, 0, 1)

KIND_CHOICES = tuple(pandas.plotting._matplotlib.PLOT_CLASSES.keys())

COMPONENT_TYPE = 'iqMatplotlibBarChart'

MATPLOTLIBBARCHART_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'kind': KIND_CHOICES[0],
    'title': None,
    'x_label': None,
    'y_label': None,
    'legend': None,
    'grid': False,

    '__package__': u'Special',
    '__icon__': 'fatcow/chart_bar',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'kind': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': KIND_CHOICES,
        },
        'title': property_editor_id.STRING_EDITOR,
        'x_label': property_editor_id.STRING_EDITOR,
        'y_label': property_editor_id.STRING_EDITOR,
        'legend': property_editor_id.STRINGLIST_EDITOR,
        'grid': property_editor_id.CHECKBOX_EDITOR,
    },
    '__help__': {
        'kind': u'The kind of plot to produce',
        'title': u'Title',
        'x_label': u'X axis label',
        'y_label': u'Y axis label',
        'legend': u'Bar chart legend',
        'grid': u'Show grid?',
    },
}

SPC = MATPLOTLIBBARCHART_SPC
