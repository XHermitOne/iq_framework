#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data object interface class.
"""

from iq.util import log_func
from iq.util import global_func

__version__ = (0, 0, 0, 1)

DATA_NAME_DELIMETER = '.'


class iqDataObject(object):
    """
    Data object interface class.
    """
    def getDataset(self):
        """
        Get dataset.

        :return: Record dictionary list.
        """
        log_func.warning(u'Not define method <getDataset> in <%s>' % self.__class__.__name__)
        return list()

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
                    link_obj = global_func.getKernel().createByPsp(psp=psp)
                    if link_obj:
                        for i, record in enumerate(dataset):
                            column_name = column.getName()
                            value = record.get(column_name, None)
                            link_rec = link_obj.getDataObjectRec(value)
                            if isinstance(link_rec, dict):
                                update_rec = dict([(DATA_NAME_DELIMETER.join([column_name,
                                                                              name]),
                                                    value) for name, value in link_rec.items()])
                                dataset[i].update(update_rec)
                            else:
                                log_func.error(u'Not valid type <%s> object additional data <%s : %s>' % (link_rec.__class__.__name__,
                                                                                                          link_obj.getType(),
                                                                                                          link_obj.getName()))
        except:
            log_func.fatal(u'Error update dataset by link object data')
        return dataset
