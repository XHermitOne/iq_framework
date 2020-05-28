#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter choice control specification module.
"""

from ...editor import property_editor_id
from ..wx_widget import SPC as wx_wisget_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxFilterChoiceCtrl'

WXFILTERCHOICECTRL_STYLE = {
}


WXFILTERCHOICECTRL_SPC = {
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

    '__package__': u'wxPython',
    '__icon__': 'fatcow/filter_reapply',
    '__parent__': wx_wisget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'save_filename': property_editor_id.FILE_EDITOR,
        'get_env': property_editor_id.METHOD_EDITOR,
        'limit': property_editor_id.INTEGER_EDITOR,
        'on_change': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'save_filename': u'Filter storage filename',
        'get_env': u'The function of obtaining the environment',
        'limit': u'Record limit',
        'on_change': u'Filter change event handler',
    },
}

SPC = WXFILTERCHOICECTRL_SPC
