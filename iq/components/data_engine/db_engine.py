#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine manager.
"""

import sqlalchemy
import sqlalchemy.engine.url

from ...util import log_func

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

    def getDialectDriver(self):
        """
        Get dialect+driver.
        """
        dialect = self.getDialect()
        driver = self.getDriver()

        dialect_driver = tuple([item for item in (dialect, driver) if item])
        return '+'.join(dialect_driver)

    def getDBUrl(self):
        """
        Get database url.
        """
        log_func.info(u'Create DB URL:')
        log_func.info(u'\tDriver: %s' % self.getDialectDriver())
        log_func.info(u'\tHost: %s' % self.getHost())
        log_func.info(u'\tPort: %s' % self.getPort())
        log_func.info(u'\tDB name: %s' % self.getDBName())
        log_func.info(u'\tUsername: %s' % self.getUsername())

        url = sqlalchemy.engine.url.URL(drivername=self.getDialectDriver(),
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
