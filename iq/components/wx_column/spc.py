#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx column specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxColumn'

WXCOLUMN_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    'label': 'column',
    'width': 50,
    'data_name': None,

    'background_colour': None,
    'foreground_colour': None,
    'font': {},
    'align': ('left', 'top'),

    'sort': False,

    'get_group_key': None,  # Получение ключа группы
    'get_group_title': None,  # Получение заголовка группы

    '__package__': u'wxPython',
    '__icon__': 'fatcow/table_select_column',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'label': property_editor_id.STRING_EDITOR,
        'width': property_editor_id.INTEGER_EDITOR,
        'data_name': property_editor_id.STRING_EDITOR,

        'background_colour': property_editor_id.COLOUR_EDITOR,
        'foreground_colour': property_editor_id.COLOUR_EDITOR,
        'font': property_editor_id.FONT_EDITOR,
        'align': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': ['(\'left\', \'top\')',
                        '(\'right\', \'top\')',
                        '(\'centre\', \'top\')',
                        '(\'left\', \'centre\')',
                        '(\'right\', \'centre\')',
                        '(\'centre\', \'centre\')',
                        '(\'left\', \'bottom\')',
                        '(\'right\', \'bottom\')',
                        '(\'centre\', \'bottom\')',
                        ],
        },

        'sort': property_editor_id.CHECKBOX_EDITOR,

        'get_group_key': property_editor_id.METHOD_EDITOR,
        'get_group_title': property_editor_id.METHOD_EDITOR,
    },
    '__help__': {
        'label': u'Column label',
        'width': u'Column width',
        'data_name': u'Data column name',

        'background_colour': u'Column background colour',
        'foreground_colour': u'Column text colour',
        'font': u'Column label font',
        'align': u'Column text alignment',

        'sort': u'Sort column?',

        'get_group_key': u'Get group key method',
        'get_group_title': u'Get group title method',
    },
}

SPC = WXCOLUMN_SPC

