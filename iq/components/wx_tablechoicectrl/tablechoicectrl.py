#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control module for selecting a record by field from a table or query.
"""

import wx

from iq.util import log_func
from iq.util import str_func

from .. import data_model
from .. import data_query

__version__ = (0, 0, 0, 1)


class iqTableChoiceCtrlProto(wx.ComboBox):
    """
    The class of the component for selecting a record by a field from a table or query.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # Read only
        style = wx.CB_READONLY
        if 'style' in kwargs:
            style = kwargs['style'] | wx.CB_READONLY
        kwargs['style'] = style

        wx.ComboBox.__init__(self, *args, **kwargs)

        # Data source object
        self._data_source = None

        # Табличные данные
        self._table_data = None

        # Selected code. Determined by the code field
        self._selected_code = None

        # The event handler is bound in the child class
        # self.Bind(wx.EVT_COMBOBOX, self.onComboBox)

    def getCode(self):
        """
        Get selected code. Determined by the code field
        """
        return self._selected_code

    def setCode(self, code):
        """
        Set selected code. Determined by the code field
        """
        if code is None:
            # An empty value can also be set in the control
            self._selected_code = None
            self.SetValue(u'')
            return True

        if self._data_source is not None:
            record = self._data_source.find_record(normal_data=self.getTableData(),
                                                   field_name=self.getCodeField(),
                                                   value=code)
            if record:
                self._selected_code = code
                label = record.get(self.getLabelField(), u'')
                self.SetValue(label)
                return True
        else:
            log_func.warning(u'Data source not defined in control <%s>' % self.getName())
        return False

    getValue = getCode
    setValue = setCode

    def setTableDataSource(self, tab_data_src, **kwargs):
        """
        Set a tabular data source.
        
        :param tab_data_src: Tabular data source object.
        :param kwargs: Extra name arguments.
            Additional parameters for generating executable text
            SQL query for example.
        :return: True/False.
        """
        self._data_source = tab_data_src
        tab_data = self.refreshTableData(self._data_source, **kwargs)
        self.setChoices(tab_data, is_empty=self.getCanEmpty())
        return tab_data is not None

    def refreshTableData(self, tab_data_src=None, **kwargs):
        """
        Refresh tabular data.
        
        :param tab_data_src: Tabular data source object.
        :param kwargs: Extra name arguments.
            Additional parameters for generating executable text
            SQL query for example.
        :return: Updated tabular data.
        """
        if tab_data_src is None:
            tab_data_src = self._data_source
        if isinstance(tab_data_src, data_model.COMPONENT):
            self._table_data = tab_data_src.get_normalized(**kwargs)
            self._table_data = self.setFilter(self._table_data)
            return self._table_data
        elif isinstance(tab_data_src, data_query.COMPONENT):
            self._table_data = tab_data_src.execute(**kwargs)
            self._table_data = self.setFilter(self._table_data)
            return self._table_data
        elif tab_data_src is None:
            log_func.warning(u'Data source table object not defined in control <%s>' % self.getName())
        else:
            log_func.warning(u'Incorrect table datasource type <%s>' % tab_data_src.__class__.__name__)
        return None

    def setFilter(self, table_data=None):
        """
        Additionally, filter records of tabular data.

        :param table_data: Table data.
        :return: Filtered tabular data.
        """
        try:
            table_data = self._setFilter(table_data)
        except:
            log_func.fatal(u'Data filtering error')
        return table_data

    def _setFilter(self, table_data=None):
        """
        Additionally, filter records of tabular data.

        :param table_data: Table data.
        :return: Filtered tabular data.
        """
        if table_data is None:
            table_data = self.getTableData()

        if table_data and self.isFilterFunc():
            # Convert to a list of dictionaries
            recordset = self._data_source.get_recordset_dict(table_data)
            # Filter
            recordset = self.getFilterFunc(RECORDSET=recordset,
                                           RECORDS=recordset)
            # And convert to reverse
            table_data = self._data_source.set_recordset_dict(table_data,
                                                              recordset=recordset)
        return table_data

    def getFilterFunc(self, *arg, **kwarg):
        """
        Get a function for additional filtering of list items.
        """
        log_func.warning(u'Method getFilterFunc not defined in component <%s>' % self.__class__.__name__)
        return list()

    def getTableData(self):
        """
        Get table data.
        """
        return self._table_data

    def getLabelField(self):
        """
        List item label field.
        """
        log_func.warning(u'Method getLabelField not defined in component <%s>' % self.__class__.__name__)
        return u''

    def getCodeField(self):
        """
        List item code field.
        """
        log_func.warning(u'Method getCodeField not defined in component <%s>' % self.__class__.__name__)
        return u''

    def isLabelFunc(self):
        """
        Have you defined a function to get the list item label?

        :return: True/False.
        """
        return False

    def isFilterFunc(self):
        """
        Defined a function for additional filtering of table data?

        :return: True/False.
        """
        return False

    def getLabelFunc(self, *arg, **kwarg):
        """
        Get the function for determining the caption of a list item.
        """
        log_func.warning(u'Method getLabelFunc not defined in component <%s>' % self.__class__.__name__)
        return None

    def getLabel(self, record, table_data=None):
        """
        Function for getting the label of an element.

        :param record: The current record being processed.
        :param table_data: Table data.
        :return: Selection text.
        """
        if table_data is None:
            table_data = self.getTableData()

        label = u''
        label_field_name = self.getLabelField()
        if label_field_name:
            label = record.get(label_field_name, u'')
        else:
            # If the field name is not defined,
            # then the function of defining the label of the element must be defined
            is_label_func = self.isLabelFunc()
            if is_label_func:
                rec_dict = self._data_source.get_record_dict(normal_data=table_data,
                                                             record=record)
                label = self.getLabelFunc(RECORD=rec_dict)
                if label is None:
                    label = u''
            else:
                log_func.warning(u'Method for getting the label of a picklist item in a component is not defined <%s>' % self.__class__.__name__)
        return label

    def setChoices(self, table_data=None, is_empty=True):
        """
        Setting the picklist.

        :param table_data: Table data.
        :param is_empty: Is there an empty string in the list?
        :return: True/False.
        """
        if table_data is None:
            table_data = self.getTableData()
        else:
            self._table_data = table_data

        if table_data is not None:
            # First, remove all elements
            self.Clear()

            # Then fill in
            try:
                if is_empty:
                    self.Append(u'')

                for record in table_data:
                    label = self.getLabel(record, table_data)
                    self.Append(label)

                self.SetSelection(0)
                return True
            except:
                log_func.fatal(u'Error filling select list with data')
        else:
            log_func.warning(u'Not defined table data in control <%s>' % self.getName())
        return False

    def getSelectedRecord(self, table_data=None, selected_idx=-1):
        """
        Get the selected record by the index of the selected item.

        :param table_data: Table data.
        :param selected_idx: The index of the selected item.
        :return: Dictionary of the selected entry, or None on error.
        """
        if selected_idx < 0:
            # Nothing selected
            selected_idx = self.GetSelection() - (1 if self.getCanEmpty() else 0)

        if selected_idx < 0:
            # Nothing selected
            return None

        if table_data is None:
            table_data = self.getTableData()

        if table_data is not None:
            records = table_data
            len_records = len(records)
            if 0 <= selected_idx < len_records:
                try:
                    record = records[selected_idx]
                    return record
                except:
                    log_func.fatal(u'Error retrieving selected record')
            else:
                log_func.warning(u'Incorrect index <%d>. Number of records <%d>' % (selected_idx, len_records))
        else:
            log_func.warning(u'Not defined table data in control <%s>' % self.getName())
        return None

    def getSelectedLabel(self):
        """
        Get selected label.
        :return: Label or empty string if error.
        """
        selected_record = self.getSelectedRecord()
        return self.getLabel(selected_record) if selected_record else u''

    def isSelected(self):
        """
        Something selected?

        :return: True/False
        """
        return self.getSelectedRecord() is not None

    def onComboBox(self, event):
        """
        Element selection handler.
        """
        selected_idx = self.GetSelection() - int(self.getCanEmpty())
        selected_rec = self.getSelectedRecord(selected_idx=selected_idx)
        # log_func.debug(u'Selected record %s' % str(selected_rec))
        if selected_rec is not None:
            code_field = self.getCodeField()
            if not code_field:
                log_func.warning(u'Not define code_field in <%s>' % self.getName())
            self._selected_code = selected_rec.get(code_field, None)
        else:
            self._selected_code = None
        if event:
            event.Skip()

    def getCanEmpty(self):
        """
        Is it possible to choose an empty value?
        """
        log_func.warning(u'Method getCanEmpty not define in component <%s>' % self.__class__.__name__)
        return True
