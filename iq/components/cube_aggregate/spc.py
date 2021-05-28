#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube aggregation specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id
# from ... import passport

from . import cube_aggregate_proto

from .. import cube_measure

__version__ = (0, 0, 0, 1)


def getMeasures(resource=None, parent_resource=None, *args, **kwargs):
    """
    Get measure names.

    :param resource: Object resource.
    :param parent_resource: Parent object resource.
    :return:
    """
    measure_names = [child['name'] for child in parent_resource.get('_children_', list()) if child['type'] == cube_measure.COMPONENT_TYPE]
    return tuple([''] + measure_names)


COMPONENT_TYPE = 'iqCubeAggregate'

CUBEAGGREGATE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'function': None,
    'measure': None,
    'expression': None,
    'label': None,

    '__package__': u'OLAP',
    '__icon__': 'fatcow/sum',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'function': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': cube_aggregate_proto.AGGREGATE_FUNCTIONS,
        },
        'measure': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getMeasures,
        },
        'expression': property_editor_id.METHOD_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'function': u'Aggregate function',
        'measure': u'Measure/Fact that is aggregated ',
        'expression': u'Aggregate expression',
        'label': u'Aggregate label',
    },
}

SPC = CUBEAGGREGATE_SPC
