#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trend pen specification module.
"""

import os.path

from ...editor import property_editor_id
from ...object import object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqTrendPen'

TRENDPEN_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'colour': (0, 0, 255),
    'legend': None,
    'tag_name': None,
    'history': None,

    '__package__': u'SCADA',
    '__icon__': 'fatcow/chart_line_edit',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.trend_pen.html',
    '__content__': (),
    '__edit__': {
        'colour': property_editor_id.COLOUR_EDITOR,
        'legend': property_editor_id.STRING_EDITOR,
        'tag_name': property_editor_id.STRING_EDITOR,
        'history': {
            'editor': property_editor_id.PASSPORT_EDITOR,
        },
    },
    '__help__': {
        'colour': u'Pen colour',
        'legend': u'Legend label',
        'tag_name': u'Data source tag name',
        'history': u'Historical data source object',
    },
}

SPC = TRENDPEN_SPC
