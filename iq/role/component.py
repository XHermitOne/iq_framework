#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Role component.
"""

import gettext

from .. import object

from . import spc

from ..util import log_func

__version__ = (0, 0, 0, 1)

_ = gettext.gettext

PERMISSIONS = list()


def addPermision(name='default', description='', type='STANDARD'):
    """
    Append permission.

    :param name: Permission name.
    :param description: Permission description.
    :param type: Permission type.
    :return: True/False.
    """
    permissions = globals()['PERMISSIONS']
    permission_names = [permission.get('name', None) for permission in permissions]
    if name not in permission_names:
        new_permission = dict(name=name, description=description, type=type)
        permissions.append(new_permission)
        return True
    else:
        log_func.warning(u'The permission <%s> is already registered in the system' % name)
    return False


def appendPermissions(permissions):
    """
    Append permission list.

    :param permissions: Permission list.
    :return: True/False.
    """
    return all([addPermision(**permission) if isinstance(permission, dict) else False for permission in permissions])


def delPermision(name='default'):
    """
    Delete permission.

    :param name: Permission name.
    :return: True/False.
    """
    permissions = globals()['PERMISSIONS']
    permission_names = [permission.get('name', None) for permission in permissions]
    if name not in permission_names:
        permission_idx = permission_names.index(name)
        del permissions[permission_idx]
        return True
    else:
        log_func.warning(u'The permission <%s> not found' % name)
    return False


def isPermision(name='default'):
    """
    Is the permission registered in the system?

    :param name: Permission name.
    :return: True/False.
    """
    permissions = globals()['PERMISSIONS']
    permission_names = [permission.get('name', None) for permission in permissions]
    return name in permission_names


def getPermissions():
    """
    Get permissions.

    :return: Selected permissions.
    """
    return globals()['PERMISSIONS']


CREATE_PERMISSION = dict(name='create', description=_('Can create'), type='STANDARD')
READ_PERMISSION = dict(name='read', description=_('Can read'), type='STANDARD')
WRITE_PERMISSION = dict(name='write', description=_('Can write'), type='STANDARD')
ADD_PERMISSION = dict(name='add', description=_('Can add'), type='STANDARD')
DEL_PERMISSION = dict(name='delete', description=_('Can delete'), type='STANDARD')
VIEW_PERMISSION = dict(name='view', description=_('Can view'), type='STANDARD')
EDIT_PERMISSION = dict(name='edit', description=_('Can edit'), type='STANDARD')

STANDARD_PERMISSIONS = (CREATE_PERMISSION, READ_PERMISSION, WRITE_PERMISSION,
                        ADD_PERMISSION, DEL_PERMISSION,
                        VIEW_PERMISSION, EDIT_PERMISSION)

appendPermissions(STANDARD_PERMISSIONS)


class iqRole(object.iqObject):
    """
    Role component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)

    def isPermission(self, permission_name=None):
        """
        Does the role have permission?

        :param permission_name: Permission name.
        :return: True/False.
        """
        permissions = self.getAttribute('permissions')
        permission_signature = '%s (' % permission_name
        return isPermision(permission_name) and permission_signature in permissions


COMPONENT = iqRole
