#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine manager.
"""

import decimal
import sqlalchemy
import sqlalchemy.engine.url
import sqlalchemy.dialects.postgresql.base
import sqlalchemy.dialects.sqlite
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from ...util import log_func

__version__ = (0, 0, 1, 2)

Base = sqlalchemy.ext.declarative.declarative_base()

ENCODING2CHARSET = {
    'utf_8': 'utf8',
    'utf-8': 'utf8'
}

DEFAULT_SESSION_CLASS_ATTR_NAME = '__session_class'


class iqDBEngineManager(object):
    """
    DB engine manager.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._db_url = None

        self._engine = None

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

    def getDBFilename(self):
        """
        Get database filename (for SQLite).

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

    def _getSQLiteDBUrl(self):
        """
        Get database url for SQLite database.

        :return: Database URL string.
        """
        log_func.info(u'Create DB URL <%s>:' % self.getDialect())
        log_func.info(u'\tDatabase filename: %s' % self.getDBFilename())

        url = sqlalchemy.engine.url.URL(drivername=self.getDialectDriver(),
                                        database=self.getDBFilename())
        db_url = str(url)
        return db_url

    def _getDBUrl(self):
        """
        Get database url for SQL database.

        :return: Database URL string.
        """
        log_func.info(u'Create DB URL <%s>:' % self.getDialect())
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
        db_url = str(url)
        return db_url

    def getDBUrl(self):
        """
        Get database url.
        """
        if self._db_url is None:
            dialect = self.getDialect()
            if dialect == sqlalchemy.dialects.sqlite.dialect.name:
                self._db_url = self._getSQLiteDBUrl()
            else:
                self._db_url = self._getDBUrl()
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
        :return:
        """
        if db_url is None:
            db_url = self.getDBUrl()

        # Set DB engine application name for PostgreSQL
        try:
            dialect = self.getDialect()
            if dialect == sqlalchemy.dialects.postgresql.base.PGDialect.name:
                db_application_name = self.getName()
                connect_args_dict = dict(connect_args={'application_name': db_application_name})
                if 'connect_args' not in kwargs:
                    kwargs.update(connect_args_dict)
        except:
            log_func.fatal(u'Error set DB engine application name in <%s>' % self.__class__.__name__)

        engine = sqlalchemy.create_engine(db_url, *args, **kwargs)
        log_func.info(u'Create sqlalchemy DB engine <%s>' % db_url)
        return engine

    def getEngine(self, *args, **kwargs):
        """
        Get sqlalchemy DB engine object.
        """
        if self._engine is None:
            self._engine = self.create(*args, **kwargs)
        return self._engine

    def close(self, engine=None):
        """
        Close sqlalchemy DB engine object.

        :param engine: Sqlalchemy DB engine object.
        :return: True/False.
        """
        if engine is None:
            try:
                if self._engine:
                    self._engine.dispose()
                    log_func.info(u'Close sqlalchemy DB engine <%s>' % self._engine.url)
                    self._engine = None
                    return True
            except:
                log_func.fatal(u'Error close sqlalchemy DB engine <%s>' % self._engine.url)
            return False

        try:
            if engine:
                engine.dispose()
                log_func.info(u'Close sqlalchemy DB engine <%s>' % engine.url)
                engine = None
                return True
        except:
            log_func.fatal(u'Error close sqlalchemy DB engine <%s>' % engine.url)
        return False

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
                result = connection.execute('SELECT 1').scalar()
                if result:
                    is_connect = True
            except:
                log_func.fatal(u'Error check connection <%s>' % self.getDBUrl())
                is_connect = False

            if connection:
                connection.close()

        return is_connect

    def executeSQL(self, sql_query, first_record=False):
        """
        Execute SQL expression.

        :param sql_query: SQL query text.
        :param first_record: True - get only first record / False - get all records.
        :return: Dataset record list or None if error.
        """
        if not self.checkConnection():
            log_func.error(u'Not connect with DB <%s>' % self.getName())
            return None

        engine = self.create()
        connection = None
        try:
            connection = engine.connect()

            recordset = list()
            transaction = connection.begin()
            try:
                result = connection.execute(sql_query)
                if result and result.returns_rows:
                    if first_record:
                        records = [result.fetchone()]
                    else:
                        records = result.fetchall()
                    recordset = [dict([(name, float(value) if isinstance(value, decimal.Decimal) else value) for name, value in dict(rec).items()]) for rec in records]
                else:
                    log_func.info(u'Query <%s> not return recordset' % sql_query)
                transaction.commit()
            except:
                transaction.rollback()
                log_func.fatal(u'Error execute SQL query <%s>' % sql_query)
            connection.close()
            return recordset
        except:
            if connection:
                connection.close()
            err_txt = u'Error execute SQL query <%s>' % str(sql_query)
            log_func.fatal(err_txt)
        return None

    def getSessionClass(self, db_url=None, base=None, *args, **kwargs):
        """
        Get session class.

        :param db_url: Database URL.
            If is None then get from DB engine.
        :param base: Base model class.
        :return: Session class.
        """
        if not hasattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME):
            if db_url is None:
                db_url = self.getDBUrl()

            if base is None:
                base = Base

            if base is None:
                log_func.warning(u'Not define base class in database engine <%s>' % self.getName())
                return None

            engine = self.create(db_url)
            base.metadata.create_all(engine, checkfirst=True)

            # creating a Session class configuration
            session_class = sqlalchemy.orm.sessionmaker(bind=engine, *args, **kwargs)
            log_func.info(u'Create database engine <%s> session' % self.getName())
            setattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME, session_class)

        if hasattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME):
            return getattr(self, DEFAULT_SESSION_CLASS_ATTR_NAME)
        else:
            log_func.warning(u'Error create database engine <%s> session class' % self.getName())
        return None

    def openSession(self, db_url=None, base=None, *args, **kwargs):
        """
        Create session object.

        :param db_url: Database URL.
            If is None then get from DB engine.
        :param base: Base model class.
        :return: Session object or None if error.
        """
        session_class = self.getSessionClass(db_url=db_url, base=base, *args, **kwargs)

        # create Session object
        session = None
        if session_class is not None:
            session = session_class()
        return session

    def closeSession(self, session=None):
        """
        Close session.
        Always close the session after use.
        otherwise the DB server does not release the connection and happens
        excess of the limit of open connections. After exceeding the limit
        DB server denies service to clients.

        :param session: Session object.
        :return: True/False.
        """
        if session is None:
            log_func.warning(u'Not define session for close')
            return False

        if session is not None:
            # session.expunge_all()
            session.close()
            # log_func.info(u'Data scheme <%s> close session' % self.getName())
            return True
        else:
            log_func.warning(u'Not define session object in database engine <%s>' % self.getName())
        return False

    def startTransaction(self, *args, **kwargs):
        """
        Start transaction.

        :return: Session/transaction object.
        """
        return self.openSession(*args, **kwargs)

    def stopTransaction(self, transaction):
        """
        Stop transaction.

        :param transaction: Session/transaction object.
        :return: True/False.
        """
        return self.closeSession(session=transaction)
