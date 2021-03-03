#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data object registry specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

from ..data_engine import spc as data_engine_spc

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqDataObjectHistory'


DATAOBJECTHISTORY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'db_engine': None,

    'operation_table': 'operation_object',
    'obj_table': 'object_tab',

    '__package__': u'Data',
    '__icon__': 'fatcow/clock_history_frame',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataColumn', ),
    '__edit__': {
        'db_engine': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_engine_spc.validDBEnginePsp,
        },
        'operation_table': property_editor_id.STRING_EDITOR,
        'obj_table': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database passport',
        'operation_table': u'Operation table name',
        'obj_table': u'Data object table name',
    },
}

SPC = DATAOBJECTHISTORY_SPC
