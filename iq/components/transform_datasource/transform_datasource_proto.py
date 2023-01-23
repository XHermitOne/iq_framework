#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transformation table data component prototype class.
"""

import pandas

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqTransformDataSourceProto(object):
    """
    Transformation table data component prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self._dataframe = None

    def getDataFrame(self):
        """
        Get DataFrame object.

        :return: Pandas DataFrame object or None if object not defined.
        """
        return self._dataframe

    getDataset = getDataFrame

    def importData(self, data=None):
        """
        Import table data to DataFrame object.

        :param data: Table data as list of dictionary.
        :return: True/False.
        """
        if data is None:
            data = tuple()

        assert isinstance(data, (list, tuple)), u'Type error import data in component <%s>' % self.__class__.__name__

        try:
            self._dataframe = pandas.DataFrame(data)
            # log_func.debug(u'Transformed DataFrame:')
            # log_func.debug(str(self._dataframe))
            return True
        except:
            log_func.fatal(u'Error import data in <%s>' % self.getName())
            self._dataframe = None
        return False

    def exportDataToValues(self, dataframe=None):
        """
        Export DataFrame object to table data as dict_values.

        :param dataframe: DataFrame object.
            If not defined then get current DataFrame object.
        :return: Table data as dict_values or None if error.
        """
        if dataframe is None:
            dataframe = self.getDataFrame()

        if isinstance(dataframe, pandas.DataFrame):
            try:
                # Indexes as column ------V
                dataframe = dataframe.reset_index()
                return dataframe.T.to_dict().values()
            except:
                log_func.fatal(u'Export error DataFrame in <%s>' % self.getName())
        else:
            log_func.warning(u'Not define DataFrame object for export')
        return None

    def exportData(self, dataframe=None):
        """
        Export DataFrame object to table data as list of dictionary.

        :param dataframe: DataFrame object.
            If not defined then get current DataFrame object.
        :return: Table data as list obj dictionary.
        """
        if dataframe is None:
            dataframe = self.getDataFrame()

        values = self.exportDataToValues(dataframe=dataframe)
        if values is not None:
            return list(values)
        return None

    def transform(self, dataframe=None):
        """
        Transform DataFrame object.

        :param dataframe: DataFrame object.
            If not defined then get current DataFrame object.
        :return: Transformed DataFrame object or None if error.
        """
        log_func.warning(u'not defined <transform> method in component <%s>' % self.__class__.__name__)
        return None
