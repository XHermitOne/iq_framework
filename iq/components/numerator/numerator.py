#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Numerator manager module.
"""

import datetime
import re

import sqlalchemy
import sqlalchemy.orm.session
import sqlalchemy.orm.scoping
import sqlalchemy.sql.functions

from ...util import log_func

__version__ = (0, 0, 0, 1)

# Number-code default format
DEFAULT_NUM_CODE_FMT = 'N-%05N'

# Line number as subcode
N_RECORD_PATTERN = r'(\%.[0-9]N)'

# External subcode
EXT_STR_PATTERN = '%E'

# Requisite types
INTEGER_REQUISITE_TYPE = 'int'
FLOAT_REQUISITE_TYPE = 'float'
TEXT_REQUISITE_TYPE = 'text'
DT_REQUISITE_TYPE = 'datetime'

# Numerator table default
DEFAULT_NUMERATOR_TABLE = 'numerator_tab'

# Numerator table fields
NUMBER_CODE_FIELD = 'number_code'   # Number-code field name
DT_NUMBER_FIELD = 'dt_num'          # Datetime generate number-code field name
CUR_COUNT_FIELD = 'cur_count'       # Counter field name


class iqNumeratorProto(object):
    """
    Numerator manager class.
    """
    def __init__(self, db_url=None,
                 numerator_table_name=DEFAULT_NUMERATOR_TABLE,
                 num_code_format=DEFAULT_NUM_CODE_FMT,
                 check_unique=False):
        """
        Constructor.

        :param db_url: DB URL / Conncetion string.
        :param numerator_table_name: Numerator table name.
        :param num_code_format: Numerator number-code format.
        :param check_unique: Check unique code?
        """
        self._db_url = db_url
        self._connection = None

        self._numerator_table_name = numerator_table_name
        self._numerator_table = None

        self._num_code_format = num_code_format

        self._check_unique = check_unique

        # Current number-code
        self._num_code = None

    def setCheckUnique(self, check_unique=True):
        """
        Set automatic verification of the uniqueness of the code number.
        """
        self._check_unique = check_unique

    def getCheckUnique(self):
        """
        Automatic verification of the uniqueness of the code number.
        """
        return self._check_unique

    def isConnected(self):
        """
        Is a connection with the database established?

        :return: True/False
        """
        return self._connection is not None

    def connect(self, db_url=None):
        """
        Establish a connection with the database.

        :param db_url: DB URL / Connection string.
        :return: Database engine object.
        """
        if db_url is None:
            db_url = self._db_url

        if self._connection:
            self.disconnect()

        self._connection = sqlalchemy.create_engine(db_url, echo=False)
        log_func.info(u'Connect to database <%s>' % db_url)
        return self._connection

    def disconnect(self):
        """
        Break the connection with the database.

        :return: True/False.
        """
        if self._connection:
            self._connection.dispose()
            self._connection = None
        return True

    def getConnection(self, auto_connect=True):
        """
        Get database engine object.

        :param auto_connect: Connect automatically?
        """
        if self._connection is None and auto_connect:
            self.connect()
        return self._connection

    def getTable(self):
        """
        Get numerator table.
        """
        if not self.isConnected():
            self.connect()

        if self._numerator_table is None:
            self.createTable()
        return self._numerator_table

    def genColumn(self, requisite_name, requisite_type):
        """
        Generate column object by requisite.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
        :return: Sqlalchemy column object or None if error.
        """
        # Make all names lowercase
        requisite_name = requisite_name.strip().lower()
        requisite_type = requisite_type.strip().lower()
        column_type = sqlalchemy.UnicodeText
        if requisite_type == INTEGER_REQUISITE_TYPE:
            column_type = sqlalchemy.Integer
        elif requisite_type == FLOAT_REQUISITE_TYPE:
            column_type = sqlalchemy.Float
        elif requisite_type == TEXT_REQUISITE_TYPE:
            column_type = sqlalchemy.UnicodeText
        elif requisite_type == DT_REQUISITE_TYPE:
            column_type = sqlalchemy.DateTime

        column = sqlalchemy.Column(requisite_name, column_type)
        return column

    def genTable(self, table_name, requisites):
        """
        Generate table object by requisites.

        :param table_name: Table name.
        :param requisites: Requisites data.
        :return: Sqlalchemy table object or None if error.
        """
        metadata = sqlalchemy.MetaData(self._connection)
        columns = [self.genColumn(**requisite) for requisite in requisites]
        table = sqlalchemy.Table(table_name, metadata, *columns)
        return table

    def _getRequisites(self):
        """
        Numerator table requisite list.

        :return: Requisite data list:
            [{'requisite_name': <Field name>,
            'requisite_type': <Field type>}, ...]
        """
        num_code_requisite = dict(requisite_name=NUMBER_CODE_FIELD,
                                  requisite_type=TEXT_REQUISITE_TYPE)

        dt_num_requisite = dict(requisite_name=DT_NUMBER_FIELD,
                                requisite_type=DT_REQUISITE_TYPE)

        cur_count_requisite = dict(requisite_name=CUR_COUNT_FIELD,
                                   requisite_type=INTEGER_REQUISITE_TYPE)
        requisites = [num_code_requisite,
                      dt_num_requisite,
                      cur_count_requisite]
        return requisites

    def createTable(self, numerator_table_name=None):
        """
        Create numerator table.

        The numbering table consists of the fields:
             1. Issued by the numbering number-code (number_code)
             2. Date-time of issue of the number (dt_num)
             3. Counter of issue of number (cur_count)

        :param numerator_table_name: Numerator table name.
        :return: Numerator table object or None if error.
        """
        if numerator_table_name is None:
            numerator_table_name = self._numerator_table_name

        requisites = self._getRequisites()
        self._numerator_table = self.genTable(numerator_table_name, requisites)
        self._numerator_table.create(checkfirst=True)
        return self._numerator_table

    def _genNewNumCode(self, fmt=None, n_count=0, *args):
        """
        Generate new number-code.

        :param fmt: Number-code format.
        :param n_count: Additional identifier of the generated row of
            the numbering table.
        :param args: Additional code options.
        :return: Generated number-code.
        """
        if fmt is None:
            fmt = self._num_code_format

        # Replace datetime params in format
        now = datetime.datetime.now()
        # need replace <%> on <%%>
        fmt = now.strftime(fmt.replace('%', '%%'))

        fmt_args = list()

        # Replace counter value
        replaces = [(element, element.replace('N', 'd')) for element in re.findall(N_RECORD_PATTERN, fmt)]
        if replaces:
            for src, dst in replaces:
                fmt = fmt.replace(src, dst)
                fmt_args.append(n_count)

        # Replace string params
        if EXT_STR_PATTERN in fmt:
            fmt = fmt.replace(EXT_STR_PATTERN, '%s')
            fmt_args += [str(arg) for arg in args]

        if fmt_args:
            # External params
            log_func.debug(u'Generate number-code by format <%s>. External params: %s' % (fmt, fmt_args))
            fmt = fmt % tuple(fmt_args)

        # Number code is generated
        return fmt

    def getActualYear(self):
        """
        Get actual year for define maximal counter.

        :return: Actual year.
        """
        return datetime.date.today().year

    def getMaxDT(self, session=None, numerator_table=None):
        """
        Determine the maximum value of the numbering counter.
        The maximum value of the counter must be produced
        taking into account the current program year.

        :param session: SQLAlchemy session.
        :param numerator_table: Numerator table.
        :return: Maximum numerator counter value.
        """
        if numerator_table is None:
            numerator_table = self.createTable()
        if session is None:
            session = sqlalchemy.orm.session.sessionmaker(bind=self._connection)

        session_query = sqlalchemy.orm.scoping.scoped_session(session)
        max_dt = session_query.query(sqlalchemy.sql.functions.max(numerator_table.c.dt_num).label('max_dt')).one()[0]
        return max_dt

    def getMaxCount(self, session=None, numerator_table=None, cur_year=None):
        """
        Determine the maximum value of the numbering counter.
        The maximum value of the counter must be produced
        taking into account the current program year.

        :param session: SQLAlchemy session.
        :param numerator_table: Numerator table.
        :param cur_year: Current year.
            If not defined then get actual year.
        :return: Maximum numerator counter value.
        """
        if numerator_table is None:
            numerator_table = self.createTable()
        if session is None:
            session = sqlalchemy.orm.session.sessionmaker(bind=self._connection)
        if cur_year is None:
            cur_year = self.getActualYear()

        min_date = datetime.date(cur_year, 1, 1)
        max_date = datetime.date(cur_year, 12, 31)

        session_query = sqlalchemy.orm.scoping.scoped_session(session)
        max_count = session_query.query(sqlalchemy.sql.functions.max(numerator_table.c.cur_count).label('max_count')).filter(sqlalchemy.between(numerator_table.c.dt_num, min_date, max_date)).one()[0]
        return max_count

    def doGenNumCode(self, check_unique=None, *args):
        """
        Generate new number-code.
        In addition to generating a code number,
        it is registered (recorded) in the numbering table
        and the time of issuing the code number is indicated.

        :param check_unique: Check unique code?
        :param args: External parameters.
        :return: Generated number-code or None if error.
        """
        if check_unique is None:
            check_unique = self.getCheckUnique()

        numerator_table = self.createTable()

        # Start transaction
        session = sqlalchemy.orm.session.sessionmaker(bind=self._connection)
        transaction = session()

        self._num_code = None
        try:
            # Get maximum counter value
            max_count = self.getMaxCount(session, numerator_table)
            max_count = max_count + 1 if max_count else 1
            log_func.debug(u'New max_value count <%s>' % max_count)

            now = datetime.datetime.now()
            now = now.replace(year=self.getActualYear())

            sql = numerator_table.insert().values(number_code=None,
                                                  dt_num=now,
                                                  cur_count=max_count)
            transaction.execute(sql)

            new_num_code = self._genNewNumCode(n_count=max_count, *args)
            if check_unique:
                # Check unique
                find = numerator_table.select(numerator_table.c.number_code == new_num_code).execute()
                if find.rowcount:
                    log_func.warning(u'Number-code <%s> exists in numerator' % new_num_code)
                    transaction.rollback()
                    return None

            sql = numerator_table.update().where(sqlalchemy.and_(numerator_table.c.dt_num == now,
                                                                 numerator_table.c.cur_count == max_count)).values(number_code=new_num_code)
            transaction.execute(sql)

            transaction.commit()

            self._num_code = new_num_code
            return self._num_code
        except:
            transaction.rollback()
            log_func.fatal(u'Error generate new number-code in numerator')
        return None

    def undoGenNumCode(self):
        """
        Cancel generation of last code number.
        The record with the number code is deleted from the numbering table.

        :return: True/False.
        """
        numerator_table = self.createTable()

        session = sqlalchemy.orm.session.sessionmaker(bind=self._connection)
        transaction = session()

        try:
            if self._num_code is not None:
                sql = numerator_table.delete().where(numerator_table.c.number_code == self._num_code)
                transaction.execute(sql)
            else:
                log_func.warning(u'Number-code not defined for undo')
                return False

            transaction.commit()

            self._num_code = None
            return True
        except:
            transaction.rollback()
            log_func.fatal(u'Error undo generate number-code in numerator')
        return False

    def delNotActual(self, dt_actual=None):
        """
        Delete not actual number-codes.

        :param dt_actual: Datetime from which data are considered relevant.
            If None then get today.
        :return: True/False.
        """
        if dt_actual is None:
            dt_actual = datetime.date.today()
        if isinstance(dt_actual, datetime.date):
            # For compare date and datetime
            dt_actual = datetime.datetime.combine(dt_actual,
                                                  datetime.datetime.min.time())
        if not isinstance(dt_actual, datetime.datetime):
            log_func.warning(u'Not valid actual datetime type <%s>' % dt_actual.__class__.__name__)
            return False

        numerator_tab = self.getTable()
        if numerator_tab is not None:
            try:
                sql = numerator_tab.delete().where(sqlalchemy.and_(numerator_tab.c.dt_num < dt_actual))
                sql.execute()
            except:
                log_func.fatal(u'Error delete not actual numerator data')
            return True
        return False

    def clear(self):
        """
        Clear numerator.

        :return: True/False.
        """
        return self.delNotActual()

    def doGen(self, *args, **kwargs):
        """
        Generate new number-code.

        :return: Generated number-code or None if error.
        """
        self.connect()
        num_code = self.doGenNumCode(*args, **kwargs)
        self.onDo(NEW_NUM=num_code)
        self.disconnect()
        return num_code

    def onDo(self, **kwargs):
        """
        It is executed when a new number is generated.

        :return: True/False.
        """
        return True

    def undoGen(self):
        """
        Undo generate number-code.

        :return: True/False.
        """
        self.connect()
        num = self.getMaxCount()
        result = self.undoGenNumCode()
        self.onUndo(NUM=num)
        self.disconnect()
        return result

    def onUndo(self, **kwargs):
        """
        It is executed when a new number is generated.

        :return: True/False.
        """
        return True

    # Other name of the method
    gen = doGen
    do = doGen
    undo = undoGen
