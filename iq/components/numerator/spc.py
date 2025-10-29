#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Numerator specification module.
"""


from iq.object import object_spc
from ...editor import property_editor_id

from . import numerator

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqNumerator'

NUMERATOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'db_engine': None,
    'num_tabname': numerator.DEFAULT_NUMERATOR_TABLE,
    'num_code_fmt': numerator.DEFAULT_NUM_CODE_FMT,
    'check_unique': False,
    'use_sys_dt': True,

    'on_do': None,
    'on_undo': None,

    '__package__': u'Special',
    '__icon__': 'fatcow/paginator',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.numerator.html',
    '__content__': (),
    '__edit__': {
        'db_engine': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': None,
        },
        'num_tabname': property_editor_id.STRING_EDITOR,
        'num_code_fmt': property_editor_id.STRING_EDITOR,
        'check_unique': property_editor_id.CHECKBOX_EDITOR,
        'use_sys_dt': property_editor_id.CHECKBOX_EDITOR,
        'on_do': property_editor_id.EVENT_EDITOR,
        'on_undo': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database engine',
        'num_tabname': u'Numerator table name',
        'num_code_fmt': u'Number-code format',
        'check_unique': u'Check unique number-code?',
        'use_sys_dt': u'Use system datetime?',
        'on_do': u'It is executed when a new number is generated',
        'on_undo': u'It is executed when the number generation is canceled',
    },
}

SPC = NUMERATOR_SPC
