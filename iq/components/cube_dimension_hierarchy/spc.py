#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension hierarchy specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id


__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCubeDimensionHierarchy'

CUBEDIMENSIONHIERARCHY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'levels': None,

    '__package__': u'OLAP',
    '__icon__': 'fugue/node-select-all',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        # 'levels': None,
    },
    '__help__': {
        'levels': u'List of dimension level names for this hierarchy',
    },
}

SPC = CUBEDIMENSIONHIERARCHY_SPC
