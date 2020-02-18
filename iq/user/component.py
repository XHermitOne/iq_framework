#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User component.
"""

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
        Standart component constructor.

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
        do_main_func = self.getAttribute('do_main')
        if do_main_func:
            exec_func.execTxtFunction(do_main_func, context=self.getContext())
        else:
            log_func.warning(u'Not define main function for <%s> user' % self.getName())

    def isRole(self, role_name):
        """
        Does the user play a role?

        :param role_name: Role name.
        :return: True/False.
        """
        roles = self.getAttribute('roles')
        return role_name in roles if roles else False


COMPONENT = iqUser
