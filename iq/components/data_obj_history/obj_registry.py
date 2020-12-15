#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Object registry manager.

Object registry is object state change log_func.

The procedure for working with the object register:
1. Create object registry
2. Create DB connection (call connect())
3. Call methods for changing the state of an object (doState/undoState)
4. Disconnect with DB (call disconnect())
"""

import uuid
import datetime
import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from ...util import log_func

__version__ = (0, 0, 0, 1)

# Default operation table
DEFAULT_OPERATIONS_TABLE = 'operations'
# Default object table
DEFAULT_OBJ_TABLE = 'object_tab'

SQL_ROLLBACK = 'ROLLBACK'

# Requisite types
INTEGER_REQUISITE_TYPE = 'int'
FLOAT_REQUISITE_TYPE = 'float'
TEXT_REQUISITE_TYPE = 'text'
DT_REQUISITE_TYPE = 'datetime'

# Operation table fields
GUID_OBJ_OPERATION_FIELD = 'guid'
OBJ_OPERATION_FIELD = 'n_obj'
PREV_OPERATION_FIELD = 'prev'
POST_OPERATION_FIELD = 'post'
DT_OPERATION_FIELD = 'dt_operation'

# Object table fields
GUID_OBJ_FIELD = 'guid'
N_OBJ_FIELD = 'n_obj'
DTCREATE_OBJ_FIELD = 'dt_create'
STATE_OBJ_FIELD = 'state'
DTSTATE_OBJ_FIELD = 'dt_state'

# Default state
DEFAULT_CREATE_STATE = 'CREATED'


class iqObjRegistry(object):
    """
    Object registry class.

      Event 1-----+
      Event 2---+ |
      Event 3-+ | |
              | | |
    +---------| | |-------------------------+
    |         V V V    Object registry      |
    | +===============+                     |
    | |  Operations   |                     |
    | +===============+                     |
    |       |                               |
    |       V                               |
    | +=============================+       |
    | | Object state changing log   |       |
    | +=============================+       |
    +---------------------------------------+

    Data object
    Объект identified by fields GUID and n_obj.
    Change object state log in fields:
    prev - previous object state.
    post - next object state.
    """
    def __init__(self, db_url=None,
                 operation_table_name=DEFAULT_OPERATIONS_TABLE,
                 obj_table_name=DEFAULT_OBJ_TABLE):
        """
        Constructor.

        :param db_url: DB URL. Connection string.
        :param operation_table_name: Operation table name.
        :param obj_table_name: Object table name.
        """
        self._db_url = db_url
        self._connection = None

        self._operation_table_name = operation_table_name
        self._operation_table = None
        self._obj_table_name = obj_table_name
        self._obj_table = None

        # Object requisites
        self._obj_requisites = list()

    def getOperationTable(self):
        """
        Get operation sqlalchemy table object.
        """
        if not self.isConnected():
            self.connect()

        if self._operation_table is None:
            self.createOperationTable()
        return self._operation_table

    def getObjectTable(self):
        """
        Get object sqlalchemy table object.
        """
        if not self.isConnected():
            self.connect()

        if self._obj_table is None:
            self.createObjectTable()
        return self._obj_table

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
        :return: DB connection object.
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

    def createOperationTable(self, operation_table_name=None):
        """
        Create operation table.

        For operation table need create fields:
            1. Datetime operation field.
            2. GUID - data object identifier (system level id).
            3. Object number (program level id).
            4. Previous object state field
            5. Next object state field

        :param operation_table_name: Oparetion table name.
        :return: Operation table object or None if error.
        """
        if operation_table_name is None:
            operation_table_name = self._operation_table_name

        dt_requisite = dict(requisite_name=DT_OPERATION_FIELD,
                            requisite_type=DT_REQUISITE_TYPE)
        guidobj_requisite = dict(requisite_name=GUID_OBJ_OPERATION_FIELD,
                                 requisite_type=TEXT_REQUISITE_TYPE)
        nobj_requisite = dict(requisite_name=OBJ_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        prev_requisite = dict(requisite_name=PREV_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        post_requisite = dict(requisite_name=POST_OPERATION_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        requisites = [dt_requisite,
                      guidobj_requisite,
                      nobj_requisite,
                      prev_requisite,
                      post_requisite] + self._obj_requisites
        self._operation_table = self.genTable(operation_table_name, requisites)
        self._operation_table.create(bind=self.getConnection(),
                                     checkfirst=True)
        return self._operation_table

    def createObjectTable(self, obj_table_name=None):
        """
        Create object table.

        :param obj_table_name: Object table name.
        :return: Object table or None if error.
        """
        if obj_table_name is None:
            obj_table_name = self._obj_table_name

        guidobj_requisite = dict(requisite_name=GUID_OBJ_FIELD,
                                 requisite_type=TEXT_REQUISITE_TYPE)
        nobj_requisite = dict(requisite_name=N_OBJ_FIELD,
                              requisite_type=TEXT_REQUISITE_TYPE)
        dtcreate_requisite = dict(requisite_name=DTCREATE_OBJ_FIELD,
                                  requisite_type=DT_REQUISITE_TYPE)
        state_requisite = dict(requisite_name=STATE_OBJ_FIELD,
                               requisite_type=TEXT_REQUISITE_TYPE)
        dtstate_requisite = dict(requisite_name=DTSTATE_OBJ_FIELD,
                                 requisite_type=DT_REQUISITE_TYPE)

        requisites = [guidobj_requisite,
                      nobj_requisite,
                      dtcreate_requisite,
                      state_requisite,
                      dtstate_requisite] + self._obj_requisites
        self._obj_table = self.genTable(obj_table_name, requisites)
        self._obj_table.create(bind=self.getConnection(),
                               checkfirst=True)
        return self._obj_table

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

    def getObjRequisiteNames(self):
        """
        Get object requisite names.

        :return: Requisite name list.
        """
        names = [requisite.get('requisite_name', None) for requisite in self._obj_requisites]
        return names

    def addObjRequisite(self, requisite_name, requisite_type):
        """
        Add object requisite.

        :param requisite_name: Requisite name.
        :param requisite_type: Requisite type.
            Requisite type
            can Integer ('int')/Float ('float')/
            DateTime('datetime')/Text ('text').
        """
        requisite = dict(requisite_name=requisite_name,
                         requisite_type=requisite_type)
        self._obj_requisites.append(requisite)

    def _getOperationRequisiteValues(self, **requisite_values):
        """
        Get only required details of details for the operation table.

        :param requisite_values: Requisite values.
        :return: List of details used in the register.
        """
        used_requisite_names = [GUID_OBJ_OPERATION_FIELD,
                                OBJ_OPERATION_FIELD,
                                DT_OPERATION_FIELD,
                                PREV_OPERATION_FIELD,
                                POST_OPERATION_FIELD] + self.getObjRequisiteNames()
        return dict([(name, value) for name, value in requisite_values.items() if name in used_requisite_names])

    def doState(self, **requisite_values):
        """
        Set new data object state.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Create table
        operation_table = self.createOperationTable()
        obj_table = self.createObjectTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        sql = None
        # Current system time
        dt_now = datetime.datetime.now()
        try:
            result = True
            # Define a way to identify an object
            guid_obj = requisite_values.get(GUID_OBJ_FIELD, None)
            n_obj = requisite_values.get(N_OBJ_FIELD, None)
            obj_id_requisites = [(name, value) for name, value in [(GUID_OBJ_FIELD, guid_obj),
                                                                   (N_OBJ_FIELD, n_obj)] if value]

            # Search for an object by given identifiers
            where = [getattr(obj_table.c, name) == value for name, value in obj_id_requisites]
            find = obj_table.select(sqlalchemy.and_(*where)).execute()
            if not find.rowcount:
                # If an object with this identifier is not found, then create it
                obj_requisite_names = self.getObjRequisiteNames()
                obj_requisites = dict([(name, requisite_values.get(name, None)) for name in obj_requisite_names])
                obj_requisites[DTCREATE_OBJ_FIELD] = requisite_values.get(DTCREATE_OBJ_FIELD, dt_now)
                obj_requisites[N_OBJ_FIELD] = n_obj
                # The object must be GUID
                guid_obj = guid_obj if guid_obj else str(uuid.uuid4())
                obj_requisites[GUID_OBJ_FIELD] = guid_obj
                # Determine the current state of the object
                obj_state = None
                new_state = requisite_values[STATE_OBJ_FIELD] if STATE_OBJ_FIELD in requisite_values else DEFAULT_CREATE_STATE
                # Record new state
                obj_requisites[STATE_OBJ_FIELD] = new_state
                obj_requisites[DTSTATE_OBJ_FIELD] = dt_now
                sql = obj_table.insert().values(**obj_requisites)
                transaction.execute(sql)
            else:
                find_obj = find.first()
                # Determine the current state of the object
                obj_state = find_obj[STATE_OBJ_FIELD]
                # The new state of the object
                new_state = requisite_values.get(STATE_OBJ_FIELD, obj_state)
                guid_obj = find_obj[GUID_OBJ_FIELD]
                n_obj = find_obj[N_OBJ_FIELD]

                # Record the new state of the object and details
                obj_requisite_names = self.getObjRequisiteNames()
                obj_requisites = dict([(name, requisite_values.get(name, None)) for name in obj_requisite_names])
                obj_requisites[STATE_OBJ_FIELD] = new_state
                obj_requisites[DTSTATE_OBJ_FIELD] = dt_now
                sql = obj_table.update().where(sqlalchemy.and_(*where)).values(**obj_requisites)
                transaction.execute(sql)

            # Record motion operation
            if obj_state != new_state:
                # Only if our condition really changes
                # otherwise no movement
                operation_requisite_values = self._getOperationRequisiteValues(**requisite_values)
                operation_requisite_values[DT_OPERATION_FIELD] = dt_now
                operation_requisite_values[GUID_OBJ_OPERATION_FIELD] = guid_obj
                operation_requisite_values[OBJ_OPERATION_FIELD] = n_obj
                operation_requisite_values[PREV_OPERATION_FIELD] = obj_state
                operation_requisite_values[POST_OPERATION_FIELD] = new_state

                sql = operation_table.insert().values(**operation_requisite_values)
                transaction.execute(sql)
            else:
                # Changing details without movement operation
                operation_requisite_values = self._getOperationRequisiteValues(**requisite_values)
                operation_requisite_values[DT_OPERATION_FIELD] = dt_now
                operation_requisite_values[GUID_OBJ_OPERATION_FIELD] = guid_obj
                operation_requisite_values[OBJ_OPERATION_FIELD] = n_obj

                where = [getattr(operation_table.c, GUID_OBJ_OPERATION_FIELD) == guid_obj,
                         getattr(operation_table.c, OBJ_OPERATION_FIELD) == n_obj,
                         getattr(operation_table.c, POST_OPERATION_FIELD) == new_state]
                sql = operation_table.update().where(sqlalchemy.and_(*where)).values(**operation_requisite_values)
                transaction.execute(sql)

            if result:
                # Commit transaction
                transaction.commit()
            return result
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error change state data object operation <%s>' % requisite_values)
        return False

    def undoState(self, **requisite_values):
        """
        Undo change data object state.

        :param requisite_values: Requisite values.
        :return: True - operation was successfully completed.
            False - Operation is not completed  due to error.
            The transaction rolled back the operation.
        """
        # Create table
        operation_table = self.createOperationTable()
        obj_table = self.createObjectTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            result = True
            # Define a way to identify an object
            guid_obj = requisite_values.get(GUID_OBJ_FIELD, None)
            n_obj = requisite_values.get(N_OBJ_FIELD, None)
            obj_id_requisites = [(name, value) for name, value in [(GUID_OBJ_FIELD, guid_obj),
                                                                   (N_OBJ_FIELD, n_obj)] if value]
            # Find the latest registration of an object state change
            oper_where = [getattr(operation_table.c, name) == value for name, value in obj_id_requisites]
            obj_where = [getattr(obj_table.c, name) == value for name, value in obj_id_requisites]
            find = operation_table.select(sqlalchemy.and_(*oper_where)).order_by(desc(DT_OPERATION_FIELD)).execute()
            if find.rowcount:
                # Records are in the table of movements
                if find.rowcount == 1:
                    # If this is the last entry in the movement table, then delete
                    sql = operation_table.delete().where(sqlalchemy.and_(*oper_where))
                    transaction.execute(sql)
                    sql = obj_table.delete().where(sqlalchemy.and_(*obj_where))
                    transaction.execute(sql)
                else:
                    find_state = find.fetchone()
                    prev_state = find.fetchone()
                    # This is not the last record you need to roll back to the previous state
                    obj_requisites = dict()
                    obj_requisites[STATE_OBJ_FIELD] = find_state[PREV_OPERATION_FIELD]
                    obj_requisites[DTSTATE_OBJ_FIELD] = prev_state[DT_OPERATION_FIELD]
                    # Restore the details of the object corresponding to the previous state
                    obj_requisite_names = self.getObjRequisiteNames()
                    for requisite_name in obj_requisite_names:
                        obj_requisites[requisite_name] = prev_state[requisite_name]
                    requisite_values.update(obj_requisites)

                    sql = obj_table.update().where(sqlalchemy.and_(*obj_where)).values(**requisite_values)
                    transaction.execute(sql)

                    # Delete last state record
                    # Check is made for a complete match record
                    sql = operation_table.delete().where(sqlalchemy.and_(*oper_where))
                    transaction.execute(sql)
            else:
                # If there are no entries in the motion log,
                # then it is not possible to determine the previous state
                # of the object, and therefore it is impossible to undo
                result = False

            if result:
                # Commit transaction
                transaction.commit()
            return result
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error undo change state operation <%s>' % requisite_values)
        return False

    def clearAll(self):
        """
        Delete all registry records!

        :return: True/False.
        """
        # Create tables
        operation_table = self.createOperationTable()
        obj_table = self.createObjectTable()

        # Start transaction
        session = sessionmaker(bind=self._connection)
        transaction = session()

        try:
            sql = operation_table.delete()
            transaction.execute(sql)

            sql = obj_table.delete()
            transaction.execute(sql)

            # Commit transaction
            transaction.commit()
            return True
        except:
            # Rollback transaction
            transaction.rollback()
            log_func.fatal(u'Error clear data object registry')
        return False

    def getOperationStateRecord(self, guid_obj=None, n_obj=None, state=None):
        """
        Get a record of an object’s movement transaction to state.

        :param guid_obj: Data object GUID.
            If None, then data object indent by n_obj.
        :param n_obj: Data object number.
            If None, then data object indent by GUID.
        :param state: Data object state.
        :return: Operation record or None if not found by state.
        """
        # Create table
        operation_table = self.createOperationTable()

        # Define a way to identify a motion operation
        obj_id_requisites = [(name, value) for name, value in [(GUID_OBJ_FIELD, guid_obj),
                                                               (N_OBJ_FIELD, n_obj),
                                                               (POST_OPERATION_FIELD, state)] if value]

        # Search operation by given identifiers
        where = [getattr(operation_table.c, name) == value for name, value in obj_id_requisites]
        find = operation_table.select(sqlalchemy.and_(*where)).order_by(desc(DT_OPERATION_FIELD)).execute()
        if find.rowcount == 1:
            record = find.first()
            return dict(record)
        elif find.rowcount > 1:
            log_func.warning(u'Redundant status operation <%s> data object [%s : %s]' % (state, guid_obj, n_obj))
            record = find.first()
            return dict(record)
        elif find.rowcount < 1:
            log_func.warning(u'Operations not found <%s> data object [%s : %s]' % (state, guid_obj, n_obj))

        return None

    def delNotActualOperation(self, dt_actual=None):
        """
        Delete not actual operations.

        :param dt_actual: Date from which data is read relevant.
            If None, then today's date is taken.
        :return: True/False.
        """
        if dt_actual is None:
            dt_actual = datetime.date.today()

        if (not isinstance(dt_actual, datetime.date)) and (not isinstance(dt_actual, datetime.datetime)):
            log_func.warning(u'Not valid actual date type <%s : %s>' % (dt_actual,
                                                                      dt_actual.__class__.__name__))
            return False

        operation_tab = self.getOperationTable()
        if operation_tab is not None:
            try:
                sql = operation_tab.delete().where(operation_tab.c.dt_oper < dt_actual)
                sql.execute()
            except:
                log_func.fatal(u'Error delete not actual operations')
                return False

        object_tab = self.getObjectTable()
        if object_tab is not None:
            try:
                sql = object_tab.delete().where(object_tab.c.dt_create < dt_actual)
                sql.execute()
            except:
                log_func.fatal(u'Error delete not actual operations')
                return False

        return True
