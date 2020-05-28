#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx widget abstract specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxWidget'

WXWIDGET_STYLE = {
}

WXWIDGET_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'position': (-1, -1),
    'size': (100, 100),
    'foreground_colour': None,
    'background_colour': None,
    'style': 0,
    'font': dict(),

    '__package__': None,
    '__icon__': 'fatcow/panel_blank',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'position': property_editor_id.POINT_EDITOR,
        'size': property_editor_id.SIZE_EDITOR,
        'foreground_colour': property_editor_id.COLOUR_EDITOR,
        'background_colour': property_editor_id.COLOUR_EDITOR,
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXWIDGET_STYLE,
        },
        'font': property_editor_id.FONT_EDITOR,
    },
    '__help__': {
        'position': u'Widget position',
        'size': u'Widget size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Widget style',
        'font': u'Text font',
    },
}

SPC = WXWIDGET_SPC
