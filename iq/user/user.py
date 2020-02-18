#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User manager module.
"""

import hashlib

from ..util import log_func
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
            log_func.error(u'Login <%s> user ... FAIL' % self.getName())

        return login_result

    def logout(self):
        """
        Logout user.

        :return: True/False.
        """
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
