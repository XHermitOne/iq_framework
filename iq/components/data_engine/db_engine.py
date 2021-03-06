#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine manager.
"""

import sqlalchemy
import sqlalchemy.engine.url

from ...util import log_func

__version__ = (0, 0, 0, 1)

ENCODING2CHARSET = {
    'utf_8': 'utf8',
    'utf-8': 'utf8'
}


class iqDBEngineManager(object):
    """
    DB engine manager.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._db_url = None

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
        if self._db_url is None:
            log_func.info(u'Create DB URL:')
            log_func.info(u'\tDriver: %s' % self.getDialectDriver())
            log_func.info(u'\tHost: %s' % self.getHost())
            log_func.info(u'\tPort: %s' % self.getPort())
            log_func.info(u'\tDB name: %s' % self.getDBName())
            log_func.info(u'\tUsername: %s' % self.getUsername())

            query = None
            charset = self.getCharset()
            if charset:
                if query is None:
                    query = dict()
                query['charset'] = charset
                log_func.info(u'\tCharset: %s' % charset)

            url = sqlalchemy.engine.url.URL(drivername=self.getDialectDriver(),
                                            username=self.getUsername(),
                                            password=self.getPassword(),
                                            host=self.getHost(),
                                            port=self.getPort(),
                                            database=self.getDBName(),
                                            query=query)
            self._db_url = str(url)
        return self._db_url

    def isEcho(self):
        """
        """
        return False

    def isConvertUnicode(self):
        """
        """
        return False

    def getCharset(self):
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

    def checkConnection(self):
        """
        Connection check.

        :return: True/False.
        """
        engine = self.create()

        is_connect = False
        if engine:
            connection = None
            try:
                connection = engine.connect()
                result = connection.execute('SELECT 1').fetchall()
                if result:
                    is_connect = True
                connection.close()
            except:
                log_func.fatal(u'Error check connection <%s>' % self.getDBUrl())
                if connection:
                    connection.close()
                is_connect = False
        return is_connect

    def executeSQL(self, sql_query):
        """
        Execute SQL expression.

        :param sql_query: SQL query text.
        :return: Dataset record list or None if error.
        """
        if not self.checkConnection():
            log_func.error(u'Not connect with DB <%s>' % self.getName())
            return None

        engine = self.create()
        connection = None
        try:
            connection = engine.connect()
            result = connection.execute(sql_query)
            records = result.fetchall()
            recordset = [dict(rec) for rec in records]
            connection.close()
            return recordset
        except:
            if connection:
                connection.close()
            err_txt = u'Error execute SQL query <%s>' % str(sql_query)
            log_func.fatal(err_txt)
        return None
