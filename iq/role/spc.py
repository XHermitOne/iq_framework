#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Role specification module.
"""

import operator
import os.path

from iq.object import object_spc

from ..editor import property_editor_id

from . import component

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqRole'

ADMINISTRATORS_ROLE_NAME = 'admins'


def getPermissions(*args, **kwargs):
    """
    Get permissions.

    :return: Selected permissions.
    """
    permissions = sorted(component.getPermissions(),
                         key=operator.itemgetter('type', 'name'))
    return ['%s.%s (%s)' % (permission.get('type', 'STANDARD'),
                            permission.get('name', 'default'),
                            permission.get('description', '')) for permission in permissions]


ROLE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    'permissions': '',

    '__package__': u'Project',
    '__icon__': 'fatcow/key_go',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'permissions': {
            'editor': property_editor_id.MULTICHOICE_EDITOR,
            'choices': getPermissions,
        },
    },
    '__help__': {
        'permissions': u'Role permissions',
    },

}

SPC = ROLE_SPC
