#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube measure/fact specification module..
"""

from ...object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCubeMeasure'

CUBEMEASURE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'field_name': None,
    'label': None,

    '__package__': u'OLAP',
    '__icon__': 'fatcow/measure',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'field_name': property_editor_id.STRING_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'field_name': u'Alternative name of the fact field in the cube table, If not specified, then the name of the object is used',
        'label': u'The label, if not defined, then the description is taken',
    },
}

SPC = CUBEMEASURE_SPC
