#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project specification module.
"""

import os.path
from iq.object import object_spc

__version__ = (0, 0, 0, 1)


PROJECT_SPC = {
    'name': 'default',
    'type': 'iqProject',
    'description': '',
    'activate': True,
    'uuid': None,

    'children': [],

    '__package__': u'Project',
    '__icon__': 'fatcow%sbricks' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ['iqUser', 'iqRole'],
}

SPC = PROJECT_SPC
