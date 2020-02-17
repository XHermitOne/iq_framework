#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Role specification module.
"""

import os.path
from iq.object import object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqRole'

ADMINISTRATORS_ROLE_NAME = 'admins'

ROLE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    'permissions': [],

    '__package__': u'Project',
    '__icon__': 'fatcow%skey_go' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
}

SPC = ROLE_SPC
