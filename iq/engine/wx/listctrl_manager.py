#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ListCtrl manager.
"""

import sys
import wx

from ...util import log_func

from . import wxcolour_func
from . import base_manager
from . import imglib_manager

__version__ = (0, 0, 0, 1)


class iqListCtrlManager(imglib_manager.iqImageLibManager):
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

    def appendListCtrlColumn(self, listctrl, label=u'', width=-1, align='LEFT'):
        """
        Append column in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param label: Column label string.
        :param width: Column width.
        :param align: Column text align LEFT/RIGHT/CENTRE.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            i = listctrl.GetColumnCount()
            if width <= 0:
                width = wx.LIST_AUTOSIZE

            col_align = str(align).strip().upper()
            if col_align == 'RIGHT':
                col_format = wx.LIST_FORMAT_RIGHT
            elif col_align == 'CENTRE':
                col_format = wx.LIST_FORMAT_CENTRE
            elif col_align == 'CENTER':
                col_format = wx.LIST_FORMAT_CENTER
            else:
                col_format = wx.LIST_FORMAT_LEFT
            listctrl.InsertColumn(i, label, width=width, format=col_format)
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
            'align': Column align}
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        result = True
        listctrl.ClearAll()
        for col in cols:
            if isinstance(col, dict):
                result = result and self.appendListCtrlColumn(listctrl=listctrl, **col)
            elif isinstance(col, (list, tuple)):
                result = result and self.appendListCtrlColumn(listctrl, *col)
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
            return True
        else:
            log_func.error(u'Not valid column index [%s] ListCtrl object <%s>' % (column_idx, str(listctrl)))
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
            log_func.error(u'Row typeerror <%s> in wx.ListCtrl object' % type(row))
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
                    item = listctrl.InsertItem(sys.maxsize, value)
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
            log_func.error(u'The row index to be set is not specified')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log_func.error(u'Invalid row data type <%s>' % row.__class__.__name__)
            return False

        row_count = listctrl.GetItemCount()
        if 0 > item > row_count:
            log_func.error(u'Not valid row index [%d] in <%s>' % (item, listctrl.__class__.__name__))
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
            log_func.warning(u'Set row [%s] foreground colour error' % item)
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
        elif issubclass(listctrl_or_event, wx.ListCtrl):
            return listctrl_or_event.GetFirstSelected()
        return -1

    def selectListCtrlItem(self, listctrl=None, item=-1,
                           is_focus=True, deselect_prev=False):
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

    def checkListCtrlAllItems(self, listctrl, check=True):
        """
        Set ticks of all list control items.

        :param listctrl: wx.ListCtrl object.
        :param check: On/Off.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        return self.checkListCtrlItems(listctrl, check=check)

    def checkListCtrlItems(self, listctrl, check=True, begin_idx=-1, end_idx=-1):
        """
        Set ticks of all list control items.

        :param listctrl: wx.ListCtrl object.
        :param check: On/Off.
        :param begin_idx: The index of the first item to be processed.
            If not defined, then the very first element is taken.
        :param end_idx: The index of the last item to be processed.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if begin_idx < 0:
            begin_idx = 0
        if end_idx < 0:
            end_idx = listctrl.GetItemCount() - 1

        for i in range(begin_idx, end_idx + 1):
            listctrl.CheckItem(i, check=check)
        return True

    def checkListCtrlItem(self, listctrl, check=True, item=-1):
        """
        Set tick list control item.

        :param listctrl: wx.ListCtrl object.
        :param check: On/Off.
        :param item: Row index.
            If not defined, then the currently selected item is taken.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if item < 0:
            item = self.getListCtrlSelectedRowIdx(listctrl)
        listctrl.CheckItem(item, check=check)
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

        :param listctrl: wx.ListCtrl object.
        :param check_selected: Treat selected list item as marked?
            If yes, then the selected item is considered marked only when
            no other item is marked.
        :return: A list of indices of tagged list controls or None if error.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            indexes = [i for i in range(listctrl.GetItemCount()) if listctrl.IsChecked(i)]

            if not indexes and check_selected:
                selected = self.getListCtrlSelectedRowIdx(listctrl)
                if selected >= 0:
                    indexes = [selected]
            return indexes
        except:
            log_func.fatal(u'Error in defining indices of marked controls <%s>' % listctrl.__class__.__name__)
        return None

    def getListCtrlCheckedItemRecords(self, listctrl, records, check_selected=False):
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
                                     expression=None, auto_select=False):
        """
        Find the index of a list string by a specific condition.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
        :param expression: lambda expression:
            lambda idx, row: ...
            Return True/False.
            If True, then we consider that the string satisfies the condition.
            False - row does not satisfy.
        :param auto_select: Automatically select a line in the control.
        :return: The index of the row found, or None if the row is not found.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        if expression is None:
            log_func.warning(u'Undefined condition for string search')
            return False

        try:
            for i, row in enumerate(rows):
                is_found = expression(i, row)
                if is_found:
                    if auto_select:
                        self.selectListCtrlItem(listctrl, item=i, is_focus=True, deselect_prev=True)
                    return i
            return True
        except:
            log_func.fatal(u'Find the index of a list string by a specific condition error')
        return False

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

    def setListCtrlItemImage(self, listctrl=None, item=None, image=None):
        """
        Set a icon of a list item.

        :param listctrl: wx.ListCtrl object.
        :param item: List item.
            A list item can be specified by either an index or a wx.ListItem object.
            If None, then there is the currently selected item.
        :param image: Icon name.
        :return: True/False.
        """
        assert issubclass(listctrl.__class__, wx.ListCtrl), u'ListCtrl manager type error'

        item_idx = -1
        if item is None:
            item_idx = self.getListCtrlSelectedRowIdx(listctrl)
            item = listctrl.GetItem(item_idx)
        elif isinstance(item, wx.ListItem):
            item_idx = item.GetId()
        elif isinstance(item, int):
            item_idx = item
            item = listctrl.GetItem(item_idx)

        if image is None:
            listctrl.SetItemImage(item, None)
        else:
            if item_idx >= 0:
                img_idx = None
                try:
                    img_idx = self.getImageLibImageBmp(image)
                    listctrl.SetItemImage(item_idx, img_idx, selImage=wx.TreeItemIcon_Normal)
                except:
                    log_func.fatal(u'Icon set error [%d] for item <%s>' % (img_idx, item))
            else:
                log_func.error(u'Invalid row index [%s]' % str(item_idx))
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
