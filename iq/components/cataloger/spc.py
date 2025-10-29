#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cataloger specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

# from . import cataloger

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCataloger'

CATALOGER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'folder': None,
    'put_physic_func': None,
    'get_physic_func': None,
    'logic_catalogs': None,

    '__package__': u'Special',
    '__icon__': 'fatcow/folders_explorer',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.cataloger.html',
    '__content__': ('iqCatalogLevel', ),
    '__edit__': {
        'folder': property_editor_id.DIR_EDITOR,
        'put_physic_func': property_editor_id.SCRIPT_EDITOR,
        'get_physic_func': property_editor_id.SCRIPT_EDITOR,
        'logic_catalogs': property_editor_id.SCRIPT_EDITOR,
    },
    '__help__': {
        'folder': u'Physic catalog folder',
        'put_physic_func': u'Physical directory placement function',
        'get_physic_func': u'Retrieve function from physical directory',
        'logic_catalogs': u'Logic catalogs',
    },
}

SPC = CATALOGER_SPC
