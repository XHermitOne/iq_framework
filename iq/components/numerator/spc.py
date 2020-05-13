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
    'uuid': None,

    '_children_': [],

    'db_engine': None,
    'num_tabname': numerator.DEFAULT_NUMERATOR_TABLE,
    'num_code_fmt': numerator.DEFAULT_NUM_CODE_FMT,
    'check_unique': False,
    'use_sys_dt': True,

    '__package__': u'Special',
    '__icon__': 'fatcow/paginator',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
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
    },
    '__help__': {
        'db_engine': u'Database engine',
        'num_tabname': u'Numerator table name',
        'num_code_fmt': u'Number-code format',
        'check_unique': u'Check unique number-code?',
        'use_sys_dt': u'Use system datetime?',
    },
}

SPC = NUMERATOR_SPC
