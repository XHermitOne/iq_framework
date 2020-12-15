#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DBF file functions.
"""

import os
import os.path
import jaydebeapi

from iq.util import log_func

try:
    import dbfpy3.dbf
except ImportError:
    log_func.warning(u'Error import dbfpy3.dbf')

__version__ = (0, 0, 0, 1)

DBF_DB_URL_FMT = 'jdbc:dbf:///%s?charSet=%s'
JDBC_DBF_DRIVER = os.path.join(os.path.dirname(__file__), 'DBF_JDBC42.jar')

DEFAULT_DBF_ENCODING = 'cp1251'


def getDBFFieldNames(dbf_filename):
    """
    Get DBF field names.

    :param dbf_filename: DBF filename.
    :return: DBF field name list.
    """
    tab_dbf = None
    field_names = list()
    try:
        log_func.info(u'Open DBF file <%s>' % dbf_filename)
        tab_dbf = dbfpy3.dbf.Dbf(dbf_filename, new=False)
        field_names = tab_dbf.fieldNames
        tab_dbf.close()
    except:
        if tab_dbf:
            tab_dbf.close()
        log_func.fatal(u'Error get DBF field names in <%s>' % dbf_filename)
    return field_names


def existsColumns(dbf_filename, columns, auto_create=True):
    """
    Exists columns in DBF table?

    :param dbf_filename: DBF filename.
    :param columns: Column list:
        [(column name, column tyle, length, default value), ...]
    :param auto_create: Create automatic column if not exists?
    :return: True/False.
    """
    results = list()
    try:
        fields = getDBFFieldNames(dbf_filename)

        results = [column[0] in fields for column in columns]
        for column in columns:
            column_name = column[0]
            if column_name not in fields:
                if auto_create:
                    column_type = column[1]
                    column_len = column[2] if len(column) > 2 else 0
                    column_default = column[3] if len(column) > 3 else None

                    appendDBFNewField(dbf_filename, column_name, column_type, column_len, default=column_default)
    except:
        log_func.fatal(u'Error exists columns ini DBF table')
    return all(results)


def appendDBFNewField(dbf_filename,
                      new_fieldname, field_type, field_length, default=None):
    """
    Append new field inDBF table.

    :param dbf_filename: DBF filename.
    :param new_fieldname: New field name.
    :param field_type: Field type (C-string and etc).
    :param field_length: Field length.
    :param default: Default value.
    :return: DBF table object.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'DBF file <%s> not found' % dbf_filename)
        return None

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

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
            log_func.warning(u'Unsupported field type <%s>' % field_type)
        dbf_connection.close()
    except:
        if dbf_connection:
            dbf_connection.close()
        log_func.fatal(u'Error append new field DBF file <%s>' % dbf_filename)
    return None


def appendDBFNewFields(dbf_filename, *field_defs):
    """
    Append new fields in DBF file.

    :param dbf_filename: DBF filename.
    :param field_defs: Fields data:
        [(field name, field type, length, default value), ...].
    :return: DBF table object.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'DBF file <%s> not found' % dbf_filename)
        return None

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        for new_fieldname, field_type, field_length, default in field_defs:
            if field_type == 'C':
                db_cursor = dbf_connection.cursor()
                sql = 'ALTER TABLE %s ADD %s VARCHAR(%d)' % (os.path.splitext(os.path.basename(dbf_filename))[0],
                                                             new_fieldname, field_length)
                if default is not None:
                    sql += ' DEFAULT \'%s\'' % str(default)
                # log_func.debug(u'Execute SQL <%s>' % sql)
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
                log_func.warning(u'Unsupported field type <%s>' % field_type)
                continue
        dbf_connection.close()
    except:
        if dbf_connection:
            dbf_connection.close()
        log_func.fatal(u'Error append new fields in DBF file <%s>' % dbf_filename)


def setDBFFieldValue(dbf_filename, field_name, value, field_type='C'):
    """
    Set field value in DBF file.

    :param dbf_filename: DBF filename.
    :param field_name: DBF field name.
    :param value: Field value.
    :param field_type: Field type.
    :return: True/False.
    """
    dbf_filename = os.path.abspath(dbf_filename)
    if not os.path.exists(dbf_filename):
        log_func.warning(u'DBF file <%s> not found' % dbf_filename)
        return False

    dbf_connection = None
    try:
        dbf_url = DBF_DB_URL_FMT % (os.path.dirname(dbf_filename), DEFAULT_DBF_ENCODING)
        dbf_connection = jaydebeapi.connect('com.hxtt.sql.dbf.DBFDriver', [dbf_url], JDBC_DBF_DRIVER)

        db_cursor = dbf_connection.cursor()

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
