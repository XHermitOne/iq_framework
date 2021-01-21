#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User component.
"""

import os

from .. import object

from . import spc
from . import user

from ..util import log_func
from ..util import exec_func

__version__ = (0, 0, 0, 1)


class iqUser(object.iqObject, user.iqUserManager):
    """
    User component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        user.iqUserManager.__init__(self, *args, **kwargs)

    def getPasswordHash(self):
        """
        Get password hash.

        :return: Hash password string.
            If none then password verification is not performed.
        """
        return self.getAttribute('password')

    def run(self):
        """
        Run engine for user.

        :return:
        """
        result = None
        do_main_func = self.getAttribute('do_main')
        if do_main_func:
            context = self.getContext()
            # Add environment variables
            if context:
                context.update(dict(os.environ))
            result = exec_func.execTxtFunction(do_main_func, context=context)
            log_func.info(u'User. Execute main function result <%s>' % str(result))
        else:
            log_func.warning(u'Not define main function for <%s> user' % self.getName())
        return result

    def isRole(self, role_name):
        """
        Does the user play a role?

        :param role_name: Role name.
        :return: True/False.
        """
        role_names = self.getRoleNames()
        return role_name in role_names if role_names else False

    def getRoleNames(self):
        """
        Get role names.
        """
        roles_attr = self.getAttribute('roles')
        if isinstance(roles_attr, str):
            return tuple([name.strip('"') for name in roles_attr.replace('" "', '"; "').split('; ')]) if roles_attr else tuple()
        elif isinstance(roles_attr, (list, tuple)):
            return roles_attr
        log_func.warning(u'Type error roles for user <%s : %s>' % (self.getName(), str(roles_attr)))
        return tuple()

    def getRoles(self):
        """
        Get user roles.

        :return: Role list.
        """
        prj = self.getParent()
        role_names = self.getRoleNames()
        # log_func.debug(u'Roles %s' % str(role_names))
        roles = [role for role in prj.getRoles() if role.getName() in role_names]
        return tuple(roles)


COMPONENT = iqUser
