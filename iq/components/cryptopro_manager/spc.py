#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CryptoPro manager specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqCryptoProManager'

CRYPTOPROMANAGER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'find_paths': None,

    '__package__': u'Special',
    '__icon__': 'csp',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.cryptopro_manager.html',
    '__content__': (),
    '__edit__': {
        'find_paths': property_editor_id.STRINGLIST_EDITOR,
    },
    '__help__': {
        'find_paths': u'Find CryptoPro console utilities paths',
    },
}

SPC = CRYPTOPROMANAGER_SPC
