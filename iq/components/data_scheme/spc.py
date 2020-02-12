#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme specification module.
"""

import os.path
from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataScheme'

PROJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'db_engine': None,

    '__package__': u'Data',
    '__icon__': 'fatcow%schart_organisation' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ['iqDataModel'],
    '__edit__': {
        'db_engine': property_editor_id.READONLY_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database engine',
    },
}

SPC = PROJECT_SPC
