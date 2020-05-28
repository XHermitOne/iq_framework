#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Accumulate registry manager.

The procedure for working with the accumulation register:
1. Create accumulate registry object
2. Create DB connection (call connect())
3. Call receipt/expense/doOperations
4. Disconnect with DB (call disconnect())
"""

import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ...util import log_func

from ..data_uniobj_model.spc import GUID_FIELD_NAME

from ..data_model import data_object

__version__ = (0, 0, 0, 1)


# Default operation table name
DEFAULT_OPERATIONS_TABLE = 'operations'
# Default summary table name
DEFAULT_RESULT_TABLE = 'result'

SQL_ROLLBACK = 'ROLLBACK'

# Requisite types
INTEGER_REQUISITE_TYPE = 'int'
FLOAT_REQUISITE_TYPE = 'float'
TEXT_REQUISITE_TYPE = 'text'
DT_REQUISITE_TYPE = 'datetime'

# Operation codes
RECEIPT_OPERATION_CODE = '+'
EXPENSE_OPERATION_CODE = '-'

# Operation table field names
CODE_OPERATION_FIELD = 'operation_code'
DT_OPERATION_FIELD = 'dt_operation'
OWNER_OPERATION_FIELD = 'owner'


class iqAccRegistry(data_object.iqDataObject):
    """
    Accumulate registry manager class.

      Event 1-----+
      Event 2---+ |
      Event 3-+ | |
              | | |
    +---------| | |-------------------------+
    |         V V V    Accumulate registry  |
    | +=============+                       |
    | | Operations  |                       |
    | +=============+                       |
    |       |                               |
    |       V                               |
    | +=================+                   |
    | | Summary results |                   |
    | +=================+                   |
    +---------------------------------------+

    The composition of the accumulation register as an object includes measurements and resources.
    Resources are used to store information about both increments and
    and the values of the indicators themselves. In fact, every resource stores data
    one indicator. However, registers can be not only one-dimensional.
    In the accumulation registers, accounting cuts are implemented using
    measurements.

    The register can include more than one dimension.
    The table of motion operations contains additional fields:
    1. Operation code - <+> (RECEIPT) or <-> (EXPENSE)
    2. Operation datetime (filled automatically)
    3. Operation owner (document number or object GUID).
    """
    def __init__(self, db_url=None,
                 operation_table_name=DEFAULT_OPERATIONS_TABLE,
                 result_table_name=DEFAULT_RESULT_TABLE):
        """
        Constructor.

        :param db_url: DB connection string.
        :param operation_table_name: Operation table name.
        :param result_table_name: Summary table name.
        """
        self._db_url = db_url
        self._connection = None

        self._operation_table_name = operation_table_name
        self._operation_table = None
        self._result_table_name = result_table_name
        self._result_table = None

        # Resource requisites
        self._resource_requisites = list()
        # Dimension requisites
        self._dimension_requisites = list()

        # Extended requisites
        self._extended_requisites = list()

    def getOperationTable(self):
        """
        Operation table sqlalchemy object.
        """
        if not self.isConnected():
            self.connect()

        if self._operation_table is None:
            self.createOperationTable()
        return self._operation_table

    def getResultTable(self):
        """
        Summary table sqlalchemy object.
        """
        if not self.isConnected():
            self.connect()

        if self._result_table is None:
            self.createResultTable()
        return self._result_table

    def getDataset(self):
        """
        Get result table dataset.

        :return: Result table record dictionary list
            or empty list if error.
        """
        try:
            result_table = self.getResultTable()
            dataset = result_table.select().execute()
            dataset = [dict(record) for record in dataset]
            dataset = self._updateLinkDataDataset(dataset)
            return dataset
        except:
            log_func.fatal(u'Error get result table dataset')
        return list()

    def isConnected(self):
        """
        Is a connection with the database established?

        :return: True/False
        """
        return self._connection is not None

    def connect(self, db_url=None):
        """
        Establish a connection with the database.

        :param db_url: DB URL. Connection string.
        :return: Db object.
        """
        if db_url is None:
            db_url = self._db_url

        if self._connection:
            self.disconnect()

        self._connection = sqlalchemy.create_engine(db_url, echo=False)
        log_func.info(u'Connect to DB <%s>' % db_url)
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
        Get DB connection object.

        :param auto_connect: If no connection is established,
             make an automatic connection?
        """
        if self._connection is None and auto_connect:
            self.connect()
        return self._connection

    def executeSQL(self, connection=None, sql='', *args):
        """
        Execute SQL expression.

        :param connection: DB connection object.
        :param sql: SQL expression.
        :param args: SQL expression parameters.
        :return: Result recordset.
        """
        if connection is None:
            connection = self._connection

        result = None
        try:
            sql_txt = sql % args
        except TypeError:
            log_func.fatal(u'Error SQL expression')
            raise

        try:
            result = connection.execute(sql_txt)
        except:
            connection.execute(SQL_ROLLBACK)
            log_func.fatal(u'Error execute SQL expression: %s' % sql_txt)
            raise
        return result

    def addResourceRequisite(self, requisite_name, requisite_type):
        """
        Append resource requisite.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
            Resource requisite type can as integer ('int') or floating ('float').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._resource_requisites.append(requisite)

    def getResourceRequisiteNames(self):
        """
        Get resource requisite name list.

        :return: Resource requisite name list.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._resource_requisites]
        return names

    def addDimensionRequisite(self, requisite_name, requisite_type):
        """
        Add dimension requisite.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
            Dimension requisite type can as Integer ('int')/Date time ('datetime')/Text ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._dimension_requisites.append(requisite)

    def getDimensionRequisiteNames(self):
        """
        Get dimension requisite name list.

        :return: Dimension requisite name list.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._dimension_requisites]
        return names

    def addExtendedRequisite(self, requisite_name, requisite_type):
        """
        Add extended requisite.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
            Extended requisite type can as Integer ('int')/Floating ('float')/Date time ('datetime')/Text ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._extended_requisites.append(requisite)

    def getExtendedRequisiteNames(self):
        """
        Get extended requisite name list.

        :return: Extended requisite name list.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._extended_requisites]
        return names

    def genColumn(self, requisite_name, requisite_type):
        """
        Generate column object by requisite data.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
        :return: Column sqlalchemy object or None if error.
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
        Generate table object by requisite data.

        :param table_name: Table name.
        :param requisites: Requisite data list.
        :return: Table sqlalchemy object or None if error.
        """
        metadata = sqlalchemy.MetaData(self._connection)
        # log_func.debug(u'genTable <%s>' % requisites)
        columns = [self.genColumn(**requisite) for requisite in requisites]
        table = sqlalchemy.Table(table_name, metadata, *columns)
        return table

    def _getOperationRequisites(self):
        """
        Get operation requisite data.

        :return: Operation requisite data:
            [{'requisite_name': <Field name>,
            'requisite_type': <Field type>}, ...]
        """
        code_requisite = dict(requisite_name=CODE_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)

        dt_requisite = dict(requisite_name=DT_OPERATION_FIELD,
                            requisite_type=DT_REQUISITE_TYPE)
        owner_requisite = dict(requisite_name=OWNER_OPERATION_FIELD,
                               requisite_type=TEXT_REQUISITE_TYPE)
        requisites = [code_requisite, dt_requisite,
                      owner_requisite] + self._dimension_requisites + self._resource_requisites
        return requisites

    def createOperationTable(self, operation_table_name=None):
        """
        Create operation table.

        :param operation_table_name: Operation table name.
        :return: Operation table object or None if error.
        """
        if operation_table_name is None:
            operation_table_name = self._operation_table_name

        requisites = self._getOperationRequisites()
        self._operation_table = self.genTable(operation_table_name, requisites)
        self._operation_table.create(checkfirst=True)
        return self._operation_table

    def _getResultRequisites(self):
        """
        Get requisites of summary table.

        :return: Requisite data:
            [{'requisite_name': <Field name>,
            'requisite_type': <Field type>}, ...]
        """
        requisites = self._dimension_requisites + self._resource_requisites + self._extended_requisites
        return requisites

    def createResultTable(self, result_table_name=None):
        """
        Create summary table.

        :param result_table_name: Result table name.
        :return: Result table object or None if error.
        """
        if result_table_name is None:
            result_table_name = self._result_table_name

        requisites = self._getResultRequisites()
        self._result_table = self.genTable(result_table_name, requisites)
        self._result_table.create(checkfirst=True)
        return self._result_table

    def isReceipt(self, **requisite_values):
        """
        Determine by operation details which operation
        carried out. It is receipt?

        :param requisite_values: Requisite values.
        :return: True/False.
        """
        code = requisite_values.get(CODE_OPERATION_FIELD, None)
        return code == RECEIPT_OPERATION_CODE

    def isExpense(self, **requisite_values):
        """
        Determine by operation details which operation
        carried out. It is expense?

        :param requisite_values: Requisite values.
        :return: True/False.
        """
        code = requisite_values.get(CODE_OPERATION_FIELD, None)
        return code == EXPENSE_OPERATION_CODE

    def _isGUIDField(self, table):
        """
        Check if the table has a GUID field.
        This is done because the final table may be table
        business facility. And when adding a new business object
        in this case, you must initialize it unique
        identifier.

        :param table: Table sqlalchemy object.
        :return: True/False.
        """
        mapper = sqlalchemy.inspect(table)
        column_names = mapper.columns.keys()
        return GUID_FIELD_NAME in column_names

    def _doOperation(self, transaction,
                     operation_table, result_table,
                     requisite_values):
        """
        Execute operation

        :param transaction: Transaction object (sqlalchemy).
        :param operation_table: Operation table object (sqlalchemy).
        :param result_table: Result table object (sqlalchemy).
        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Extended requisites (only needed for the summary table)
        extended_requisite_names = self.getExtendedRequisiteNames()
        extended_requisites = dict([(name, requisite_values[name]) for name in extended_requisite_names if name in requisite_values])

        # Check if there is a record in the summary table according to measurements
        dimension_requisite_names = self.getDimensionRequisiteNames()
        dimension_requisites = dict([(name, value) for name, value in requisite_values.items() if name in dimension_requisite_names])
        where = [getattr(result_table.c, name) == value for name, value in dimension_requisites.items()]
        find = result_table.select(sqlalchemy.and_(*where)).execute()
        if not find.rowcount:
            # If there is no such record, then create it
            resource_requisite_names = self.getResourceRequisiteNames()
            resource_requisites = dict([(name, 0) for name in resource_requisite_names])
            requisites = dict()
            requisites.update(dimension_requisites)
            requisites.update(resource_requisites)
            requisites.update(extended_requisites)

            sql = result_table.insert().values(**requisites)
            transaction.execute(sql)

        # Update values of resource details
        resource_requisite_names = self.getResourceRequisiteNames()
        if self.isReceipt(**requisite_values):
            # If the operation of receipt, then add
            resource_requisites = dict([(name, getattr(result_table.c, name)+requisite_values.get(name, 0)) for name in resource_requisite_names])
        elif self.isExpense(**requisite_values):
            # If the operation of expense, then subtract
            resource_requisites = dict([(name, getattr(result_table.c, name)-requisite_values.get(name, 0)) for name in resource_requisite_names])
        else:
            log_func.error(u'Unsupported operation <%s>' % requisite_values.get(CODE_OPERATION_FIELD, None))
            transaction.rollback()
            return False

        requisites = dict()
        requisites.update(resource_requisites)
        requisites.update(extended_requisites)
        sql = result_table.update().where(sqlalchemy.and_(*where)).values(**requisites)
        transaction.execute(sql)

        operation_requisite_values = self._getOperationRequisiteValues(**requisite_values)
        # After changing the values in the final table, add the operation to the motion table
        # Do not forget to add the date-time field of the motion operation
        operation_requisite_values[DT_OPERATION_FIELD] = datetime.datetime.now()
        sql = operation_table.insert().values(**operation_requisite_values)
        transaction.execute(sql)
        return True

    def _getOperationRequisiteValues(self, **requisite_values):
        """
        Get only required details of details for the operation table.

        :param requisite_values: Requisite values.
        :return: List of details used in the registry.
        """
        used_requisite_names = [CODE_OPERATION_FIELD,
                                DT_OPERATION_FIELD,
                                OWNER_OPERATION_FIELD] + \
                               [requisite['requisite_name'] for requisite in self._dimension_requisites] + \
                               [requisite['requisite_name'] for requisite in self._resource_requisites]
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def _getResultRequisiteValues(self, **requisite_values):
        """
        Get only required details of details for the totals table.

        :param requisite_values: Requisite values.
        :return: List of details used in the registry.
        """
        used_requisite_names = [requisite['requisite_name'] for requisite in self._dimension_requisites] + \
                               [requisite['requisite_name'] for requisite in self._resource_requisites] + \
                               [requisite['requisite_name'] for requisite in self._extended_requisites]
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def doOperation(self, **requisite_values):
        """
        Execute operation.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Create tables
        operation_table = self.createOperationTable()
        result_table = self.createResultTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = self._doOperation(transaction,
                                       operation_table, result_table,
                                       requisite_values)
            if result:
                # Commit transaction
                transaction.commit()
            return result
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error execute operation <%s>' % requisite_values)
        return False

    def undoOperation(self, **requisite_values):
        """
        Undo operation.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Create table
        operation_table = self.createOperationTable()
        result_table = self.createResultTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            # Find the operation corresponding to the specified details
            where = [getattr(operation_table.c, name) == value for name, value in requisite_values.items()]
            # Need use ORDER_BY DESC by field dt_operation
            # to cancel operations in the exact reverse chronological order
            find = operation_table.select().where(sqlalchemy.and_(*where)).order_by(operation_table.c.dt_oper.desc()).execute()
            if find.rowcount:
                # There is operation
                for operation in find:
                    operation_code = operation[CODE_OPERATION_FIELD]
                    if operation_code == RECEIPT_OPERATION_CODE:
                        # It is receipt, then need to be subtracted from the summary table
                        resource_requisite_names = self.getResourceRequisiteNames()
                        resource_requisites = dict([(name, getattr(result_table.c, name)-operation[name]) for name in resource_requisite_names])
                        # Dictionary of details for adding a position
                        init_resource_requisites = dict([(name, -operation[name]) for name in resource_requisite_names])
                    elif operation_code == EXPENSE_OPERATION_CODE:
                        # It is expense, then you need to add in the result table
                        resource_requisite_names = self.getResourceRequisiteNames()
                        resource_requisites = dict([(name, getattr(result_table.c, name)+operation[name]) for name in resource_requisite_names])
                        # Dictionary of details for adding a position
                        init_resource_requisites = dict([(name, operation[name]) for name in resource_requisite_names])
                    else:
                        log_func.error(u'Unsupported operation <%s>' % operation_code)
                        transaction.rollback()
                        return False

                    # Make an update in the summary table
                    dimension_requisite_names = self.getDimensionRequisiteNames()
                    operation_values = dict(operation)
                    dimension_requisites = dict([(name, value) for name, value in operation_values.items() if name in dimension_requisite_names])
                    where = [getattr(result_table.c, name) == value for name, value in dimension_requisites.items()]
                    # If the search condition is not defined in the summary table,
                    # then there is no way to make an update in the summary table
                    if where:
                        # There is a search term in the summary table
                        log_func.debug(u'Undo operation <%s>' % dimension_requisites)
                        # If there is such a position, then do update
                        # if there is no such position then do insert
                        # because value from the summary table deleted
                        # When checking for the existence of a record, it is used first()
                        # If the returned recordset is empty, then the function returns None.
                        # Need execute <execute()>. Get ResultProxy and call first()
                        if result_table.select().where(sqlalchemy.and_(*where)).execute().first() is not None:
                            sql = result_table.update().where(sqlalchemy.and_(*where)).values(**resource_requisites)
                            transaction.execute(sql)
                        else:
                            try:
                                requisites = dict()
                                requisites.update(init_resource_requisites)
                                requisites.update(dimension_requisites)
                                extended_requisite_names = self.getExtendedRequisiteNames()
                                extended_requisites = dict(
                                    [(name, value) for name, value in operation_values.items() if
                                     name in extended_requisite_names])
                                requisites.update(extended_requisites)
                                log_func.debug(u'Undo operation. Add position in result table %s' % requisites)
                                sql = result_table.insert().values(**requisites)
                                transaction.execute(sql)
                            except:
                                log_func.fatal(u'Error add undo position')
                                sql = None
                    else:
                        log_func.error(u'Error records identification in result table for update [%s]' % dimension_requisites)

                operation_requisite_values = self._getOperationRequisiteValues(**requisite_values)

                # Delete operation
                where = [getattr(operation_table.c, name) == value for name, value in operation_requisite_values.items()]
                sql = operation_table.delete().where(sqlalchemy.and_(*where))
                transaction.execute(sql)
            else:
                log_func.error(u'OPeration not found <%s> for undo' % requisite_values)
                transaction.rollback()
                return False

            # Commit transaction
            transaction.commit()
            return True
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error undo operation <%s>' % requisite_values)
        return False

    def doOperations(self, requisite_values_list):
        """
        Execute group operations.

        :param requisite_values_list: Requisite values list.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Create tables
        operation_table = self.createOperationTable()
        result_table = self.createResultTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = True
            for requisite_values in requisite_values_list:
                result = result and self._doOperation(transaction,
                                                      operation_table, result_table,
                                                      requisite_values)

            if result:
                # Commit transaction
                transaction.commit()
            return result
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error execute group operations <%s>' % requisite_values_list)
        return False

    def receipt(self, **requisite_values):
        """
        Execute receipt.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        requisite_values[CODE_OPERATION_FIELD] = '+'
        return self.doOperation(**requisite_values)

    def expense(self, **requisite_values):
        """
        Execute expanse.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        requisite_values[CODE_OPERATION_FIELD] = '-'
        return self.doOperation(**requisite_values)

    def delNotActualOperations(self, dt_actual=None):
        """
        Delete not actual operation for clear operation table.

        :param dt_actual: The date-time from which data are considered relevant.
            If None, then use now.
        :return: True/False.
        """
        if dt_actual is None:
            dt_actual = datetime.date.today()
        if isinstance(dt_actual, datetime.date):
            # You cannot compare date and datetime.
            # Therefore it is necessary to do type casting
            dt_actual = datetime.datetime.combine(dt_actual,
                                                  datetime.datetime.min.time())
        if not isinstance(dt_actual, datetime.datetime):
            log_func.error(u'Not valid operation actual datetime type <%s>' % dt_actual.__class__.__name__)
            return False

        operation_tab = self.getOperationTable()
        if operation_tab is not None:
            try:
                # Delete all records where the operation time is not defined
                sql = operation_tab.delete().where(operation_tab.c.dt_oper==None)
                sql.execute()
                sql = operation_tab.delete().where(operation_tab.c.dt_oper < dt_actual)
                sql.execute()
            except:
                log_func.fatal(u'Error delete not actual operations')
            return True
        return False
