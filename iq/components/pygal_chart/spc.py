#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pygal chart manager specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

import pygal

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqPygalChart'


PYGALCHART_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'chart_type': 'bar',
    'width': None,
    'height': None,
    'args': None,
    'output_type': 'png',
    
    '__package__': u'Special',
    '__icon__': 'fatcow/chart_pie_plane',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'chart_type': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': tuple(pygal.CHARTS_BY_NAME.keys()),
        },
        'width': property_editor_id.INTEGER_EDITOR,
        'height': property_editor_id.INTEGER_EDITOR,
        'args': property_editor_id.SCRIPT_EDITOR,
        'output_type': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': ('svg', 'png'),
        },
    },
    '__help__': {
        'chart_type': u'Chart type',
        'width': u'Result image width',
        'height': u'Result image height',
        'args': u'Arguments as dictionary',
        'output_type': u'Destination image file type',
    },
}

SPC = PYGALCHART_SPC
