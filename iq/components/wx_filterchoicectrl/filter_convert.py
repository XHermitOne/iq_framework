#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for converting filter results to different views.
For example to SQL.
"""

import datetime
import sqlalchemy

from ...util import log_func

__version__ = (0, 0, 1, 2)

DEFAULT_SQL_DATE_FMT = '%Y-%m-%d'
DEFAULT_SQL_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'


def convertFilter2PgSQL(filter_data, table_name, fields=('*',), limit=None):
    """
    Convert filter to Postgres SQL view.

    :param filter_data: Filter data.
    :param table_name: Table name.
    :param fields: Field name list.
    :param limit: Record limit. If not defined, then there is no limit.
    :return: SELECT operator text in PgSQL dialect.
    """
    sql_fmt = '''SELECT %s
    FROM %s
    WHERE %s
    '''
    fields_sql = ', '.join(fields)
    converter = iqFilter2PostgreSQLConverter(filter_data)
    where = converter.convert()
    if not where:
        sql_fmt = 'SELECT %s FROM %s'
        sql = sql_fmt % (fields_sql, table_name)
    else:
        sql = sql_fmt % (fields_sql, table_name, where)
    if limit:
        sql += 'LIMIT %d' % limit
    return sql


def convertFilterWhereSection2PgSQLWhereSection(filter_data):
    """
    Convert WHERE section as filter to WHERE section in PostgreSQL dialect.

    :param filter_data: Filter data.
    :return: WHERE section text in PgSQL dialect.
    """
    converter = iqFilter2PostgreSQLConverter(filter_data)
    where = converter.convert()
    return where


class iqFilter2PostgreSQLConverter(object):
    """
    Filter to PostgreSQL converter class.
    """
    def __init__(self, filter_data, code_page='utf-8'):
        """
        Constructor.

        :param filter_data: Filter data.
        :param code_page: Code page.
        """
        self.filter = filter_data
        self.codepage = code_page
    
    def convert(self):
        """
        Run convert.

        :return: Returns a string representation of the WHERE clause of an SELECT operator.
        """
        if self.filter:
            sql_txt = self.genGroupSQL(self.filter)
            return sql_txt
        return ''
    
    def genGroupSQL(self, group_data):
        """
        Generation of the part of the SQL expression corresponding to the group of attribute elements.

        :param group_data: Group data.
        :return: Returns the row string of the WHERE SQL section corresponding to this group.
        """
        sql_fmt = '''( %s )'''
        
        sql_elements = []
        for element in group_data['children']:
            if element['type'] == 'group':
                sql_element = self.genGroupSQL(element)
            elif element['type'] == 'compare':
                sql_element = self.genRequisiteSQL(element)
            else:
                log_func.warning(u'Not defined filter item type <%s>' % element['type'])
                continue
            sql_elements.append(sql_element)
            
        sql_group = (' ' + group_data['logic'] + ' ').join(sql_elements)
        return (sql_fmt % sql_group) if sql_group.strip() else ''
    
    def genRequisiteSQL(self, requisite):
        """
        Generation of the part of the SQL expression corresponding to this attribute.

        :param requisite: Requisite data.
        :return: Returns the row string of the WHERE SQL section corresponding to this group.
        """
        if '__sql__' in requisite:
            return ' '.join(requisite['__sql__'])

        try:
            if 'get_args' in requisite and requisite['get_args']:
                ext_dict = requisite['get_args']()
                requisite.update(ext_dict)
        except:
            log_func.fatal(u'Error get arguments')

        try:
            if requisite['function'] == 'equal':
                # <Equal> verify
                return '%s = %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'not_equal':
                # <Not equal> verify
                return '%s <> %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'great':
                # <Great>
                return '%s > %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'great_or_equal':
                # <Great or equal>
                return '%s >= %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'lesser':
                # <Lesser>
                return '%s < %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'lesser_or_equal':
                # <Lesser or equal>
                return '%s <= %s' % (requisite['requisite'], self._getArgumentSQL(requisite['arg_1']))
            elif requisite['function'] == 'between':
                # <Between>
                return '%s BETWEEN %s AND %s' % (requisite['requisite'],
                                                 self._getArgumentSQL(requisite['arg_1']),
                                                 self._getArgumentSQL(requisite['arg_2']))
            elif requisite['function'] == 'not_between':
                # <Not between>
                return 'NOT (%s BETWEEN %s AND %s)' % (requisite['requisite'],
                                                       self._getArgumentSQL(requisite['arg_1']),
                                                       self._getArgumentSQL(requisite['arg_2']))
            elif requisite['function'] == 'contain':
                return '%s LIKE(\'%%%%%s%%%%\')' % (requisite['requisite'], requisite['arg_1'])
            elif requisite['function'] == 'not_contain':
                return '%s NOT LIKE(\'%%%%%s%%%%\')' % (requisite['requisite'], requisite['arg_1'])
            elif requisite['function'] == 'startswith':
                return '%s LIKE(\'%s%%%%\')' % (requisite['requisite'], requisite['arg_1'])
            elif requisite['function'] == 'endswith':
                return '%s LIKE(\'%%%%%s\')' % (requisite['requisite'], requisite['arg_1'])
            elif requisite['function'] == 'mask':
                log_func.warning(u'Unsupported compare <mask>')
                return None
            elif requisite['function'] == 'not_mask':
                log_func.warning(u'Unsupported compare <not mask>')
                return None
            elif requisite['function'] == 'is_null':
                return '%s IS NULL' % requisite['requisite']
            elif requisite['function'] == 'is_not_null':
                return '%s IS NOT NULL' % requisite['requisite']
            elif requisite['function'] == 'into':
                return '%s IN %s' % (requisite['requisite'], requisite['arg_1'])
            elif requisite['function'] == 'not_into':
                return '%s NOT IN %s' % (requisite['requisite'], requisite['arg_1'])

            log_func.warning(u'Not define function type <%s> filter requisite in convert' % requisite['function'])
        except:
            log_func.fatal(u'Error convert filter requisite <%s>' % requisite)

        return None

    def _getArgumentSQL(self, arg_value):
        """
        Get argument in SQL dialect.

        :param arg_value: Argument value.
        :return: Argument value as text in SQL dialect.
        """
        if arg_value is None:
            return 'NULL'
        elif isinstance(arg_value, str):
            return '\'%s\'' % arg_value
        elif isinstance(arg_value, datetime.date):
            return '\'%s\'' % arg_value.strftime(DEFAULT_SQL_DATE_FMT)
        elif isinstance(arg_value, datetime.datetime):
            return '\'%s\'' % arg_value.strftime(DEFAULT_SQL_DATETIME_FMT)
        return str(arg_value)


# --- Converter to SQLAlchemy ---
# Transfer logical operations
LOGIC_NAME2SQLALCHEMY_LOGIC = {'AND': sqlalchemy.and_,
                               'OR': sqlalchemy.or_,
                               'NOT': sqlalchemy.not_,
                               }


def convertFilter2SQLAlchemySelect(filter_data, table, fields=('*',), limit=None, order_by=None):
    """
    Convert filter data to SQLAlchemy view.

    :param filter_data: Filter data.
    :param table: Table.
    :param fields: Filed name list.
    :param limit: Record limit. If not defined, then there is no limit.
    :param order_by: Sorting.
    :return: sqlalchemy.sql.selectable.Select object.
    """
    converter = iqFilter2SQLAlchemySelectConverter(filter_data, table)
    where = converter.convert()
    columns = None
    if '*' not in fields:
        columns = [getattr(table.c, fld_name) for fld_name in fields]
    else:
        columns = [table]
    query = sqlalchemy.select(columns, where)

    if limit:
        query = query.limit(int(limit))

    if order_by:
        if isinstance(order_by, str):
            order_by = (order_by, )
        order_by_columns = [getattr(table.c, fld_name) for fld_name in order_by]
        query = query.order_by(*order_by_columns)
    return query


class iqFilter2SQLAlchemySelectConverter(object):
    """
    Filter data to SQLAlchemy converter class.
    """
    def __init__(self, filter_data, table, code_page='utf-8'):
        """
        Constructor.

        :param filter_data: Filter data.
        :param table: Table object.
        """
        self.filter = filter_data
        self.table = table
        self.codepage = code_page
        
    def convert(self):
        """
        Run convert.
        """
        if self.filter:
            query = self.genGroupSection(self.filter)
            return query
        else:
            log_func.warning(u'Filter not defined <%s>' % self.filter)
        return None
    
    def genGroupSection(self, group_data):
        """
        Generate group section.

        :param group_data: Group data.
        """
        sql_alchemy_elements = []
        for element in group_data.get('children', []):
            if element['type'] == 'group':
                sql_alchemy_element = self.genGroupSection(element)
            elif element['type'] == 'compare':
                sql_alchemy_element = self.genRequisiteSection(element)
            else:
                log_func.warning(u'Not defined filter item type <%s>' % element['type'])
                continue

            if sql_alchemy_element is not None:
                sql_alchemy_elements.append(sql_alchemy_element)
                
        sql_alchemy_elements = tuple(sql_alchemy_elements)
        return LOGIC_NAME2SQLALCHEMY_LOGIC.get(group_data['logic'].upper())(*sql_alchemy_elements)

    def genRequisiteSection(self, requisite):
        """
        Generate filter requisite section.

        :param requisite: Requisite data.
        """
        try:
            if 'get_args' in requisite and requisite['get_args']:
                ext_dict = requisite['get_args']()
                requisite.update(ext_dict)
        except:
            log_func.fatal(u'Error get arguments')

        try:
            if requisite['function'] == 'equal':
                # <Equal> verify
                return getattr(self.table.c, requisite['requisite']) == requisite['arg_1']
            elif requisite['function'] == 'not_equal':
                # <Not equal> verify
                return getattr(self.table.c, requisite['requisite']) != requisite['arg_1']
            elif requisite['function'] == 'great':
                # <Great>
                return getattr(self.table.c, requisite['requisite']) > requisite['arg_1']
            elif requisite['function'] == 'great_or_equal':
                # <Great or equal>
                return getattr(self.table.c, requisite['requisite']) >= requisite['arg_1']
            elif requisite['function'] == 'lesser':
                # <Lesser>
                return getattr(self.table.c, requisite['requisite']) < requisite['arg_1']
            elif requisite['function'] == 'lesser_or_equal':
                # <Lesser or equal>
                return getattr(self.table.c, requisite['requisite']) <= requisite['arg_1']
            elif requisite['function'] == 'between':
                # <Between>
                return getattr(self.table.c, requisite['requisite']).between(requisite['arg_1'],
                                                                                requisite['arg_2'])
            elif requisite['function'] == 'not_between':
                # <Not between>
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).between(requisite['arg_1'],
                                                                                                requisite['arg_2']))
            elif requisite['function'] == 'contain':
                return getattr(self.table.c, requisite['requisite']).contains(requisite['arg_1'])
            elif requisite['function'] == 'not_contain':
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).contains(requisite['arg_1']))
            elif requisite['function'] == 'startswith':
                return getattr(self.table.c, requisite['requisite']).startswith(requisite['arg_1'])
            elif requisite['function'] == 'endswith':
                return getattr(self.table.c, requisite['requisite']).endswith(requisite['arg_1'])
            elif requisite['function'] == 'mask':
                log_func.warning(u'Unsupported compare <mask>')
                return None
            elif requisite['function'] == 'not_mask':
                log_func.warning(u'Unsupported compare <not mask>')
                return None
            elif requisite['function'] == 'is_null':
                return getattr(self.table.c, requisite['requisite']) is None
            elif requisite['function'] == 'is_not_null':
                return getattr(self.table.c, requisite['requisite']) is not None
            elif requisite['function'] == 'into':
                return getattr(self.table.c, requisite['requisite']).in_(requisite['arg_1'])
            elif requisite['function'] == 'not_into':
                return sqlalchemy.not_(getattr(self.table.c, requisite['requisite']).in_(requisite['arg_1']))
        
            log_func.warning(u'Not define function type <%s> filter requisite in convert' % requisite['function'])
        except:
            log_func.fatal(u'Error convert filter requisite <%s>' % requisite)
            
        return None


def convertFilter2SQLAlchemyQuery(filter_data, model, query, fields=('*',), limit=None, order_by=None):
    """
    Convert filter data to SQLAlchemy model query.

    :param filter_data: Filter data.
    :param model: Model object.
    :param query: Model sqlalchemy.orm.query.Query object.
    :param fields: Filed name list.
    :param limit: Record limit. If not defined, then there is no limit.
    :param order_by: Sorting.
    :return: sqlalchemy.orm.query.Query object.
    """
    if '*' not in fields:
        columns = [getattr(model, fld_name) for fld_name in fields]
        query.add_columns(*columns)

    converter = iqFilter2SQLAlchemyQueryConverter(filter_data, model, query)
    where = converter.convert()

    # log_func.debug(u'Filter: %s' % str(where))
    query = query.filter(*where)
    if limit:
        query = query.limit(int(limit))
    if order_by:
        if isinstance(order_by, str):
            order_by = (order_by, )
        order_by_columns = [getattr(model, fld_name) for fld_name in order_by]
        query = query.order_by(*order_by_columns)
    return query


class iqFilter2SQLAlchemyQueryConverter(object):
    """
    Filter data to SQLAlchemy converter class.
    """
    def __init__(self, filter_data, model, query, code_page='utf-8'):
        """
        Constructor.

        :param filter_data: Filter data.
        :param model: Model object.
        :param query: Model sqlalchemy.orm.query.Query object.
        """
        self.filter = filter_data
        self.model = model
        self.query = query
        self.codepage = code_page

    def convert(self):
        """
        Run convert.
        """
        if self.filter:
            if isinstance(self.filter, dict):
                filter_list = [self.filter]
            elif isinstance(self.filter, (list, tuple)):
                filter_list = self.filter
            else:
                log_func.warning(u'Not valid filter data type <%s>' % self.filter.__class__.__name__)
            query = [self.genRequisiteSection(element) if element['type'] == 'compare' else self.genGroupSection(element) for element in filter_list]
            return query
        else:
            log_func.warning(u'Filter not defined <%s>' % self.filter)
        return None

    def genGroupSection(self, group_data):
        """
        Generate group section.

        :param group_data: Group data.
        """
        sql_alchemy_elements = list()
        children = group_data.get('children', list())
        # log_func.debug(u'Convert filter group logic %s' % group_data['logic'])
        for element in children:
            if element['type'] == 'group':
                sql_alchemy_element = self.genGroupSection(element)
            elif element['type'] == 'compare':
                sql_alchemy_element = self.genRequisiteSection(element)
                # log_func.debug(u'Convert filter compare %s' % sql_alchemy_element)
            else:
                log_func.warning(u'Not defined filter item type <%s>' % element['type'])
                continue

            if sql_alchemy_element is not None:
                sql_alchemy_elements.append(sql_alchemy_element)

        sql_alchemy_elements = tuple(sql_alchemy_elements)
        return LOGIC_NAME2SQLALCHEMY_LOGIC.get(group_data['logic'].upper())(*sql_alchemy_elements)

    def genRequisiteSection(self, requisite):
        """
        Generate filter requisite section.

        :param requisite: Requisite data.
        """
        try:
            if 'get_args' in requisite and requisite['get_args']:
                ext_dict = requisite['get_args']()
                requisite.update(ext_dict)
        except:
            log_func.fatal(u'Error get arguments')

        try:
            if requisite['function'] == 'equal':
                # <Equal> verify
                return getattr(self.model, requisite['requisite']) == requisite['arg_1']
            elif requisite['function'] == 'not_equal':
                # <Not equal> verify
                return getattr(self.model, requisite['requisite']) != requisite['arg_1']
            elif requisite['function'] == 'great':
                # <Great>
                return getattr(self.model, requisite['requisite']) > requisite['arg_1']
            elif requisite['function'] == 'great_or_equal':
                # <Great or equal>
                return getattr(self.model, requisite['requisite']) >= requisite['arg_1']
            elif requisite['function'] == 'lesser':
                # <Lesser>
                return getattr(self.model, requisite['requisite']) < requisite['arg_1']
            elif requisite['function'] == 'lesser_or_equal':
                # <Lesser or equal>
                return getattr(self.model, requisite['requisite']) <= requisite['arg_1']
            elif requisite['function'] == 'between':
                # <Between>
                return getattr(self.model, requisite['requisite']).between(requisite['arg_1'],
                                                                             requisite['arg_2'])
            elif requisite['function'] == 'not_between':
                # <Not between>
                return sqlalchemy.not_(getattr(self.model, requisite['requisite']).between(requisite['arg_1'],
                                                                                             requisite['arg_2']))
            elif requisite['function'] == 'contain':
                return getattr(self.model, requisite['requisite']).contains(requisite['arg_1'])
            elif requisite['function'] == 'not_contain':
                return sqlalchemy.not_(getattr(self.model, requisite['requisite']).contains(requisite['arg_1']))
            elif requisite['function'] == 'startswith':
                return getattr(self.model, requisite['requisite']).startswith(requisite['arg_1'])
            elif requisite['function'] == 'endswith':
                return getattr(self.model, requisite['requisite']).endswith(requisite['arg_1'])
            elif requisite['function'] == 'mask':
                log_func.warning(u'Unsupported compare <mask>')
                return None
            elif requisite['function'] == 'not_mask':
                log_func.warning(u'Unsupported compare <not mask>')
                return None
            elif requisite['function'] == 'is_null':
                return getattr(self.model, requisite['requisite']) is None
            elif requisite['function'] == 'is_not_null':
                return getattr(self.model, requisite['requisite']) is not None
            elif requisite['function'] == 'into':
                return getattr(self.model, requisite['requisite']).in_(requisite['arg_1'])
            elif requisite['function'] == 'not_into':
                return sqlalchemy.not_(getattr(self.model, requisite['requisite']).in_(requisite['arg_1']))

            log_func.warning(u'Not define function type <%s> filter requisite in convert' % requisite['function'])
        except:
            log_func.fatal(u'Error convert filter requisite <%s>' % requisite)

        return None
