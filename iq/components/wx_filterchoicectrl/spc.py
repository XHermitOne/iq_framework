#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter choice control specification module.
"""

from ...editor import property_editor_id
from ...object import object_spc

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

    'style': 0,
    'position': (-1, -1),
    'size': (-1, -1),
    'font': {},
    'foreground_colour': None,
    'background_colour': None,

    'save_filename': None,
    'get_env': None,
    'limit': None,

    'on_change': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/filter_reapply',
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
            'choices': WXFILTERCHOICECTRL_STYLE,
        },
        'font': property_editor_id.FONT_EDITOR,

        'save_filename': property_editor_id.FILE_EDITOR,
        'get_env': property_editor_id.METHOD_EDITOR,
        'limit': property_editor_id.INTEGER_EDITOR,
        'on_change': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'position': u'Control position',
        'size': u'Control size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Control style',
        'font': u'Text font',

        'save_filename': u'Filter storage filename',
        'get_env': u'The function of obtaining the environment',
        'limit': u'Record limit',
        'on_change': u'Filter change event handler',
    },
}

SPC = WXFILTERCHOICECTRL_SPC
