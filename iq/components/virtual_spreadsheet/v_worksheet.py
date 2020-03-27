#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

from . import v_prototype
from . import v_range
from . import paper_size
from . import exceptions


__version__ = (0, 0, 0, 1)

DETECT_MERGE_CELL_ERROR = False


class iqVWorksheet(v_prototype.iqVPrototype):
    """
    Worksheet.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Worksheet', 'Name': 'default',
                            'children': [{'name': 'WorksheetOptions',
                                          'children': [{'name': 'PageSetup',
                                                        'children': [{'name': 'PageMargins',
                                                                      'Bottom': 0.984251969, 'Left': 0.787401575,
                                                                      'Top': 0.984251969, 'Right': 0.787401575,
                                                                      'children': []}]}]}]}

        # Worksheet table
        # Cached to increase performance
        self._table = None

    def _isWorksheetsName(self, worksheets, name):
        """
        Are there sheets with the name?
        """
        for sheet in worksheets:
            if not isinstance(sheet['Name'], str):
                sheet_name = str(sheet['Name'])
            else:
                sheet_name = sheet['Name']
            if sheet_name == name:
                return True
        return False

    def _createNewName(self):
        """
        Create a new name for the sheet.
        """
        work_sheets = [element for element in self._parent.getAttributes()['children'] if element['name'] == 'Worksheet']
        i = 1
        new_name = u'Лист%d' % i
        while self._isWorksheetsName(work_sheets, new_name):
            i += 1
            new_name = u'Лист%d' % i
        return new_name

    def create(self):
        """
        Create worksheet.
        """
        attrs = self._parent.getAttributes()
        self._attributes['Name'] = self._createNewName()
        attrs['children'].append(self._attributes)
        return self._attributes

    def getName(self):
        """
        Get worksheet name.
        """
        return self._attributes['Name']

    def setName(self, Name_):
        """
        Set worksheet name.
        """
        self._attributes['Name'] = Name_

    def createTable(self):
        """
        Create table.
        """
        self._table = iqVTable(self)
        attrs = self._table.create()
        return self._table

    def getTable(self):
        """
        Get table.
        """
        if self._table:
            return self._table

        tab_attr = [element for element in self._attributes['children'] if element['name'] == 'Table']

        if tab_attr:
            self._table = iqVTable(self)
            self._table.setAttributes(tab_attr[0])
        else:
            self.createTable()
        return self._table

    def getCell(self, row, col):
        """
        Get cell.
        """
        return self.getTable().getCell(row, col)

    def getRange(self, row, col, height, width):
        """
        Get cell range.
        """
        new_range = v_range.iqVRange(self)
        new_range.setAddress(row, col, height, width)
        return new_range

    def getUsedRange(self):
        """
        Get table range.
        """
        used_height, used_width = self.getTable().getUsedSize()
        return self.getRange(1, 1, used_height, used_width)

    def clearWorksheet(self):
        """
        Clear worksheet.
        """
        return self.getTable().clearTab()

    def getWorksheetOptions(self):
        """
        Get worksheet options.
        """
        options_attr = [element for element in self._attributes['children'] if element['name'] == 'WorksheetOptions']
        if options_attr:
            options = iqVWorksheetOptions(self)
            options.setAttributes(options_attr[0])
        else:
            options = self.createWorksheetOptions()
        return options

    def createWorksheetOptions(self):
        """
        Create worksheet options.
        """
        options = iqVWorksheetOptions(self)
        attrs = options.create()
        return options

    def getPrintNumberofCopies(self):
        """
        Get print number of copies.
        """
        options = self.getWorksheetOptions()
        if options:
            print_section = options.getPrint()
            if print_section:
                n_copies = print_section.getNumberofCopies()
                return n_copies
        return None

    def setPrintNumberofCopies(self, number_of_copies=1):
        """
        Set print number of copies.
        """
        options = self.getWorksheetOptions()
        if options:
            print_section = options.getPrint()
            if print_section:
                return print_section.setNumberofCopies(number_of_copies)
        return False

    def clone(self, new_name):
        """
        Create a clone of a sheet and add it to the workbook.

        :param new_name: New worksheet name.
        """
        new_attributes = copy.deepcopy(self._attributes)
        new_attributes['Name'] = new_name

        new_worksheet = self._parent.createWorksheet()
        new_worksheet.updateAttributes(new_attributes)
        return new_worksheet

    def delColumn(self, idx=-1):
        """
        Delete column.
        """
        return self.getTable().delColumn(idx)

    def delRow(self, idx=-1):
        """
        Delete row.
        """
        return self.getTable().delRow(idx)

    def getColumns(self, start_idx=0, stop_idx=None):
        """
        Get column list.

        :param start_idx: First column index.
        :param stop_idx: Last column index.
        """
        return self.getTable().getColumns(start_idx, stop_idx)

    def getPageBreaks(self):
        """
        Get page breaks.
        """
        page_breaks_attr = [element for element in self._attributes['children'] if element['name'] == 'PageBreaks']
        if page_breaks_attr:
            page_breaks = iqVPageBreaks(self)
            page_breaks.setAttributes(page_breaks_attr[0])
        else:
            page_breaks = self.createPageBreaks()
        return page_breaks

    def createPageBreaks(self):
        """
        Create page breaks.
        """
        page_breaks = iqVPageBreaks(self)
        attrs = page_breaks.create()
        return page_breaks


class iqVTable(v_prototype.iqVPrototype):
    """
    Table.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Table', 'children': []}

        # Basic row and column
        self._basis_row = None
        self._basis_col = None

        # Dictionary of merged cells
        self._merge_cells = None

    def getUsedSize(self):
        """
        Get used size.
        """
        n_cols = self._maxColIdx()+1
        n_rows = self._maxRowIdx()+1
        return n_rows, n_cols

    def createColumn(self):
        """
        Create column.
        """
        col = v_range.iqVColumn(self)
        attrs = col.create()
        return col

    def getColumns(self, start_idx=0, stop_idx=None):
        """
        Get column list.

        :param start_idx: First column index.
        :param stop_idx: Last column index.
        """
        col_count = self.getColumnCount()
        if stop_idx is None:
            stop_idx = col_count
        # Protection against incorrect input data
        if start_idx > stop_idx:
            start_idx = stop_idx
        return [self.getColumn(idx) for idx in range(start_idx, stop_idx)]

    def getColumnsAttrs(self):
        """
        column list. Attributes.
        """
        return [element for element in self._attributes['children'] if element['name'] == 'Column']

    def getColumnCount(self):
        """
        Get number of columns.
        """
        return self._maxColIdx()+1

    def _reIndexCol(self, column, index, idx):
        """
        Re-indexing of the columns in the table.
        """
        return self._getBasisCol()._reIndexElement('Column', column, index, idx)

    def _createColIdx(self, index, idx):
        """
        Create a column with an index.

        :param index: Excel index.
        :param idx: Index in children list.
        """
        col = v_range.iqVColumn(self)
        idx = 0
        for i, child in enumerate(self._attributes['children']):
            if child['name'] == 'Column':
                if idx >= idx:
                    attrs = col.createIndex(idx)

                    self._reIndexCol(col, index, idx)
                    break
                idx += 1

        return col

    def getColumn(self, idx=-1):
        """
        Bet column by index.
        """
        col = None
        idxs, _i, col_data = self._findColIdxAttr(idx)
        if col_data is not None:
            col = v_range.iqVColumn(self)
            col.setAttributes(col_data)
        elif _i >= 0 and col_data is None:
            for i in idxs:
                if idx <= i:
                    return self._createColIdx(idx, _i)
            return self.createColumn()
        return col

    def createRow(self):
        """
        Create row.
        """
        row = v_range.iqVRow(self)
        attrs = row.create()
        return row

    def cloneRow(self, clear_cell=True, row=-1):
        """
        Clone table row.

        :param clear_cell: To clear the values in the cells.
        :param row: Index (Starting with 0) of the cloned cell. -1 is the last one.
        :return: Returns an object of the cloned string.
            If there are no rows in the table, it returns None.
        """
        if self._attributes['children']:
            row_attr = copy.deepcopy(self._attributes['children'][row])
            if clear_cell:
                row_attr['children'] = [dict(cell.items()+[('value', None)]) for cell in row_attr['children']]

            row_obj = v_range.iqVRow(self)
            row_obj.setAttributes(row_attr)
            return row_obj
        return None

    def _reIndexRow(self, row, index, idx):
        """
        A re-index of the row in the table.
        """
        return self._getBasisRow()._reIndexElement('Row', row, index, idx)

    def _createRowIdx(self, index, idx):
        """
        Create row with index.
        """
        row = v_range.iqVRow(self)
        for i, child in enumerate(self._attributes['children']):
            if child['name'] == 'Row':
                if i >= idx:
                    attrs = row.createIndex(i)

                    self._reIndexRow(row, index, i)
                    break

        return row

    def getRowsAttrs(self):
        """
        Get row attributes list.
        """
        return [element for element in self._attributes['children'] if element['name'] == 'Row']

    def getRowCount(self):
        """
        Get number of rows.
        """
        return self._maxRowIdx()+1

    def getRow(self, idx=-1):
        """
        Get row by index.
        """
        row = None
        idxs, _i, row_data = self._findRowIdxAttr(idx)
        if row_data is not None:
            row = v_range.iqVRow(self)
            row.setAttributes(row_data)
        else:
            for i in idxs:
                if idx <= i:
                    return self._createRowIdx(idx, _i)
            return self.createRow()
        return row

    def createCell(self, row, col):
        """
        Create cell (row, col).
        """
        col_count = self.getColumnCount()
        if col > col_count:
            for i in range(col - col_count):
                self.createColumn()

        row_count = self.getRowCount()
        if row > row_count:
            for i in range(row - row_count):
                self.createRow()

        # Check for getting into the merged cell
        if self.isInMergeCell(row, col):
            sheet_name = self.getParentByName('Worksheet').getName()
            err_txt = 'Getting new_cell (sheet: %s, row: %d, column: %d) into merge new_cell!' % (sheet_name, row, col)
            raise exceptions.iqMergeCellError((100, err_txt))

        cur_row = self.getRow(row)
        cell = cur_row.createCellIdx(col)
        return cell

    def getCell(self, row, col):
        """
        Get cell (row, col).
        """
        # If the coordinates are not valid, then an error
        if row <= 0:
            raise IndexError
        if col <= 0:
            raise IndexError

        # Limit on row and column indices
        if row > 65535:
            return None
        if col > 256:
            return None

        col_count = self.getColumnCount()
        if col > col_count:
            for i in range(col-col_count):
                self.createColumn()

        row_count = self.getRowCount()
        if row > row_count:
            for i in range(row-row_count):
                self.createRow()

        # Check for getting into the merged cell
        if self.isInMergeCell(row, col):
            if DETECT_MERGE_CELL_ERROR:
                sheet_name = self.getParentByName('Worksheet').getName()
                err_txt = 'Getting new_cell (sheet: %s, row: %d, column: %d) into merge new_cell!' % (sheet_name, row, col)
                raise exceptions.iqMergeCellError((100, err_txt))
            else:
                cell = self.getInMergeCell(row, col)
                return cell

        cur_row = self.getRow(row)
        cell = cur_row.getCellIdx(col)
        # Set cell coordinates
        cell._row_idx = row
        cell._col_idx = col
        return cell

    def clearTab(self):
        """
        Clear table.
        """
        return self.clear()

    def _findColIdxAttr(self, idx):
        """
        Find the attributes of a column in a table by index.
        Indexing starts at 0.
        """
        return self._getBasisCol()._findElementIdxAttr(idx, 'Column')

    def _findRowIdxAttr(self, idx):
        """
        Find row attributes in a table by index.
        Indexing starts at 0.
        """
        return self._getBasisRow()._findElementIdxAttr(idx, 'Row')

    def _maxColIdx(self):
        """
        The maximum column index in the table.
        Indexing starts at 0.
        """
        return self._getBasisCol()._maxElementIdx(elements=self.getColumnsAttrs())

    def _maxRowIdx(self):
        """
        The maximum row index in the table.
        Indexing starts at 0.
        """
        return self._getBasisRow()._maxElementIdx(elements=self.getRowsAttrs())

    def setExpandedRowCount(self, expanded_row_count=None):
        """
        Calculation of the maximum number of rows in a table.
        """
        if expanded_row_count:
            self._attributes['ExpandedRowCount'] = expanded_row_count
        else:
            if 'ExpandedRowCount' in self._attributes:
                cur_count = int(self._attributes['ExpandedRowCount'])
                calc_count = self._maxRowIdx()+1
                # If the calculated amount is greater than the current one,
                # the generator added rows and the ExpandedRowCount
                # value must be increased. Line limit 65535.
                self._attributes['ExpandedRowCount'] = min(max(calc_count, cur_count), 65535)

    def setExpandedColCount(self, expanded_col_count=None):
        """
        Calculation of the maximum number of columns per row.
        """
        if expanded_col_count:
            self._attributes['ExpandedColumnCount'] = expanded_col_count
        else:
            if 'ExpandedColumnCount' in self._attributes:
                cur_count = int(self._attributes['ExpandedColumnCount'])
                calc_count = self._maxColIdx()+1
                # If the calculated amount is greater than the current one,
                # the generator has added columns and the value of ExpandedColumnCount
                # must be increased. The limit on the number of columns is 256
                self._attributes['ExpandedColumnCount'] = min(max(calc_count, cur_count), 256)

    def paste(self, paste, to=None):
        """
        Insert a copy of the attributes of the object inside the current object
        by the address.
        If to None, then a replacement occurs.
        """
        if paste['name'] == 'Range':
            return self._pasteRange(paste, to)
        else:
            print('ERROR: Error paste object attributes %s' % paste)
        return False

    def _pasteRange(self, paste, to):
        """
        Insert a range into the table at the cell address.
        """
        if isinstance(to, tuple) and len(to) == 2:
            to_row, to_col = to
            # Cell address (row, col)
            for i_row in range(paste['height']):
                for i_col in range(paste['width']):
                    cell_attrs = paste['children'][i_row][i_col]
                    cell = self.getCell(to_row+i_row, to_col+i_col)
                    cell.set_attributes(cell_attrs)
            return True
        else:
            print('ERROR: Paste address error %s' % to)
        return False

    def _getBasisRow(self):
        """
        The base row relative to which work with row indices occurs.
        """
        if self._basis_row is None:
            self._basis_row = v_range.iqVRow(self)
        return self._basis_row

    def _getBasisCol(self):
        """
        The base column relative to which the column indices work.
        """
        if self._basis_col is None:
            self._basis_col = v_range.iqVColumn(self)
        return self._basis_col

    def getMergeCells(self):
        """
        Dictionary of merged cells. As a key, a tuple of the cell coordinate.
        """
        merge_cells = {}
        rows = [element for element in self._attributes['children'] if element['name'] == 'Row']
        for i_row, row in enumerate(rows):
            i_col = 0
            for cell in row['children']:
                if cell['name'] == 'Cell':
                    if 'Index' in cell:
                        new_i_col = int(cell['Index'])
                        if new_i_col >= i_col:
                            i_col = new_i_col
                    else:
                        i_col += 1

                    if 'MergeAcross' in cell or 'MergeDown' in cell:
                        cur_row = self.getRow(i_row+1)
                        cell_obj = cur_row.getCellIdx(i_col)
                        # Set cell coordinates
                        cell_obj._row_idx = i_row+1
                        cell_obj._col_idx = i_col
                        merge_cells[cell_obj.getRegion()] = cell_obj
                    if 'MergeAcross' in cell:
                        # Accounting of the unified cells DO MANDATORY !!!
                        # Otherwise, the previous merged cells are not counted
                        i_col += int(cell['MergeAcross'])-1

        return merge_cells

    def isInMergeCell(self, row, column):
        """
        Does the specified cell get in the merged?
        """
        # Caching merged cells in case of a hit
        # in them when creating a new cell
        if self._merge_cells is None:
            self._merge_cells = self.getMergeCells()

        for cell in self._merge_cells.items():
            cell_region = cell[0]
            if (row >= cell_region[0]) and (row <= (cell_region[0]+cell_region[2])) and \
                    (column >= cell_region[1]) and (column <= (cell_region[1]+cell_region[3])):
                if row != cell_region[0] or column != cell_region[1]:
                    return True
        return False

    def getInMergeCell(self, row, column):
        """
        Get the combined cell indicated by the coordinates.
        """
        # Caching merged cells in case of a hit
        # in them when creating a new cell
        if self._merge_cells is None:
            self._merge_cells = self.getMergeCells()

        for cell in self._merge_cells.items():
            cell_region = cell[0]
            if (row >= cell_region[0]) and (row<= (cell_region[0]+cell_region[2])) and \
                    (column >= cell_region[1]) and (column <= (cell_region[1]+cell_region[3])):
                if row != cell_region[0] or column != cell_region[1]:
                    return cell[1]
        return None

    def delColumn(self, idx=-1):
        """
        Delete column.
        """
        col = self.getColumn(idx)
        if col:
            # Delete column from table
            result = col._delElementIdxAttr(idx - 1, 'Column')
            # In addition, delete the cell corresponding to the current column
            for i_row in range(self.getRowCount()):
                row = self.getRow(i_row+1)
                if row:
                    row.delCell(idx)
            return result
        return False

    def delRow(self, idx=-1):
        """
        Delete row.
        """
        row = self.getRow(idx)

        if row:
            # Delete row from table
            return row._delElementIdxAttr(idx - 1, 'Row')
        return False


