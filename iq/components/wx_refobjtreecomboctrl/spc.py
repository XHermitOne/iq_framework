#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjTreeComboCtrl specification module.
"""

import wx

from iq.object import object_spc
from ...editor import property_editor_id

from ... import passport

from .. import data_ref_object

__version__ = (0, 0, 0, 1)


REF_OBJ_TYPES = (data_ref_object.COMPONENT_TYPE, )


def validRefObjPsp(psp, *args, **kwargs):
    """
    Validate reference object passport.

    :param psp: Passport.
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in REF_OBJ_TYPES


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

    'style': 0,
    'position': (-1, -1),
    'size': (-1, -1),
    'font': {},
    'foreground_colour': None,
    'background_colour': None,

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
            'choices': WXREFOBJTREECOMBOCTRL_STYLE,
        },

        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validRefObjPsp,
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
        'position': u'Control position',
        'size': u'Control size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Control style',

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
