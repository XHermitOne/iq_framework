#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MatPlotLib bar chart specification module.
"""

from ...editor import property_editor_id
from ...object import object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqMatplotlibBarChart'

MATPLOTLIBBARCHART_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    '__package__': u'Special',
    '__icon__': 'fatcow/chart_bar',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        # 'colour': property_editor_id.COLOUR_EDITOR,
        # 'legend': property_editor_id.STRING_EDITOR,
        # 'tag_name': property_editor_id.STRING_EDITOR,
        # 'history': {
        #     'editor': property_editor_id.PASSPORT_EDITOR,
        # },
    },
    '__help__': {
        # 'colour': u'Pen colour',
        # 'legend': u'Legend label',
        # 'tag_name': u'Data source tag name',
        # 'history': u'Historical data source object',
    },
}

SPC = MATPLOTLIBBARCHART_SPC