class iqVWorksheetOptions(v_prototype.iqVPrototype):
    """
    Worsheet options.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'WorksheetOptions', 'children': []}

    def getPageSetup(self):
        """
        Page setup.
        """
        page_setup_attr = [element for element in self._attributes['children'] if element['name'] == 'PageSetup']
        if page_setup_attr:
            page_setup = iqVPageSetup(self)
            page_setup.setAttributes(page_setup_attr[0])
        else:
            page_setup = self.createPageSetup()
        return page_setup

    def createPageSetup(self):
        """
        Create page setup.
        """
        page_setup = iqVPageSetup(self)
        attrs = page_setup.create()
        return page_setup

    def getPrint(self):
        """
        Print setup.
        """
        print_attr = [element for element in self._attributes['children'] if element['name'] == 'Print']
        if print_attr:
            print_setup = iqVPrint(self)
            print_setup.setAttributes(print_attr[0])
        else:
            print_setup = self.createPrint()
        return print_setup

    def createPrint(self):
        """
        Create print setup.
        """
        print_section = iqVPrint(self)
        attrs = print_section.create()
        return print_section

    def isFitToPage(self):
        """
        Page layout scale.
        """
        fit_to_page = [element for element in self._attributes['children'] if element['name'] == 'FitToPage']
        return bool(fit_to_page)


class iqVPageSetup(v_prototype.iqVPrototype):
    """
    Page setup.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'PageSetup', 'children': []}

    def getLayout(self):
        """
        Layout page.
        """
        layout = [element for element in self._attributes['children'] if element['name'] == 'Layout']
        if layout:
            return layout[0]
        return None

    def getOrientation(self):
        """
        Orientation page.
        """
        layout = self.getLayout()
        if layout:
            if 'Orientation' in layout:
                return layout['Orientation']
        # Default portrait orientation
        return 'Portrait'

    def getCenter(self):
        """
        Centering horizontally / vertically.
        """
        layout = self.getLayout()
        if layout:
            c_horiz = '0'
            if 'CenterHorizontal' in layout:
                c_horiz = layout['CenterHorizontal']
            c_vert = '0'
            if 'CenterVertical' in layout:
                c_vert = layout['CenterVertical']
            return bool(c_horiz == '1'), bool(c_vert == '1')

        return False, False

    def getPageMargins(self):
        """
        Page margins.
        """
        margins = [element for element in self._attributes['children'] if element['name'] == 'PageMargins']
        if margins:
            return margins[0]
        return {}

    def getMargins(self):
        """
        Get margins.
        """
        margins = self.getPageMargins()
        if margins:
            left_margin = 0
            if 'Left' in margins:
                left_margin = float(margins['Left'])

            top_margin = 0
            if 'Top' in margins:
                top_margin = float(margins['Top'])

            right_margin = 0
            if 'Right' in margins:
                right_margin = float(margins['Right'])

            bottom_margin = 0
            if 'Bottom' in margins:
                bottom_margin = float(margins['Bottom'])

            return left_margin, top_margin, right_margin, bottom_margin

        return 0, 0, 0, 0


