#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx TableChoiceCtrl specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id
from ... import passport

from ..data_model import spc as data_model_spc
from ..data_query import spc as data_query_spc

__version__ = (0, 0, 0, 1)


TABLE_MODEL_TYPES = (data_model_spc.COMPONENT_TYPE, data_query_spc.COMPONENT_TYPE)


def validTableObjPsp(psp, *args, **kwargs):
    """
    Validate table object passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in TABLE_MODEL_TYPES


COMPONENT_TYPE = 'iqWxTableChoiceCtrl'

WXTABLECHOICECTRL_STYLE = {
    'CB_SIMPLE': wx.CB_SIMPLE,
    'CB_DROPDOWN': wx.CB_DROPDOWN,
    'CB_READONLY': wx.CB_READONLY,
    'CB_SORT': wx.CB_SORT,
}


WXTABLECHOICECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'table': None,
    'code_field': '',
    'label_field': '',
    'get_label': None,
    'get_filter': None,
    'can_empty': True,

    'on_change': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/combo_box_light_blue',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'table': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validTableObjPsp,
        },
        'code_field': property_editor_id.STRING_EDITOR,
        'label_field': property_editor_id.STRING_EDITOR,
        'can_empty': property_editor_id.CHECKBOX_EDITOR,

        'get_label': property_editor_id.METHOD_EDITOR,
        'get_filter': property_editor_id.METHOD_EDITOR,

        'on_change': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'table': u'Data source table / query passport',
        'code_field': u'The field that is the record code',
        'label_field': u'The field that is displayed in the control',
        'get_filter': u'Additional filtering code for table / query data',
        'can_empty': u'Is it possible to choose an empty value?',
        'get_label': u'Get tree item label function',
        'on_change': u'Change selected cod event handler',
    },
}

SPC = WXTABLECHOICECTRL_SPC
