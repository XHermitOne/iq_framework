#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User specification module.
"""

import os.path

from ..object import object_spc
from ..util import global_func

__version__ = (0, 0, 0, 1)


USER_SPC = {
    'name': 'default',
    'type': 'iqUser',
    'description': '',
    'activate': True,
    'uuid': None,

    'password': None,
    'roles': [],
    'engine': global_func.getEngineType(),
    'do_main': None,

    '__package__': u'Project',
    '__icon__': 'fatcow%suser' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': [],

    '__help__': {
        'password': u'User password',
        'roles': u'Role list',
        'engine': u'Engine type',
        'do_main': u'Main method',
    },
}

SPC = USER_SPC
