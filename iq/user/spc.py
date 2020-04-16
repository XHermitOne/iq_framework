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
from .. import global_data
from ..util import file_func
from ..util import res_func
from ..util import spc_func
from .. import role

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqUser'


def getProjectRoles(prj_name=None, *args, **kwargs):
    """
    Get project role name list.

    :param prj_name: Project name. If None get actual project name.
    :return: Project role name list.
    """
    if prj_name is None:
        prj_name = global_func.getProjectName()

    if not prj_name:
        log_func.error(u'Not define project name')
        return list()

    res_filename = os.path.join(file_func.getProjectPath(),
                                prj_name + res_func.RESOURCE_FILE_EXT)
    prj_resource = res_func.loadResource(res_filename)
    if prj_resource:
        children = prj_resource.get(spc_func.CHILDREN_ATTR_NAME, list())
        child_names = [child.get('name', u'Unknown') for child in children if child.get('type', None) == role.COMPONENT_TYPE]
        return child_names
    return list()


USER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    'password': None,
    'roles': [],
    'engine': global_func.getEngineType(),
    'do_main': None,

    '__package__': u'Project',
    '__icon__': 'fatcow/user',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'password': property_editor_id.PASSWORD_EDITOR,
        'roles': {
            'editor': property_editor_id.MULTICHOICE_EDITOR,
            'choices': getProjectRoles,
        },
        'engine': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': global_data.ENGINE_TYPES,
        },
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
