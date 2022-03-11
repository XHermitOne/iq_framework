#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query dataset navigator manager.
"""

import sys
import datetime
import sqlalchemy.sql.functions

from ...util import log_func

# from ..data_model import data_object

from ..wx_filterchoicectrl import filter_convert

from ..data_navigator import navigator_proto

__version__ = (0, 0, 0, 1)


class iqQueryNavigatorManager(navigator_proto.iqNavigatorManagerProto):
    """
    Data query dataset navigator manager class.
    """
    def __init__(self, query=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        self.__query__ = query

        self.__dataset__ = None
        self.__rec_no__ = -1

        self.__filter_environment__ = None

        # Limit dataset records
        self.__limit__ = -1
        # Current filter
        self.__rec_filter__ = None
        # Sorting
        self.__order_by__ = None

    def setQuery(self, query=None):
        """
        Set query.
        """
        self.__query__ = query
        self.__dataset__ = list()
        self.__rec_no__ = -1

    def getQuery(self):
        """
        Get query.
        """
        return self.__query__

    def getQueryWhereName(self):
        """
        Get records filter name in Query expression WHERE section.
        """
        return 'WHERE'

    def getQueryOrderByName(self):
        """
        Sorting name in Query expression ORDER BY section.
        """
        return 'ORDER_BY'

    def getQueryLimitName(self):
        """
        Limiting name in Query expression LIMIT section.
        """
        return 'LIMIT'

    def getReadOnly(self):
        """
        Get readonly option.
        """
        return True

    def setReadOnly(self, readonly=True):
        """
        Set readonly option.
        """
        pass

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
        # self.__dataset__ = self._updateLinkDataDataset(self.__dataset__)
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

            variables = dict()
            variables[self.getQueryWhereName()] = rec_filter
            variables[self.getQueryOrderByName()] = order_by
            variables[self.getQueryLimitName()] = limit if limit >= 0 else ''

            query = self.getQuery()
            if query is not None:
                return query.execute(**variables)
            else:
                log_func.error(
                    u'<%s> method. <%s> object. <%s> class. Not define query object' % (sys._getframe().f_code.co_name,
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

    def _getQueryColumnTypeEnv(self, value):
        """
        Get query column type by value.
        """
        if isinstance(value, str):
            return 'Text'
        elif isinstance(value, datetime.date):
            return 'Date'
        elif isinstance(value, datetime.datetime):
            return 'DateTime'
        elif isinstance(value, float):
            return 'Float'
        elif isinstance(value, int):
            return 'Int'
        return None

    def _genFilterEnv(self, unused_columns=('id',)):
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

        query = self.getQuery()
        if query:
            rec_filter = self.getRecFilter()
            limit = self.getLimit()
            order_by = self.getOrderBy()

            variables = dict()
            variables[self.getQueryWhereName()] = rec_filter
            variables[self.getQueryOrderByName()] = order_by
            variables[self.getQueryLimitName()] = limit if limit >= 0 else ''

            first_records = query.getFirstRecord(**variables)

            if first_records:
                columns = list(first_records[0].items())
                for column_name, value in columns:
                    if column_name not in unused_columns:
                        requisite_env = dict()
                        requisite_env['name'] = column_name
                        requisite_env['description'] = u''
                        requisite_env['field'] = column_name
                        # field_type = column.getFieldType()
                        # requisite_env['type'] = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(field_type)
                        field_type = self._getQueryColumnTypeEnv(value)
                        requisite_env['type'] = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(field_type)
                        requisite_env['funcs'] = filter_builder_env.DEFAULT_FUNCS.get(requisite_env['type'])
                        env['requisites'].append(requisite_env)
        else:
            log_func.warning(u'Not define query object for query navigator <%s>' % self.getName())
        return env

