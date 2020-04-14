#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

from . import v_prototype
from . import v_cell

__version__ = (0, 0, 0, 1)

RANGE_ROW_IDX = 0
RANGE_COL_IDX = 1
RANGE_HEIGHT_IDX = 2
RANGE_WIDTH_IDX = 3


class iqVRange(v_prototype.iqVPrototype):
    """
    Range of cells. Required for group operations on cells.
    """
    def __init__(self, parent, row=0, col=0, height=0, width=0, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)

        self.row = 1
        self.col = 1
        self.height = 1
        self.width = 1
        self._height_1 = 0
        self._width_1 = 0
        self._address = []
        self.setAddress(row, col, height, width)

        # Current offset for relative cell indexing function
        self._cur_span_offset = (0, 0)

        # Basis row
        self._basis_row = None

    def setAddress(self, row, column, height, width):
        """
        Set address.
        """
        self.row = max(row, 1)
        self.col = max(column, 1)
        self.height = max(height, 1)
        self.width = max(width, 1)
        self._height_1 = self.height-1
        self._width_1 = self.width-1
        self._address = [self.row, self.col, self.height, self.width]
        return self._address

    def setValues(self, values=None):
        """
        Set value in range.
        """
        for i_row, row in enumerate(values):
            if i_row < self.height:
                for i_col, col in enumerate(row):
                    if i_col < self.width:
                        cell = self._parent.getCell(self.row+i_row, self.col+i_col)
                        value = col
                        cell.setValue(value)

    def setStyle(self, alignment=None,
                 borders=None, font=None, interior=None,
                 number_format=None):
        """
        Set style in range.
        """
        my_workbook = self.getParentByName('Workbook')
        find_style = my_workbook.getStyles().findStyle(alignment, borders, font, interior, number_format)
        if find_style is None:
            style = my_workbook.getStyles().createStyle()
            style.setAttrs(alignment, borders, font, interior, number_format)
        else:
            style = find_style

        for i_row in range(self.height):
            for i_col in range(self.width):
                cell = self._parent.getCell(self.row+i_row, self.col+i_col)
                cell.setStyleID(style.getID())

    def updateStyle(self, alignment=None,
                    borders=None, font=None, interior=None,
                    number_format=None,
                    style_auto_create=True):
        """
        Set style in range.
        """
        for i_row in range(self.height):
            for i_col in range(self.width):
                cell = self._parent.getCell(self.row+i_row, self.col+i_col)
                cell_style = cell.getStyle()
                # If the cell style is not defined, then skip its processing
                if cell_style is None:
                    continue

                if not style_auto_create:
                    cell_style.updateAttrs(alignment, borders, font, interior, number_format)
                else:
                    cell_style_attrs = cell_style.getAttrs()
                    if alignment:
                        cell_style_attrs['alignment'] = alignment
                    if borders:
                        cell_style_attrs['borders'] = borders
                    if font:
                        cell_style_attrs['font'] = font
                    if interior:
                        cell_style_attrs['interior'] = interior
                    if number_format:
                        cell_style_attrs['number_format'] = number_format

                    my_workbook = self.getParentByName('Workbook')
                    find_style = my_workbook.getStyles().findStyle(**cell_style_attrs)
                    if find_style is None:
                        style = my_workbook.getStyles().createStyle()
                        style.setAttrs(**cell_style_attrs)
                    else:
                        style = find_style

                    cell.setStyleID(style.getID())

    def _isBorderPosition(self, style, border_position):
        """
        Check if the specified border is in the style in the description of the frame.
        """
        return bool([border for border in style['__children__'] if border['Position'] == border_position])

    def _getCellBorderAttrIdx(self, old_borders, i_row, i_col,
                              border_left=None, border_top=None, border_right=None, border_bottom=None):
        """
        Define style attributes in a range depending
        from the coordinates of the current cell.
        """
        if old_borders and '__children__' in old_borders:
            attrs = {'borders': {'name': 'Borders', '__children__': copy.deepcopy(old_borders['__children__'])}}
        else:
            attrs = {'borders': {'name': 'Borders', '__children__': []}}

        if i_row == 0:
            # Upper border cell
            if border_top:
                if not self._isBorderPosition(attrs['borders'], 'Top'):
                    cur_border = border_top
                    cur_border['name'] = 'Border'
                    cur_border['Position'] = 'Top'
                    attrs['borders']['__children__'].append(cur_border)
            if i_col == 0:
                # Upper left cell
                if border_left:
                    if not self._isBorderPosition(attrs['borders'], 'Left'):
                        cur_border = border_left
                        cur_border['name'] = 'Border'
                        cur_border['Position'] = 'Left'
                        attrs['borders']['__children__'].append(cur_border)
            if i_col == self._width_1:
                # Upper right cell
                if border_right:
                    if not self._isBorderPosition(attrs['borders'], 'Right'):
                        cur_border = border_right
                        cur_border['name'] = 'Border'
                        cur_border['Position'] = 'Right'
                        attrs['borders']['__children__'].append(cur_border)

        if i_row == self._height_1:
            # Bottom border cell
            if border_bottom:
                if not self._isBorderPosition(attrs['borders'], 'Bottom'):
                    cur_border = border_bottom
                    cur_border['name'] = 'Border'
                    cur_border['Position'] = 'Bottom'
                    attrs['borders']['__children__'].append(cur_border)
            if i_col == 0:
                # Lower left cell
                if border_left:
                    if not self._isBorderPosition(attrs['borders'], 'Left'):
                        cur_border = border_left
                        cur_border['name'] = 'Border'
                        cur_border['Position'] = 'Left'
                        attrs['borders']['__children__'].append(cur_border)
            if i_col == self._width_1:
                # Bottom right cell
                if border_right:
                    if not self._isBorderPosition(attrs['borders'], 'Right'):
                        cur_border = border_right
                        cur_border['name'] = 'Border'
                        cur_border['Position'] = 'Right'
                        attrs['borders']['__children__'].append(cur_border)

        if i_col == 0:
            # Left border cell
            if border_left:
                if not self._isBorderPosition(attrs['borders'], 'Left'):
                    cur_border = border_left
                    cur_border['name'] = 'Border'
                    cur_border['Position'] = 'Left'
                    attrs['borders']['__children__'].append(cur_border)
        if i_col == self._width_1:
            # Right border cell
            if border_right:
                if not self._isBorderPosition(attrs['borders'], 'Right'):
                    cur_border = border_right
                    cur_border['name'] = 'Border'
                    cur_border['Position'] = 'Right'
                    attrs['borders']['__children__'].append(cur_border)

        return attrs

    def setBorderOn(self, border_left=None,
                    border_top=None, border_right=None, border_bottom=None):
        """
        Framing a range of cells.
        """
        my_workbook = self.getParentByName('Workbook')

        for i_row in range(self.height):
            for i_col in range(self.width):
                # Only process cells around the perimeter
                if (i_row == 0) or (i_col == 0) or \
                   (i_row == self._height_1) or (i_col == self._width_1):

                    # Cell
                    cell = self._parent.getCell(self.row+i_row, self.col+i_col)
                    # Cell style id
                    style_id = cell.getStyleID()
                    # Define style
                    if style_id is not None:
                        style = my_workbook.getStyles().getStyle(style_id)
                        if style:
                            style_attrs = style.getAttrs()
                        else:
                            style_attrs = {'borders': {'name': 'Borders', '__children__': []}}
                    else:
                        style_attrs = {'borders': {'name': 'Borders', '__children__': []}}

                    if 'borders' not in style_attrs:
                        style_attrs['borders'] = {'name': 'Borders', '__children__': []}

                    cur_style_borders = self._getCellBorderAttrIdx(style_attrs['borders'],
                                                                   i_row, i_col,
                                                                   border_left, border_top,
                                                                   border_right, border_bottom)
                    style_attrs['borders'] = cur_style_borders['borders']

                    # Set cell style
                    cell.setStyle(**style_attrs)
        return True

    def _limitOffset(self, offset_row, offset_col):
        """
        Offset limit.
        """
        row_offset = max(min(offset_row, 0), self._height_1)
        col_offset = max(min(offset_col, 0), self._width_1)
        return row_offset, col_offset

    def spanColumn(self, step=1):
        """
        Take a cell in the range by column offset.
        """
        self._cur_span_offset = self._limitOffset(self._cur_span_offset[0],
                                                  self._cur_span_offset[1] + step)
        return self.getCellOffset(*self._cur_span_offset)

    def spanRow(self, step=1):
        """
        Take a cell in a range by line offset.
        """
        self._cur_span_offset = self._limitOffset(self._cur_span_offset[0] + step,
                                                  self._cur_span_offset[1])
        return self.getCellOffset(*self._cur_span_offset)

    def getCellOffset(self, offset_row=0, offset_column=0):
        """
        Get a cell in a range by the relative coordinates of the range.
        """
        # Offset limit
        row_offset, col_offset = self._limitOffset(offset_row, offset_column)
        return self._parent.getCell(self.row+row_offset, self.col+col_offset)

    def _getBasisRow(self):
        """
        The base row relative to which work with row indices occurs.
        """
        if self._basis_row is None:
            self._basis_row = iqVRow(self)
        return self._basis_row

    def copy(self):
        """
        Get a copy of the attributes of the object.
        """
        copy_result = {'name': 'Range',
                       'width': self.width,
                       'height': self.height,
                       '__children__': []}

        for i_row in range(self.height):
            cur_row = {'name': 'Row', '__children__': []}
            copy_result['__children__'].append(cur_row)

            cell = None
            for i_col in range(self.width):
                cell = self._parent.getCell(self.row+i_row, self.col+i_col)
                cell_attrs = copy.deepcopy(cell.getAttributes())
                cur_row['__children__'].append(cell_attrs)

            if cell:
                # Re-index all cells in a row
                cell._reIndexAllElements(('Cell',))

        # Re-index all rows in a cell range
        self._getBasisRow()._reIndexAllElements(('Row',))

        return copy_result


