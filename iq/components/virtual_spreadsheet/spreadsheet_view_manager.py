#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SpreadSheet struct view manager by wx.Grid control.
"""

import wx
import wx.grid

from ...util import log_func

from . import v_spreadsheet

# from ...engine.wx import panel_manager
from ...engine.wx import wxobj_func
from ...engine.wx import wxcolour_func


__version__ = (0, 0, 0, 1)


class iqSpreadSheetViewManager(v_spreadsheet.iqVSpreadsheet):
    """
    SpreadSheet struct view manager by wx.Grid control.
    """
    def __init__(self, grid=None, *args, **kwargs):
        """
        Constructor.

        :param grid: View wx.Grid control object.
        """
        v_spreadsheet.iqVSpreadsheet.__init__(self, *args, **kwargs)

        self._spreadsheet_grid = grid

    def getSpreadSheetGrid(self):
        """
        Get spreadsheet wx.Grid control.
        """
        return self._spreadsheet_grid

    def setSpreadSheetGrid(self, grid=None):
        """
        Set spreadsheet wx.Grid control.

        :param grid: Spreadsheet wx.Grid control object.
        """
        self._spreadsheet_grid = grid

    def viewSpreadSheet(self, spreadsheet_data, auto_size=True):
        """
        View SpreadSheet struct in grid control.

        :param spreadsheet_data: SpreadSheet struct data.
        :param auto_size: Auto size grid control?
        :return: True/False.
        """
        # log.debug(u'View SpreadSheet %s' % str(spreadsheet_data))
        if self._spreadsheet_grid is None:
            log_func.warning(u'Not define wx.Grid control for view SpreadSheet struct')
            return False
        if wxobj_func.isWxDeadObject(self._spreadsheet_grid):
            log_func.warning(u'wx.Grid control for view SpreadSheet struct is dead')
            return False

        try:
            result = self._viewSpreadSheet(spreadsheet_data)

            if auto_size:
                grid = self.getSpreadSheetGrid()
                if grid:
                    grid.AutoSize()
            return result
        except:
            log_func.fatal(u'Error view SpreadSheet struct in grid control')
        return False

    def _viewSpreadSheet(self, spreadsheet_data, worksheet_name=None):
        """
        View SpreadSheet struct in grid control.

        :param spreadsheet_data: SpreadSheet struct data.
        :param worksheet_name: Woksheet name.
            If not specified, then the first sheet is taken.
        :return: True/False.
        """
        self.setSpreadSheetData(spreadsheet_data)
        workbook = self.getWorkbook()
        if not workbook:
            log_func.warning(u'SpreadSheet. Incorrect workbook struct')
            return False

        worksheet = workbook.getWorksheetIdx() if not worksheet_name else workbook.findWorksheet(worksheet_name)
        if not worksheet:
            log_func.warning(u'SpreadSheet. Incorrect worksheet <%s> struct' % str(worksheet_name))
            return False

        table = worksheet.getTable()
        if not table:
            log_func.warning(u'SpreadSheet. Incorrect table struct')
            return False

        # Set grid size
        column_count = table.getColumnCount()
        row_count = table.getRowCount()
        self.reCreateGrid(self._spreadsheet_grid, row_count, column_count)

        for i_row in range(row_count):
            # row = table.getRow(i_row)
            for i_col in range(column_count):
                # Addressing starts with 1---V
                cell = table.getCell(row=i_row + 1, col=i_col + 1)
                self._setGridCellStyle(i_row, i_col, cell.getStyle())
                # cell = row.getCellIdx(i_col)
                if cell:
                    value = cell.getValue()
                    if value:
                        row_idx, col_idx, merge_down, merge_accross = cell.getRegion()
                        if merge_down >= 1 or merge_accross >= 1:
                            self._spreadsheet_grid.SetCellSize(row_idx - 1, col_idx - 1,
                                                               merge_down + 1, merge_accross + 1)
                        self._spreadsheet_grid.SetCellValue(row_idx - 1, col_idx - 1, str(value))
        return True

    def _setGridCellStyle(self, row, col, style):
        """
        Set grid cell style attribute.

        :param row: Cell row.
        :param col: Cell column.
        :param style: Style object.
        :return: True/False.
        """
        if style:
            # Font
            font_dict = style.getFontAttrs()
            if font_dict:
                cell_attr = wx.grid.GridCellAttr()
                if font_dict.get('Bold', None) in (True, 1, '1'):
                    # Set bold
                    font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
                    cell_attr.SetFont(font)
                self._spreadsheet_grid.SetAttr(row, col, cell_attr)

                text_color = font_dict.get('Color', None)
                if text_color:
                    wx_colour = wxcolour_func.StrRGB2wxColour(text_color)
                    self._spreadsheet_grid.SetCellTextColour(row, col, wx_colour)

            # Interior
            interior_dict = style.getInteriorAttrs()
            if interior_dict:
                rgb_color = interior_dict.get('Color', None)
                # log.debug(u'RGB %s' % str(rgb_color))
                if rgb_color:
                    # Установить цвет фона
                    wx_colour = wxcolour_func.StrRGB2wxColour(rgb_color)
                    # log.debug(u'Set cell <%d x %d> colour %s' % (row, col, str(wx_colour)))
                    self._spreadsheet_grid.SetCellBackgroundColour(row, col, wx_colour)
            return True
        else:
            log_func.warning(u'Cell style <%d x %d> not defined' % (row, col))
        return False

    def reCreateGrid(self, grid=None, row_count=5, col_count=5):
        """
        Re create grid object with new rows and columns

        :param grid: wx.Grid control object.
        :param row_count: Number of row.
        :param col_count: Number of columns.
        :return: True/False.
        """
        if grid is None:
            grid = self._spreadsheet_grid

        if not isinstance(grid, wx.grid.Grid):
            log_func.warning(u'Error grid control type <%s>' % grid.__class__.__name__)
            return False
        try:
            prev_row_count = grid.GetNumberRows()
            prev_col_count = grid.GetNumberCols()
            delta_row_count = row_count - prev_row_count
            delta_col_count = col_count - prev_col_count

            # Clear all data
            grid.ClearGrid()

            if delta_col_count > 0:
                grid.AppendCols(delta_col_count)
            else:
                grid.DeleteCols(prev_col_count + delta_col_count - 1, -delta_col_count)
            if delta_row_count > 0:
                grid.AppendRows(delta_row_count)
            else:
                grid.DeleteRows(prev_row_count + delta_row_count - 1, -delta_row_count)
            # self.Layout()
            return True
        except:
            log_func.fatal(u'Error recreate grid object')
        return False
