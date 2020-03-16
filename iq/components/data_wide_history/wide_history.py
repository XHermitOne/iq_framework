#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data wide history manager.
"""

import sqlalchemy

from ..data_navigator import model_navigator

from ...util import log_func

__version__ = (0, 0, 0, 1)

# Default temporary field name
DEFAULT_DT_FIELDNAME = 'dt'


class iqWideHistoryManager(model_navigator.iqModelNavigatorManager):
    """
    Data wide history manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        model_navigator.iqModelNavigatorManager.__init__(self, model=model)

    def getDTColumnName(self):
        """
        Get datetime column name.
        """
        return 'dt'

    def getFilter(self):
        """
        Additional record filter.
        """
        return None

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

        return [record for record in records if rec_filter(record)]

    def get(self, start_dt, stop_dt, rec_filter=None):
        """
        Get historical data for the specified range.

        :type start_dt: datetime.datetime.
        :param start_dt: The start date-time of the cache range.
        :type stop_dt: datetime.datetime.
        :param stop_dt: The end date-time of the cache range.
        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :return: List of dictionaries for wide format entries of the specified range.
             Or None in case of an error.
        """
        if rec_filter is None:
            rec_filter = self.getFilter()

        model = self.getModel()
        if model:
            dt_field = getattr(model, self.getDTColumnName())
            recordset = self.getModelQuery().filter_by(dt_field.between(start_dt, stop_dt))
            records = [vars(record) for record in recordset]

            if rec_filter:
                return self.filterFuncRecords(rec_filter, records)
            else:
                return records
        else:
            log_func.error(u'The table of storage of historical data in the object is not defined <%s>' % self.getName())
        return list()

    def getValues(self, col_name, start_dt, stop_dt, rec_filter=None):
        """
        Get historical data of a specified range for a specific column.

        :param col_name: Column name.
        :type start_dt: datetime.datetime.
        :param start_dt: The start date-time of the cache range.
        :type stop_dt: datetime.datetime.
        :param stop_dt: The end date-time of the cache range.
        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :return: Record list {'dt': date-time from the specified range,
                              'data': value}.
            Or an empty list in case of an error.
        """
        records = self.get(start_dt, stop_dt, rec_filter=rec_filter)
        dt_fieldname = self.getDTColumnName()
        tag_data = [(rec.get(dt_fieldname, None), rec.get(col_name, 0)) for rec in records]
        # Be sure to sort by time
        tag_data.sort()
        return tag_data

    def getLastRecord(self, rec_filter=None, rec_limit=1):
        """
        Get the latest recorded historical data.

        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :param rec_limit: Limit the number of entries.
        :return: The last registered wide format entry in the form of a dictionary.
             Or an empty dictionary in case of an error.
        """
        if rec_filter is None:
            rec_filter = self.getFilter()

        model = self.getModel()
        # log_func.debug(u'Model <%s>' % str(tab))
        if model:
            dt_fieldname = self.getDTColumnName()
            dt_field = getattr(model, dt_fieldname)
            recordset = self.getModelQuery().order_by(sqlalchemy.desc(dt_field)).limit(rec_limit).all()
            records = [vars(record) for record in recordset]

            if rec_filter:
                records = self.filterFuncRecords(rec_filter, records)

            if records:
                record = dict(records[0])
                if DEFAULT_DT_FIELDNAME not in record:
                    # Set time using a standard key
                    record[DEFAULT_DT_FIELDNAME] = record[dt_fieldname]
                return record
            else:
                log_func.warning(u'No data in historical data table <%s>' % model.getName())
        else:
            log_func.error(u'The table of storage of historical data in the object is not defined <%s>' % self.getName())
        return dict()

    def getLastValue(self, col_name, rec_filter=None, rec_limit=1):
        """
        Get the latest recorded historical data for a specific column.

        :param col_name: Column name.
        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :param rec_limit: Limit the number of entries.
        :return: Dictionary {'dt': date-time of last registration,
                            'data': value}.
            Or an empty dictionary in case of an error.
        """
        last_record = self.getLastRecord(rec_filter, rec_limit)
        if last_record:
            dt_fieldname = self.getDTColumnName()
            tag_data = dict(dt=last_record.get(dt_fieldname),
                            data=last_record.get(col_name))
            return tag_data
        return dict()

    def getFirstRecord(self, rec_filter=None, rec_limit=1):
        """
        Get the first recorded historical data.

        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :param rec_limit: Limit the number of entries.
        :return: The first registered wide format entry in the form of a dictionary.
             Or an empty dictionary in case of an error.
        """
        if rec_filter is None:
            rec_filter = self.getFilter()

        model = self.getModel()
        if model:
            dt_fieldname = self.getDTColumnName()
            dt_field = getattr(model, dt_fieldname)
            recordset = self.getModelQuery().order_by(dt_field).limit(rec_limit).all()
            records = [vars(record) for record in recordset]

            if rec_filter:
                records = self.filterFuncRecords(rec_filter, records)

            if records:
                record = dict(records[0])
                if DEFAULT_DT_FIELDNAME not in record:
                    record[DEFAULT_DT_FIELDNAME] = record[dt_fieldname]
                return record
            else:
                log_func.warning(u'No data in historical data table <%s>' % model.getName())
        else:
            log_func.error(u'The table of storage of historical data in the object is not defined <%s>' % self.getName())
        return dict()

    def getFirstValue(self, col_name, rec_filter=None, rec_limit=1):
        """
        Get the first recorded historical data for a specific column.

        :param col_name: Column name.
        :param rec_filter: Function of additional filter of records.
            If the function is specified by a text block of code:
            As an argument, the function takes the current entry as a dictionary.
            There is a RECORD variable in the namespace that points to the current record.
            The function returns True for the record that falls into the resulting list,
            False - if missed.
        :param rec_limit: Limit the number of entries.
        :return: Dictionary {'dt': date-time of last registration,
                            'data': value}.
            Or an empty dictionary in case of an error.
        """
        first_record = self.getFirstRecord(rec_filter, rec_limit)
        if first_record:
            dt_fieldname = self.getDTColumnName()
            tag_data = dict(dt=first_record.get(dt_fieldname),
                            data=first_record.get(col_name))
            return tag_data
        return dict()