class iqVColumn(v_prototype.iqVIndexedPrototype, iqVRange):
    """
    Column.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVIndexedPrototype.__init__(self, parent, *args, **kwargs)
        iqVRange.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Column', '__children__': []}

    def setCaption(self, caption):
        """
        Set column caption.
        """
        self._attributes['Caption'] = caption

    def setWidth(self, width):
        """
        Set column width.
        """
        self._attributes['Width'] = str(width)

    def setCharacterWidth(self, character_count, font=None):
        """
        Setting the column width by the number of characters in the column.

        :param character_count: The number of characters in the column.
        :param font: Specifying the font, if not specified, then take Arial size 10.
        """
        width = self._calcWidthByCharacter(character_count, font)
        self.setWidth(width)

    def _calcWidthByCharacter(self, character_count, font=None):
        """
        The function of converting the number of characters in the column in width.
        """
        return int(character_count * 6)

    def setHidden(self, hidden=True):
        """
        Hiding the column.
        """
        if hidden:
            self._attributes['Hidden'] = str(int(hidden))
        else:
            if 'Hidden' in self._attributes:
                del self._attributes['Hidden']

    def setAutoFitWidth(self, auto_fit_width=True):
        """
        Set auto size to width.

        :param auto_fit_width: A sign of autosizing a column.
        """
        if auto_fit_width:
            self._attributes['AutoFitWidth'] = str(int(auto_fit_width))
        else:
            if 'AutoFitWidth' in self._attributes:
                del self._attributes['AutoFitWidth']


class iqVRow(v_prototype.iqVIndexedPrototype, iqVRange):
    """
    Row.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVIndexedPrototype.__init__(self, parent, *args, **kwargs)
        iqVRange.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Row', '__children__': []}

        # Basis cell
        self._basis_cell = None

