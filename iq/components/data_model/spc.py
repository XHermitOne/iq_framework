#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model specification module.
"""

import copy
import os.path

from iq.object import object_spc
from ...editor import property_editor_id

from .. import data_column

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataModel'

# Automatically add an identifier column
ID_COLUMN_SPC = copy.deepcopy(data_column.SPC)
ID_COLUMN_SPC['name'] = 'id'
ID_COLUMN_SPC['description'] = 'Identifier'
ID_COLUMN_SPC['field_type'] = 'BigInteger'
ID_COLUMN_SPC['primary_key'] = True
ID_COLUMN_SPC['autoincrement'] = True


DATAMODEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [ID_COLUMN_SPC],

    'tablename': None,

    '__package__': u'Data',
    '__icon__': 'fatcow/table',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataColumn', 'iqDataModel'),
    '__edit__': {
        'tablename': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'tablename': u'Storage table name',
    },
}

SPC = DATAMODEL_SPC