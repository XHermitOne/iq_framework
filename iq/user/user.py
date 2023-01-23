#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User manager module.
"""

import hashlib

from ..util import log_func
from ..util import global_func

from .. import role

__version__ = (0, 0, 0, 1)


class iqUserManager(object):
    """
    User manager class.
    """
    def getPasswordHash(self):
        """
        Get password hash.

        :return: Hash password string.
            If none then password verification is not performed.
        """
        return None

    def login(self, password=None):
        """
        Login user by password.

        :param password: Password string.
        :return: True/False.
        """
        password_hash = self.getPasswordHash()
        login_result = False
        if not password_hash:
            # Password verification is not performed
            login_result = True
        else:
            password = password if password else ''
            login_password_hash = hashlib.md5(password.encode()).hexdigest()
            # log_func.debug(u'Check password <%s> : <%s>' % (login_password_hash, password_hash))
            login_result = password_hash == login_password_hash

        if login_result:
            log_func.info(u'Login <%s> user ... OK' % self.getName())
        else:
            log_func.warning(u'Login <%s> user ... FAIL' % self.getName())

        return login_result

    def logout(self):
        """
        Logout user.

        :return: True/False.
        """
        log_func.info(u'Logout <%s> user ... OK' % self.getName())
        return True

    def run(self):
        """
        Run engine for user.

        :return:
        """
        pass

    def isAdministrator(self):
        """
        Is the user an administrator?

        :return: True/False.
        """
        return self.isRole(role_name=role.ADMINISTRATORS_ROLE_NAME)

    def isRole(self, role_name):
        """
        Does the user play a role?

        :param role_name: Role name.
        :return: True/False.
        """
        return False

    def isPermission(self, permission_name):
        """
        Use rights check.

        :param permission_name: Permission name.
        :return: True - can use / False - no.
        """
        roles = self.getRoles()
        if not roles:
            log_func.warning(u'Not define roles for user <%s>' % self.getName())

        for role in roles:
            if role.isPermission(permission_name=permission_name):
                return True
        # log_func.warning(u'Not permission <%s> for user <%s>' % (permission_name, self.getName()))
        return False

    def getRoleNames(self):
        """
        Get role names.
        """
        log_func.warning(u'Not define get role names method')
        return tuple()

    def getRoles(self):
        """
        Get user roles.

        :return: Role list.
        """
        log_func.warning(u'Not define get roles method')
        return tuple()

    def getEngineType(self):
        """
        Get engine type.
        """
        return global_func.getEngineType()

    def initEngineType(self):
        """
        Init user engine.
        """
        engine_type = self.getEngineType()
        cur_engine_type = global_func.getEngineType()
        log_func.info(u'User <%s> engine type: %s / System engine type: %s' % (self.getName(), engine_type, cur_engine_type))
        if engine_type != cur_engine_type:
            global_func.setEngineType(engine_type)
        return global_func.getEngineType()
