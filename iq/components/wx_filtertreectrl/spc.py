#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter tree control specification module.
"""

from ...editor import property_editor_id
from ..wx_widget import SPC as wx_widget_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxFilterTreeCtrl'

WXFILTERTREECTRL_STYLE = {
}


WXFILTERTREECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'save_filename': None,
    'get_env': None,
    'limit': None,

    'on_change': None,

    'get_records': None,
    'get_filter_tree': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/table_filter',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'save_filename': property_editor_id.FILE_EDITOR,
        'get_env': property_editor_id.METHOD_EDITOR,
        'limit': property_editor_id.INTEGER_EDITOR,
        'on_change': property_editor_id.EVENT_EDITOR,
        'get_records': property_editor_id.METHOD_EDITOR,
        'get_filter_tree': property_editor_id.METHOD_EDITOR,
    },
    '__help__': {
        'save_filename': u'Filter storage filename',
        'get_env': u'The function of obtaining the environment',
        'limit': u'Record limit',
        'on_change': u'Filter change event handler',
        'get_records': u'Code for getting a set of records matching the filter for indicators',
        'get_filter_tree': 'Code for getting the filter tree. Alternative option for reading from a file',
    },
}

SPC = WXFILTERTREECTRL_SPC
