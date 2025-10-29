#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter tree control specification module.
"""

import wx

from ...editor import property_editor_id
from ..wx_widget import SPC as wx_widget_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxFilterTreeCtrl'

WXFILTERTREECTRL_STYLE = {
    'TR_DEFAULT_STYLE': wx.TR_DEFAULT_STYLE,
    'TR_HAS_BUTTONS': wx.TR_HAS_BUTTONS,
    'TR_EDIT_LABELS': wx.TR_EDIT_LABELS,
    'TR_MULTIPLE': wx.TR_MULTIPLE,
    'TR_HIDE_ROOT': wx.TR_HIDE_ROOT,
    'TR_FULL_ROW_HIGHLIGHT': wx.TR_FULL_ROW_HIGHLIGHT,
    'TR_HAS_VARIABLE_ROW_HEIGHT': wx.TR_HAS_VARIABLE_ROW_HEIGHT,
    'TR_LINES_AT_ROOT': wx.TR_LINES_AT_ROOT,
    'TR_NO_BUTTONS': wx.TR_NO_BUTTONS,
    'TR_NO_LINES': wx.TR_NO_LINES,
    'TR_ROW_LINES': wx.TR_ROW_LINES,
    'TR_SINGLE': wx.TR_SINGLE,
    'TR_TWIST_BUTTONS': wx.TR_TWIST_BUTTONS,
}


WXFILTERTREECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'style': wx.TR_DEFAULT_STYLE,

    'save_filename': None,
    'get_env': None,
    'limit': None,

    'on_change': None,

    'get_records': None,
    'get_filter_tree': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/table_filter',
    '__parent__': wx_widget_spc,
    '__doc__': 'iq.components.wx_filtertreectrl.html',
    '__content__': (),
    '__edit__': {
        'save_filename': property_editor_id.FILE_EDITOR,
        'get_env': property_editor_id.METHOD_EDITOR,
        'limit': property_editor_id.INTEGER_EDITOR,
        'on_change': property_editor_id.EVENT_EDITOR,
        'get_records': property_editor_id.METHOD_EDITOR,
        'get_filter_tree': property_editor_id.METHOD_EDITOR,

        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXFILTERTREECTRL_STYLE,
        },
    },
    '__help__': {
        'save_filename': u'Filter storage filename',
        'get_env': u'The function of obtaining the environment',
        'limit': u'Record limit',
        'on_change': u'Filter change event handler',
        'get_records': u'Code for getting a set of records matching the filter for indicators',
        'get_filter_tree': 'Code for getting the filter tree. Alternative option for reading from a file',
        'style': u'Control style',
    },
}

SPC = WXFILTERTREECTRL_SPC