#     def setIndex(self,index):
#         """
#         The row index in the table.
#         """
#         self._attributes['Index']=text(index)

    def setHeight(self, height):
        """
        Set row height.
        """
        self._attributes['Height'] = str(height)

    def setHidden(self, hidden=True):
        """
        Hiding a row.
        """
        if hidden:
            self._attributes['Hidden'] = str(int(hidden))
        else:
            if 'Hidden' in self._attributes:
                del self._attributes['Hidden']

    def createCell(self):
        """
        Create / Add to row cell.
        """
        cell = v_cell.iqVCell(self)
        attrs = cell.create()
        return cell

    def insertCellIdx(self, cell, idx):
        """
        Insert a cell in a row by index.
        """
        indexes, cell_attr = self._findCellIdxAttr(idx)
        ins_i = max(0, len([i for i in indexes if i < idx]))

        if cell_attr is None:
            cell.setIndex(idx)
        self._attributes['__children__'].insert(ins_i, cell.getAttributes())
        return cell

    def createCellIdx(self, idx):
        """
        Create / Add to row cell.
        """
        cell = self.createCell()
        self._attributes['__children__'] = self._attributes['__children__'][:-1]

        # Move cell by index
        cell = self.insertCellIdx(cell, idx)
        return cell

    def _getBasisCell(self):
        """
        The base cell with respect to which work with cell indices occurs.
        """
        if self._basis_cell is None:
            self._basis_cell = v_cell.iqVCell(self)
        return self._basis_cell

    def _findCellIdxAttr(self, idx):
        """
        Find cell attributes in a row by index.
        Indexing starts at 0.
        """
        return self._getBasisCell()._findElementIdxAttr(idx, 'Cell')

    def getCellIdx(self, idx):
        """
        Get a cell from a row by number.
        """
        indexes, cell_attr = self._findCellIdxAttr(idx)

        if cell_attr is None:
            cell = self.createCellIdx(idx)
        else:
            cell = v_cell.iqVCell(self)
            cell.setAttributes(cell_attr)
        return cell

    def delCell(self, idx):
        """
        Remove cell from row.
        """
        cell = self.getCellIdx(idx - 1)
        if cell:
            # Remove cell from row
            return cell._delElementIdxAttr(idx - 1, 'Cell')
        return False
