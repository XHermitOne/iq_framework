#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database connection functions.
"""

import os
import traceback

try:
    import pyodbc
except ImportError:
    pass

try:
    import jaydebeapi
except ImportError:
    pass

try:
    import sqlalchemy
except:
    pass


__version__ = (0, 0, 1, 2)


# --- Use ODBC ---
def validDBConnectODBC(db_url=None):
    """
    Check connection with ODBC database.

    :param db_url: Connection string/Database URL.
    :return: True - connected. False - not connected.
    """
    if db_url is None:
        return False

    try:
        connection = pyodbc.connect(db_url)
    except:
        return False

    is_connect = False
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()

            if result:
                is_connect = True
            cursor.close()
        except:
            if cursor:
                cursor.close()
            is_connect = False
        connection.close()
    return is_connect


def getNotValidDBConnectODBCErrTxt(db_url=None):
    """
    Get connection error message if not connected with ODBC database.

    :param db_url: Connection string/Database URL.
    :return: Error message or empty string if not error .
    """
    if db_url is None:
        return u'Not define database connection string'

    try:
        connection = pyodbc.connect(db_url)
    except:
        return u'Error connection with database server\n<%s>\n%s' % (db_url, traceback.format_exc())

    error_txt = u''
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()
            if not result:
                error_txt = u'Not valid test query result\nDatabase <%s>' % db_url
            cursor.close()
        except:
            if cursor:
                cursor.close()
            error_txt = u'Error execute test query\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())
        connection.close()
    else:
        error_txt = u'Not define connection object\nDatabase <%s>' % db_url

    return error_txt


# --- Use JDBC ---
# JDBC driver types
JDBC_TYPES = ('DBF', 'MSSQL', 'POSTGRESQL')
JAVA_DRIVER_CLASS = {'DBF': 'com.hxtt.sql.dbf.DBFDriver',
                     'MSSQL': 'com.microsoft.sqlserver.jdbc.SQLServerDriver',
                     'POSTGRESQL': 'org.postgresql.Driver',
                     }

JDBC_DRIVER_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'JDBC')
JDBC_DRIVER_FILENAME = {'DBF': os.path.join(JDBC_DRIVER_DIR, 'DBF_JDBC40.jar'),
                        'MSSQL': os.path.join(JDBC_DRIVER_DIR, 'sqljdbc4.jar'),
                        'POSTGRESQL': os.path.join(JDBC_DRIVER_DIR, 'postgresql-42.2.5.jar'),
                        }


def validDBConnectJDBC(db_url=None, jdbc_type=None):
    """
    Check connection with JDBC database.

    :param db_url: Connection string/Database URL.
    :param jdbc_type: JDBC driver type:
        DBF, MSSQL or POSTGRESQL.
    :return: True - connected. False - not connected.
    """
    if jdbc_type is None or jdbc_type not in JDBC_TYPES:
        return False
    java_driver_class = JAVA_DRIVER_CLASS.get(jdbc_type, None)
    if not java_driver_class:
        return False

    # When creating a JDBC connection, all
    # JDBC drivers. Used drivers are registered at the first connect.
    # Subsequent connections look for drivers among the registered ones.
    jdbc_drivers = list(JDBC_DRIVER_FILENAME.values())
    if not jdbc_drivers or not all([os.path.exists(jdbc_driver) for jdbc_driver in jdbc_drivers]):
        return False

    if db_url is None:
        return False

    try:
        connection = jaydebeapi.connect(java_driver_class, [db_url], jdbc_drivers)
    except:
        return False

    is_connect = False
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            result = cursor.execute('SELECT 1').fetchall()

            if result:
                is_connect = True
            cursor.close()
        except:
            if cursor:
                cursor.close()
            is_connect = False
        connection.close()
    return is_connect


def getNotValidDBConnectJDBCErrTxt(db_url=None, jdbc_type=None):
    """
    Get connection error message if not connected with JDBC database.

    :param db_url: Connection string/Database URL.
    :param jdbc_type: JDBC driver type:
        DBF, MSSQL or POSTGRESQL.
    :return: Error message or empty string if not error .
    """
    if jdbc_type is None or jdbc_type not in JDBC_TYPES:
        return u'Not define JDBC driver'
    java_driver_class = JAVA_DRIVER_CLASS.get(jdbc_type, None)
    if not java_driver_class:
        return u'Not define Java driver class'

    # When creating a JDBC connection, all
    # JDBC drivers. Used drivers are registered at the first connect.
    # Subsequent connections look for drivers among the registered ones.
    jdbc_drivers = list(JDBC_DRIVER_FILENAME.values())
    if not jdbc_drivers or not all([os.path.exists(jdbc_driver) for jdbc_driver in jdbc_drivers]):
        return u'Error JDBC drivers <%s>' % jdbc_drivers

    if db_url is None:
        return u'Not define connection string'

    try:
        connection = jaydebeapi.connect(java_driver_class, [db_url], jdbc_drivers)
    except:
        return u'Error connect with database server\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())

    error_txt = u''
    if connection:
        cursor = None
        try:
            cursor = connection.cursor()

            cursor.execute('SELECT 1')
            result = cursor.fetchall()
            if not result:
                error_txt = u'Not valid test query result\nDatabase <%s>' % db_url
            cursor.close()
        except:
            if cursor:
                cursor.close()
            error_txt = u'Error execute test query\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())
        connection.close()
    else:
        error_txt = u'Not define connection object\nDatabase <%s>' % db_url

    return error_txt


# --- Use SQLAlchemy ---
def validDBConnectSQLAlchemy(db_url=None):
    """
    Check connection with database by SQLAlchemy.

    :param db_url: Connection string/Database URL.
    :return: True - connected. False - not connected.
    """
    if db_url is None:
        return False

    try:
        engine = sqlalchemy.create_engine(db_url, echo=False,
                                          connect_args={'application_name': 'Valid DB connect'})
    except:
        return False

    is_connect = False
    if engine:
        connection = None
        try:
            connection = engine.connect()
            result = connection.execute('SELECT 1').scalar()
            if result:
                is_connect = True
        except:
            is_connect = False

        if connection:
            connection.close()

    engine.dispose()
    return is_connect


def getNotValidDBConnectSQLAlchemyErrTxt(db_url=None):
    """
    Get connection error message if not connected with database by SQLAlchemy.

    :param db_url: Connection string/Database URL.
    :return: Error message or empty string if not error .
    """
    if db_url is None:
        return u'Not define connection string'

    try:
        engine = sqlalchemy.create_engine(db_url, echo=False,
                                          connect_args={'application_name': 'Valid DB connect'})
    except:
        return u'Error connect with database server\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())

    error_txt = u''
    if engine:
        connection = None
        try:
            connection = engine.connect()

            result = connection.execute('SELECT 1').scalar()
            if not result:
                error_txt = u'Not valid test query result\nDatabase <%s>' % db_url
        except:
            error_txt = u'Error execute test query\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())

        if connection is not None:
            connection.close()
    else:
        error_txt = u'Not define connection object\nDatabase <%s>' % db_url

    engine.dispose()
    return error_txt


def executeSQL(db_url=None, sql=None):
    """
    Open connection. Execute SQL. Close connection.

    :param db_url: Connection string/Database URL for connection.
    :param sql: SQL expression.
    :return: Result SQL as list of dictionaries or None if error.
    """
    if not db_url:
        print(u'Not define connection string')
        return None

    if not sql:
        print(u'Not define SQL expression')
        return None

    try:
        engine = sqlalchemy.create_engine(db_url, echo=False)
    except:
        err_msg = u'Error connect with database server\nDatabase <%s>\n%s' % (db_url, traceback.format_exc())
        print(err_msg)
        return None

    result = None
    if engine:
        connection = None
        try:
            connection = engine.connect()

            result = connection.execute(sql).fetchall()
            if not result:
                print(u'Empty query result\nDatabase <%s>' % db_url)
        except:
            print(u'Error execute test query\nDatabase <%s>\n%s' % (db_url, traceback.format_exc()))

        if connection is not None:
            connection.close()
    else:
        print(u'Not define connection object\nDatabase <%s>' % db_url)

    engine.dispose()

    records = None
    if result is not None:
        records = [dict(record) for record in result]
    return records
