#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Object specification module.
"""

from ..editor import property_editor_id

__version__ = (0, 0, 0, 1)


OBJECT_SPC = {
    'name': 'default',
    'type': 'iqObjectProto',
    'description': '',
    'activate': True,
    'guid': None,

    '_children_': [],

    '__icon__': None,
    # '__parent__': None,
    '__doc__': None,
    '__help__': {
        'name': u'Object name',
        'type': u'Object type',
        'description': u'Description',
        'activate': u'Activate trigger',
        'guid': u'Global object identifier',
    },
    '__edit__': {
        'name': property_editor_id.STRING_EDITOR,
        'type': property_editor_id.READONLY_EDITOR,
        'description': property_editor_id.TEXT_EDITOR,
        'activate': property_editor_id.CHECKBOX_EDITOR,
        'guid': property_editor_id.READONLY_EDITOR,
    },
    '__content__': (),

    '__test__': None,       # Test function
    '__design__': None,     # Design function
}
