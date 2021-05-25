#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pivot table manager.
"""

import numpy
import pandas

from ...util import log_func
from ...util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

AGGREGATE_FUNCTION_NAMES = ('sum', 'min_value', 'max_value', 'mean')

TOTAL_LABEL = _(u'TOTAL:')
TOTAL_GROUP_LABEL = _(u'Total')


class iqPivotDataFrameManager(object):
    """
    Pivot table manager.
    """
    def __init__(self):
        """
        Constructor.
        """
        # Current pivot table as pandas.DataFrame
        self._cur_pivot_dataframe = None

    def getPivotDataFrame(self):
        """
        Get current pivot table as pandas.DataFrame.
        """
        return self._cur_pivot_dataframe

    def createDataFrame(self, rows, column_names):
        """
        Create pivot table dataframe.

        :param rows: Row list.
            List of strings - a list of lists according to the list of column names.
        :param column_names: Column names.
        :return: pandas.DataFrame.
        """
        self._cur_pivot_dataframe = None

        try:
            data_rows = [pandas.Series(row) for row in rows]
            self._cur_pivot_dataframe = pandas.DataFrame(data_rows)
            # Set column names
            if data_rows:
                self._cur_pivot_dataframe.columns = column_names
        except:
            log_func.fatal(u'Error create pivot table dataframe. Columns: %s' % str(column_names))

        return self._cur_pivot_dataframe

    def setPivotDimensions(self, row_dimension, col_dimension):
        """
        Set row and column dimensions in a pivot table.

        :param row_dimension: Measurement / measurements to be displayed line by line.
            Specified by a list of column names.
        :param col_dimension: Measurement / Measurements to be displayed column by column.
            Specified by a list of column names.
        :return: Current pandas.DataFrame object.
        """
        if not row_dimension:
            row_dimension = list()
        if not col_dimension:
            col_dimension = list()

        dimensions = list(row_dimension) + list(col_dimension)
        # Setting dimension indices
        self._cur_pivot_dataframe = self._cur_pivot_dataframe.set_index(dimensions)
        if col_dimension:
            # Transferring column measurements
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.unstack(col_dimension)
        return self._cur_pivot_dataframe

    def fillNaNValue(self, value=0):
        """
        Replace undefined NaN values in the pivot table with the specified value.

        :param value: Replacement value.
        :return: Current pandas.DataFrame object.
        """
        self._cur_pivot_dataframe = self._cur_pivot_dataframe.fillna(value=value)
        return self._cur_pivot_dataframe

    def groupByDimensions(self, row_dimension):
        """
        Grouping rows by dimensions.

        :param row_dimension: Measurement / measurements to be displayed line by line.
            Specified by a list of column names.
        :return: Current pandas.DataFrame object.
        """
        if (isinstance(row_dimension, tuple) or isinstance(row_dimension, list)) and len(row_dimension) == 1:
            row_dimension = row_dimension[0]

        self._cur_pivot_dataframe = self._cur_pivot_dataframe.groupby(row_dimension)
        return self._cur_pivot_dataframe

    def aggregateDimensions(self, aggregate_function_name='sum'):
        """
        Perform group aggregation.

        :param aggregate_function_name: The name of the aggregation function.
        :return: Current pandas.DataFrame object.
        """
        if aggregate_function_name == 'sum':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.sum)
        elif aggregate_function_name == 'min_value':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.min)
        elif aggregate_function_name == 'max_value':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.max)
        elif aggregate_function_name == 'mean':
            self._cur_pivot_dataframe = self._cur_pivot_dataframe.aggregate(numpy.mean)
        return self._cur_pivot_dataframe

    def getPivotShape(self, dataframe=None):
        """
        The size of the pivot table data.

        :param dataframe: Pivot table pandas.DataFrame object.
            If not defined, then the internal one is taken.
        :return: Number of rows, number of columns.
        """
        if dataframe is None:
            dataframe = self._cur_pivot_dataframe
        return dataframe.shape

    def getPivotTableSize(self, dataframe=None):
        """
        The size of the pivot table.

        :param dataframe: Pivot table pandas.DataFrame object.
            If not defined, then the internal one is taken.
        :return: Number of rows, number of columns.
        """
        if dataframe is None:
            dataframe = self._cur_pivot_dataframe

        row_count, col_count = self.getPivotShape(dataframe)
        # Posting a row of labels for row level columns---V
        row_level_count = 1 if any(dataframe.index.names) else 0

        row_count = row_count + dataframe.columns.nlevels + row_level_count
        col_count = col_count + dataframe.index.nlevels
        return row_count, col_count

    def totalPivotTable(self, dataframe):
        """
        Calculation of the grand totals of the pivot table by rows.

        :param dataframe: Pivot table pandas.DataFrame object.
        :return: pandas.DataFrame object.
        """
        total = dataframe.agg(numpy.sum)

        # Index for new row of totals
        row_idx = [u''] * dataframe.index.nlevels
        if row_idx:
            row_idx[0] = TOTAL_LABEL
            # To determine the index of the newline
            # a tuple is used, or if level 1, then the string
            row_idx = tuple(row_idx) if len(row_idx) > 1 else row_idx[0]
            dataframe.loc[row_idx] = total
        return dataframe

    def totalGroupPivotTable(self, dataframe):
        """
        Calculation of totals by groups of the pivot table by rows.

        :param dataframe: Pivot table pandas.DataFrame object.
        :return: pandas.DataFrame object.
        """
        try:
            levels = dataframe.index.names
            log_func.debug(u'Levels %s' % str(levels))

            dataframe = pandas.concat([
                dataframe.assign(
                    **{x: '' for x in levels}
                ).groupby(level=levels[:-1]).sum() for i_level in range(len(levels)-1)
            ])
            # Remove duplicate entries
            dataframe = dataframe.drop_duplicates()

            log_func.debug(u'Calculation of group totals by values:\n%s' % str(dataframe))
        except:
            log_func.fatal(u'Error calculating totals for pivot table groups :\n%s\n' % str(dataframe))

        return dataframe
