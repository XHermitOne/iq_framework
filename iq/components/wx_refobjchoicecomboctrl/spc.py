#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjChoiceComboCtrl specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

from ..data_ref_object import spc as data_ref_object_spc

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqWxRefObjChoiceComboCtrl'

WXREFOBJCHOICECOMBOCTRL_STYLE = {
    'CB_SIMPLE': wx.CB_SIMPLE,
    'CB_DROPDOWN': wx.CB_DROPDOWN,
    'CB_READONLY': wx.CB_READONLY,
    'CB_SORT': wx.CB_SORT,
}


WXREFOBJCHOICECOMBOCTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'ref_obj': None,

    'view_fields': None,
    'search_fields': None,

    'on_select': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/address_bar',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXREFOBJCHOICECOMBOCTRL_STYLE,
        },

        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_ref_object_spc.validRefObjPsp,
        },

        'view_fields': property_editor_id.STRINGLIST_EDITOR,
        'search_fields': property_editor_id.STRINGLIST_EDITOR,

        'on_select': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'ref_obj': u'Reference object passport',

        'view_fields': u'List of displayed fields',
        'search_fields': u'List of fields to search',

        'on_select': u'Combobox change event handler',
    },
}

SPC = WXREFOBJCHOICECOMBOCTRL_SPC
