#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

try:
    from . import v_prototype
except ImportError:
    # Для запуска тестов
    import icprototype

try:
    # Если Virtual Excel работает в окружении icReport
    from ic.std.log import log
except ImportError:
    # Если Virtual Excel работает в окружении DEFIS
    from ic.log import log

__version__ = (0, 1, 2, 1)


class icVCell(v_prototype.iqVIndexedPrototype):
    """
    Ячейка.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVIndexedPrototype.__init__(self, parent, *args, **kwargs)

        self._attributes = {'name': 'Cell', 'children': []}

        self._colsA1 = []   # Имена колонок Excel в формате A1

        self._row_idx = -1  # Индекс ячейки в строках
        self._col_idx = -1  # Индекся ячейки в колонках

    def createData(self):
        """
        Создать данные ячейки.
        """
        data = iqVData(self)
        attrs = data.create()
        return data

    def getDataAttrs(self):
        """
        Данные ячейки.
        """
        return [element for element in self._attributes['children'] if element['name'] == 'Data']

    def getDataCount(self):
        """
        Количество данных ячейки.
        """
        return len(self.getDataAttrs())

    def getData(self):
        """
        Данные ячейки.
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
        Значение ячейки.
        """
        data = self.getData()
        return data.getValue()

    def isFormula(self, value):
        """
        Проверка является ли значение формулой.

        :param value: Проверяемое значение.
        """
        return type(value) == str and bool(value) and value[0] == '='
    
    def setValue(self, value, value_type='String'):
        """
        Записать значение в ячейку.
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
        Установить стиль.
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
        Стиль ячейки.
        """
        style = None
        if 'StyleID' in self._attributes:
            # Взять стиль из списка стилей
            my_workbook = self.getParentByName('Workbook')
            style = my_workbook.getStyles().getStyle(self._attributes['StyleID'])
            self._attributes['StyleID'] = style.getAttributes()['ID']
        else:
            # Создать новый стиль
            my_workbook = self.getParentByName('Workbook')
            style = my_workbook.getStyles().createStyle()
            self._attributes['StyleID'] = style.getAttributes()['ID']
        return style

    def setStyleID(self, style_id):
        """
        Установить идентификатор стиля для ячейки.
        """
        if style_id:
            self._attributes['StyleID'] = str(style_id)

    def getStyleID(self):
        """
        Идентификатор стиля ячейки.
        """
        if 'StyleID' in self._attributes:
            return self._attributes['StyleID']
        return None

    def _get_col_name_A1_lst(self):
        """
        Возвращает список имен колонок.
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

    def _get_row_col_A1(self, addr):
        """
        Преобразут Excel адрес к картежу (ряд, колонка).
        """
        lst = self._get_col_name_A1_lst()
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
        Конвертация адресации ячеек из формата A1 в формат R1C1.
        """
        parse_all = re.findall(self.A1_FORMAT, formula)
        for replace_addr in parse_all:
            r1c1 = 'R%dC%d' % self._get_row_col_A1(replace_addr)
            formula = formula.replace(replace_addr, r1c1)
        return formula

    def setFormulaR1C1(self, formula):
        """
        Установить формулу в формате RC.
        """
        self._attributes['Formula'] = self._A1Fmt2R1C1Fmt(formula)

    def setMerge(self, across, down):
        """
        Установить объединение ячеек.
        """
        # Удалить ячейки попавшие в зону объединения.
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

        # ВНИМАНИЕ!!!
        # После объединения необходимо почистить словарь объединенных ячеек
        # table=self.getParentByName('Table')
        # table._merge_cells=None

    def _delMergeArreaCells(self, row, column, merge_down, merge_across):
        """
        Удалить ячейки попавшие в зону объединения.

        :param row: Номер строки.
        :param column: Номер колонки.
        :param merge_down: Количество строк объединения.
        :param merge_across: Количество колонок объединения.
        """
        table = self.getParentByName('Table')
        for i_row in range(row, row + merge_down + 1):
            row_obj = table.getRow(i_row)
            for i_col in range(column, column + merge_across + 1):
                if not (i_row == row and i_col == column):
                    row_obj._delElementIdxAttrChild(i_col-1, 'Cell', False)

    def _findElementIdxAttr(self, idx, element_name):
        """
        Найти атрибуты ячеки в строке по индексу.
        ВНИМАНИЕ! В этой функции индексация начинается с 0.
        """
        indexes = []
        cur_idx = 0
        for i, cell_attr in enumerate(self._parent.getAttributes()['children']):
            if 'Index' in cell_attr:
                cur_idx = int(cell_attr['Index'])
            else:
                cur_idx += 1

            indexes.append(cur_idx)

            # Учет объединенных ячеек
            if 'MergeAcross' in cell_attr:
                cur_idx += int(cell_attr['MergeAcross'])

        if idx in indexes:
            # Ячейка с указанным индексом есть
            return indexes, self._parent.getAttributes()['children'][indexes.index(idx)]
        return indexes, None

    def getOffset(self, offset_row=0, offset_column=0):
        """
        Получить ячейку по смещению с учетом объединенных ячеек.

        :param offset_row: Смещение по строкам.
        :param offset_column: Смещение по колонкам.
        :return: Возвращает объект ячейки по смещению или None в случае ошибки.
        """
        if offset_row <= 0 and offset_column <= 0:
            return self
        # Определение адреса новой ячейки
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
        Адрес ячейки.

        :return: Возвращает кортеж (номер строки, номер колонки).
        """
        return self._row_idx, self._col_idx

    def getRegion(self):
        """
        Область ячеки=Адрес ячейки + количество объединненных строк и колонок.

        :return: Возвращает кортеж
            (номер строки, номер колонки,
            объединненных строк, объединенных колонок).
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
        Следующая ячейка за текущей по горизонтали.
        """
        return self.getOffset(0, 1)

    def set_xmlns(self, xmlns='http://www.w3.org/TR/REC-html40'):
        """
        Установить способ форматирования текста в ячейке.
        """
        data = self.getData()
        data.set_xmlns(xmlns)


