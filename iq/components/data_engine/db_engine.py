#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine manager.
"""

import sqlalchemy
import sqlalchemy.engine.url

__version__ = (0, 0, 0, 1)


class iqDBEngineManager(object):
    """
    DB engine manager.
    """
    def getDialect(self):
        """
        Get database type/dialect.

        :return:
        """
        return None

    def getDriver(self):
        """
        Get database driver.

        :return:
        """
        return None

    def getHost(self):
        """
        Get database host.

        :return:
        """
        return None

    def getPort(self):
        """
        Get port.

        :return:
        """
        return 0

    def getDBName(self):
        """
        Get database name.

        :return:
        """
        return None

    def getUsername(self):
        """
        Get database username.

        :return:
        """
        return None

    def getPassword(self):
        """
        Get user password.

        :return:
        """
        return None

    def getDBUrl(self):
        """
        Get database url.
        """
        url = sqlalchemy.engine.url.URL(drivername=self.getDriver(),
                                        username=self.getUsername(),
                                        password=self.getPassword(),
                                        host=self.getHost(),
                                        port=self.getPort(),
                                        database=self.getDBName(),
                                        )
        return str(url)

    def isEcho(self):
        """
        """
        return False

    def isConvertUnicode(self):
        """
        """
        return False

    def getEncoding(self):
        """
        """
        return 'utf-8'

    def create(self, db_url=None, *args, **kwargs):
        """
        Create engine.

        :param db_url: Database URL.
            If None then generate.
        :param args:
        :param kwargs:
        :return:
        """
        if db_url is None:
            db_url = self.getDBUrl()

        return sqlalchemy.create_engine(db_url, *args, **kwargs)
