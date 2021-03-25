#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции манипулирования DBF таблицами.
"""

import os
import os.path
import jaydebeapi

from . import log_func

try:
    import dbfpy3.dbf
except ImportError:
    log_func.error(u'Import error dbfpy3.dbf')

__version__ = (0, 0, 0, 1)

#
DBF_DB_URL_FMT = 'jdbc:dbf:///%s?charSet=%s'
JDBC_DBF_DRIVER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'JDBC', 'DBF_JDBC42.jar')

DEFAULT_DBF_ENCODING = 'cp1251'


def getDBFFieldNames(tab_filename):
    """
    Get DBF file field names.

    :param tab_filename: DBF table filename.
    :return: DBF file field name list.
    """
    tab_dbf = None
    field_names = list()
    try:
        log_func.info(u'Open dbf table <%s>' % tab_filename)
        tab_dbf = dbfpy3.dbf.Dbf(tab_filename, new=False)
        field_names = tab_dbf.fieldNames
        tab_dbf.close()
    except:
        if tab_dbf:
            tab_dbf.close()
        log_func.fatal(u'Error get DBF file <%s> field names' % tab_filename)
    return field_names


def existsColumns(tab_filename, columns, auto_create=True):
    """
    Exists column in DBF file?.

    :param tab_filename: DBF table filename.
    :param columns: Column list.
        [(Column name, Column type, Length, Default value), ...]
    :param auto_create: Create column automatic, if not exists?
    :return: True - all columns exists. False - column not found.
    """
    results = list()
    try:
        fields = getDBFFieldNames(tab_filename)

        results = [column[0] in fields for column in columns]
        for column in columns:
            column_name = column[0]
            if column_name not in fields:
                if auto_create:
                    column_type = column[1]
                    column_len = column[2] if len(column) > 2 else 0
                    column_default = column[3] if len(column) > 3 else None

                    addDBFNewField(tab_filename, column_name, column_type, column_len, default=column_default)
    except:
        log_func.fatal(u'Error check exists columns in DBF table <%s>' % tab_filename)
    return all(results)


def addDBFNewField(dbf_filename,
                   new_fieldname,
                   field_type='C',
                   field_length=255,
                   default=None):
    """
    Append new field in DBF file.

    :param dbf_filename: DBF table filename.
    :param new_fieldname: Field name.
    :param field_type: Fielt type (C-string).
    :param field_length: Field length.
    :param default: Default value.
    :return: True/False.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'Add field in DBF file. File <%s> not found' % dbf_filename)
        return False

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        # Create new field
        if field_type == 'C':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s VARCHAR(%d)' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                         new_fieldname, field_length)
            if default is not None:
                sql += ' DEFAULT \'%s\'' % str(default)
            log_func.debug(u'Execute SQL <%s>' % sql)
            db_cursor.execute(sql)
        elif field_type == 'L':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s BOOLEAN' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                     new_fieldname)
            if default is not None:
                sql += ' DEFAULT %s' % str(default)
            db_cursor.execute(sql)
        elif field_type == 'D':
            db_cursor = dbf_connection.cursor()
            sql = 'ALTER TABLE %s ADD %s DATE' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                  new_fieldname)
            if default is not None:
                sql += ' DEFAULT \'%s\'' % str(default)
            db_cursor.execute(sql)
        else:
            log_func.warning(u'Add field in DBF file. Field type <%s> not supported' % field_type)
        dbf_connection.close()
        return True
    except:
        if dbf_connection:
            dbf_connection.close()
        log_func.fatal(u'Error add field in DBF file <%s>' % dbf_filename)
    return False


def addDBFNewFields(dbf_filename, *field_defs):
    """
    Append new fields in DBF file.

    :param dbf_filename: DBF table filename.
    :param field_defs: Field defines (Field name, Field type, Length, Default value).
    :return: True/False.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'Add fields in DBF file. File <%s> not found' % dbf_filename)
        return False

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        for new_fieldname, field_type, field_length, default in field_defs:
            # Create new field
            if field_type == 'C':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s VARCHAR(%d)' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                             new_fieldname, field_length)
                if default is not None:
                    sql += ' DEFAULT \'%s\'' % str(default)
                # log.debug(u'Execute SQL <%s>' % sql)
                db_cursor.execute(sql)
            elif field_type == 'L':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s BOOLEAN' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                         new_fieldname)
                if default is not None:
                    sql += ' DEFAULT %s' % str(default)
                db_cursor.execute(sql)
            elif field_type == 'D':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s DATE' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                      new_fieldname)
                if default is not None:
                    sql += ' DEFAULT \'%s\'' % str(default)
                db_cursor.execute(sql)
            else:
                log_func.warning(u'Add fields in DBF file. Field type <%s> not supported' % field_type)
                continue
        dbf_connection.close()
        return True
    except:
        if dbf_connection:
            dbf_connection.close()
        log_func.fatal(u'Error add fields in FBG file <%s>' % dbf_filename)
    return False


def setDBFFieldValue(dbf_filename, field_name, value, field_type='C'):
    """
    Set DBF file field value.

    :param dbf_filename: DBF table filename.
    :param field_name: Field name.
    :param value: Value.
    :param field_type: Field type.
    :return: True/False.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'Set field value in DBF file. File <%s> not found' % dbf_filename)
        return False

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        db_cursor = dbf_connection.cursor()

        # String types are quoted
        if field_type in ('C', 'D'):
            value = '\'%s\'' % str(value)

        sql = 'UPDATE %s SET %s=%s' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                       field_name, value)
        db_cursor.execute(sql)
        dbf_connection.close()
        return True
    except:
        if dbf_connection:
            dbf_connection.close()
        log_func.fatal(u'Error set field value in DBF file <%s>' % dbf_filename)
    return False
