#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator manager.
"""

import copy
from ...util import log_func

from ..data_model import data_object

from ..wx_filterchoicectrl import filter_convert

__version__ = (0, 0, 0, 1)


class iqModelNavigatorManager(data_object.iqDataObject):
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

    def getModelQuery(self):
        """
        Get model query object.

        :return: Query object or None if error.
        """
        session = self.getScheme().getSession()
        model = self.getModel()
        if session and model:
            return session.query(model)
        return None

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
                query = self.getModelQuery().filter(*search_args, **search_kwargs)
                if limit >= 0:
                    query = query.limit(limit)
                if order_by:
                    if isinstance(order_by, str):
                        order_by = (order_by,)
                    order_by_columns = [getattr(model, fld_name) for fld_name in order_by]
                    query = query.order_by(*order_by_columns)
                records = query
            else:
                table = self.getTable()
                select = filter_convert.convertFilter2SQLAlchemySelect(filter_data=rec_filter,
                                                                       table=table,
                                                                       limit=limit if limit >= 0 else None,
                                                                       order_by=order_by)
                result = select.execute()
                records = result.fetchall()
            return [vars(record) for record in records]
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
        Create new record.

        :param record: Record dictionary.
        :return: New model object or None if error.
        """
        try:
            if not isinstance(record, dict):
                # log_func.debug(u'Record type <%s>' % record.__class__.__name__)
                record = dict(record)

            model = self.getModel()
            model_rec = dict([(col_name, value) for col_name, value in record.items() if hasattr(model, col_name)])
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
        session = self.getScheme().getSession()
        try:
            new_obj = self.newRec(record)

            if session and new_obj:
                session.add(new_obj)
                session.commit()
                return True
        except:
            if session:
                session.rollback()
            log_func.fatal(u'<%s>. Error add record %s' % (self.getName(), str(record)))
        return False

    def addRecs(self, records):
        """
        Add records in model.

        :param records: Record list.
        :return: True/False.
        """
        session = self.getScheme().getSession()
        try:
            if not isinstance(records, (list, tuple)):
                # List casting
                records = list(records)

            for record in records:
                new_obj = self.newRec(record)
                if session and new_obj:
                    session.add(new_obj)

            if session:
                session.commit()
                return True
        except:
            if session:
                session.rollback()
            log_func.fatal(u'<%s>. Error add records' % self.getName())
        return False

    def saveRec(self, id, record, id_field=None):
        """
        Save record in model.

        :param id: Record identifier in model.
        :param record: Record dictionary.
        :param id_field: Identifier field name.
        :return: True/False.
        """
        if id_field is None:
            id_field = 'id'

        session = self.getScheme().getSession()
        try:
            model = self.getModel()
            query = self.getModelQuery()

            save_record = [(col_name, value) for col_name, value in record.items() if hasattr(model, col_name)]
            values = dict([(getattr(model, col_name), value) for col_name, value in save_record])
            query.filter(getattr(model, id_field) == id).update(values=values, synchronize_session=False)
            if session:
                session.commit()
            return True
        except:
            if session:
                session.rollback()
            log_func.fatal(u'Error save record [%s]' % str(id))
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
        if id_field is None:
            id_field = 'id'

        session = self.getScheme().getSession()
        try:
            model = self.getModel()
            query = self.getModelQuery()
            query.filter(getattr(model, id_field) == id).delete()
            if session:
                session.commit()
            return True
        except:
            if session:
                session.rollback()
            log_func.fatal(u'Error delete record [%s]' % str(id))
        return False

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

    def validRec(self):
        """

        :return:
        """
        pass

    def getValidErrors(self):
        """

        :return:
        """
        pass

    def linkTo(self):
        """

        :return:
        """
        pass

    def unlink(self):
        """

        :return:
        """
        pass

    def checkRec(self):
        """

        :return:
        """
        pass

    def uncheckRec(self):
        """

        :return:
        """
        pass

    def attachRec(self):
        """

        :return:
        """
        pass

    def detachRec(self):
        """

        :return:
        """
        pass

    def sumRecs(self):
        """

        :return:
        """
        pass

    def countRecs(self):
        """

        :return:
        """
        pass

    def copyRecTo(self):
        """

        :return:
        """
        pass

    def copyRecsTo(self):
        """

        :return:
        """
        pass

    def removeRecTo(self):
        """

        :return:
        """
        pass

    def removeRecsTo(self):
        """

        :return:
        """
        pass

    def clear(self):
        """
        Clear reference data object tables.

        :return: True/False.
        """
        try:
            self.getModelQuery().delete(synchronize_session=False)
            self.getScheme().getSession().commit()
            log_func.info(u'Clear reference data object <%s>' % self.getName())
            return True
        except:
            self.getScheme().getSession().rollback()
            log_func.fatal(u'Error clear reference data object <%s>' % self.getName())
        return False

    def setDefault(self, records=()):
        """
        Set default data object tables.

        :param records: Record list as tuple of record dictionaries.
        :return: True/False.
        """
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
                    field_type = column.getFieldType()
                    requisite_env['type'] = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(field_type)
                    requisite_env['funcs'] = column.getFilterFuncs()
                    link_psp = column.getLinkPsp()
                    if link_psp:
                        requisite_env['link_psp'] = link_psp

                    env['requisites'].append(requisite_env)
        else:
            log_func.warning(u'Not define model object for model navigator <%s>' % self.getName())
        return env
