#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model specification module.
"""

import os.path
from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataModel'

PROJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'tablename': None,
    # 'mapper_args': None,

    '__package__': u'Data',
    '__icon__': 'fatcow%stable' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataColumn', ),
    '__edit__': {
        'tablename': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'tablename': u'Storage table name',
    },
}

SPC = PROJECT_SPC
