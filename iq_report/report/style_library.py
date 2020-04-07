#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль библиотеки стилей для отчетов.
"""

import copy
import string

from ic.std.log import log
from ic.std.convert import xml2dict

from ic.report import icreptemplate

__version__ = (0, 1, 1, 2)

# Стиль
IC_REP_STYLE = {'font': None,   # Шрифт Структура типа ic.components.icfont.SPC_IC_FONT
                'color': None,  # Цвет
                # 'border':None, #Обрамление
                # 'align':None, #Расположение текста
                # 'num_format': None, #Формат ячейки
                }


class icRepStyleLib(icreptemplate.icReportTemplate):
    """
    Класс библиотеки стилей для отчетов.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        icreptemplate.icReportTemplate.__init__(self)
        self._style_lib = {}
        
    def convert(self, src_data):
        """
        Конвертация из XML представления библиотеки стилей в представление
            библиотеки стилей отчета.

        :param src_data: Исходные данные.
        """
        pass
        
    def get(self):
        """
        Получить сконвертированные данные библиотеки стилей отчета.
        """
        return self._style_lib


class icXMLRepStyleLib(icRepStyleLib):
    """
    Класс преобразования XML библиотеки стилей для отчетов.
    """
    def __init__(self):
        """
        Конструктор.
        """
        icRepStyleLib.__init__(self)

    def open(self, xml_filename):
        """
        Открыть XML файл.

        :param xml_filename: Имя XML файла библиотеки стилей отчета.
        """
        return xml2dict.XmlFile2Dict(xml_filename)

    def convert(self, xml_filename):
        """
        Конвертация из XML файла в представление библиотеки стилей отчета.

        :param xml_filename: Исходные данные.
        """
        xml_data = self.open(xml_filename)
        self._style_lib = self.covert_data(xml_data)
        return self._style_lib

    def covert_data(self, data):
        """
        Преобразование данных из одного представления в другое.
        """
        try:
            style_lib = {}
            
            # Определение основных структур
            workbook = data['children'][0]
            # Стили (в виде словаря)
            styles = {}
            styles_lst = [element for element in workbook['children'] if element['name'] == 'Styles']
            if styles_lst:
                styles = dict([(style['ID'], style) for style in  styles_lst[0]['children']])

            worksheets = [element for element in workbook['children'] if element['name'] == 'Worksheet']

            rep_worksheet = worksheets[0]
            rep_data_tab = rep_worksheet['children'][0]
            # Список строк
            rep_data_rows = [element for element in rep_data_tab['children'] if element['name'] == 'Row']

            # Заполнение
            style_lib = self._getStyles(rep_data_rows, styles)
            return style_lib
        except:
            # Вывести сообщение об ошибке в лог
            log.error(u'Ошибка преобразования данных библиотеки стилей отчета.')
            return None

    # Разрешенные символы в именах тегов стилей
    LATIN_CHARSET = string.ascii_uppercase+string.ascii_lowercase+string.digits+'_'

    def _isStyleTag(self, value):
        """
        Определить является ли значение тегом стиля.

        :param value: Строка-значение в ячейке.
        :return: True/False.
        """
        for symbol in value:
            if symbol not in self.LATIN_CHARSET:
                return False
        return True

    def _getStyles(self, rows, styles):
        """
        Определить словарь стилей.

        :param rows: Список строк в XML.
        :param styles: Словарь стилей в XML.
        """
        new_styles = {}
        for row in rows:
            for cell in row['children']:
                # Получить значение
                value = cell['children'][0]['value']
                # Обрабатывать только строковые значения
                if value and isinstance(value, str):
                    if self._isStyleTag(value):
                        style_id = cell['StyleID']
                        new_styles[value] = self._getStyle(style_id, styles)
        return new_styles
                            
    def _getStyle(self, style_id, styles):
        """
        Определить стиль по его идентификатору.

        :param style_id: Идентификатор стиля в XML описании.
        :param styles: Словарь стилей в XML.
        """
        style = copy.deepcopy(IC_REP_STYLE)
        
        if style_id in styles:
            style['font'] = self._getFontStyle(styles[style_id])
            style['color'] = self._getColorStyle(styles[style_id])
            # style['border']=self._getBordersStyle(styles[style_id])
            # style['align']=self._getAlignStyle(styles[style_id])
            # style['num_format']=self._getFmtStyle(styles[style_id])
        return style
