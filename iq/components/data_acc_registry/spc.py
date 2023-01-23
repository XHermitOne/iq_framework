#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Accumulate registry specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

from ..data_engine import spc as data_engine_spc

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqDataAccumulateRegistry'


DATAACCUMULATEREGISTRY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'db_engine': None,

    'dimension_requisites': [],
    'resource_requisites': [],
    'operation_table': 'operation_tab',
    'result_table': 'result_tab',

    '__package__': u'Data',
    '__icon__': 'fatcow/table_sum',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataColumn', ),
    '__edit__': {
        'db_engine': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_engine_spc.validDBEnginePsp,
        },
        'dimension_requisites': property_editor_id.STRINGLIST_EDITOR,
        'resource_requisites': property_editor_id.STRINGLIST_EDITOR,
        'operation_table': property_editor_id.STRING_EDITOR,
        'result_table': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database passport',
        'dimension_requisites': u'Dimension requisite names',
        'resource_requisites': u'Resource requisite names',
        'operation_table': u'Operation table name',
        'result_table': 'Result table name',
    },
}

SPC = DATAACCUMULATEREGISTRY_SPC
