#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine specification module.
"""

import os.path
import sqlalchemy.dialects
import wx.propgrid

from iq.object import object_spc
from ...editor import property_editor_id
from ...util import str_func

__version__ = (0, 0, 0, 1)


DB_DRIVERS = {
    'firebird': ('fdb', 'kinterbasdb'),
    'mssql': ('adodbapi', 'mxodbc', 'pymssql', 'pyodbc', 'zxjdbc'),
    'mysql': ('cymysql', 'gaerdbms', 'mysqldb', 'oursql', 'pymysql', 'pyodbc', 'zxjdbc'),
    'oracle': ('cx_oracle', 'zxjdbc'),
    'postgresql': ('pg8000', 'psycopg2', 'psycopg2cffi', 'pygresql', 'pypostgresql', 'zxjdbc'),
    'sqlite': ('pysqlcipher', 'pysqlite'),
    'sybase': ('pyodbc', 'pysybase'),
}


def getDrivers(resource=None, *args, **kwargs):
    """
    Get database drivers.

    :param resource: Object resource.
    :return:
    """
    dialect = resource.get('dialect', None)
    return [''] + list(DB_DRIVERS.get(dialect, list()))


def getEncodings(*args, **kwargs):
    """
    Get database encoding list.
    """
    return [''] + list(str_func.getEncodings())


def onDialectChange(resource_editor=None, resource=None, *args, **kwargs):
    """
    Change dialect.
    When replacing a dialect, the list of DBAPI drivers changes.

    :param resource_editor: Resource editor frame.
    :param resource: Object resource.
    """
    if resource:
        dialect = resource.get('dialect', None)
        drivers = [''] + list(DB_DRIVERS.get(dialect, list()))
        if resource_editor:
            choices = wx.propgrid.PGChoices(drivers)
            resource_editor.getProperty('driver').SetChoices(choices)


COMPONENT_TYPE = 'iqDataEngine'

PROJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'dialect': None,
    'driver': None,
    'host': 'localhost',
    'port': 0,
    'db_name': '',
    'username': 'user',
    'password': '',
    'db_filename': '',
    'convert_unicode': False,
    'echo': False,
    # 'echo_pool': False,
    'encoding': None,
    # 'execution_options': None,
    # 'implicit_returning': True,
    # 'isolation_level': None,
    # 'label_length': 0,

    '__package__': u'Data',
    '__icon__': 'fatcow%sdatabase_gear' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': [],
    '__edit__': {
        'dialect': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': sqlalchemy.dialects.__all__,
            'on_change': onDialectChange,
        },
        'driver': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getDrivers,
        },
        'host': property_editor_id.STRING_EDITOR,
        'port': property_editor_id.INTEGER_EDITOR,
        'db_name': property_editor_id.STRING_EDITOR,
        'username': property_editor_id.STRING_EDITOR,
        'password': property_editor_id.STRING_EDITOR,
        'db_filename': property_editor_id.FILE_EDITOR,
        'convert_unicode': property_editor_id.CHECKBOX_EDITOR,
        'echo': property_editor_id.CHECKBOX_EDITOR,
        # 'echo_pool': property_editor_id.CHECKBOX_EDITOR,
        'encoding': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getEncodings,
        },
        # 'execution_options': property_editor_id.SCRIPT_EDITOR,
        # 'implicit_returning': property_editor_id.CHECKBOX_EDITOR,
        # 'isolation_level': property_editor_id.STRING_EDITOR,
        # 'label_length': property_editor_id.INTEGER_EDITOR,

    },
    '__help__': {
        'dialect': 'Database type',
        'driver': 'Name of a DBAPI',
        'host': 'Host',
        'port': 'Port',
        'db_name': 'Database name',
        'username': 'Database username',
        'password': 'Password',
        'db_filename': 'DB filename for SQLite',
        'convert_unicode': u'If set to True, sets all String-based columns to accommodate Python unicode objects',
        'echo': u'If True, the engine will log all statements',
        # 'echo_pool': u'if True, the connection pool will log all checkouts/checkins to the logging stream',
        'encoding': 'Database code page',
        # 'execution_options': u'Dictionary execution options which will be applied to all connections',
        # 'implicit_returning': u'When True, a RETURNING-compatible construct, if available, will be used to fetch newly generated primary key values',
        # 'isolation_level': u'This string parameter is interpreted by various dialects in order to affect the transaction isolation level of the database connection',
        # 'label_length': u'Optional integer value which limits the size of dynamically generated column labels to that many characters',
        # 'logging_name': u'',
        # 'max_overflow': u'',
        # 'paramstyle': u'',
        # 'pool': u'',
        # 'poolclass': u'',
        # 'pool_logging_name': u'',
        # 'pool_size': u'',
        # 'pool_recycle': u'',
        # 'pool_reset_on_return': u'',
        # 'pool_timeout': u'',
        # 'strategy': u'',
        # 'executor': u'',
    },
}

SPC = PROJECT_SPC