DEFAULT_PERCENTAGE_TYPE = 'Percentage'
DEFAULT_NUMBER_TYPE = 'Number'


class iqVData(v_prototype.iqVPrototype):
    """
    Данные ячейки.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Data', 'value': None, 'Type': 'String', 'children': []}

    def getValue(self):
        """
        Значение.
        """
        return self._attributes['value']

    def _isPersentageType(self):
        """
        ВНИМАНИЕ! Здесь идет проверка на принадлежность данных к процентному типу
        т. к. нет возможности отделить проценты от числовых типов
        """
        analize_type = self.getAttributes().get('Type', '').lower().title() == DEFAULT_PERCENTAGE_TYPE
        
        style = self.getParent().getStyle()
        number_format = style.findChildAttrsByName('NumberFormat')
        analize_style = number_format and 'Format' in number_format and \
            (('%' in number_format['Format']) or ('Percent' in number_format['Format']))
        return analize_type or analize_style
    
    def setValue(self, value, value_type='String'):
        """
        Установить значение.
        """
        val = value
        val_type = value_type
        
        if self._isPersentageType():
            # ВНИМАНИЕ! Здесь идет проверка на принадлежность данных к процентному типу
            # т. к. нет возможности отделить проценты от числовых типов
            val_type = DEFAULT_PERCENTAGE_TYPE
        elif type(value) in (int, float):
            val_type = DEFAULT_NUMBER_TYPE
        # elif isinstance(value, text):
        #    val = val.encode(self.getApp().encoding)
        
        # Обработка формул
        if self.getParent().isFormula(value):
            self.getParent().setFormulaR1C1(value)
            if self._isPersentageType():
                val_type = DEFAULT_PERCENTAGE_TYPE
            else:
                val_type = DEFAULT_NUMBER_TYPE

        self._attributes['value'] = str(val)
        self._attributes['Type'] = val_type

    def set_xmlns(self, xmlns='http://www.w3.org/TR/REC-html40'):
        """
        Установить способ форматирования текста в ячейке.
        """
        self._attributes['xmlns'] = str(xmlns)


if __name__ == '__main__':
    cell = icVCell(None)
    print(u'Cell address BI40: %s' % cell._get_row_col_A1('BI40'))
