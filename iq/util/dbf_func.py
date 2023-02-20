#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции манипулирования DBF таблицами.
"""

import os
import os.path

from . import log_func

try:
    import jaydebeapi
except ImportError:
    log_func.error(u'Import error jaydebeapi. Install <pip3 install jaydebeapi jpype1>')

try:
    import dbfpy3.dbf
except ImportError:
    log_func.error(u'Import error dbfpy3. Install <pip3 install dbfpy3>')

try:
    import dbfread
except ImportError:
    log_func.error(u'Import error dbfread. Install <pip3 install dbfread>')

__version__ = (0, 0, 1, 1)

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


def openDBF(tab_filename, *args, **kwargs):
    """
    Open DBF table.

    :param tab_filename: DBF table filename.
    :param read_only: if 'f' argument is a string file will
           be opend in read-only mode; in other cases
           this argument is ignored. This argument is ignored
           even if 'new' argument is True.
    :param new: True if new data table must be created. Assume
           data table exists if this argument is False.
    :param ignore_errors: if set, failing field value conversion will return
           'INVALID_VALUE' instead of raising conversion error.
    :return: DBF table object.
    """
    tab_dbf = None
    try:
        log_func.info(u'Open dbf table <%s>' % tab_filename)
        tab_dbf = dbfpy3.dbf.Dbf(tab_filename, *args, **kwargs)
    except:
        if tab_dbf:
            tab_dbf.close()
            tab_dbf = None
        log_func.fatal(u'Error open DBF file <%s>' % tab_filename)
    return tab_dbf


def closeDBF(dbf_table):
    """
    Close DBF table.

    :param dbf_table: DBF table object.
    :return: True/False.
    """
    if isinstance(dbf_table, dbfpy3.dbf.Dbf):
        try:
            dbf_table.close()
            return True
        except:
            log_func.fatal(u'Error close DBF file <%s>' % dbf_table.name)
    else:
        log_func.warning(u'Not supported DBF table type <%s>' % dbf_table.__class__.__name__)
    return False


def openDBFReadonly(tab_filename, *args, **kwargs):
    """
    Open DBF table in readonly mode.

    :param tab_filename: DBF table filename.
    :param load: By default records will streamed directly from disk.
        If you pass load=True they will instead be loaded into lists
        and made available as the records and deleted attributes.
        You can load and unload records at any time with the load() and unload() methods.
    :param encoding: Specify character encoding to use.
        By default dbfread will try to guess character encoding from
        the language_driver byte. If this fails it falls back on ASCII.

    :param char_decode_errors: The error handling scheme to use for the
        handling of decoding errors. This is passed as the errors option
        to the bytes.decode() method. From the documentation of that method:
        The default is 'strict' meaning that decoding errors
        raise a UnicodeDecodeError.
        Other possible values are 'ignore' and 'replace' as well as any
        other name registered with codecs.register_error that
        can handle UnicodeDecodeErrors.

    :param lowernames: Field names are typically uppercase.
        If you pass True all field names will be converted to lowercase.

    :param recfactory: Takes a function that will be used to produce new records.
        The function will be called with a list of (name, value) pairs.
        If you pass recfactory=None you will get the original (name, value) list.

    :param ignorecase:  Windows uses a case preserving file system which means
        people.dbf and PEOPLE.DBF are the same file.
        This causes problems in for example Linux where case is significant.
        To get around this dbfread ignores case in file names.
        You can turn this off by passing ignorecase=False.

    :param parserclass: The parser to use when parsing field values.
        You can use this to add new field types or do custom parsing
        by subclassing dbfread.FieldParser. (See Field Types.)

    :param ignore_missing_memofile: If you don’t have the memo field you can pass
        ignore_missing_memofile=True. All memo fields will then be returned as None,
        so you at least get the rest of the data.

    :param raw: Returns all data values as byte strings. This can be used for
        debugging or for doing your own decoding.

    :return: DBF table object.
    """
    tab_dbf = None
    try:
        log_func.info(u'Open READONLY dbf table <%s>' % tab_filename)
        tab_dbf = dbfread.DBF(tab_filename, *args, **kwargs)
    except:
        if tab_dbf:
            # tab_dbf.close()
            tab_dbf = None
        log_func.fatal(u'Error open READONLY DBF file <%s>' % tab_filename)
    return tab_dbf
