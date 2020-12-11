#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from . import v_prototype

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqVCell(v_prototype.iqVIndexedPrototype):
    """
    Cell.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVIndexedPrototype.__init__(self, parent, *args, **kwargs)

        self._attributes = {'name': 'Cell', '_children_': []}

        self._colsA1 = []   # Excel column names in A1 format

        self._row_idx = -1  # Cell index in rows
        self._col_idx = -1  # Cell index in columns

    def createData(self):
        """
        Create cell data.
        """
        data = iqVData(self)
        attrs = data.create()
        return data

    def getDataAttrs(self):
        """
        Get attributes data.
        """
        return [element for element in self._attributes['_children_'] if element['name'] == 'Data']

    def getDataCount(self):
        """
        Cell attributes number.
        """
        return len(self.getDataAttrs())

    def getData(self):
        """
        Get cell data.
        """
        data_attrs = self.getDataAttrs()
        if data_attrs:
            data = iqVData(self)
            data.setAttributes(data_attrs[0])
        else:
            data = self.createData()

        return data

    def getValue(self):
        """
        Get cell value.
        """
        data = self.getData()
        return data.getValue()

    def isFormula(self, value):
        """
        Check if the value is a formula.

        :param value: Cell value.
        """
        return isinstance(value, str) and bool(value) and value[0] == '='
    
    def setValue(self, value, value_type='String'):
        """
        Set cell value.
        """
        if self.isFormula(value):
            self.setFormulaR1C1(value)
        else:
            data = self.getData()
            data.setValue(value, value_type)

    def setStyle(self, alignment=None,
                 borders=None, font=None, interior=None,
                 number_format=None):
        """
        Set cell style.
        """
        my_workbook = self.getParentByName('Workbook')
        find_style = my_workbook.getStyles().findStyle(alignment,
                                                       borders, font, interior, number_format)

        if find_style:
            self._attributes['StyleID'] = find_style.getAttributes()['ID']
        else:
            style = my_workbook.getStyles().createStyle()
            style.setAttrs(alignment,
                           borders, font, interior, number_format)
            self._attributes['StyleID'] = style.getAttributes()['ID']

    def getStyle(self):
        """
        Get cell style.
        """
        style = None
        if 'StyleID' in self._attributes:
            # Get style from style list
            my_workbook = self.getParentByName('Workbook')
            style = my_workbook.getStyles().getStyle(self._attributes['StyleID'])
            self._attributes['StyleID'] = style.getAttributes()['ID']
        else:
            # Create new style
            my_workbook = self.getParentByName('Workbook')
            style = my_workbook.getStyles().createStyle()
            self._attributes['StyleID'] = style.getAttributes()['ID']
        return style

    def setStyleID(self, style_id):
        """
        Set style id for cell.
        """
        if style_id:
            self._attributes['StyleID'] = str(style_id)

    def getStyleID(self):
        """
        Get cell style id.
        """
        if 'StyleID' in self._attributes:
            return self._attributes['StyleID']
        return None

    def _getColNameA1List(self):
        """
        Returns a list of column names.
        """
        if self._colsA1:
            return self._colsA1

        sAlf1 = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        sAlf2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._colsA1 = []
        for s1 in sAlf1:
            for s2 in sAlf2:
                self._colsA1.append((s1+s2).strip())
                if len(self._colsA1) == 256:
                    return self._colsA1
        return self._colsA1

    def _getRowColA1(self, addr):
        """
        Transform Excel address to a tuple (row, column).
        """
        lst = self._getColNameA1List()
        beg = 26
        end = -1
        step = 26

        if addr[1] in '1234567890':
            beg = 0
            end = 26
            step = 0

        if end < 0:
            lst = lst[beg:]
        else:
            lst = lst[beg:end]

        for col, nm in enumerate(lst):
            if addr.startswith(nm):
                return int(addr.split(nm)[-1]), col+1+step

    A1_FORMAT = r'[a-zA-Z]{1,2}\d{1,5}'

    def _A1Fmt2R1C1Fmt(self, formula):
        """
        Convert cell addressing from A1 format to R1C1 format.
        """
        parse_all = re.findall(self.A1_FORMAT, formula)
        for replace_addr in parse_all:
            r1c1 = 'R%dC%d' % self._getRowColA1(replace_addr)
            formula = formula.replace(replace_addr, r1c1)
        return formula

    def setFormulaR1C1(self, formula):
        """
        Set the formula in RC format.
        """
        self._attributes['Formula'] = self._A1Fmt2R1C1Fmt(formula)

    def setMerge(self, across, down):
        """
        Set cells merge.
        """
        # Delete cells in the merge zone.
        self._delMergeArreaCells(self._row_idx, self._col_idx, down, across)

        if across > 0:
            self._attributes['MergeAcross'] = str(across)
        else:
            if 'MergeAcross' in self._attributes:
                del self._attributes['MergeAcross']

        if down > 0:
            self._attributes['MergeDown'] = str(down)
        else:
            if 'MergeDown' in self._attributes:
                del self._attributes['MergeDown']

        # After merging, you need to clean the dictionary of merged cells
        # table=self.getParentByName('Table')
        # table._merge_cells=None

    def _delMergeArreaCells(self, row, column, merge_down, merge_across):
        """
        Delete cells in the merge zone.

        :param row: Row number.
        :param column: Column number.
        :param merge_down: The number of merge lines.
        :param merge_across: The number of merge columns.
        """
        table = self.getParentByName('Table')
        for i_row in range(row, row + merge_down + 1):
            row_obj = table.getRow(i_row)
            for i_col in range(column, column + merge_across + 1):
                if not (i_row == row and i_col == column):
                    row_obj._delElementIdxAttrChild(i_col-1, 'Cell', False)

    def _findElementIdxAttr(self, idx, element_name):
        """
        Find cell attributes in a row by index.
        Indexing starts at 0.
        """
        indexes = []
        cur_idx = 0
        for i, cell_attr in enumerate(self._parent.getAttributes()['_children_']):
            if 'Index' in cell_attr:
                cur_idx = int(cell_attr['Index'])
            else:
                cur_idx += 1

            indexes.append(cur_idx)

            # Combined cell accounting
            if 'MergeAcross' in cell_attr:
                cur_idx += int(cell_attr['MergeAcross'])

        if idx in indexes:
            # The cell with the specified index is
            return indexes, self._parent.getAttributes()['_children_'][indexes.index(idx)]
        return indexes, None

    def getOffset(self, offset_row=0, offset_column=0):
        """
        Get cell by offset taking into account merged cells.

        :param offset_row: Row offset.
        :param offset_column: Column offset.
        :return: Returns the cell object by offset or None in case of an error.
        """
        if offset_row <= 0 and offset_column <= 0:
            return self
        # Defining a new cell address
        cell_row = 1
        if self._row_idx > 0:
            cell_row = self._row_idx
        cell_col = 1
        if self._col_idx > 0:
            cell_col = self._col_idx

        if offset_row > 0:
            if 'MergeDown' in self._attributes:
                cell_row += int(self._attributes['MergeDown'])
        if offset_column > 0:
            if 'MergeAcross' in self._attributes:
                cell_col += int(self._attributes['MergeAcross'])

        cell_row += offset_row
        cell_col += offset_column

        tab = self.getParentByName('Table')
        if tab:
            return tab.getCell(cell_row, cell_col)
        return None

    def getAddress(self):
        """
        Get cell address.

        :return: Returns a tuple (row number, column number).
        """
        return self._row_idx, self._col_idx

    def getRegion(self):
        """
        Cell Area = Cell Address + number of combined rows and columns.

        :return: Returns a tuple
             (row number, column number, merged rows, merged columns).
        """
        merge_down = 0
        if 'MergeDown' in self._attributes:
            merge_down = int(self._attributes['MergeDown'])
        merge_across = 0
        if 'MergeAcross' in self._attributes:
            merge_across = int(self._attributes['MergeAcross'])
        return self._row_idx, self._col_idx, merge_down, merge_across

    def getNext(self):
        """
        The next cell is the current one horizontally.
        """
        return self.getOffset(0, 1)

    def set_xmlns(self, xmlns='http://www.w3.org/TR/REC-html40'):
        """
        Set the way to format text in a cell.
        """
        data = self.getData()
        data.setXmlns(xmlns)


DEFAULT_PERCENTAGE_TYPE = 'Percentage'
DEFAULT_NUMBER_TYPE = 'Number'


class iqVData(v_prototype.iqVPrototype):
    """
    Cell data.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Data', 'value': None, 'Type': 'String', '_children_': []}

    def getValue(self):
        """
        Get value.
        """
        return self._attributes['value']

    def _isPersentageType(self):
        """
        Here is a check for data belonging to the percentage type
        since there is no way to separate percent from numeric types.
        """
        analize_type = self.getAttributes().get('Type', '').lower().title() == DEFAULT_PERCENTAGE_TYPE
        
        style = self.getParent().getStyle()
        number_format = style.findChildAttrsByName('NumberFormat')
        analize_style = number_format and 'Format' in number_format and \
            (('%' in number_format['Format']) or ('Percent' in number_format['Format']))
        return analize_type or analize_style
    
    def setValue(self, value, value_type='String'):
        """
        Set value.
        """
        val = value
        val_type = value_type
        
        if self._isPersentageType():
            val_type = DEFAULT_PERCENTAGE_TYPE
        elif type(value) in (int, float):
            val_type = DEFAULT_NUMBER_TYPE
        # elif isinstance(value, text):
        #    val = val.encode(self.getApp().encoding)
        
        # Formula processing
        if self.getParent().isFormula(value):
            self.getParent().setFormulaR1C1(value)
            if self._isPersentageType():
                val_type = DEFAULT_PERCENTAGE_TYPE
            else:
                val_type = DEFAULT_NUMBER_TYPE

        self._attributes['value'] = str(val)
        self._attributes['Type'] = val_type

    def setXmlns(self, xmlns='http://www.w3.org/TR/REC-html40'):
        """
        Set the way to format text in a cell.
        """
        self._attributes['xmlns'] = str(xmlns)
