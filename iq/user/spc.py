#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User specification module.
"""

import os.path
from iq.object import object_spc

__version__ = (0, 0, 0, 1)


USER_SPC = {
    'name': 'default',
    'type': 'iqUser',
    'description': '',
    'activate': True,
    'uuid': None,

    'password': None,
    'application': None,
    'roles': [],

    '__icon__': 'fatcow%suser' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': [],
}

SPC = USER_SPC
