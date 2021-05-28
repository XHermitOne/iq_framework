#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension hierarchy specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

from .. import cube_dimension_level

__version__ = (0, 0, 0, 1)


def getLevelChoices(resource=None, parent_resource=None, *args, **kwargs):
    """
    Get levels.

    :param resource: Object resource.
    :param parent_resource: Parent object resource.
    :return:
    """
    level_names = [child['name'] for child in parent_resource.get('_children_', list()) if child['type'] == cube_dimension_level.COMPONENT_TYPE]
    return level_names


COMPONENT_TYPE = 'iqCubeDimensionHierarchy'

CUBEDIMENSIONHIERARCHY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'levels': [],

    '__package__': u'OLAP',
    '__icon__': 'fugue/node-select-all',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'levels': {
            'editor': property_editor_id.MULTICHOICE_EDITOR,
            'choices': getLevelChoices,
        },
    },
    '__help__': {
        'levels': u'List of dimension level names for this hierarchy',
    },
}

SPC = CUBEDIMENSIONHIERARCHY_SPC
