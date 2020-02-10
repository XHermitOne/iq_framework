#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User specification module.
"""

import os.path

from ..object import object_spc
from ..util import global_func
from ..util import log_func
from ..editor import property_editor_id
from .. import config

__version__ = (0, 0, 0, 1)


def getProjectRoles(prj_name=None):
    """
    Get project role name list.

    :param prj_name: Project name. If None get actual project name.
    :return: Project role name list.
    """
    if prj_name is None:
        prj_name = global_func.getProjectName()
    log_func.debug(u'Project name <%s>' % prj_name)
    return list()


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
    '__edit__': {'password': property_editor_id.PASSWORD_EDITOR,
                 'roles': {'editor': property_editor_id.MULTICHOICE_EDITOR,
                           'choices': getProjectRoles},
                 'engine': {'editor': property_editor_id.CHOICE_EDITOR,
                            'choices': config.ENGINE_TYPES},
                 'do_main': property_editor_id.METHOD_EDITOR,
                 },
    '__help__': {
        'password': u'User password',
        'roles': u'Role list',
        'engine': u'Engine type',
        'do_main': u'Main method',
    },
}

SPC = USER_SPC
