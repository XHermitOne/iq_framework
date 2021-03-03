#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project specification module.
"""

import os.path
from iq.object import object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqProject'

PROJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    '__package__': u'Project',
    '__icon__': 'fatcow/bricks',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqUser', 'iqRole'),
}

SPC = PROJECT_SPC
