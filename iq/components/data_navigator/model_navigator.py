#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator manager.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqModelNavigatorManager(object):
    """
    Data model navigator manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        self.__model__ = model

        self.__dataset__ = list()
        self.__rec_no__ = -1

    def getModel(self):
        """
        Get model.
        """
        if not self.__model__:
            model = self.createModel()
            self.setModel(model)
        return self.__model__

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

    def findRec(self, **find_params):
        """
        Find record in model. Get first record found.

        :param find_params: Search options.
        :return: Record dictionary or None if record not found.
        """
        records = self.searchRecs(**find_params)
        return records[0] if records else None

    def searchRecs(self, **search_params):
        """
        Search records in model.

        :param search_params: Search options.
        :return: Record dictionary list or None if records not found.
        """
        return list()

    def filterRecs(self, **filter_params):
        """
        Filter records in model.

        :param filter_params: Filter options.
        :return: Record dictionary list or None if records not found.
        """
        return list()

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
        pass

    def saveDatasetRecs(self, id_field=None):
        """
        Save records from dataset.

        :param id_field: Identifier field name.
        :return: True/False.
        """
        pass

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