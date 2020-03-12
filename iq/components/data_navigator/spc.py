#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator specification module.
"""

import os.path
from iq.object import object_spc

from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataNavigator'

DATANAVIGATOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'model': None,

    '__package__': u'Data',
    '__icon__': 'fatcow%scompass' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),

    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
        },
    },
    '__help__': {
        'model': u'Manager management model',
    },

}

SPC = DATANAVIGATOR_SPC
