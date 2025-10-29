#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension level specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)


def getAttributeChoices(resource=None, parent_resource=None, *args, **kwargs):
    """
    Get attribute choices.

    :param resource: Object resource.
    :param parent_resource: Parent object resource.
    :return:
    """
    attributes = resource.get('attributes', list())
    if isinstance(attributes, str):
        attributes = [attributes]
    elif isinstance(attributes, tuple):
        attributes = list(attributes)
    return [''] + attributes if attributes else list()


COMPONENT_TYPE = 'iqCubeDimensionLevel'

CUBEDIMENSIONLEVEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'attributes': None,
    'key': None,
    'label_attribute': None,
    'label': None,
    'mapping': None,
    'get_normal': None,

    '__package__': u'OLAP',
    '__icon__': 'fugue/node-select-child',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.cube_dimension_level.html',
    '__content__': (),
    '__edit__': {
        'attributes': property_editor_id.STRINGLIST_EDITOR,
        'key': {
            'editor': property_editor_id.SINGLE_CHOICE_EDITOR,
            'choices': getAttributeChoices,
        },
        'label_attribute': {
            'editor': property_editor_id.SINGLE_CHOICE_EDITOR,
            'choices': getAttributeChoices,
        },
        'label': property_editor_id.STRING_EDITOR,
        'mapping': property_editor_id.STRING_EDITOR,
        'get_normal': property_editor_id.METHOD_EDITOR,
    },
    '__help__': {
        'attributes': u'List of field names of additional attributes',
        'key': u'Indicates which attribute will be used for filtering',
        'label_attribute': u'Indicates which attribute will be displayed in the user interface',
        'label': u'Dimension level label',
        'mapping': u'Physically specifying the field to display',
        'get_normal': u'Level data normalization function',
    },
}

SPC = CUBEDIMENSIONLEVEL_SPC
