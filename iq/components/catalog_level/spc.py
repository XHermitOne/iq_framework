#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Catalog level specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCatalogLevel'

CATALOGLEVEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'get_folder_name': None,

    '__package__': u'Special',
    '__icon__': 'fatcow/folder_brick',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'get_folder_name': property_editor_id.SCRIPT_EDITOR,
    },
    '__help__': {
        'get_folder_name': u'Folder name retrieval function',
    },
}

SPC = CATALOGLEVEL_SPC
