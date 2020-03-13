#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme specification module.
"""

import os.path
from iq.object import object_spc
from ...editor import property_editor_id

from . import scheme_module_generator

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataScheme'

DATASCHEME_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,
    'module': None,

    '_children_': [],

    'db_engine': None,

    '__gen_module__': scheme_module_generator.genModule,
    '__package__': u'Data',
    '__icon__': 'fatcow%schart_organisation' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataModel', ),
    '__edit__': {
        'db_engine': property_editor_id.PASSPORT_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database engine',
    },
}

SPC = DATASCHEME_SPC
