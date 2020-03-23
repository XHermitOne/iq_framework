#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data wide history component.
"""

from ...components import data_navigator

from . import spc
from . import wide_history
from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqDataWideHistory(wide_history.iqWideHistoryManager, data_navigator.COMPONENT):
    """
    Data wide history component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        data_navigator.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        wide_history.iqWideHistoryManager.__init__(self, *args, **kwargs)

    def getDTColumnName(self):
        """
        Get datetime column name.
        """
        return self.getAttribute('dt_column')

    def getFilter(self):
        """
        Additional record filter.
        """
        return self.getAttribute('filter')

    def filterFuncRecords(self, rec_filter, records):
        """
        Filter records by filter function.

        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :return: Filtered list of entries.
        """
        if not rec_filter:
            # If no filter is specified, then return the original list of records
            return records

        if isinstance(rec_filter, str):
            context = self.getContext()
            if context:
                context.set(RECORDS=records)
            return exec_func.execTxtFunction(rec_filter, context=context)

        return [record for record in records if rec_filter(record)]


COMPONENT = iqDataWideHistory
