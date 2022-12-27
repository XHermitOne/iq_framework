#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator manager.
"""

import sys
import sqlalchemy.sql.functions

from ...util import log_func

# from ..data_model import data_object

from ..wx_filterchoicectrl import filter_convert

from . import navigator_proto

__version__ = (0, 0, 2, 2)


class iqModelNavigatorManager(navigator_proto.iqNavigatorManagerProto):
    """
    Data model navigator manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        self.__model__ = model

        self.__dataset__ = None
        self.__rec_no__ = -1

        self.__filter_environment__ = None

        # Limit dataset records
        self.__limit__ = -1
        # Current filter
        self.__rec_filter__ = None
        # Sorting
        self.__order_by__ = None
        # Readonly
        self.__readonly__ = False

    def getReadOnly(self):
        """
        Get readonly option.
        """
        return self.__readonly__

    def setReadOnly(self, readonly=True):
        """
        Set readonly option.
        """
        self.__readonly__ = readonly

    def getModel(self):
        """
        Get model.
        """
        if not self.__model__:
            model = self.createModel()
            self.setModel(model)
        return self.__model__

    def getTable(self):
        """
        Get table object.
        """
        model = self.getModel()
        if model:
            return model.__table__
        return None

    def createModel(self):
        """
        Create model object.

        :return: Model or None if error.
        """
        log_func.error(u'Not define method createModel in <%s : %s>' % (self.getName(),
                                                                        self.getType()))
        return None

    def setModel(self, model=None):
        """
        Set model.
        """
        self.__model__ = model
        self.__dataset__ = list()
        self.__rec_no__ = -1

    def getModelObj(self):
        """
        Get model resource object.
        """
        return None

    def getScheme(self):
        """
        Get scheme object by model.

        :return: Data scheme object or None if error.
        """
        log_func.error(u'Not define method getScheme in <%s>' % self.__class__.__name__)
        return None

    def startTransaction(self, *args, **kwargs):
        """
        Start transaction.

        :return: Session/transaction object.
        """
        scheme = self.getScheme()
        return scheme.startTransaction(*args, **kwargs) if scheme else None

    def stopTransaction(self, transaction, *args, **kwargs):
        """
        Stop transaction.

        :param transaction: Session/transaction object.
        :return: True/False.
        """
        scheme = self.getScheme()
        return scheme.stopTransaction(transaction, *args, **kwargs) if scheme else False

    def getLimit(self):
        """
        Get limit dataset records.
        If the value is <0, then the number is not limited.
        """
        return self.__limit__

    def setLimit(self, limit=-1):
        """
        Set limit dataset records.
        :param limit: Limit dataset records.
            If the value is <0, then the number is not limited.
        """
        if not isinstance(limit, int):
            self.__limit__ = -1
        else:
            self.__limit__ = limit

    def getOrderBy(self):
        """
        Get sorting dataset records.
        """
        return self.__order_by__

    def setOrderBy(self, order_by=None):
        """
        Set sorting dataset records.
        :param order_by: Sorting dataset records.
        """
        if not isinstance(order_by, (str, tuple, list)):
            self.__order_by__ = None
        else:
            self.__order_by__ = order_by

    def getRecFilter(self):
        """
        Get current filter.
        """
        return self.__rec_filter__

    def setRecFilter(self, rec_filter=None):
        """
        Set current filter.
        :param rec_filter: Current filter.
        """
        self.__rec_filter__ = rec_filter

    def getDataset(self, do_update=False):
        """
        Get current dataset.

        :param do_update: Update dataset?
        :return: Dataset.
        """
        if self.__dataset__ is None or do_update:
            return self.updateDataset()
        return self.__dataset__

    def setDataset(self, dataset=None, clear=True, *args, **kwargs):
        """
        Set dataset in model.

        :param dataset: Dataset as list of record dictionaries.
        :param clear: Clear data object/model?
        :return: True/False.
        """
        result = super().setDataset(self, dataset=dataset, clear=clear, *args, **kwargs)
        if result:
            self.updateDataset()
        return result

    def updateDataset(self, *filter_args, **filter_kwargs):
        """
        Update dataset by filter.

        :param filter_args: Filter options.
        :param filter_kwargs: Filter options.
        :return: Dataset.
        """
        self.__dataset__ = self.filterRecs(*filter_args, **filter_kwargs)

        # Update dataset by link object data
        self.__dataset__ = self._updateLinkDataDataset(self.__dataset__)
        return self.__dataset__

    def getFirstDatasetRec(self):
        """
        Get first record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        if self.__dataset__:
            self.__rec_no__ = 0
            return self.__dataset__[0]
        return None

    def getLastDatasetRec(self):
        """
        Get last record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        if self.__dataset__:
            self.__rec_no__ = len(self.__dataset__) - 1
            return self.__dataset__[-1]
        return None

    def getPrevDatasetRec(self):
        """
        Get previous record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        if self.__dataset__:
            self.__rec_no__ = max(0, self.__rec_no__ - 1)
            return self.__dataset__[self.__rec_no__]
        return None

    def getNextDatasetRec(self):
        """
        Get next record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        if self.__dataset__:
            self.__rec_no__ = min(len(self.__dataset__) - 1, 
                                  self.__rec_no__ + 1)
            return self.__dataset__[self.__rec_no__]
        return None

    def getDatasetRec(self, rec_no=None):
        """
        Get record of dataset or None if dataset is empty.        

        :param rec_no: Record index. If None then get current record index.
        :return: Record dictionary or None if dataset is empty.
        """
        if rec_no is not None:
            self.__rec_no__ = max(0, min(len(self.__dataset__) - 1, rec_no))
        rec_no = self.__rec_no__

        if self.__dataset__:
            return self.__dataset__[rec_no]
        return None

    def findRec(self, *find_args, **find_kwargs):
        """
        Find record in model. Get first record found.

        :param find_args: Search options.
        :param find_kwargs: Search options.
        :return: Record dictionary or None if record not found.
        """
        records = self.searchRecs(*find_args, **find_kwargs)
        return records[0] if records else None

    def searchRecs(self, *search_args, **search_kwargs):
        """
        Search records in model.

        :param search_args: Search options.
        :param search_kwargs: Search options.
        :return: Record dictionary list or None if records not found.
        """
        try:
            rec_filter = self.getRecFilter()
            limit = self.getLimit()
            order_by = self.getOrderBy()

            if not rec_filter:
                model = self.getModel()
                transaction = self.startTransaction()
                query = transaction.query(model).filter(*search_args, **search_kwargs)
                if limit >= 0:
                    query = query.limit(limit)
                if order_by:
                    if isinstance(order_by, str):
                        order_by = (order_by,)
                    order_by_columns = [getattr(model, fld_name) for fld_name in order_by]
                    query = query.order_by(*order_by_columns)
                records = [vars(record) for record in query]
                self.stopTransaction(transaction)
                return records
            else:
                table = self.getTable()
                if table is not None:
                    select = filter_convert.convertFilter2SQLAlchemySelect(filter_data=rec_filter,
                                                                           table=table,
                                                                           limit=limit if limit >= 0 else None,
                                                                           order_by=order_by)
                    transaction = self.startTransaction()
                    result = transaction.execute(select)
                    records = [dict(record) for record in result.fetchall()]
                    self.stopTransaction(transaction)
                    return records
                else:
                    log_func.error(u'<%s> method. <%s> object. <%s> class. Not define table object' % (sys._getframe().f_code.co_name,
                                                                                                       self.getName(),
                                                                                                       self.__class__.__name__))
        except:
            log_func.fatal(u'Error search records by %s %s' % (str(search_args), str(search_kwargs)))
        return list()

    def filterRecs(self, *filter_args, **filter_kwargs):
        """
        Filter records in model.

        :param filter_args: Filter options.
        :param filter_kwargs: Filter options.
        :return: Record dictionary list or None if records not found.
        """
        return self.searchRecs(*filter_args, **filter_kwargs)

    def sortDatasetRecs(self, *field_names):
        """
        Sort records in dataset.

        :param field_names: Sort field sort order.
        :return: Sorted dataset.
        """
        return self.__dataset__

    def reverseDatasetRecs(self, *field_names):
        """
        Reverse sort records in dataset.

        :param field_names: Sort field sort order.
        :return: Sorted dataset.
        """
        return self.__dataset__

    def newRec(self, record):
        """
        Create new record (without commit).

        :param record: Record dictionary.
        :return: New model object or None if error.
        """
        if self.getReadOnly():
            log_func.error(u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                            self.getName(),
                                                                                            self.__class__.__name__))
            return None

        try:
            if not isinstance(record, dict):
                # log_func.debug(u'Record type <%s>' % record.__class__.__name__)
                record = dict(record)

            model = self.getModel()
            model_rec = {col_name: value for col_name, value in record.items() if hasattr(model, col_name)}
            new_obj = model(**model_rec)
            return new_obj
        except:
            log_func.fatal(u'<%s>. Error create new record %s' % (self.getName(), str(record)))
        return None

    def addRec(self, record, auto_commit=True):
        """
        Add record in model.

        :param record: Record dictionary.
        :param auto_commit: Automatic commit?
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                            self.getName(),
                                                                                            self.__class__.__name__))
            return None

        scheme = self.getScheme()
        transaction = scheme.startTransaction()
        try:
            new_obj = self.newRec(record)

            if transaction and new_obj:
                transaction.add(new_obj)
                transaction.commit()
                scheme.stopTransaction(transaction)
                return True
        except:
            if transaction:
                transaction.rollback()
                scheme.stopTransaction(transaction)
            log_func.fatal(u'<%s>. Error add record %s' % (self.getName(), str(record)))
        scheme.closeSession()
        return False

    def addRecs(self, records):
        """
        Add records in model.

        :param records: Record list.
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return None

        scheme = self.getScheme()
        transaction = scheme.startTransaction()
        try:
            if not isinstance(records, (list, tuple)):
                # List casting
                records = list(records)

            for record in records:
                new_obj = self.newRec(record)
                if transaction and new_obj:
                    transaction.add(new_obj)

            if transaction:
                transaction.commit()
                scheme.stopTransaction(transaction)
                return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'<%s>. Error add records' % self.getName())

        scheme.stopTransaction(transaction)
        return False

    def saveRec(self, id, record, id_field=None):
        """
        Save record in model.

        :param id: Record identifier in model.
        :param record: Record dictionary.
        :param id_field: Identifier field name.
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return False

        if id_field is None:
            id_field = 'id'

        model = self.getModel()
        transaction = self.startTransaction()
        try:
            query = transaction.query(model)
            save_record = [(col_name, value) for col_name, value in record.items() if hasattr(model, col_name)]
            values = {getattr(model, col_name): value for col_name, value in save_record}
            query.filter(getattr(model, id_field) == id).update(values=values, synchronize_session=False)
            if transaction:
                transaction.commit()
            self.stopTransaction(transaction)
            return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error save record [%s]' % str(id))
        self.stopTransaction(transaction)
        return False

    def saveDatasetRecs(self, id_field=None):
        """
        Save records from dataset.

        :param id_field: Identifier field name.
        :return: True/False.
        """
        pass

    def deleteRec(self, id, id_field=None):
        """
        Delete record in model.

        :param id: Record identifier in model.
        :param id_field: Identifier field name.
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return False

        if id_field is None:
            id_field = 'id'

        model = self.getModel()
        transaction = self.startTransaction()
        try:
            query = transaction.query(model)
            query.filter(getattr(model, id_field) == id).delete()
            if transaction:
                transaction.commit()
            self.stopTransaction(transaction)
            return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error delete record [%s]' % str(id))
        self.stopTransaction(transaction)
        return False

    def deleteWhere(self, *where_args, **where_kwargs):
        """
        Delete record in model by filter.

        :param where_args: Where options.
        :param where_kwargs: Where options.
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return False

        transaction = None
        try:
            rec_filter = self.getRecFilter()

            if not rec_filter:
                # log_func.debug(u'Delete by where %s %s' % (str(where_args), str(where_kwargs)))
                model = self.getModel()
                transaction = self.startTransaction()
                query = transaction.query(model).filter(*where_args, **where_kwargs).delete(synchronize_session=False)
                transaction.commit()
                self.stopTransaction(transaction)
            else:
                # log_func.debug(u'Delete by record filter %s' % str(rec_filter))
                table = self.getTable()
                if table is not None:
                    select = filter_convert.convertFilter2SQLAlchemySelect(filter_data=rec_filter,
                                                                           table=table)
                    transaction = self.startTransaction()
                    transaction.execute(select).delete(synchronize_session=False)
                    transaction.commit()
                    self.stopTransaction(transaction)
                    return True
                else:
                    log_func.error(u'<%s> method. <%s> object. <%s> class. Not define table object' % (sys._getframe().f_code.co_name,
                                                                                                       self.getName(),
                                                                                                       self.__class__.__name__))
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error delete records by filter %s %s' % (str(where_args), str(where_kwargs)))
        return False

    def existsQuery(self, query):
        """
        Exists query result?

        :param query: SQLAlchemy query object.
        :return: True/False or None if error.
        """
        scheme = self.getScheme()
        transaction = scheme.startTransaction()
        try:
            result = transaction.query(query.exists()).scalar()
            scheme.stopTransaction(transaction)
            return result
        except:
            log_func.fatal(u'Exists query result error')
        scheme.stopTransaction(transaction)
        return None

    def loadRec(self, id, id_field=None):
        """
        Load record from model.

        :param id_field: Identifier field name.
        :return: Record dictionary or None if error.
        """
        pass

    def loadDatasetRecs(self, id_field=None):
        """
        Load all dataset records from model.

        :param id_field: Identifier field name.
        :return: New dataset record list or None if error.
        """
        pass

    def clear(self):
        """
        Clear reference data object tables.

        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return False

        transaction = self.startTransaction()
        try:
            transaction.query(self.getModel()).delete(synchronize_session=False)
            transaction.commit()
            log_func.info(u'Clear reference data object <%s>' % self.getName())
            self.stopTransaction(transaction)
            return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error clear reference data object <%s>' % self.getName())
        self.stopTransaction(transaction)
        return False

    def setDefault(self, records=()):
        """
        Set default data object tables.

        :param records: Record list as tuple of record dictionaries.
        :return: True/False.
        """
        if self.getReadOnly():
            log_func.error(
                u'<%s> method. <%s> object. <%s> class. Set readonly option.' % (sys._getframe().f_code.co_name,
                                                                                 self.getName(),
                                                                                 self.__class__.__name__))
            return False

        if self.clear():
            return self.addRecs(records)
        return False

    def getFilterEnv(self):
        """
        Get filter environment.
        """
        if self.__filter_environment__ is None:
            try:
                self.__filter_environment__ = self._genFilterEnv()
            except:
                log_func.fatal(u'Generate filter environment error')
        return self.__filter_environment__

    def _genFilterEnv(self, unused_columns=('id', )):
        """
        Generate filter environment.
        
        :param unused_columns: Unused column names.
        :return: Filter environment dictionary.
        """
        from ..wx_filterchoicectrl import filter_builder_env

        env = {'requisites': [],  # Requisite list
               'logic': filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS,  # Standart logic operations
               'funcs': filter_builder_env.DEFAULT_ENV_FUNCS,  # Standart functions
               }

        model_obj = self.getModelObj()
        if model_obj:
            columns = model_obj.getColumns()
            for column in columns:
                column_name = column.getName()
                if column_name not in unused_columns:
                    requisite_env = dict()
                    requisite_env['name'] = column_name
                    requisite_env['description'] = column.getDescription()
                    requisite_env['field'] = column_name
                    # field_type = column.getFieldType()
                    # requisite_env['type'] = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(field_type)
                    requisite_env['type'] = column.getFilterRequisiteType()
                    requisite_env['funcs'] = column.getFilterFuncs()
                    link_psp = column.getLinkPsp()
                    if link_psp:
                        requisite_env['link_psp'] = link_psp

                    env['requisites'].append(requisite_env)
        else:
            log_func.warning(u'Not define model object for model navigator <%s>' % self.getName())
        return env

    def getMinColumnValue(self, column_name):
        """
        Get minimum column value.

        :param column_name: Column name.
        :return: Minimum value. If table is empty return None.
        """
        model = self.getModel()
        transaction = self.startTransaction()
        try:
            min_value = transaction.query(sqlalchemy.sql.functions.min(getattr(model, column_name))).scalar()
            if transaction:
                transaction.commit()
            self.stopTransaction(transaction)
            return min_value
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error get minimum column <%s> value ' % column_name)
        self.stopTransaction(transaction)
        return None

    def getMaxColumnValue(self, column_name):
        """
        Get maximum column value.

        :param column_name: Column name.
        :return: Minimum value. If table is empty return None.
        """
        model = self.getModel()
        transaction = self.startTransaction()
        try:
            max_value = transaction.query(sqlalchemy.sql.functions.max(getattr(model, column_name))).scalar()
            if transaction:
                transaction.commit()
            self.stopTransaction(transaction)
            return max_value
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error get maximum column <%s> value ' % column_name)
        self.stopTransaction(transaction)
        return None
