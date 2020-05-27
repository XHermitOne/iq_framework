#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjLevelChoiceCtrl specification module.
"""

import wx

from iq.object import object_spc
from ...editor import property_editor_id

from ..data_ref_object import spc as data_ref_object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxRefObjLevelChoiceCtrl'

WXREFOBJLEVELCHOICECTRL_STYLE = {
}

WXREFOBJLEVELCHOICECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'style': 0,
    'position': (-1, -1),
    'size': (-1, -1),
    'font': {},
    'foreground_colour': None,
    'background_colour': None,

    'ref_obj': None,

    'label': None,
    'auto_select': True,
    'on_select_code': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/combo_boxes',
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
            'choices': WXREFOBJLEVELCHOICECTRL_STYLE,
        },
        'font': property_editor_id.FONT_EDITOR,

        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_ref_object_spc.validRefObjPsp,
        },

        'label': property_editor_id.STRING_EDITOR,
        'auto_select': property_editor_id.CHECKBOX_EDITOR,
        'on_select_code': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'position': u'Control position',
        'size': u'Control size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Control style',
        'font': u'Text font',

        'ref_obj': u'Reference object passport',

        'label': u'Selection area title',
        'auto_select': u'Auto-complete',
        'on_select_code': u'Select code handler',
    },
}

SPC = WXREFOBJLEVELCHOICECTRL_SPC
