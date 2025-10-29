#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqCube'

CUBE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'table_name': None,
    'label': None,

    '__package__': u'OLAP',
    '__icon__': 'fatcow/soil_layers',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.cube.html',
    '__content__': ('iqCubeDimension', 'iqCubeMeasure', 'iqCubeAggregate'),
    '__edit__': {
        'table_name': property_editor_id.STRING_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'table_name': u'Alternative name of the cube table in the database, If not specified, then the name of the cube is used',
        'label': u'Label, if not specified, is taken description',
    },
}

SPC = CUBE_SPC
