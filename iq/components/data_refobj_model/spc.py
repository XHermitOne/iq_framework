#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object model specification module.
"""

import copy
import os.path

from ..data_model import spc
# from ...editor import property_editor_id

from .. import data_column

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataRefObjModel'

# Automatically add reference object model columns
COD_COLUMN_SPC = copy.deepcopy(data_column.SPC)
COD_COLUMN_SPC['name'] = 'cod'
COD_COLUMN_SPC['description'] = 'Code'
COD_COLUMN_SPC['field_type'] = 'Text'

NAME_COLUMN_SPC = copy.deepcopy(data_column.SPC)
NAME_COLUMN_SPC['name'] = 'name'
NAME_COLUMN_SPC['description'] = 'Name'
NAME_COLUMN_SPC['field_type'] = 'Text'

ACTIVATE_COLUMN_SPC = copy.deepcopy(data_column.SPC)
ACTIVATE_COLUMN_SPC['name'] = 'activate'
ACTIVATE_COLUMN_SPC['description'] = 'Activate'
ACTIVATE_COLUMN_SPC['field_type'] = 'Boolean'
ACTIVATE_COLUMN_SPC['default'] = 'True'

COMPUTER_COLUMN_SPC = copy.deepcopy(data_column.SPC)
COMPUTER_COLUMN_SPC['name'] = 'computer'
COMPUTER_COLUMN_SPC['description'] = 'Computer'
COMPUTER_COLUMN_SPC['field_type'] = 'Text'
COMPUTER_COLUMN_SPC['default'] = 'iq.getComputerName()'

USERNAME_COLUMN_SPC = copy.deepcopy(data_column.SPC)
USERNAME_COLUMN_SPC['name'] = 'username'
USERNAME_COLUMN_SPC['description'] = 'User name'
USERNAME_COLUMN_SPC['field_type'] = 'Text'
USERNAME_COLUMN_SPC['default'] = 'iq.getUsername()'

DT_EDIT_COLUMN_SPC = copy.deepcopy(data_column.SPC)
DT_EDIT_COLUMN_SPC['name'] = 'dt_edit'
DT_EDIT_COLUMN_SPC['description'] = 'Datetime last editing'
DT_EDIT_COLUMN_SPC['field_type'] = 'DateTime'
DT_EDIT_COLUMN_SPC['default'] = 'datetime.datetime.now'
DT_EDIT_COLUMN_SPC['onupdate'] = 'datetime.datetime.now'

REF_OBJ_DATAMODEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [spc.ID_COLUMN_SPC,
                   COD_COLUMN_SPC,
                   NAME_COLUMN_SPC,
                   ACTIVATE_COLUMN_SPC,
                   COMPUTER_COLUMN_SPC,
                   USERNAME_COLUMN_SPC,
                   DT_EDIT_COLUMN_SPC],

    '__package__': u'Data',
    '__icon__': 'fatcow/table',
    '__parent__': spc.DATAMODEL_SPC,
    '__doc__': None,
    '__content__': ('iqDataColumn', ),
    '__edit__': {
    },
    '__help__': {
    },
}

SPC = REF_OBJ_DATAMODEL_SPC
