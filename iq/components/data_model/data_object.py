#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data object interface class.
"""

from ...util import log_func
from ...util import global_func

__version__ = (0, 0, 1, 2)

DATA_NAME_DELIMETER = '.'


class iqDataObjectProto(object):
    """
    Data object interface prototype class.
    """
    def getDataset(self, *args, **kwargs):
        """
        Get dataset.

        :return: Record dictionary list.
        """
        log_func.warning(u'Not define method <getDataset> in <%s>' % self.__class__.__name__)
        return list()

    def setDataset(self, dataset=None, clear=True, *args, **kwargs):
        """
        Set dataset in model.

        :param dataset: Dataset as list of record dictionaries.
        :param clear: Clear data object/model?
        :return: True/False.
        """
        log_func.warning(u'Not define method <setDataset> in <%s>' % self.__class__.__name__)
        return False

    def clear(self):
        """
        Clear data object/model.

        :return: True/False.
        """
        log_func.warning(u'Not define method <clear> in <%s>' % self.__class__.__name__)
        return False

    def getScheme(self):
        """
        Get scheme object.

        :return:
        """
        log_func.warning(u'Not define method <getScheme> in <%s>' % self.__class__.__name__)
        return None

    def getModel(self):
        """
        Get model.
        """
        log_func.warning(u'Not define method <getModel> in <%s>' % self.__class__.__name__)
        return None


class iqDataObject(iqDataObjectProto):
    """
    Data object interface class.
    """
    def getDataObjectRec(self, value):
        """
        Get data object record by value.

        :param value: Reference data code.
        :return: Record dictionary or None if error.
        """
        log_func.warning(u'Not define method <getDataObjectRec> in <%s>' % self.__class__.__name__)
        return None

    def _updateLinkDataDataset(self, dataset, columns=None):
        """
        Update dataset by link object data

        :param dataset: Dataset list.
        :param columns: Column object list.
        :return: Updated dataset.
        """
        try:
            for column in columns:
                if column.isAttributeValue('link'):
                    psp = column.getAttribute('link')
                    link_obj = global_func.getKernel().getObject(psp=psp)
                    if link_obj:
                        for i, record in enumerate(dataset):
                            column_name = column.getName()
                            value = record.get(column_name, None)
                            link_rec = link_obj.getDataObjectRec(value)
                            if isinstance(link_rec, dict):
                                update_rec = {DATA_NAME_DELIMETER.join([column_name, name]): value for name, value in link_rec.items()}
                                dataset[i].update(update_rec)
                            else:
                                log_func.warning(u'Not valid type <%s> object additional data <%s : %s>' % (link_rec.__class__.__name__,
                                                                                                          link_obj.getType(),
                                                                                                          link_obj.getName()))
        except:
            log_func.fatal(u'Error update dataset by link object data')
        return dataset

    def getDataset(self, *args, **kwargs):
        """
        Get dataset.

        :return: Record dictionary list.
        """
        try:
            model = self.getModel()
            if model:
                records = model.query.all()
                dataset = [dict(record) for record in records]
                return dataset
        except:
            log_func.fatal(u'Error get dataset in <%s>' % self.getName())
        return list()

    def setDataset(self, dataset=None, clear=True, *args, **kwargs):
        """
        Set dataset in model.

        :param dataset: Dataset as list of record dictionaries.
        :param clear: Clear data object/model?
        :return: True/False.
        """
        clear_result = self.clear() if clear else True
        if not clear_result:
            return False

        scheme = self.getScheme()
        if not scheme:
            log_func.warning(u'Data object/Model must be defined in the schema')
            return False

        scheme_model = self.getModel()
        if scheme_model is None:
            log_func.warning(u'Data object/Model not defined in <%s>' % self.getName())
            return False

        transaction = scheme.startTransaction()
        try:
            for record in dataset:
                model_rec = {col_name: value for col_name, value in record.items() if hasattr(scheme_model, col_name)}
                new_model_rec = scheme_model(**model_rec)
                transaction.add(new_model_rec)
            transaction.commit()
            scheme.stopTransaction(transaction)
            return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error set dataset to data object/model <%s>' % self.getName())
        scheme.stopTransaction(transaction)
        return False

    def clear(self):
        """
        Clear data object/model.

        :return: True/False.
        """
        scheme = self.getScheme()
        if not scheme:
            log_func.warning(u'Data object/Model must be defined in the schema')
            return False

        scheme_model = self.getModel()
        if scheme_model is None:
            log_func.warning(u'Data object/Model not defined in <%s>' % self.getName())
            return False

        transaction = scheme.startTransaction()
        try:
            transaction.query(scheme_model).delete(synchronize_session=False)
            transaction.commit()
            log_func.info(u'Clear data object <%s>' % self.getName())
            scheme.stopTransaction(transaction)
            return True
        except:
            if transaction:
                transaction.rollback()
            log_func.fatal(u'Error clear data object/model in <%s>' % self.getName())
        scheme.stopTransaction(transaction)
        return False
