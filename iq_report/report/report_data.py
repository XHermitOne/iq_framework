#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль подготовки данных для отчетов.

Данные организуются в следующей структуре:

data={
    '__fields__': [('имя поля1',), ('имя поля2',) ,...],    # Описания полей
    '__data__': [('Значение поля 1', 'Значение поля 2', ...), ...],     # Табличные данные (список списков)
    '__variables__': {
                    'имя  переменной1': 'значение переменной 1',
                    'имя  переменной2': 'значение переменной 2',
                    ...},   # Пространство имен
    '__coord_fill__': {
                        (строка 1, столбец 1): 'значение 1',
                        (строка 2, столбец 2): 'значение 2',
                       ...},    # Координатные замены значений ячеек
    }
Например:
data={
        '__variables__':
            {
                'form_torg': 'Бесплатная',
                'name_torg': 'Безбашенная',

                'm_name': 'Рога и копыта',
                'm_where': 'Садовая 32',
                'm_address': 'Садовая 32',
                'm_email': 'ss@mail.ru',
                'm_phone': '5-40-33',
            },
        '__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
        '__data__': [('1', 'Любой предмет', '123.45')],
    }

Значения м.б. многострочными. В этом случае они заключаются в тройные кавычки.
"""

# Подключение библиотек
import copy
import string

from ic.std.log import log

from ic.std.convert import xml2dict

__version__ = (0, 1, 1, 2)

# --- Константы ---
# --- Спецификации и структуры ---
# Структура данных для отчета
IC_REP_DATA = {
    '__fields__': list(),       # Описания полей
    '__data__': list(),         # Табличные данные (список списков)
    '__variables__': dict(),    # Пространство имен
    '__coord_fill__': None,     # Координатные замены значений ячеек
    '__sub__': dict(),          # Данные подотчетов
    }

# Структура данных подотчетов
IC_SUBREP_DATA = {
    'report': '',           # Файл шаблона отчета или описание отчета в IC_REP_TMPL
    'rep_data': dict(),     # Данные  IC_REP_DATA
    }


class icReportData:
    """
    Класс подготовки данных для отчетов.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        self._rep_data = None
        
    def convert(self, src_data):
        """
        Конвертация из первоначального представления данные в представление
            данных отчета.

        :param src_data: Исходные данные.
        """
        pass
        
    def get(self):
        """
        Получить сконвертированные данные отчета.
        """
        return self._rep_data


class icXMLReportData(icReportData):
    """
    Класс преобразования XML данных в первичные.
    """
    def __init__(self):
        """
        Конструктор.
        """
        icReportData.__init__(self)
        
    def convert(self, xml_filename):
        """
        Конвертация из первоначального представления данные в представление
            данных отчета.

        :param xml_filename: Исходные данные.
        """
        xml_data = self.open(xml_filename)
        self._rep_data = self.data_convert(xml_data)
        return self._rep_data
    
    def open(self, xml_filename):
        """
        Открыть XML файл.

        :param xml_filename: Имя XML файла данных отчета.
        """
        return xml2dict.XmlFile2Dict(xml_filename)

    def data_convert(self, Data_):
        """
        Преобразование данных из одного представления в другое.
        """
        try:
            # Создать первоначальный шаблон
            rep_data = copy.deepcopy(IC_REP_DATA)

            # --- Определение основных структур ---
            workbook = Data_['children'][0]
            # Стили (в виде словаря)
            styles = dict()
            styles_lst = [element for element in workbook['children'] if element['name'] == 'Styles']
            if styles_lst:
                styles = dict([(style['ID'], style) for style in styles_lst[0]['children']])

            worksheets = [element for element in workbook['children'] if element['name'] == 'Worksheet']
            # Получить переменные
            variables = [element for element in workbook['children'] if element['name'] == 'Variables']
            # Полчить координатные замены
            coord_values = [element for element in workbook['children'] if element['name'] == 'CoordFill']

            rep_worksheet = worksheets[0]
            rep_data_tab = rep_worksheet['children'][0]
            # Список строк
            rep_data_rows = [element for element in rep_data_tab['children'] if element['name'] == 'Row']
            # Список колонок
            rep_data_cols = [element for element in rep_data_tab['children'] if element['name'] == 'Column']
            if not rep_data_cols:
                # Если колонки не определены в файле данных,
                # то автоматом сгенерировать список колонок
                col_count = max([len(row['children']) for row in rep_data_rows])
                for col in range(col_count):
                    rep_data_cols.append({'name': 'Column'})

            # --- Заполнение ---
            rep_data['fields'] = self._getFields(rep_data_cols)
            rep_data['data'] = self._getData(rep_data_rows)
            rep_data['__variables__'] = self._getVariables(variables[0]['children'])
            rep_data['__coord_fill__'] = self._getCoordFill(coord_values[0]['children'])
            
            return rep_data
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка преобразования данных отчета.')
            return None
        
    FIELD_NAMES = string.ascii_uppercase

    def _getFields(self, columns):
        """
        Получить описания полей. Поля заполняются по колонкам.
        """
        try:
            fields = list()
            i_name = 0
            for col in columns:
                field = list()
                # Имя поля
                if 'Name' in col:
                    name = col['Name']
                else:
                    name = self.FIELD_NAMES[i_name]
                i_name += 1
                field.append(name)
                # Тип поля
                field.append('String')
                fields.append(tuple(field))
            return fields
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения описания полей.')
            return None
        
    def _getData(self, rows):
        """
        Получить данные.
        """
        try:
            data = list()
            i_rec = 0
            for row in rows:
                rec = list()
                
                # Отслеживание пустых участков
                if 'Index' in row:
                    idx = int(row['Index'])
                    if idx > i_rec:
                        data += [[]]*(idx-i_rec)
                # Заполнение записи
                for cell in row['children']:
                    cell_data = None
                    if 'value' in cell['children'][0]:
                        cell_data = cell['children'][0]['value']
                    rec.append(cell_data)
                    
                data.append(rec)
                i_rec = len(data)
                
            return data
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения данных отчета.')
            return None
        
    def _getVariables(self, variables):
        """
        Переменные пространства имен.
        """
        try:
            variables = dict([(var['Name'], var['value']) for var in variables])
            return variables
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения переменных пространства имен отчета.')
            return None

    def _getCoordFill(self, coord_values):
        """
        Координатные замены значений ячеек.
        """
        try:
            coord_fill = dict([((int(fill['Row']), int(fill['Col'])),
                                fill['value']) for fill in coord_values])
            return coord_fill
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения координатных замен отчета.')
            return None
