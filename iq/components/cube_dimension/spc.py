#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCubeDimension'

CUBEDIMENSION_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'field_name': None,
    'attributes': None,
    'detail_tabname': None,
    'detail_fldname': None,
    'label': None,
    'mapping': None,

    '__package__': u'OLAP',
    '__icon__': 'proportion',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqCubeDimensionLevel', 'iqCubeDimensionHierarchy'),
    '__edit__': {
        'field_name': property_editor_id.STRING_EDITOR,
        'attributes': property_editor_id.STRINGLIST_EDITOR,
        'detail_tabname': property_editor_id.STRING_EDITOR,
        'detail_fldname': property_editor_id.STRING_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
        'mapping': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'field_name': u'Alternative name of the dimension field in the cube table, If not specified, then the object name is used',
        'attributes': u'List of field names of additional attributes',
        'detail_tabname': u'The name of the drill table associated with the cube table field',
        'detail_fldname': u'Name of the detail table field by which the link is made',
        'label': u'Dimension label',
        'mapping': u'Physically specifying the field to display',
    },
}

SPC = CUBEDIMENSION_SPC
