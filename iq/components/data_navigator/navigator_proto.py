#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Navigator manager prototype.
"""

import sys

from ...util import log_func

from ..data_model import data_object

__version__ = (0, 0, 1, 2)


class iqNavigatorManagerProto(data_object.iqDataObject):
    """
    Navigator manager prototype class.
    """
    def getReadOnly(self):
        """
        Get readonly option.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def setReadOnly(self, readonly=True):
        """
        Set readonly option.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def getLimit(self):
        """
        Get limit dataset records.
        If the value is <0, then the number is not limited.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return -1

    def setLimit(self, limit=-1):
        """
        Set limit dataset records.

        :param limit: Limit dataset records.
            If the value is <0, then the number is not limited.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def getOrderBy(self):
        """
        Get sorting dataset records.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def setOrderBy(self, order_by=None):
        """
        Set sorting dataset records.

        :param order_by: Sorting dataset records.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def getRecFilter(self):
        """
        Get current filter.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def setRecFilter(self, rec_filter=None):
        """
        Set current filter.
        :param rec_filter: Current filter.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def getDataset(self, do_update=False):
        """
        Get current dataset.

        :param do_update: Update dataset?
        :return: Dataset.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def setDataset(self, dataset=None, clear=True, *args, **kwargs):
        """
        Set dataset in model.

        :param dataset: Dataset as list of record dictionaries.
        :param clear: Clear data object/model?
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def updateDataset(self, *filter_args, **filter_kwargs):
        """
        Update dataset by filter.

        :param filter_args: Filter options.
        :param filter_kwargs: Filter options.
        :return: Dataset.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getFirstDatasetRec(self):
        """
        Get first record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getLastDatasetRec(self):
        """
        Get last record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getPrevDatasetRec(self):
        """
        Get previous record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getNextDatasetRec(self):
        """
        Get next record of dataset or None if dataset is empty.

        :return: Record dictionary or None if dataset is empty.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getDatasetRec(self, rec_no=None):
        """
        Get record of dataset or None if dataset is empty.

        :param rec_no: Record index. If None then get current record index.
        :return: Record dictionary or None if dataset is empty.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def findRec(self, *find_args, **find_kwargs):
        """
        Find record in model. Get first record found.

        :param find_args: Search options.
        :param find_kwargs: Search options.
        :return: Record dictionary or None if record not found.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def searchRecs(self, *search_args, **search_kwargs):
        """
        Search records in model.

        :param search_args: Search options.
        :param search_kwargs: Search options.
        :return: Record dictionary list or None if records not found.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return list()

    def filterRecs(self, *filter_args, **filter_kwargs):
        """
        Filter records in model.

        :param filter_args: Filter options.
        :param filter_kwargs: Filter options.
        :return: Record dictionary list or None if records not found.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def sortDatasetRecs(self, *field_names):
        """
        Sort records in dataset.

        :param field_names: Sort field sort order.
        :return: Sorted dataset.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def reverseDatasetRecs(self, *field_names):
        """
        Reverse sort records in dataset.

        :param field_names: Sort field sort order.
        :return: Sorted dataset.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def newRec(self, record):
        """
        Create new record (without commit).

        :param record: Record dictionary.
        :return: New model object or None if error.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def addRec(self, record, auto_commit=True):
        """
        Add record in model.

        :param record: Record dictionary.
        :param auto_commit: Automatic commit?
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def addRecs(self, records):
        """
        Add records in model.

        :param records: Record list.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def saveRec(self, id, record, id_field=None):
        """
        Save record in model.

        :param id: Record identifier in model.
        :param record: Record dictionary.
        :param id_field: Identifier field name.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def saveDatasetRecs(self, id_field=None):
        """
        Save records from dataset.

        :param id_field: Identifier field name.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        pass

    def deleteRec(self, id, id_field=None):
        """
        Delete record in model.

        :param id: Record identifier in model.
        :param id_field: Identifier field name.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def deleteWhere(self, *where_args, **where_kwargs):
        """
        Delete record in model by filter.

        :param where_args: Where options.
        :param where_kwargs: Where options.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def existsQuery(self, query):
        """
        Exists query result?

        :param query: SQLAlchemy query object.
        :return: True/False or None if error.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def loadRec(self, id, id_field=None):
        """
        Load record from model.

        :param id_field: Identifier field name.
        :return: Record dictionary or None if error.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def loadDatasetRecs(self, id_field=None):
        """
        Load all dataset records from model.

        :param id_field: Identifier field name.
        :return: New dataset record list or None if error.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def validRec(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def getValidErrors(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def linkTo(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def unlink(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def checkRec(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def uncheckRec(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def attachRec(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def detachRec(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def sumRecs(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def countRecs(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def copyRecTo(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def copyRecsTo(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def removeRecTo(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def removeRecsTo(self):
        """

        :return:
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))

    def clear(self):
        """
        Clear reference data object tables.

        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def setDefault(self, records=()):
        """
        Set default data object tables.

        :param records: Record list as tuple of record dictionaries.
        :return: True/False.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return False

    def getFilterEnv(self):
        """
        Get filter environment.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getMinColumnValue(self, column_name):
        """
        Get minimum column value.

        :param column_name: Column name.
        :return: Minimum value. If table is empty return None.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None

    def getMaxColumnValue(self, column_name):
        """
        Get maximum column value.

        :param column_name: Column name.
        :return: Minimum value. If table is empty return None.
        """
        log_func.error(u'Not define <%s> method in <%s>' % (sys._getframe().f_code.co_name, self.__class__.__name__))
        return None
