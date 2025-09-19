#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ListCtrl manager.
"""

import sys
import os.path
import wx

from ...util import log_func
from ...util import file_func
from ...util import res_func
from ...util import lang_func
from ...util import sys_func
from ...util import list_func

from . import wxcolour_func
from . import base_manager
from . import imglib_manager

from .. import stored_manager

from .dlg import wxdlg_func

try:
    import ObjectListView
except ImportError:
    ObjectListView = None
    log_func.error(u'Import error ObjectListView. Install: pip3 install objectlistview')

__version__ = (0, 1, 2, 1)

_ = lang_func.getTranslation().gettext

LISTCTRL_DATA_CACHE_ATTR_NAME = '__listctrl_data'
LISTCTR_COLUMNS_ATTR_NAME = '__listctrl_columns'
LISTCTR_RECORDS_ATTR_NAME = '__listctrl_records'


class iqStoredListCtrlManager(stored_manager.iqStoredManager):
    """
    Manager for storing properties of wxPython ListCtrl objects.
    """
    def genCustomPropertiesFilename(self, listctrl=None):
        """
        Generate custom data stored file name.

        :param listctrl: wx.ListCtrl object.
        :return:
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        profile_path = file_func.getProjectProfilePath()
        return os.path.join(profile_path,
                            self.getClassName() + '_' + str(listctrl.GetId()) + res_func.PICKLE_RESOURCE_FILE_EXT)

    def loadListCtrlProperties(self, listctrl=None, save_filename=None):
        """
        Load custom properties.

        :param listctrl: wx.ListCtrl object.
        :param save_filename: Stored file name.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if save_filename is None:
            save_filename = self.genCustomPropertiesFilename(listctrl=listctrl)

        var_data = self.loadCustomData(save_filename=save_filename)
        if var_data:
            columns = var_data.get('columns', list())
            if columns:
                for i, column in enumerate(columns):
                    hide = column.get('hide', False)
                    if hide:
                        self.hideListCtrlColumn(listctrl=listctrl, column_idx=i)
                    else:
                        self.showListCtrlColumn(listctrl=listctrl, column_idx=i)
            return True
        return False

    def saveListCtrlProperties(self, listctrl=None, save_filename=None):
        """
        Save custom properties.

        :param listctrl: wx.ListCtrl object.
        :param save_filename: Stored file name.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if save_filename is None:
            save_filename = self.genCustomPropertiesFilename(listctrl=listctrl)

        columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME) if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME) else list()
        for i in range(len(columns)):
            columns[i]['hide'] = not self.isListCtrlShownColumn(listctrl=listctrl, column_idx=i)

        res = dict(columns=columns)
        return self.saveCustomData(save_filename=save_filename, save_data=res)


