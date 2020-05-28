#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjLevelChoiceCtrl specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
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

    'ref_obj': None,

    'label': None,
    'auto_select': True,
    'on_select_code': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/combo_boxes',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_ref_object_spc.validRefObjPsp,
        },

        'label': property_editor_id.STRING_EDITOR,
        'auto_select': property_editor_id.CHECKBOX_EDITOR,
        'on_select_code': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'ref_obj': u'Reference object passport',

        'label': u'Selection area title',
        'auto_select': u'Auto-complete',
        'on_select_code': u'Select code handler',
    },
}

SPC = WXREFOBJLEVELCHOICECTRL_SPC
