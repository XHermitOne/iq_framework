#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
# import sys

try:
    from . import v_prototype
    from . import v_range
    from . import paper_size
    from . import config
    from . import exceptions
except ImportError:
    # Для запуска тестов
    import icprototype
    import icrange
    import paper_size
    import config
    import icexceptions


__version__ = (0, 1, 2, 1)


class iqVWorksheet(v_prototype.iqVPrototype):
    """
    Лист.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Worksheet', 'Name': 'default',
                            'children': [{'name': 'WorksheetOptions',
                                          'children': [{'name': 'PageSetup',
                                                        'children': [{'name': 'PageMargins',
                                                                      'Bottom': 0.984251969, 'Left': 0.787401575,
                                                                      'Top': 0.984251969, 'Right': 0.787401575,
                                                                      'children': []}]}]}]}

        # Таблица листа
        # ВНИМАНИЕ! Кэшируется для увеличения производительности
        self._table = None

    def _is_worksheets_name(self, worksheets, name):
        """
        Существуют листы с именем name?
        """
        for sheet in worksheets:
            if not isinstance(sheet['Name'], str):
                sheet_name = str(sheet['Name'])   # 'utf-8')
            else:
                sheet_name = sheet['Name']
            if sheet_name == name:
                return True
        return False

    def _create_new_name(self):
        """
        Создать новое имя для листа.
        """
        work_sheets = [element for element in self._parent.getAttributes()['children'] if element['name'] == 'Worksheet']
        i = 1
        new_name = u'Лист%d' % i
        while self._is_worksheets_name(work_sheets, new_name):
            i += 1
            new_name = u'Лист%d' % i
        return new_name

    def create(self):
        """
        Создать.
        """
        attrs = self._parent.getAttributes()
        self._attributes['Name'] = self._create_new_name()
        attrs['children'].append(self._attributes)
        return self._attributes

    def getName(self):
        """
        Имя листа.
        """
        return self._attributes['Name']

    def setName(self, Name_):
        """
        Установить имя листа.
        """
        self._attributes['Name'] = Name_

    def createTable(self):
        """
        Создать таблицу.
        """
        self._table = iqVTable(self)
        attrs = self._table.create()
        return self._table

    def getTable(self):
        """
        Таблица.
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
        Получить ячейку.
        """
        return self.getTable().getCell(row, col)

    def getRange(self, row, col, height, width):
        """
        Диапазон ячеек.
        """
        new_range = v_range.iqVRange(self)
        new_range.setAddress(row, col, height, width)
        return new_range

    def getUsedRange(self):
        """
        Весь диапазон таблицы.
        """
        used_height, used_width = self.getTable().getUsedSize()
        return self.getRange(1, 1, used_height, used_width)

    def clearWorksheet(self):
        """
        Очистка листа.
        """
        return self.getTable().clearTab()

    def getWorksheetOptions(self):
        """
        Параметры листа.
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
        Параметры листа.
        """
        options = iqVWorksheetOptions(self)
        attrs = options.create()
        return options

    def getPrintNumberofCopies(self):
        """
        Количество копий припечати листа.
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
        Количество копий припечати листа.
        """
        options = self.getWorksheetOptions()
        if options:
            print_section = options.getPrint()
            if print_section:
                return print_section.setNumberofCopies(number_of_copies)
        return False

    def clone(self, new_name):
        """
        Создать клон листа и добавить его в книгу.
        param new_name: Новое имя листа.
        """
        new_attributes = copy.deepcopy(self._attributes)
        new_attributes['Name'] = new_name

        new_worksheet = self._parent.createWorksheet()
        new_worksheet.updateAttributes(new_attributes)
        return new_worksheet

    def delColumn(self, idx=-1):
        """
        Удалить колонку.
        """
        return self.getTable().delColumn(idx)

    def delRow(self, idx=-1):
        """
        Удалить строку.
        """
        return self.getTable().delRow(idx)

    def getColumns(self, start_idx=0, stop_idx=None):
        """
        Список объектов колонок.

        :param start_idx: Индекс первой колонки. По умолчанию с первой.
        :param stop_idx: Индекс последней колонки. По умолчанию до последней.
        """
        return self.getTable().getColumns(start_idx, stop_idx)

    def getPageBreaks(self):
        """
        Разрывы страниц.
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
        Разрывы страниц.
        """
        page_breaks = iqVPageBreaks(self)
        attrs = page_breaks.create()
        return page_breaks


class iqVTable(v_prototype.iqVPrototype):
    """
    Таблица.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Table', 'children': []}

        # Базисные строка и колонка
        self._basis_row = None
        self._basis_col = None

        # Словарь объединенных ячеек
        self._merge_cells = None

    def getUsedSize(self):
        """
        Используемый размер таблицы.
        """
        n_cols = self._maxColIdx()+1
        n_rows = self._maxRowIdx()+1
        return n_rows, n_cols

    def createColumn(self):
        """
        Создать колонку.
        """
        col = v_range.icVColumn(self)
        attrs = col.create()
        return col

    def getColumns(self, start_idx=0, stop_idx=None):
        """
        Список объектов колонок.

        :param start_idx: Индекс первой колонки. По умолчанию с первой.
        :param stop_idx: Индекс последней колонки. По умолчанию до последней.
        """
        col_count = self.getColumnCount()
        if stop_idx is None:
            stop_idx = col_count
        # Защита от не корректных входных данных
        if start_idx > stop_idx:
            start_idx = stop_idx
        return [self.getColumn(idx) for idx in range(start_idx, stop_idx)]

    def getColumnsAttrs(self):
        """
        Список колонок. Данные.
        """
        return [element for element in self._attributes['children'] if element['name'] == 'Column']

    def getColumnCount(self):
        """
        Количество колонок.
        """
        return self._maxColIdx()+1

    def _reIndexCol(self, column, index, idx):
        """
        Переиндексирование колонки в таблице.
        """
        return self._getBasisCol()._reIndexElement('Column', column, index, idx)

    def _createColIdx(self, index, idx):
        """
        Создать колонку с индексом.

        :param index: Индекс Excel.
        :param idx: Индекс в списке children.
        """
        col = v_range.icVColumn(self)
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
        Взять колонку по индексу.
        """
        col = None
        idxs, _i, col_data = self._findColIdxAttr(idx)
        if col_data is not None:
            col = v_range.icVColumn(self)
            col.setAttributes(col_data)
        elif _i >= 0 and col_data is None:
            for i in idxs:
                if idx <= i:
                    return self._createColIdx(idx, _i)
            return self.createColumn()
        return col

    def createRow(self):
        """
        Создать строку.
        """
        row = v_range.icVRow(self)
        attrs = row.create()
        return row

    def cloneRow(self, bClearCell=True, row=-1):
        """
        Клонировать строку таблицы.

        :param bClearCell: Очистить значения в ячейках.
        :param row: Индекс(Начинаяется с 0) клонируемой ячейки. -1 - Последняя.
        :return: Возвращает объект клонированной строки. Если строк в таблице нет, то возвращает None.
        """
        if self._attributes['children']:
            row_attr = copy.deepcopy(self._attributes['children'][row])
            if bClearCell:
                row_attr['children'] = [dict(cell.items()+[('value', None)]) for cell in row_attr['children']]

            row_obj = v_range.icVRow(self)
            row_obj.setAttributes(row_attr)
            return row_obj
        return None

    def _reIndexRow(self, row, index, idx):
        """
        Переиндексирование строки в таблице.
        """
        return self._getBasisRow()._reIndexElement('Row', row, index, idx)

    def _createRowIdx(self, index, idx):
        """
        Создать строку с индексом.
        """
        row = v_range.icVRow(self)
        for i, child in enumerate(self._attributes['children']):
            if child['name'] == 'Row':
                if i >= idx:
                    attrs = row.createIndex(i)

                    self._reIndexRow(row, index, i)
                    break

        return row

    def getRowsAttrs(self):
        """
        Список строк. Данные.
        """
        return [element for element in self._attributes['children'] if element['name'] == 'Row']

    def getRowCount(self):
        """
        Количество строк.
        """
        return self._maxRowIdx()+1

    def getRow(self, idx=-1):
        """
        Взять строку по индексу.
        """
        row = None
        idxs, _i, row_data = self._findRowIdxAttr(idx)
        if row_data is not None:
            row = v_range.icVRow(self)
            row.setAttributes(row_data)
        else:
            for i in idxs:
                if idx <= i:
                    return self._createRowIdx(idx, _i)
            return self.createRow()
        return row

    def createCell(self, row, col):
        """
        Создать ячейку (row,col).
        """
        col_count = self.getColumnCount()
        if col > col_count:
            for i in range(col - col_count):
                self.createColumn()

        row_count = self.getRowCount()
        if row > row_count:
            for i in range(row - row_count):
                self.createRow()

        # Проверка на попадание в объединенную ячейку
        if self.isInMergeCell(row, col):
            sheet_name = self.getParentByName('Worksheet').getName()
            err_txt = 'Getting new_cell (sheet: %s, row: %d, column: %d) into merge new_cell!' % (sheet_name, row, col)
            raise exceptions.iqMergeCellError((100, err_txt))

        cur_row = self.getRow(row)
        cell = cur_row.createCellIdx(col)
        return cell

    def getCell(self, row, col):
        """
        Получить ячейку (row,col).
        """
        # Если координаты недопустимы, тогда ошибка
        if row <= 0:
            raise IndexError
        if col <= 0:
            raise IndexError

        # Ограничение по индексам строк и колонок
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

        # Проверка на попадание в объединенную ячейку
        if self.isInMergeCell(row, col):
            if config.DETECT_MERGE_CELL_ERROR:
                sheet_name = self.getParentByName('Worksheet').getName()
                err_txt = 'Getting new_cell (sheet: %s, row: %d, column: %d) into merge new_cell!' % (sheet_name, row, col)
                raise exceptions.iqMergeCellError((100, err_txt))
            else:
                cell = self.getInMergeCell(row, col)
                return cell

        cur_row = self.getRow(row)
        cell = cur_row.getCellIdx(col)
        # Установить координаты ячейки
        cell._row_idx = row
        cell._col_idx = col
        return cell

    def clearTab(self):
        """
        Очистка таблицы.
        """
        return self.clear()

    def _findColIdxAttr(self, idx):
        """
        Найти атрибуты колонки в таблице по индексу.
        ВНИМАНИЕ! В этой функции индексация начинается с 0.
        """
        return self._getBasisCol()._findElementIdxAttr(idx, 'Column')

    def _findRowIdxAttr(self, idx):
        """
        Найти атрибуты строки в таблице по индексу.
        ВНИМАНИЕ! В этой функции индексация начинается с 0.
        """
        return self._getBasisRow()._findElementIdxAttr(idx, 'Row')

    def _maxColIdx(self):
        """
        Максимальный индекс колонок в таблице.
        ВНИМАНИЕ! В этой функции индексация начинается с 0.
        """
        return self._getBasisCol()._maxElementIdx(elements=self.getColumnsAttrs())

    def _maxRowIdx(self):
        """
        Максимальный индекс строк в таблице.
        ВНИМАНИЕ! В этой функции индексация начинается с 0.
        """
        return self._getBasisRow()._maxElementIdx(elements=self.getRowsAttrs())

    def setExpandedRowCount(self, expanded_row_count=None):
        """
        Вычисление максимального количества строк таблицы.
        """
        if expanded_row_count:
            self._attributes['ExpandedRowCount'] = expanded_row_count
        else:
            if 'ExpandedRowCount' in self._attributes:
                cur_count = int(self._attributes['ExpandedRowCount'])
                calc_count = self._maxRowIdx()+1
                # Если расчетное количество больше текущего, то
                # генератор добавил строки и значение ExpandedRowCount
                # надо увеличить
                # Ограничение количества строк 65535
                self._attributes['ExpandedRowCount'] = min(max(calc_count, cur_count), 65535)

    def setExpandedColCount(self, expanded_col_count=None):
        """
        Вычисление максимального количества колонок в строке.
        """
        if expanded_col_count:
            self._attributes['ExpandedColumnCount'] = expanded_col_count
        else:
            if 'ExpandedColumnCount' in self._attributes:
                cur_count = int(self._attributes['ExpandedColumnCount'])
                calc_count = self._maxColIdx()+1
                # Если расчетное количество больше текущего, то
                # генератор добавил колонки и значение ExpandedColumnCount
                # надо увеличить
                # Ограничение количества колонок 256
                self._attributes['ExpandedColumnCount'] = min(max(calc_count, cur_count), 256)

    def paste(self, paste, to=None):
        """
        Вставить копию атрибутов Past_ объекта внутрь текущего объекта
        по адресу to. Если to None, тогда происходит замена.
        """
        if paste['name'] == 'Range':
            return self._pasteRange(paste, to)
        else:
            print('ERROR: Error paste object attributes %s' % paste)
        return False

    def _pasteRange(self, paste, to):
        """
        Вставить Range в таблицу по адресу ячейки.
        """
        if isinstance(to, tuple) and len(to) == 2:
            to_row, to_col = to
            # Адресация ячеек задается как (row,col)
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
        Базисная строка, относительно которой происходит работа с индексами строк.
        """
        if self._basis_row is None:
            self._basis_row = v_range.icVRow(self)
        return self._basis_row

    def _getBasisCol(self):
        """
        Базисная колонка, относительно которой происходит работа с индексами колонок.
        """
        if self._basis_col is None:
            self._basis_col = v_range.icVColumn(self)
        return self._basis_col

    def getMergeCells(self):
        """
        Словарь объединенных ячеек. В качестве ключа - кортеж координаты ячейки.
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
                        # Установить координаты ячейки
                        cell_obj._row_idx = i_row+1
                        cell_obj._col_idx = i_col
                        merge_cells[cell_obj.getRegion()] = cell_obj
                    if 'MergeAcross' in cell:
                        # Учет объекдиненных ячеек ДЕЛАТЬ ОБЯЗАТЕЛЬНО!!!
                        # иначе не происходит учет предыдущих объединенных ячеек
                        i_col += int(cell['MergeAcross'])-1

        return merge_cells

    def isInMergeCell(self, row, column):
        """
        Попадает указанная ячейка в объединенную?
        """
        # Кеширование объединенных ячеек на случай попадания
        # в них при создании новой ячейки
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
        Получить объединенную ячейку на которую указывают координаты.
        """
        # Кеширование объединенных ячеек на случай попадания
        # в них при создании новой ячейки
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
        Удалить колонку.
        """
        col = self.getColumn(idx)
        if col:
            # Удалить колонку из таблицы
            result = col._delElementIdxAttr(idx - 1, 'Column')
            # Кроме этого удалить ячейку, соответствующую текущей колонке
            for i_row in range(self.getRowCount()):
                row = self.getRow(i_row+1)
                if row:
                    row.delCell(idx)
            return result
        return False

    def delRow(self, idx=-1):
        """
        Удалить строку.
        """
        row = self.getRow(idx)

        if row:
            # Удалить строку из таблицы
            return row._delElementIdxAttr(idx - 1, 'Row')
        return False


class iqVWorksheetOptions(v_prototype.iqVPrototype):
    """
    Параметры листа.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'WorksheetOptions', 'children': []}

    def getPageSetup(self):
        """
        Параметры печати.
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
        Параметры печати.
        """
        page_setup = iqVPageSetup(self)
        attrs = page_setup.create()
        return page_setup

    def getPrint(self):
        """
        Параметры принтера.
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
        Параметры принтера.
        """
        print_section = iqVPrint(self)
        attrs = print_section.create()
        return print_section

    def isFitToPage(self):
        """
        Масштаб по размещению страниц.
        """
        fit_to_page = [element for element in self._attributes['children'] if element['name'] == 'FitToPage']
        return bool(fit_to_page)


