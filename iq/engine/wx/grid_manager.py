#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Grid manager.
"""

import wx
import wx.grid

from ...util import log_func

from . import wxcolour_func
from . import base_manager
from . import imglib_manager


__version__ = (0, 0, 0, 1)


class iqGridManager(imglib_manager.iqImageLibManager):
    """
    Grid manager.
    """
    def createGrid(self, grid, row_count=1, column_count=1, *args, **kwargs):
        """
        Create wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param row_count: Row number.
        :param column_count: Column number.
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        try:
            return grid.CreateGrid(row_count, column_count, *args, **kwargs)
        except:
            log_func.fatal(u'Error create wx.grid.Grid object')
        return False

    def reCreateGrid(self, grid, row_count=1, column_count=1, clear_grid=True):
        """
        Re create wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param row_count: Row number.
        :param column_count: Column number.
        :param clear_grid: Clear grid?
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        try:
            if clear_grid:
                grid.ClearGrid()

            original_row_count = grid.GetNumberRows()
            original_col_count = grid.GetNumberCols()
            delta_row = row_count - original_row_count
            delta_col = column_count - original_col_count

            if delta_row > 0:
                grid.AppendRows(delta_row)
            elif delta_row < 0:
                grid.DeleteRows(numRows=abs(delta_row))

            if delta_col > 0:
                grid.AppendCols(delta_col)
            elif delta_col < 0:
                grid.DeleteCols(numCols=abs(delta_col))
            return True
        except:
            log_func.fatal(u'Error re-create wx.grid.Grid object')
        return False

    def appendGridColumn(self, grid, label=u'', width=-1, align='LEFT'):
        """
        Append column in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param label: Column label string.
        :param width: Column width.
        :param align: Column text align LEFT/RIGHT/CENTRE.
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        try:
            i = grid.GetNumberCols()
            grid.AppendCols(1)

            grid.SetColLabelValue(i, label)

            if width <= 0:
                width = -1
            grid.SetColSize(i, width)

            col_align = str(align).strip().upper()
            col_attr = wx.grid.GridCellAttr()
            if col_align == 'RIGHT':
                col_attr.SetAlignment(hAlign=wx.ALIGN_RIGHT, vAlign=wx.ALIGN_CENTRE)
            elif col_align == 'CENTRE':
                col_attr.SetAlignment(hAlign=wx.ALIGN_CENTRE, vAlign=wx.ALIGN_CENTRE)
            elif col_align == 'CENTER':
                col_attr.SetAlignment(hAlign=wx.ALIGN_CENTER, vAlign=wx.ALIGN_CENTER)
            else:
                col_attr.SetAlignment(hAlign=wx.ALIGN_LEFT, vAlign=wx.ALIGN_CENTRE)
            grid.SetColAttr(i, col_attr)
            return True
        except:
            log_func.fatal(u'Append column in wx.grid.Grid object error')
        return False

    def setGridColumns(self, grid=None, cols=()):
        """
        Set columns in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param cols: List of column definitions.
            As tuple ('Column title', width, align)
            or as dictionary:
            {'label': 'Column title',
            'width': Column width,
            'align': Column align}
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        try:
            result = self.reCreateGrid(grid=grid,
                                       row_count=grid.GetNumberRows(),
                                       column_count=0)

            for col in cols:
                if isinstance(col, dict):
                    result = result and self.appendGridColumn(grid=grid, **col)
                elif isinstance(col, (list, tuple)):
                    result = result and self.appendGridColumn(grid, *col)
            return result
        except:
            log_func.fatal(u'Error set columns in wx.grid.Grid object')
        return False

    def appendGridRow(self, grid, row=(),
                      even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                      odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                      auto_select=False):
        """
        Append row in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param row: List of rows by fields.
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param auto_select: Automatically select the added row?
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        if not isinstance(row, (list, tuple)):
            log_func.warning(u'Row typeerror <%s> in wx.grid.Grid object' % type(row))
            return False

        try:
            item = -1

            result = grid.AppendRows(1)

            row = row[:grid.GetNumberCols()]
            for i, value in enumerate(row):
                if value is None:
                    value = u''
                elif isinstance(value, (int, float)):
                    value = str(value)
                elif isinstance(value, str):
                    pass
                else:
                    value = str(value)

                grid.SetCellValue(item, i, value)

            if item != -1:
                if even_background_colour and not (item & 1):

                    colour = wxcolour_func.getDefaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                    row_attr = wx.grid.GridCellAttr()
                    row_attr.SetBackgroundColour(colour)
                    grid.SetRowAttr(item, row_attr)
                elif odd_background_colour and (item & 1):
                    colour = wxcolour_func.getDefaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                    row_attr = wx.grid.GridCellAttr()
                    row_attr.SetBackgroundColour(colour)
                    grid.SetRowAttr(item, row_attr)

                if auto_select:
                    grid.SelectRow(item)
            return result
        except:
            log_func.fatal(u'Append row %s  error in wx.grid.Grid object' % str(row))
        return False

    def delGridRow(self, grid=None, item=None):
        """
        Delete row in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param item: Row index.
            If not defined, the current selected row is taken.
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        if item is None:
            item = self.getGridSelectedRowIdx(grid)
        if 0 <= item < grid.GetNumberRows():
            return grid.DeleteRows(pos=item, numRows=1)
        else:
            log_func.warning(u'Not valid row index [%d] on wx.grid.Grid object' % item)
        return False

    def setGridRow(self, grid=None, item=-1, row=(),
                   even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                   odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                   keep_pos=False):
        """
        Set row in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param item: Row index.
        :param row: Row as tuple.
            (value 1, value 2, ..., value N),
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        if item == -1:
            log_func.warning(u'The row index to be set is not specified')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log_func.warning(u'Invalid row data type <%s>' % row.__class__.__name__)
            return False

        row_count = grid.GetNumberRows()
        if 0 > item > row_count:
            log_func.warning(u'Not valid row index [%d] in <%s>' % (item, grid.__class__.__name__))
            return False

        cursor_pos = None
        if keep_pos:
            cursor_pos = self.getGridSelectedRowIdx(grid_or_event=grid)

        for i, item in enumerate(row):
            item_str = str(item)

            grid.SetCellValue(item, i, item_str)
            if even_background_colour and not (item & 1):
                colour = wxcolour_func.getDefaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                row_attr = wx.grid.GridCellAttr()
                row_attr.SetBackgroundColour(colour)
                grid.SetRowAttr(item, row_attr)
            elif odd_background_colour and (item & 1):
                colour = wxcolour_func.getDefaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                row_attr = wx.grid.GridCellAttr()
                row_attr.SetBackgroundColour(colour)
                grid.SetRowAttr(item, row_attr)
        if cursor_pos not in (None, -1) and cursor_pos < row_count:
            grid.SelectRow(cursor_pos)
        return True

    def setGirdRows(self, grid=None, rows=(),
                    even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                    odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                    keep_pos=False):
        """
        Set rows in wx.grid.Grid object.

        :param grid: wx.grid.Grid object.
        :param rows: Row list.
            [
            (value 1, value 2, ..., value N), ...
            ]
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        result = True
        cursor_pos = None

        if keep_pos:
            cursor_pos = self.getGridSelectedRowIdx(grid_or_event=grid)

        self.reCreateGrid(grid=grid, row_count=0, column_count=grid.GetNumberCols())
        for row in rows:
            if isinstance(row, list) or isinstance(row, tuple):
                result = result and self.appendGridRow(grid=grid, row=row,
                                                       even_background_colour=even_background_colour,
                                                       odd_background_colour=odd_background_colour)
        if cursor_pos not in (None, -1):
            try:
                len_rows = len(rows)
                if cursor_pos < len_rows:
                    grid.SelectRow(cursor_pos)
                    # grid.Focus(cursor_pos)
                elif len_rows:
                    grid.SelectRow(len_rows - 1)
                    # listctrl.Focus(len_rows - 1)
            except:
                log_func.fatal(u'Grid row selection recovery error')
        return result

    def getGridRows(self, grid=None):
        """
        Get a list of rows as a list of tuples.

        :param grid: wx.grid.Grid object.
        :return: Row list.
            [
            (value 1, value 2, ..., value N), ...
            ]
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        rows = list()
        row_count = grid.GetNumberRows()
        col_count = grid.GetNumberCols()
        for i_row in range(row_count):
            row = [grid.GetCellValue(row=i_row, col=i_col) for i_col in range(col_count)]
            rows.append(row)
        return rows

    def getGridRow(self, grid=None, item=-1):
        """
        Get a row by index as a tuple.

        :param grid: wx.grid.Grid object.
        :param item: Row index.
            If None then get selected row.
        :return: Tuple row or None if error.
            (value 1, value 2, ..., value N)
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        if 0 > item or item is None:
            item = self.getGridSelectedRowIdx(grid_or_event=grid)

        row = None
        col_count = grid.GetNumberCols()
        if 0 <= item:
            row = tuple([grid.GetCellValue(row=item, col=i_col) for i_col in range(col_count)])
        return row

    def getGridSelectedRowIdx(self, grid_or_event):
        """
        Get the index of the selected control.

        :param grid_or_event: Object of wx.grid.Grid control or event.
        :return: The index of the selected item or -1 if nothing is selected.
        """
        if isinstance(grid_or_event, wx.grid.GridEvent):
            return grid_or_event.GetRow()
        elif issubclass(grid_or_event.__class__, wx.grid.Grid):
            selected_rows = grid_or_event.GetSelectedRows()
            if selected_rows:
                return selected_rows[0]
        return -1

    def selectGridCell(self, grid=None, row=-1, column=-1,
                       is_focus=True, deselect_prev=True):
        """
        Select grid cell by position.

        :param grid: wx.grid.Grid object.
        :param row: Row index.
        :param column: Column index.
        :param is_focus: Automatically move focus to an item?
        :param deselect_prev: Unselect the previous selected item?
        :return: True/False.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        if (0 > row) or (row >= grid.GetNumberRows()):
            log_func.warning(u'Not valid row index [%d] Grid object <%s>' % (row, grid.__class__.__name__))
            return False

        # if deselect_prev:
        #     grid.Select(self.getListCtrlSelectedRowIdx(listctrl), 0)

        grid.SetGridCursor(row=row, col=column)

        # if is_focus:
        #     listctrl.Focus(item)
        return True

    def getGridRowCount(self, grid):
        """
        Get the number of rows.

        :param grid: wx.grid.Grid object.
        :return: The number of list controls.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'
        return grid.GetNumberRows()

    def getGridLastRowIdx(self, grid):
        """
        The index of the last row in the grid.

        :param grid: wx.grid.Grid object.
        :return: The index of the last item in the list or
            -1 if there are no items in the list.
        """
        assert issubclass(grid.__class__, wx.grid.Grid), u'Grid manager type error'

        row_count = self.getGridRowCount(grid)
        return row_count - 1
