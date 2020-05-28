#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjTreeComboCtrl specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

from ..data_ref_object import spc as data_ref_object_spc

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqWxRefObjTreeComboCtrl'

WXREFOBJTREECOMBOCTRL_STYLE = {
    'CB_SIMPLE': wx.CB_SIMPLE,
    'CB_DROPDOWN': wx.CB_DROPDOWN,
    'CB_READONLY': wx.CB_READONLY,
    'CB_SORT': wx.CB_SORT,
}


WXREFOBJTREECOMBOCTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'ref_obj': None,
    'root_code': None,
    'view_all': False,
    'level_enable': -1,
    'popup_type': 0,
    'expand': True,
    'complex_load': True,

    'get_label': None,
    'find_item': None,
    'get_selected_code': None,
    'set_selected_code': None,

    'on_change': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/combo_box_light_blue',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_ref_object_spc.validRefObjPsp,
        },
        'root_code': property_editor_id.STRING_EDITOR,
        'view_all': property_editor_id.CHECKBOX_EDITOR,
        'level_enable': property_editor_id.INTEGER_EDITOR,
        'popup_type': property_editor_id.INTEGER_EDITOR,
        'expand': property_editor_id.CHECKBOX_EDITOR,
        'complex_load': property_editor_id.CHECKBOX_EDITOR,

        'get_label': property_editor_id.METHOD_EDITOR,
        'find_item': property_editor_id.METHOD_EDITOR,
        'get_selected_code': property_editor_id.METHOD_EDITOR,
        'set_selected_code': property_editor_id.METHOD_EDITOR,

        'on_change': property_editor_id.EVENT_EDITOR,

    },
    '__help__': {
        'ref_obj': u'Reference object passport',
        'root_code': u'Reference object root item cod',
        'view_all': u'View all items',
        'level_enable': u'The number of the level from which the elements to select',
        'popup_type': u'',
        'expand': u'Expand tree',
        'complex_load': u'Load all items data',

        'get_label': u'Get tree item label function',
        'find_item': u'Find tree item function',
        'get_selected_code': u'Get selected cod function',
        'set_selected_code': u'Set selected cod function',

        'on_change': u'Change selected cod event handler',
    },
}

SPC = WXREFOBJTREECOMBOCTRL_SPC