class iqVPageSetup(v_prototype.iqVPrototype):
    """
    Параметры печати.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'PageSetup', 'children': []}

    def getLayout(self):
        """
        Размещение листа.
        """
        layout = [element for element in self._attributes['children'] if element['name'] == 'Layout']
        if layout:
            return layout[0]
        return None

    def getOrientation(self):
        """
        Ориентация листа.
        """
        layout = self.getLayout()
        if layout:
            if 'Orientation' in layout:
                return layout['Orientation']
        # По умолчанию портретная ориентация
        return 'Portrait'

    def getCenter(self):
        """
        Центрирование по горизонтали/вертикали.
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

        # По умолчанию портретная ориентация
        return False, False

    def getPageMargins(self):
        """
        Поля.
        """
        margins = [element for element in self._attributes['children'] if element['name'] == 'PageMargins']
        if margins:
            return margins[0]
        return {}

    def getMargins(self):
        """
        Поля.
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
    Параметры принтера.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Print', 'children': []}

    def getPaperSizeIndex(self):
        """
        Код размера бумаги.
        """
        paper_size_lst = [element for element in self._attributes['children'] if element['name'] == 'PaperSizeIndex']
        if paper_size_lst:
            return int(paper_size_lst[0]['value'])
        # По умолчанию размер A4
        return paper_size.xlPaperA4

    def getPaperSize(self):
        """
        Размер бумаги в 0.01 мм.
        """
        paper_size_i = self.getPaperSizeIndex()
        if paper_size_i > 0:
            return paper_size.XL_PAPER_SIZE.setdefault(paper_size_i, None)
        return None

    def getScale(self):
        """
        Масштаб бумаги.
        """
        scale = [element for element in self._attributes['children'] if element['name'] == 'Scale']
        if scale:
            return int(scale[0]['value'])
        # По умолчанию масштаб 100%
        return 100

    def getFitWidth(self):
        """
        Масштаб. Разместить не более чем на X стр. в ширину.
        """
        fit_width = [element for element in self._attributes['children'] if element['name'] == 'FitWidth']
        if fit_width:
            try:
                return int(fit_width[0]['value'])
            except:
                pass
        # По умолчанию 1
        return 1

    def getFitHeight(self):
        """
        Масштаб. Разместить не более чем на X стр. в высоту.
        """
        fit_height = [element for element in self._attributes['children'] if element['name'] == 'FitHeight']
        if fit_height:
            try:
                return int(fit_height[0]['value'])
            except:
                pass
        # По умолчанию 1
        return 1

    def getFit(self):
        """
        Масштаб в размещенных страницах.
        """
        return self.getFitWidth(), self.getFitHeight()

    def getNumberofCopies(self):
        """
        Количество копий листа.
        """
        n_copies = [element for element in self._attributes['children'] if element['name'] == 'NumberofCopies']
        if n_copies:
            try:
                return int(n_copies[0]['value'])
            except:
                pass
        # По умолчанию 1
        return 1

    def setNumberofCopies(self, number_of_copies=1):
        """
        Количество копий листа.
        """
        number_of_copies = min(max(int(number_of_copies), 1), 256)
        n_copies = {'name': 'NumberofCopies', 'value': number_of_copies}
        self._attributes['children'].append(n_copies)
        return n_copies


class iqVPageBreaks(v_prototype.iqVPrototype):
    """
    Разрывы страниц.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'PageBreaks', 'children': [{'name': 'RowBreaks', 'children': []}]}

    def addRowBreak(self, row):
        """
        Добавить разрыв страницы по строке.

        :param row: Номер строки.
        """
        row_break = {'name': 'RowBreak', 'children': [{'name': 'Row', 'value': row}]}
        self._attributes['children'][0]['children'].append(row_break)
