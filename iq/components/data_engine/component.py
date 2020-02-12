#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine component.
"""

from ... import object

from . import spc
from . import db_engine

__version__ = (0, 0, 0, 1)


class iqDataEngine(object.iqObject, db_engine.iqDBEngineManager):
    """
    Data engine component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(parent=parent, resource=resource, spc=spc.SPC, context=context)
        db_engine.iqDBEngineManager.__init__(self, *args, **kwargs)

    def getDialect(self):
        """
        Get database type/dialect.

        :return:
        """
        return self.getAttribute('dialect')

    def getDriver(self):
        """
        Get database driver.

        :return:
        """
        return self.getAttribute('driver')

    def getHost(self):
        """
        Get database host.

        :return:
        """
        return self.getAttribute('host')

    def getPort(self):
        """
        Get port.

        :return:
        """
        return self.getAttribute('port')

    def getDBName(self):
        """
        Get database name.

        :return:
        """
        return self.getAttribute('db_name')

    def getUsername(self):
        """
        Get database username.

        :return:
        """
        return self.getAttribute('username')

    def getPassword(self):
        """
        Get user password.

        :return:
        """
        return self.getAttribute('password')


COMPONENT = iqDataEngine
