#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pandas DataFrame to Spreadsheet convert manager.
"""

import os.path
import pandas

from . import v_spreadsheet

from ...util import log_func
from ...util import file_func
from ...util import xlsx2ods

__version__ = (0, 0, 0, 1)


class iqDataFrame2SpreadsheetManager(v_spreadsheet.iqVSpreadsheet):
    """
    Pandas DataFrame to Spreadsheet convert manager.
    """
    def __init__(self, dataframe=None, *args, **kwargs):
        """
        Constructor.

        :param dataframe: Pandas DataFrame object.
        """
        v_spreadsheet.iqVSpreadsheet.__init__(self, *args, **kwargs)

        self._dataframe = dataframe
        if self._dataframe is None:
            self._dataframe = pandas.DataFrame()
        else:
            self.importDataFrame(dataframe)

    def getDataFrame(self):
        """
        Get pandas DataFrame object.
        """
        return self._dataframe

    def importDataFrame(self, dataframe=None, auto_delete=True):
        """
        Import DataFrame object as spreadsheet.

        :param dataframe: DataFrame object.
        :param auto_delete: Auto delete result file?
        :return: Spreadsheet data.
        """
        if dataframe is None:
            dataframe = self._dataframe

        try:
            return self._importDataFrame(dataframe=dataframe, auto_delete=auto_delete)
        except:
            log_func.fatal(u'Error import pandas DataFrame object')
        return None

    def _importDataFrame(self, dataframe=None, auto_delete=True):
        """
        Import DataFrame object as spreadsheet.

        :param dataframe: DataFrame object.
        :param auto_delete: Auto delete result file?
        :return: Spreadsheet data or None if error.
        """
        assert issubclass(dataframe.__class__, pandas.DataFrame), u'Pandas DataFrame type error'

        result = None

        tmp_xlsx_filename = file_func.getPrjProfileTempFilename() + xlsx2ods.XLSX_FILENAME_EXT
        dataframe.to_excel(tmp_xlsx_filename)

        tmp_ods_filename = file_func.setFilenameExt(tmp_xlsx_filename, xlsx2ods.ODS_FILENAME_EXT)
        if xlsx2ods.xlsx2ods(tmp_xlsx_filename, tmp_ods_filename):
            result = self.loadODS(tmp_ods_filename)

        if auto_delete:
            file_func.deleteFile(tmp_xlsx_filename)
            file_func.deleteFile(tmp_ods_filename)
        return result