class iqVPrint(v_prototype.iqVPrototype):
    """
    Print setup.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Print', 'children': []}

    def getPaperSizeIndex(self):
        """
        Paper size.
        """
        paper_size_lst = [element for element in self._attributes['children'] if element['name'] == 'PaperSizeIndex']
        if paper_size_lst:
            return int(paper_size_lst[0]['value'])
        # Default A4 size
        return paper_size.xlPaperA4

    def getPaperSize(self):
        """
        The paper size is 0.01 mm.
        """
        paper_size_i = self.getPaperSizeIndex()
        if paper_size_i > 0:
            return paper_size.XL_PAPER_SIZE.setdefault(paper_size_i, None)
        return None

    def getScale(self):
        """
        Paper scale.
        """
        scale = [element for element in self._attributes['children'] if element['name'] == 'Scale']
        if scale:
            return int(scale[0]['value'])
        # The default scale is 100%.
        return 100

    def getFitWidth(self):
        """
        Scale. Place no more than X pages wide.
        """
        fit_width = [element for element in self._attributes['children'] if element['name'] == 'FitWidth']
        if fit_width:
            try:
                return int(fit_width[0]['value'])
            except:
                pass
        # Default 1
        return 1

    def getFitHeight(self):
        """
        Scale. Place no more than X pages high.
        """
        fit_height = [element for element in self._attributes['children'] if element['name'] == 'FitHeight']
        if fit_height:
            try:
                return int(fit_height[0]['value'])
            except:
                pass
        # Default 1
        return 1

    def getFit(self):
        """
        Scale in hosted pages.
        """
        return self.getFitWidth(), self.getFitHeight()

    def getNumberofCopies(self):
        """
        The number of copies of the sheet.
        """
        n_copies = [element for element in self._attributes['children'] if element['name'] == 'NumberofCopies']
        if n_copies:
            try:
                return int(n_copies[0]['value'])
            except:
                pass
        # Default 1
        return 1

    def setNumberofCopies(self, number_of_copies=1):
        """
        The number of copies of the sheet.
        """
        number_of_copies = min(max(int(number_of_copies), 1), 256)
        n_copies = {'name': 'NumberofCopies', 'value': number_of_copies}
        self._attributes['children'].append(n_copies)
        return n_copies


class iqVPageBreaks(v_prototype.iqVPrototype):
    """
    Page breaks.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'PageBreaks', 'children': [{'name': 'RowBreaks', 'children': []}]}

    def addRowBreak(self, row):
        """
        Add page break line by line.

        :param row: Row number.
        """
        row_break = {'name': 'RowBreak', 'children': [{'name': 'Row', 'value': row}]}
        self._attributes['children'][0]['children'].append(row_break)