class iqListCtrlManager(imglib_manager.iqImageLibManager,
                        iqStoredListCtrlManager):
    """
    ListCtrl manager.
    """
    def refreshListCtrl(self, listctrl, data_list=None, columns=None):
        """
        Refresh rows wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param columns: Column list.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        self.setListCtrlRows(listctrl, data_list)

    def moveUpListCtrlRow(self, listctrl, data_list=None, idx=wx.NOT_FOUND,
                          columns=None, n_col=None, do_refresh=False):
        """
        Move up row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param idx: Moving row index.
        :param columns: Column list.
        :param n_col: Number column name/index.
        :param do_refresh: Make a complete update control?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if idx != wx.NOT_FOUND and idx > 0:

            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value

            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                self.refreshListCtrl(listctrl, data_list, columns=columns)
            else:
                for i_col, value in enumerate(data_list[idx-1]):
                    listctrl.SetStringItem(idx - 1, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx]):
                    listctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
            listctrl.Select(idx - 1)
            return True
        else:
            log_func.warning(u'Not select moving row')
        return False

    def moveDownListCtrlRow(self, listctrl, data_list=None, idx=wx.NOT_FOUND,
                            columns=None, n_col=None, do_refresh=False):
        """
        Move down row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param idx: Moving row index.
        :param columns: Column list.
        :param n_col: Number column name/index.
        :param do_refresh: Make a complete update control?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value

            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                self.refreshListCtrl(listctrl, data_list, columns=columns)
            else:
                for i_col, value in enumerate(data_list[idx]):
                    listctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx+1]):
                    listctrl.SetStringItem(idx + 1, i_col, value if isinstance(value, str) else str(value))
            listctrl.Select(idx + 1)
            return True
        else:
            log_func.warning(u'Not select moving row')
        return False

    def appendListCtrlColumn(self, listctrl, label=u'', width=-1, align='LEFT', hide=False, has_image=False):
        """
        Append column in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param label: Column label string.
        :param width: Column width.
        :param align: Column text align LEFT/RIGHT/CENTRE.
        :param hide: Hide column?
        :param has_image: Has image?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            i = listctrl.GetColumnCount()
            if width <= 0:
                width = wx.LIST_AUTOSIZE

            info = wx.ListItem()
            info.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
            if has_image:
                info.Mask |= wx.LIST_MASK_IMAGE
            info.Image = -1
            info.Align = 0
            info.Text = label

            col_align = str(align).strip().upper()
            if col_align == 'RIGHT':
                info.Align = wx.LIST_FORMAT_RIGHT
            elif col_align == 'CENTRE':
                info.Align = wx.LIST_FORMAT_CENTRE
            elif col_align == 'CENTER':
                info.Align = wx.LIST_FORMAT_CENTER
            else:
                info.Align = wx.LIST_FORMAT_LEFT
            listctrl.InsertColumn(i, info)
            # listctrl.InsertColumn(i, label, format=col_format, width=width)

            if hide:
                listctrl.SetColumnWidth(i, 0)
            else:
                listctrl.SetColumnWidth(i, width)

            if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME):
                columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME)
                columns.append(dict(label=label, width=width, align=col_align, hide=hide, has_image=has_image))
            return True
        except:
            log_func.fatal(u'Append column in wx.ListCtrl object error')
        return False

    def setListCtrlColumns(self, listctrl=None, cols=()):
        """
        Set columns in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param cols: List of column definitions.
            As tuple ('Column title', width, align)
            or as dictionary:
            {'label': 'Column title',
            'width': Column width,
            'align': Column align,
            'hide': Hide column?,
            'has_image': Has image?}
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        result = True
        listctrl.ClearAll()
        columns = list()
        for col in cols:
            if isinstance(col, dict):
                append_result = self.appendListCtrlColumn(listctrl=listctrl, **col)
                if append_result:
                    columns.append(col)
                result = result and append_result
            elif isinstance(col, (list, tuple)):
                append_result = self.appendListCtrlColumn(listctrl=listctrl, **col)
                if append_result:
                    columns.append(dict(label=col[0],
                                        width=col[1] if len(col) > 1 else -1,
                                        align=col[2] if len(col) > 2 else 'LEFT'))
                result = result and append_result
        # Set internal columns attribute
        setattr(self, LISTCTR_COLUMNS_ATTR_NAME, columns)
        return result

    def setListCtrlColumnsAutoSize(self, listctrl=None):
        """
        Set auto-size columns in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        for i in range(listctrl.GetColumnCount()):
            listctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME):
                columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME)
                columns[i]['width'] = -1
        return True

    def setListCtrlColumnLabel(self, listctrl=None, column_idx=0, label=u''):
        """
        Set column label.

        :param listctrl: wx.ListCtrl object.
        :param column_idx: Column index.
        :param label: Column label.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if 0 <= column_idx < listctrl.GetColumnCount():
            column = listctrl.GetColumn(column_idx)
            column.SetText(label)
            listctrl.SetColumn(column_idx, column)

            if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME):
                columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME)
                column[column_idx]['label'] = label
            return True
        else:
            log_func.warning(u'Not valid column index [%s] ListCtrl object <%s>' % (column_idx, str(listctrl)))
        return False

    def appendListCtrlRow(self, listctrl, row=(),
                          even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                          odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                          auto_select=False):
        """
        Append row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param row: List of rows by fields.
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param auto_select: Automatically select the added row?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if not isinstance(row, (list, tuple)):
            log_func.warning(u'Row typeerror <%s> in wx.ListCtrl object' % type(row))
            return False

        try:
            item = -1

            row = row[:listctrl.GetColumnCount()]
            for i, value in enumerate(row):
                if value is None:
                    value = u''
                elif isinstance(value, (int, float)):
                    value = str(value)
                elif isinstance(value, str):
                    pass
                else:
                    value = str(value)

                if i == 0:
                    item = listctrl.InsertItem(listctrl.GetItemCount(), value)
                else:
                    listctrl.SetItem(item, i, value)

            if item != -1:
                if even_background_colour and not (item & 1):

                    colour = wxcolour_func.getDefaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                    listctrl.SetItemBackgroundColour(item, colour)
                elif odd_background_colour and (item & 1):
                    colour = wxcolour_func.getDefaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                    listctrl.SetItemBackgroundColour(item, colour)

                if auto_select:
                    listctrl.Select(item)
            return True
        except:
            log_func.fatal(u'Append row %s  error in wx.ListCtrl object' % str(row))
        return False

    def delListCtrlRow(self, listctrl=None, item=None):
        """
        Delete row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
            If not defined, the current selected row is taken.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if item is None:
            item = self.getListCtrlSelectedRowIdx(listctrl)
        if 0 <= item < listctrl.GetItemCount():
            listctrl.DeleteItem(item=item)
            return True
        else:
            log_func.warning(u'Not valid row index [%d] on wx.ListCtrl object' % item)
        return False

    def setListCtrlRow(self, listctrl=None, item=-1, row=(),
                       even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                       odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                       keep_pos=False):
        """
        Set row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
        :param row: Row as tuple.
            (value 1, value 2, ..., value N),
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if item == -1:
            log_func.warning(u'The row index to be set is not specified')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log_func.warning(u'Invalid row data type <%s>' % row.__class__.__name__)
            return False

        row_count = listctrl.GetItemCount()
        if 0 > item > row_count:
            log_func.warning(u'Not valid row index [%d] in <%s>' % (item, listctrl.__class__.__name__))
            return False

        cursor_pos = None
        if keep_pos:
            cursor_pos = listctrl.GetFirstSelected()

        for i, item in enumerate(row):
            item_str = str(item)

            listctrl.SetItem(item, i, item_str)
            if even_background_colour and not (item & 1):
                colour = wxcolour_func.getDefaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                listctrl.SetItemBackgroundColour(item, colour)
            elif odd_background_colour and (item & 1):
                colour = wxcolour_func.getDefaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                listctrl.SetItemBackgroundColour(item, colour)
        if cursor_pos not in (None, -1) and cursor_pos < row_count:
            listctrl.Select(cursor_pos)
        return True

    def setListCtrlRows(self, listctrl=None, rows=(),
                        even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                        odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                        keep_pos=False):
        """
        Set rows in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
            [
            (value 1, value 2, ..., value N), ...
            ]
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        result = True
        cursor_pos = None

        if keep_pos:
            cursor_pos = listctrl.GetFirstSelected()

        listctrl.DeleteAllItems()
        for row in rows:
            if isinstance(row, list) or isinstance(row, tuple):
                result = result and self.appendListCtrlRow(listctrl=listctrl, row=row,
                                                           even_background_colour=even_background_colour,
                                                           odd_background_colour=odd_background_colour)
        if cursor_pos not in (None, -1):
            try:
                len_rows = len(rows)
                if cursor_pos < len_rows:
                    listctrl.Select(cursor_pos)
                    listctrl.Focus(cursor_pos)
                elif len_rows:
                    listctrl.Select(len_rows - 1)
                    listctrl.Focus(len_rows - 1)
            except:
                log_func.fatal(u'List item selection recovery error')
        return result

    def getListCtrlRows(self, listctrl=None):
        """
        Get a list of rows as a list of tuples.

        :param listctrl: wx.ListCtrl object.
        :return: Row list.
            [
            (value 1, value 2, ..., value N), ...
            ]
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        rows = list()
        for i_row in range(listctrl.GetItemCount()):
            row = [listctrl.GetItemText(i_row, col=i_col) for i_col in range(listctrl.GetColumnCount())]
            rows.append(row)
        return rows

    def getListCtrlRow(self, listctrl=None, item=-1):
        """
        Get a row by index as a tuple.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
            If None then get selected row.
        :return: Tuple row or None if error.
            (value 1, value 2, ..., value N)
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if 0 > item or item is None:
            item = self.getListCtrlSelectedRowIdx(listctrl_or_event=listctrl)

        row = None
        if 0 <= item:
            row = tuple([listctrl.GetItemText(item, col=i_col) for i_col in range(listctrl.GetColumnCount())])
        return row

    def setListCtrlRowColourExpression(self, listctrl=None, rows=(),
                                       foreground_colour=None,
                                       background_colour=None,
                                       expression=None):
        """
        Set the line color in the list control according to a certain condition.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
        :param foreground_colour: Text color if condition is met.
        :param background_colour: Background color if condition is met.
        :param expression: lambda expression:
            lambda idx, row: ...
            Return True/False.
            If True, then the color setting will be done.
            False - the line does not color.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if expression is None:
            log_func.warning(u'Color condition not defined')
            return False

        if foreground_colour is None and background_colour is None:
            log_func.warning(u'Undefined colors')
            return False

        for i, row in enumerate(rows):
            colorize = expression(i, row)
            if foreground_colour and colorize:
                self.setListCtrlRowForegroundColour(listctrl, i, foreground_colour)
            if background_colour and colorize:
                self.setListCtrlRowBackgroundColour(listctrl, i, background_colour)
        return True

    def setListCtrlRowForegroundColour(self, listctrl=None, item=0, colour=None):
        """
        Set the color of the string text in the list control.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
        :param colour: wx.Colour object.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT)

        try:
            colour = colour if not wxcolour_func.isDefaultColour(colour) else wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT)
            listctrl.SetItemTextColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set row [%s] foreground colour error' % item)
        return False

    def setListCtrlRowBackgroundColour(self, listctrl=None, item=0, colour=None):
        """
        Set the background color of the string in the list control.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
        :param colour: wx.Colour object.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION)

        try:
            colour = colour if not wxcolour_func.isDefaultColour(colour) else wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
            listctrl.SetItemBackgroundColour(item, colour)
            return True
        except:
            log_func.warning(u'Set row [%s] background colour error' % item)
        return False

    def getListCtrlSelectedRowIdx(self, listctrl_or_event):
        """
        Get the index of the selected control.

        :param listctrl_or_event: Object of wx.ListCtrl control or event.
        :return: The index of the selected item or -1 if nothing is selected.
        """
        if isinstance(listctrl_or_event, wx.ListEvent):
            return listctrl_or_event.Index
        elif issubclass(listctrl_or_event.__class__, wx.ListCtrl):
            return listctrl_or_event.GetFirstSelected()
        return -1

    def setListCtrlRecords(self, listctrl, records=(), columns=(),
                           even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                           odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                           keep_pos=False):
        """
        Set rows as records in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param records: Record dictionary list.
            [
            {'name1': value 1, 'name2': value 2, ..., 'nameN': value N), ...
            ]
        :param columns: Column names as record keys:
            ('name1', 'name2', ...)
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            # Convert records to rows
            rows = list_func.dataset2rows(dataset=records, columns=columns)

            result = self.setListCtrlRows(listctrl=listctrl, rows=rows,
                                          even_background_colour=even_background_colour,
                                          odd_background_colour=odd_background_colour,
                                          keep_pos=keep_pos)
            if result:
                setattr(listctrl, LISTCTR_RECORDS_ATTR_NAME, records)
            return result
        except:
            log_func.fatal(u'Error set wx.ListCtrl records')
        return False

    def getListCtrlRecords(self, listctrl):
        """
        Get a list of rows as a list of dictionaries.

        :param listctrl: wx.ListCtrl object.
        :return: Record list.
            [
            {'name1': value 1, 'name2': value 2, ..., 'nameN': value N), ...
            ]
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            records = getattr(listctrl, LISTCTR_RECORDS_ATTR_NAME) if hasattr(listctrl, LISTCTR_RECORDS_ATTR_NAME) else list()
            return records
        except:
            log_func.fatal(u'Error get wx.ListCtrl records')
        return list()

    def getListCtrlRecord(self, listctrl, record_idx=None):
        """
        Get record by index.

        :param listctrl: wx.ListCtrl object.
        :param record_idx: Record index [0...N].
            If None, then there is the currently selected item.
        :return: Record dictionary or None if error.
        """
        records = self.getListCtrlRecords(listctrl=listctrl)
        try:
            if record_idx is None:
                record_idx = self.getListCtrlSelectedRowIdx(listctrl_or_event=listctrl)
            return records[record_idx]
        except IndexError:
            log_func.warning(u'Inncorrect index [%d] ListCtrl records' % record_idx)
        return None

    def getListCtrlSelectedItemRecord(self, listctrl):
        """
        Get selected item record.

        :param listctrl: wx.ListCtrl object.
        :return: Record dictionary or None if error.
        """
        return self.getListCtrlRecord(listctrl=listctrl)

    def getListCtrlSelectedRow(self, listctrl):
        """
        Get the row of the selected control.

        :param listctrl: wx.ListCtrl object.
        :return: Tuple row or None if error.
            (value 1, value 2, ..., value N).
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'
        selected_row_idx = self.getListCtrlSelectedRowIdx(listctrl_or_event=listctrl)
        return self.getListCtrlRow(listctrl=listctrl, item=selected_row_idx)

    def getListCtrlSelectedItemData(self, listctrl):
        """
        Get the data of the selected item.

        :param listctrl: Object of wx.ListCtrl control.
        :return: Data or None if nothing is selected.
        """
        return self.getListCtrlItemData(listctrl=listctrl)

    def selectListCtrlItem(self, listctrl=None, item=-1,
                           is_focus=True, deselect_prev=True):
        """
        Select a list control by index.

        :param listctrl: wx.ListCtrl object.
        :param item: Row index.
        :param is_focus: Automatically move focus to an item?
        :param deselect_prev: Unselect the previous selected item?
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if (0 > item) or (item >= listctrl.GetItemCount()):
            log_func.warning(u'Not valid row index [%d] ListCtrl object <%s>' % (item, listctrl.__class__.__name__))
            return False

        if deselect_prev:
            listctrl.Select(self.getListCtrlSelectedRowIdx(listctrl), 0)
        listctrl.Select(item)
        if is_focus:
            listctrl.Focus(item)
        return True

    def getListCtrlItemCount(self, listctrl):
        """
        Get the number of controls.

        :param listctrl: wx.ListCtrl object.
        :return: The number of list controls.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        return listctrl.GetItemCount()

    def getListCtrlLastItemIdx(self, listctrl):
        """
        The index of the last item in the list.

        :param listctrl: wx.ListCtrl object.
        :return: The index of the last item in the list or
            -1 if there are no items in the list.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        item_count = self.getListCtrlItemCount(listctrl)
        return item_count - 1

    def enableListCtrlCheckBoxes(self, listctrl, enable=True):
        """
        Enable or disable checkboxes for list items.

        :param listctrl: wx.ListCtrl/wx.CheckListBox object.
        :param enable: If True, enable checkboxes, otherwise disable checkboxes.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, (wx.ListCtrl, wx.CheckListBox)), u'ListCtrl/CheckListBox manager type error'
        return listctrl.EnableCheckBoxes(enable=enable)

    def checkListCtrlAllItems(self, listctrl, check=True):
        """
        Set ticks of all list control items.

        :param listctrl: wx.ListCtrl/wx.CheckListBox object.
        :param check: On/Off.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, (wx.ListCtrl, wx.CheckListBox)), u'ListCtrl/CheckListBox manager type error'

        return self.checkListCtrlItems(listctrl, check=check)

    def checkListCtrlItems(self, listctrl, check=True, begin_idx=-1, end_idx=-1):
        """
        Set ticks of all list control items.

        :param listctrl: wx.ListCtrl/wx.CheckListBox object.
        :param check: On/Off.
        :param begin_idx: The index of the first item to be processed.
            If not defined, then the very first element is taken.
        :param end_idx: The index of the last item to be processed.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, (wx.ListCtrl, wx.CheckListBox)), u'ListCtrl/CheckListBox manager type error'

        if begin_idx < 0:
            begin_idx = 0
        if end_idx < 0:
            if isinstance(listctrl, wx.ListCtrl):
                end_idx = listctrl.GetItemCount() - 1
            elif isinstance(listctrl, wx.CheckListBox):
                end_idx = listctrl.GetCount() - 1

        for i in range(begin_idx, end_idx + 1):
            if isinstance(listctrl, wx.ListCtrl):
                listctrl.CheckItem(i, check=check)
            elif isinstance(listctrl, wx.CheckListBox):
                listctrl.Check(i, check=check)

        return True

    def checkListCtrlItem(self, listctrl, check=True, item=-1):
        """
        Set tick list control item.

        :param listctrl: wx.ListCtrl/wx.CheckListBox object.
        :param check: On/Off.
        :param item: Row index.
            If not defined, then the currently selected item is taken.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, (wx.ListCtrl, wx.CheckListBox)), u'ListCtrl/CheckListBox manager type error'

        if item < 0:
            item = self.getListCtrlSelectedRowIdx(listctrl)
        if isinstance(listctrl, wx.ListCtrl):
            listctrl.CheckItem(item, check=check)
        elif isinstance(listctrl, wx.CheckListBox):
            listctrl.Check(item, check=check)

        return True

    def checkListCtrlItemsExpression(self, listctrl=None, rows=(),
                                     expression=None, do_set=False):
        """
        Find and mark a list line by a specific condition.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
        :param expression: lambda expression:
            lambda idx, row: ...
            Return True/False.
            If True, then we consider that the string satisfies the condition.
            False - row does not satisfy.
        :param do_set: Label all items according to the condition.
        :return: List of indices of marked lines.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        check_list = list()

        if not rows:
            return check_list

        for i, row in enumerate(rows):
            checked = expression(i, row)
            if checked:
                check_list.append(i)
            if do_set:
                self.checkListCtrlItems(listctrl=listctrl, check=checked,
                                        begin_idx=i, end_idx=i)
            elif not do_set and checked:
                self.checkListCtrlItem(listctrl=listctrl, check=True, item=i)
        return check_list

    def getListCtrlCheckedItems(self, listctrl, check_selected=False):
        """
        Get the list of indices of the marked list control items.

        :param listctrl: wx.ListCtrl/wx.CheckListBox object.
        :param check_selected: Treat selected list item as marked?
            If yes, then the selected item is considered marked only when
            no other item is marked.
        :return: A list of indices of tagged list controls or None if error.
        """
        assert issubclass(listctrl.__class__, (wx.ListCtrl, wx.CheckListBox)), u'ListCtrl/CheckListBox manager type error'

        try:
            indexes = list()
            if isinstance(listctrl, wx.ListCtrl):
                indexes = [i for i in range(listctrl.GetItemCount()) if listctrl.IsItemChecked(i)]
            elif isinstance(listctrl, wx.CheckListBox):
                indexes = [i for i in range(listctrl.GetCount()) if listctrl.IsChecked(i)]

            if not indexes and check_selected:
                selected = self.getListCtrlSelectedRowIdx(listctrl)
                if selected >= 0:
                    indexes = [selected]
            return indexes
        except:
            log_func.fatal(u'Error in defining indices of marked controls <%s>' % listctrl.__class__.__name__)
        return None

    def getListCtrlCheckedItemRecords(self, listctrl, records=None, check_selected=False):
        """
        Get a list of checked entries for list control items.

        :param listctrl: wx.ListCtrl object.
        :param records: Record list.
        :param check_selected: Treat selected list item as marked?
            If yes, then the selected item is considered marked only when
            no other item is marked.
        :return: List of records of labeled list lontrols or None if error.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            if records is None:
                records = self.getListCtrlRecords(listctrl=listctrl)

            check_records = [records[i] for i in range(listctrl.GetItemCount()) if listctrl.IsChecked(i)]

            if not check_records and check_selected:
                selected = self.getListCtrlSelectedRowIdx(listctrl)
                if selected >= 0:
                    check_records = [records[selected]]
            return check_records
        except:
            log_func.fatal(u'Error determining marked control records <%s>' % listctrl.__class__.__name__)
        return None

    def setListCtrlRowsBackgroundColour(self, listctrl,
                                        even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                                        odd_background_colour=wxcolour_func.DEFAULT_COLOUR):
        """
        Just colorize the background of even and not even lines.

        :param listctrl: wx.ListCtrl object.
        :param even_background_colour: Background color of even lines.
        :param odd_background_colour: Background color of odd lines.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        for item in range(listctrl.GetItemCount()):
            if even_background_colour and not (item & 1):
                colour = wxcolour_func.getDefaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                listctrl.SetItemBackgroundColour(item, colour)
            elif odd_background_colour and (item & 1):
                colour = wxcolour_func.getDefaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                listctrl.SetItemBackgroundColour(item, colour)

    def findListCtrlRowIdxExpression(self, listctrl=None, rows=(),
                                     expression=None, start_row=0, auto_select=False):
        """
        Find the index of a list string by a specific condition.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
        :param expression: lambda expression:
            lambda idx, row: ...
            Return True/False.
            If True, then we consider that the string satisfies the condition.
            False - row does not satisfy.
        :param start_row: Start row.
        :param auto_select: Automatically select a line in the control.
        :return: The index of the row found, or -1 if the row is not found.
            And None if error.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if expression is None:
            log_func.warning(u'Undefined condition for string search')
            return False

        try:
            if start_row >= len(rows):
                start_row = 0

            for i, row in enumerate(rows):
                if i >= start_row:
                    is_found = expression(i, row)
                    if is_found:
                        if auto_select:
                            self.selectListCtrlItem(listctrl, item=i, is_focus=True, deselect_prev=True)
                        return i
            return -1
        except:
            log_func.fatal(u'Find the index of a list string by a specific condition error')
        return None

    def selectListCtrlRowExpression(self, listctrl=None, rows=(), expression=None):
        """
        Find and highlight the list row index by a specific condition.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
        :param expression: lambda expression:
            lambda idx, row: ...
            Return True/False.
            If True, then we consider that the string satisfies the condition.
            False - row does not satisfy.
        :return: The index of the row found, or None if the row is not found.
        """
        return self.findListCtrlRowIdxExpression(listctrl=listctrl, rows=rows, expression=expression)

    def setListCtrlItemImage(self, listctrl=None, item=None, img_name=None):
        """
        Set a icon of a list item.

        :param listctrl: wx.ListCtrl object.
        :param item: List item.
            A list item can be specified by either an index or a wx.ListItem object.
            If None, then there is the currently selected item.
        :param img_name: Icon name.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if not self.isInitImageLib():
            self.initImageLib(assign_ctrl=listctrl)
            listctrl.SetImageList(self.getImageLibImageList(), wx.IMAGE_LIST_SMALL)

        item_idx = -1
        if item is None:
            item_idx = self.getListCtrlSelectedRowIdx(listctrl)
        elif isinstance(item, wx.ListItem):
            item_idx = item.GetId()
        elif isinstance(item, int):
            item_idx = listctrl.GetItem(item).GetId()

        if img_name is None:
            listctrl.SetItemImage(item, None)
        else:
            if item_idx >= 0:
                img_idx = None
                try:
                    img_idx = self.getImageLibImageIdx(img_name)
                    listctrl.SetItemImage(item_idx, img_idx, selImage=-1)
                except:
                    log_func.fatal(u'Icon set error [%s] for item <%s>' % (img_idx, item_idx))
            else:
                log_func.warning(u'Invalid row index [%s]' % str(item_idx))
        return True

    def clearListCtrl(self, listctrl=None):
        """
        Clearing the list control.

        :param listctrl: wx.ListCtrl object.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        listctrl.DeleteAllItems()
        return True

    def setListCtrlItemData(self, listctrl=None, item=None, data=None):
        """
        Set item data.

        :param listctrl: wx.ListCtrl object.
        :param item: List item.
            A list item can be specified by either an index or a wx.ListItem object.
            If None, then there is the currently selected item.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        item_idx = -1
        try:
            if item is None:
                item_idx = self.getListCtrlSelectedRowIdx(listctrl)
            elif isinstance(item, wx.ListItem):
                item_idx = item.GetId()
            elif isinstance(item, int):
                item_idx = item
            else:
                log_func.warning(u'Incorrect ListCtrl item type <%s> : [%s]' % (item.__class__.__name__, str(item)))

            if not hasattr(listctrl, LISTCTRL_DATA_CACHE_ATTR_NAME):
                setattr(listctrl, LISTCTRL_DATA_CACHE_ATTR_NAME, dict())
            data_idx = wx.NewId()
            data_cache = getattr(listctrl, LISTCTRL_DATA_CACHE_ATTR_NAME)
            data_cache[data_idx] = data
            # log_func.debug(u'Item index [%s] Data id [%s]' % (item_idx, data_idx))
            return listctrl.SetItemData(item=item_idx, data=data_idx)
        except:
            log_func.fatal(u'Error set ListCtrl item <%s> data <%s>' % (str(item_idx), str(data)))
        return False

    def getListCtrlItemData(self, listctrl=None, item=None):
        """
        Get item data.

        :param listctrl: wx.ListCtrl object.
        :param item: List item.
            A list item can be specified by either an index or a wx.ListItem object.
            If None, then there is the currently selected item.
        :return: Item data or None if error.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        item_idx = -1
        try:
            if item is None:
                item_idx = self.getListCtrlSelectedRowIdx(listctrl)
            elif isinstance(item, wx.ListItem):
                item_idx = item.GetId()
            elif isinstance(item, int):
                item_idx = item
            else:
                log_func.warning(u'Incorrect ListCtrl item type <%s> : [%s]' % (item.__class__.__name__, str(item)))

            data_cache = getattr(listctrl, LISTCTRL_DATA_CACHE_ATTR_NAME) if hasattr(listctrl, LISTCTRL_DATA_CACHE_ATTR_NAME) else dict()

            if item_idx >= 0:
                data_idx = listctrl.GetItemData(item=item_idx)
                return data_cache.get(data_idx, None)
        except:
            log_func.fatal(u'Error get ListCtrl item <%s> data' % str(item_idx))
        return None

    def showListCtrlColumn(self, listctrl=None, column_idx=0):
        """
        Show column.

        :param listctrl: wx.ListCtrl object.
        :param column_idx: Column index.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            width = -1
            if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME):
                columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME)
                width = columns[column_idx].get('width', -1)
                columns[column_idx]['hide'] = False
            listctrl.SetColumnWidth(column_idx, wx.LIST_AUTOSIZE if width <= -1 else width)
            return True
        except:
            log_func.fatal(u'Error show ListCtrl column [%d]' % column_idx)
        return False

    def hideListCtrlColumn(self, listctrl=None, column_idx=0):
        """
        Hide column.

        :param listctrl: wx.ListCtrl object.
        :param column_idx: Column index.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            listctrl.SetColumnWidth(column_idx, 0)
            if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME):
                columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME)
                columns[column_idx]['hide'] = True
            return True
        except:
            log_func.fatal(u'Error hide ListCtrl column [%d]' % column_idx)
        return False

    def isListCtrlShownColumn(self, listctrl=None, column_idx=0):
        """
        Is shown column?

        :param listctrl: wx.ListCtrl object.
        :param column_idx: Column index.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            return listctrl.GetColumnWidth(column_idx) > 0
        except:
            log_func.fatal(u'Error is shown ListCtrl column [%d]' % column_idx)
        return False

    def selectListCtrlShownColumns(self, listctrl=None, parent=None, auto_save=True, pos=None):
        """
        Select shown columns.

        :param listctrl: wx.ListCtrl object.
        :param parent: Parent window.
        :param auto_save: Auto save properties file.
        :param pos: Dialog position.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if parent is None:
            parent = listctrl

        try:
            columns = getattr(self, LISTCTR_COLUMNS_ATTR_NAME) if hasattr(self, LISTCTR_COLUMNS_ATTR_NAME) else list()
            choices = [(not column.get('hide', False), column.get('label', 'column%d' % i)) for i, column in enumerate(columns)]
            selections = wxdlg_func.getMultiChoiceDlg(parent=parent, title=_('COLUMNS'),
                                                      prompt_text=_('Select shown columns'),
                                                      pos=pos, choices=choices)
            if selections is None:
                return False

            columns = [dict(label=columns[i].get('label', item[1]),
                            width=columns[i].get('width', -1),
                            align=columns[i].get('align', 'LEFT'),
                            hide=not item[0]) for i, item in enumerate(selections)]
            setattr(self, LISTCTR_COLUMNS_ATTR_NAME, columns)

            for i, column in enumerate(columns):
                if column['hide']:
                    self.hideListCtrlColumn(listctrl=listctrl, column_idx=i)
                else:
                    self.showListCtrlColumn(listctrl=listctrl, column_idx=i)

            if auto_save:
                self.saveListCtrlProperties(listctrl=listctrl)
            return True
        except:
            log_func.fatal(u'Error select shown columns')
        return False

    def setObjectListViewSortColumn(self, objectlistview, sort_column, reverse=False):
        """
        Set sort column for ObjectListView widgets.

        :param objectlistview: ObjectListView control.
        :param sort_column: Sort column valueGetter as string or index.
        :param reverse: Reverse sort?
        :return: True/False.
        """
        if ObjectListView:
            assert issubclass(objectlistview.__class__, ObjectListView.ObjectListView), u'ObjectListView widget type error'
        else:
            log_func.warning(u'Not installed ObjectListView. Install: pip3 install objectlistview')
            return False

        if sort_column is not None:
            try:
                column_count = len(objectlistview.columns)
                if isinstance(sort_column, int) and (0 <= sort_column < column_count):
                    sort_column_idx = sort_column
                elif isinstance(sort_column, str):
                    column_names = [column.valueGetter for column in objectlistview.columns]
                    sort_column_idx = column_names.index(sort_column) if sort_column in column_names else -1
                else:
                    log_func.warning(u'Not supported sort column indent for %s' % objectlistview.__class__)
                    return False

                if 0 <= sort_column_idx < column_count:
                    objectlistview.SortBy(sort_column_idx, ascending=not reverse)
                    log_func.debug(u'Set sort column <%s> for ObjectListView control' % sort_column)
                    return True
            except:
                log_func.fatal(u'Error set sort column <%s> for ObjectListView control' % sort_column)
        return False

    def getObjectListViewSortColumn(self, objectlistview):
        """
        Get sort column for ObjectListView widgets as index or valueGetter if it string.

        :param objectlistview: ObjectListView control.
        :return: Index/Name valueGetter sort column or -1.
        """
        if ObjectListView:
            assert issubclass(objectlistview.__class__, ObjectListView.ObjectListView), u'ObjectListView widget type error'
        else:
            log_func.warning(u'Not installed ObjectListView. Install: pip3 install objectlistview')
            return -1

        try:
            sort_column = objectlistview.GetSortColumn()
            sort_column = sort_column.valueGetter if sort_column and isinstance(sort_column.valueGetter, str) else objectlistview.sortColumnIndex
            return sort_column
        except:
            log_func.fatal(u'Error get sort column for ObjectListView control')
        return -1
