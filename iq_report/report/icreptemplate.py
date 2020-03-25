#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль шаблона отчетов.
"""

# Подключение библиотек
import os.path
import string
import copy
import pickle
import re

from ic.std.log import log
from ic.std.convert import xml2dict
from ic.std.utils import execfunc
from ic.std.utils import textfunc

from ic.report import icrepgen

__version__ = (0, 1, 1, 2)

# Константы
# Теги шаблона
DESCRIPTION_TAG = '[description]'   # Описание
VAR_TAG = '[var]'                   # Бэнд переменных
GENERATOR_TAG = '[generator]'       # Бэнд указания системы генерации
DATASRC_TAG = '[data_source]'       # Бэнд указания источника данных для отчета/БД
QUERY_TAG = '[query]'               # Бэнд указания запроса для получения таблицы запроса
STYLELIB_TAG = '[style_lib]'        # Бэнд указания библиотеки стилей

HEADER_TAG = '[header]'             # Бэнд заголовка отчета (Координаты и размер)
FOOTER_TAG = '[footer]'             # Бэнд подвала/примечания отчета (Координаты и размер)
DETAIL_TAG = '[detail]'             # Бэнд области данных (Координаты и размер)
HEADER_GROUP_TAG = '[head_grp]'     # Список бэндов групп (Координаты и размер)
FOOTER_GROUP_TAG = '[foot_grp]'     # Список бэндов групп (Координаты и размер)
UPPER_TAG = '[upper]'               # Бэнд верхнего колонтитула (Координаты и размер)
UNDER_TAG = '[under]'               # Бэнд нижнего колонтитула (Координаты и размер)

# Список всех тегов
ALL_TAGS = [DESCRIPTION_TAG, VAR_TAG, GENERATOR_TAG, DATASRC_TAG, QUERY_TAG, STYLELIB_TAG,
            HEADER_TAG, FOOTER_TAG, DETAIL_TAG,
            HEADER_GROUP_TAG, FOOTER_GROUP_TAG, UPPER_TAG, UNDER_TAG]
    
# Заголовочные теги
TITLE_TAGS = [DESCRIPTION_TAG, VAR_TAG, GENERATOR_TAG, DATASRC_TAG, QUERY_TAG, STYLELIB_TAG]

# ВНИМАНИЕ: Коэффициенты для преобразования ширины и высоты
# колонок и строк получены экспериментальным путем. М.б. уточнены.
IC_XL_COEF_WIDTH = 2
IC_XL_COEF_HEIGHT = 2

# Параметры заполнения по умолчанию
DEFAULT_FIT_WIDTH = 1
DEFAULT_FIT_HEIGHT = 1

# Плотность печати
DEFAULT_HORIZ_RESOLUTION = 300
DEFAULT_VERT_RESOLUTION = 300

DEFAULT_REPORT_FILE_EXT = '.rprt'

TRANSPARENT_COLOR = 'transparent'

CODE_SIGNATURE = 'PRG:'
PY_SIGNATURE = 'PY:'


class icReportTemplate:
    """
    Класс шаблона отчета.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        # Структура шаблона отчета,  которую понимает генератор отчетов.
        self._rep_template = None

        # Полное имя исходного файла шаблона
        self.template_filename = None

    def setTemplateFilename(self, template_filename):
        """
        Полное имя исходного файла шаблона.

        :param template_filename: Полное имя исходного файла шаблона
        """
        self.template_filename = template_filename

    def getTemplateFilename(self):
        """
        Полное имя исходного файла шаблона.
        """
        return self.template_filename

    def save(self, template_filename, template_name=None):
        """
        Сохранить шаблон в Pickle файле.

        :param template_filename: Имя XML файла шаблона.
        :param template_name: Имя шаблона (листа).
        """
        pickle_file_name = os.path.splitext(template_filename)[0]+DEFAULT_REPORT_FILE_EXT
        pickle_file = None
        try:
            pickle_file = open(pickle_file_name, 'wb')
            pickle.dump(self._rep_template, pickle_file)
            pickle_file.close()
        except:
            if pickle_file:
                pickle_file.close()

    def load(self, template_filename, template_name=None):
        """
        Загрузить шаблон из Pickle файла.

        :param template_filename: Имя XML файла шаблона.
        :param template_name: Имя шаблона (листа).
        """
        self.setTemplateFilename(template_filename)
        pickle_file_name = os.path.splitext(template_filename)[0]+DEFAULT_REPORT_FILE_EXT
        pickle_file = None
        try:
            pickle_file = open(pickle_file_name, 'rb')
            self._rep_template = pickle.load(pickle_file)
            pickle_file.close()
        except:
            if pickle_file:
                pickle_file.close()

    def mustRenew(self, template_filename, template_name=None):
        """
        Надо обновить Pickle файл шаблона отчета?

        :param template_filename: Имя XML файла шаблона.
        :param template_name: Имя шаблона (листа).
        :return: True-необходимо обновление. False-обновлять не надо.
        """
        pickle_file_name = os.path.splitext(template_filename)[0]+DEFAULT_REPORT_FILE_EXT
        if not os.path.exists(pickle_file_name) or os.path.getsize(pickle_file_name) < 10:
            # 1. Pickle файл не существует, значит надо сделать обновление
            # 2. Подразумевается что размер шаблона не может быть меньше 10 байт,
            # иначе там записан None или пустой словарь
            return True
        # Проверка на время создания xml шаблона
        xml_create_time = os.path.getmtime(template_filename)
        rtp_create_time = os.path.getmtime(pickle_file_name)
        return xml_create_time > rtp_create_time
        
    def read(self, tmpl_filename, template_name=None):
        """
        Прочитать файл шаблона отчета.

        :param tmpl_filename: Файл шаблона отчета.
        :param template_name: Имя шаблона (листа).
        """
        pass

    def get(self):
        """
        Получить подготовленные данные шаблона отчета.
        """
        return self._rep_template

    _lineStyle = {'Continuous': icrepgen.IC_REP_LINE_SOLID,
                  'Dash': icrepgen.IC_REP_LINE_SHORT_DASH,
                  'DashDot': icrepgen.IC_REP_LINE_DOT_DASH,
                  'Dot': icrepgen.IC_REP_LINE_DOT,
                  }

    def _getLineStyle(self, line_style):
        """
        Перекодировать стиль.
        """
        return self._lineStyle.setdefault(line_style, icrepgen.IC_REP_LINE_TRANSPARENT)
        
    def _getBordersStyle(self, style):
        """
        Определить границы ячейки из стиля.

        :param style: Описание стиля.
        """
        style_border = [style_attr for style_attr in style['children'] if style_attr['name'] == 'Borders']
        if style_border:
            style_border = style_border[0]['children']
        else:
            style_border = []
            
        borders = [None, None, None, None]
        for border in style_border:
            if 'Position' in border:
                cur_border = dict()
                if border['Position'] == 'Left':
                    borders[0] = {}
                    cur_border = borders[0]
                elif border['Position'] == 'Top':
                    borders[1] = {}
                    cur_border = borders[1]
                elif border['Position'] == 'Bottom':
                    borders[2] = {}
                    cur_border = borders[2]
                elif border['Position'] == 'Right':
                    borders[3] = {}
                    cur_border = borders[3]
                # Заполнение описния
                if 'LineStyle' in border:
                    cur_border['style'] = self._getLineStyle(border['LineStyle'])
                if 'Weight' in border:
                    cur_border['weight'] = int(round(float(border['Weight'])))
    
        return tuple(borders)
        
    def _getFontStyle(self, style):
        """
        Взять описание шрифта из стиля.

        :param style: Описание стиля.
        """
        # Шрифт описанный в стиле
        style_font = [style_attr for style_attr in style['children'] if style_attr['name'] == 'Font']
        log.debug('Font <%s> Style <%s>' % (style_font, style['ID']))
        if style_font:
            style_font = style_font[0]
        else:
            style_font = {}
        
        # Выходная структура шрифта
        font = {'name': 'Arial Cyr',
                'size': 10,
                'family': 'default',
                'faceName': None,
                'underline': False,
                'style': 'regular',
                }
        if 'FontName' in style_font:
            font['name'] = style_font['FontName']
            font['faceName'] = style_font['FontName']
        if 'Size' in style_font:
            font['size'] = float(style_font['Size'])

        if 'Underline' in style_font:
            font['underline'] = True
    
        if 'Bold' in style_font and style_font['Bold'] == '1':
            style = 'bold'
            if 'Italic' in style_font and style_font['Italic'] == '1':
                style = 'boldItalic'
            font['style'] = style
        elif 'Italic' in style_font and style_font['Italic'] == '1':
            font['style'] = 'italic'
            
        return font
        
    def _getColorRGB(self, color):
        """
        Преобразование цвета из #RRGGBB в (R,G,B).
        """
        if color.strip().lower() == TRANSPARENT_COLOR:
            return None
        return int('0x'+color[1:3], 16), int('0x'+color[3:5], 16), int('0x'+color[5:7], 16)
        
    def _getColorStyle(self, style):
        """
        Определить цвет, определенный в стиле.

        :param style: Описание стиля.
        """
        color = {}
        # Шрифт описанный в стиле
        style_font = [style_attr for style_attr in style['children'] if style_attr['name'] == 'Font']
        if style_font:
            style_font = style_font[0]
        else:
            style_font = {}
            
        if 'Color' in style_font:
            color['text'] = self._getColorRGB(style_font['Color'])
        else:
            # Цвет текста по умолчанию ЧЕРНЫЙ
            color['text'] = (0, 0, 0)
            
        # Интерьер описанный в стиле
        style_interior = [style_attr for style_attr in style['children'] if style_attr['name'] == 'Interior']
        if style_interior:
            style_interior = style_interior[0]
        else:
            style_interior = {}

        if 'Color' in style_interior:
            color['background'] = self._getColorRGB(style_interior['Color'])
        else:
            # Цвет фона по умолчанию БЕЛЫЙ
            color['background'] = None
        return color

    def _getAlignStyle(self, style):
        """
        Определить размещение.

        :param style: Описание стиля.
        """
        style_align = [style_attr for style_attr in style['children'] if style_attr['name'] == 'Alignment']
        if style_align:
            style_align = style_align[0]
        else:
            style_align = {}
        
        align = {'align_txt': [icrepgen.IC_HORIZ_ALIGN_LEFT, icrepgen.IC_VERT_ALIGN_CENTRE],
                 'wrap_txt': False,
                 }
        # Выравнивание текста
        if 'Horizontal' in style_align:
            if style_align['Horizontal'] == 'Left':
                align['align_txt'][0] = icrepgen.IC_HORIZ_ALIGN_LEFT
            elif style_align['Horizontal'] == 'Right':
                align['align_txt'][0] = icrepgen.IC_HORIZ_ALIGN_RIGHT
            elif style_align['Horizontal'] == 'Center':
                align['align_txt'][0] = icrepgen.IC_HORIZ_ALIGN_CENTRE
        if 'Vertical' in style_align:
            if style_align['Vertical'] == 'Top':
                align['align_txt'][1] = icrepgen.IC_VERT_ALIGN_TOP
            elif style_align['Vertical'] == 'Bottom':
                align['align_txt'][1] = icrepgen.IC_VERT_ALIGN_BOTTOM
            elif style_align['Vertical'] == 'Center':
                align['align_txt'][1] = icrepgen.IC_VERT_ALIGN_CENTRE
        align['align_txt'] = tuple(align['align_txt'])
        # Перенос по словам
        if 'WrapText' in style_align and style_align['WrapText'] == '1':
            align['wrap_txt'] = True

        return align

    def _getFmtStyle(self, style):
        """
        Определить формат ячейки.
        """
        style_fmt = [style_attr for style_attr in style['children'] if style_attr['name'] == 'NumberFormat']
        if style_fmt:
            style_fmt = style_fmt[0]
        else:
            style_fmt = {}
        
        if 'Format' in style_fmt:
            return icrepgen.REP_FMT_EXCEL+style_fmt['Format']
        return icrepgen.REP_FMT_NONE

    def _getPageSetup(self, page_setup):
        """
        Определить параметры страницы.
        """
        new_page_setup = {}
        # Ориентиция
        layouts = [obj for obj in page_setup['children'] if obj['name'] == 'Layout']
        log.debug('Layout %s' % layouts)
        if layouts:
            layout = layouts[0]
            if 'Orientation' in layout:
                if layout['Orientation'] == 'Landscape':
                    new_page_setup['orientation'] = icrepgen.IC_REP_ORIENTATION_LANDSCAPE
                elif layout['Orientation'] == 'Portrait':
                    new_page_setup['orientation'] = icrepgen.IC_REP_ORIENTATION_PORTRAIT
            # Начало нумерации страниц
            if 'StartPageNumber' in layout:
                new_page_setup['start_num'] = int(layout['StartPageNumber'])
        # Поля
        page_margins = [obj for obj in page_setup['children'] if obj['name'] == 'PageMargins']
        log.debug('PageMargins %s' % page_margins)
        if page_margins:
            page_margin = page_margins[0]
            new_page_setup['page_margins'] = []
            new_page_setup['page_margins'].append(float(page_margin.get('Left', 0)))
            new_page_setup['page_margins'].append(float(page_margin.get('Right', 0)))
            new_page_setup['page_margins'].append(float(page_margin.get('Top', 0)))
            new_page_setup['page_margins'].append(float(page_margin.get('Bottom', 0)))
            new_page_setup['page_margins'] = tuple(new_page_setup['page_margins'])

        return new_page_setup

    def _getPrintSetup(self, print_setup):
        """
        Определить параметры страницы.
        """
        new_print_setup = {}
        # Размер бумаги
        paper_sizes = [obj for obj in print_setup['children'] if obj['name'] == 'PaperSizeIndex']
        if paper_sizes:
            new_print_setup['paper_size'] = paper_sizes[0]['value']
        # Масштаб
        scales = [obj for obj in print_setup['children'] if obj['name'] == 'Scale']
        if scales:
            new_print_setup['scale'] = int(scales[0]['value'])
        else:
            # Параметры заполнения
            try:
                h_fit = [obj for obj in print_setup['children'] if obj['name'] == 'FitWidth'][0]['value']
            except:
                h_fit = DEFAULT_FIT_WIDTH
            try:
                v_fit = [obj for obj in print_setup['children'] if obj['name'] == 'FitHeight'][0]['value']
            except:
                v_fit = DEFAULT_FIT_HEIGHT
            new_print_setup['fit'] = (int(h_fit), int(v_fit))
        # Плотность печати
        try:
            h_resolution = [obj for obj in print_setup['children'] if obj['name'] == 'HorizontalResolution'][0]['value']
        except:
            h_resolution = DEFAULT_HORIZ_RESOLUTION
        try:    
            v_resolution = [obj for obj in print_setup['children'] if obj['name'] == 'VerticalResolution'][0]['value']
        except:
            v_resolution = DEFAULT_VERT_RESOLUTION
        new_print_setup['resolution'] = (int(h_resolution), int(v_resolution))

        return new_print_setup


class icExcelXMLReportTemplate(icReportTemplate):
    """
    Шаблон отчета в формате Excel XMLSpreadSheet.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        icReportTemplate.__init__(self)
        
        # Номер колонки тегов бендов
        self._tag_band_col = None
        # Тег текущего бенда
        self.__cur_band = None
        
        # Текущий обрабоатываемый лист шаблона отчета
        self._rep_worksheet = None

        # Ширина колонки с повторяющимися атрибутами
        self._column_span_width = None
        # Высота строки с повторяющимися атрибутами
        self._row_span_height = 12.75
        
        # Ширина колонки по умолчанию
        self._default_column_width = None
        # Высота строки по умолчанию
        self._default_row_height = 12.75

    def read(self, tmpl_filename, template_name=None):
        """
        Прочитать файл шаблона отчета.

        :param tmpl_filename: Файл шаблона отчета.
        :param template_name: Имя шаблона (листа).
        """
        if self.mustRenew(tmpl_filename, template_name):
            # Надо обновить шаблон
            template_data = self.open(tmpl_filename)
            self._rep_template = self.parse(template_data, template_name)
            self.save(tmpl_filename, template_name)
        else:
            # Можно просто загрузить из Pickle файла
            self.load(tmpl_filename, template_name)
        return self._rep_template

    def open(self, tmpl_filename):
        """
        Открыть файл шаблона отчета.

        :param tmpl_filename: Файл шаблона отчета.
        """
        return xml2dict.XmlFile2Dict(tmpl_filename)

    def _normList(self, data_list, element_name, length=None):
        """
        Нормализация списка.

        :param length: Максимальная длина списка, если указана, то
            список нормализуется до максимальной длины.
        """
        element_template = {'name': element_name}
        lst = []
        for i in range(len(data_list)):
            element = data_list[i]
            # Проверка индексов
            if 'Index' in element:
                if int(element['Index']) > len(lst):
                    lst += [element_template] * (int(element['Index'])-len(lst)-1)
            lst.append(element)
            # Проверка на объединенные ячейки
            if 'MergeAcross' in element:
                lst += [element_template] * int(element['MergeAcross'])
                
        if length:
            if length > len(lst):
                # Удлинить
                lst += [element_template]*(length - len(lst))
        return lst
        
    def _normTable(self, table):
        """
        Нормализация (приведение к квадратному виду) таблицы.
        """
        new_table = {}.fromkeys([key for key in table.keys() if key != 'children'])
        for key in new_table.keys():
            new_table[key] = table[key]
        new_table['children'] = []
        # Колонки
        cols = [element for element in table['children'] if element['name'] == 'Column']
        cols = self._normList(cols, 'Column')
        max_len = len(cols)
        # Строки
        rows = [element for element in table['children'] if element['name'] == 'Row']
        rows = self._normList(rows, 'Row')
        # Ячейки
        for i_row in range(len(rows)):
            row = rows[i_row]
            if 'children' in row:
                rows[i_row]['children'] = self._normList(row['children'], 'Cell', max_len)

        new_table['children'] += cols
        new_table['children'] += rows
        return new_table

    def _defineSpan(self, obj_list):
        """
        Задублировать описания объектов с указанием атрибута Span.

        :param obj_list: Список описаний объектов.
        :return: Список с добавленными дубликатами объектов.
        """
        result = list()
        for obj in obj_list:
            if 'Span' in obj:
                # ВНИМАНИЕ! Это учет объекта описание которого мы используем
                #                         v
                span = int(obj['Span']) + 1
                new_obj = copy.deepcopy(obj)
                del new_obj['Span']
                result += [new_obj] * span
            else:
                result.append(obj)
        return result

    def parse(self, template_data, template_name=None):
        """
        Разобрать/преобразовать прочитанную структуру.

        :param template_data: Словарь описания шаблона.
        :param template_name: Имя шаблона(листа), если None то первый лист.
        """
        try:
            # Создать первоначальный шаблон
            rep = copy.deepcopy(icrepgen.IC_REP_TMPL)

            # 0. Определение основных структур
            workbook = template_data['children'][0]
            # Стили (в виде словаря)
            styles = dict([(style['ID'], style) for style in [element for element in workbook['children']
                                                              if element['name'] == 'Styles'][0]['children']])
            worksheets = [element for element in workbook['children'] if element['name'] == 'Worksheet']

            # I. Определить все бэнды в шаблоне
            # Если имя шаблона не определено, тогда взять первый лист
            if template_name is None:
                template_name = worksheets[0]['Name']
                self._rep_worksheet = worksheets[0]
            else:
                # Установить активной страницу выбранного шаблона отчета
                self._rep_worksheet = [sheet for sheet in worksheets if sheet['Name'] == template_name][0]
            # Прописать имя отчета
            rep['name'] = template_name
            
            # Взять таблицу
            rep_template_tabs = [rep_obj for rep_obj in self._rep_worksheet['children'] if rep_obj['name'] == 'Table']
            self._setDefaultCellSize(rep_template_tabs[0])
            # Привести таблицу к нормальному виду
            rep_template_tab = self._normTable(rep_template_tabs[0])

            # Взять описания колонок
            rep_template_cols = [element for element in rep_template_tab['children'] if element['name'] == 'Column']
            rep_template_cols = self._defineSpan(rep_template_cols)
            # Взять описания строк
            rep_template_rows = [element for element in rep_template_tab['children'] if element['name'] == 'Row']
            rep_template_rows = self._defineSpan(rep_template_rows)

            # Количество колонок без колонки тегов бендов
            col_count = self._getColumnCount(rep_template_rows)
            log.debug(u'Количество колонок: %d' % col_count)

            # II. Определить все ячейки листа
            used_rows = range(len(rep_template_rows))
            used_cols = range(col_count)

            self.__cur_band = None  # Тег текущего бенда
            # Перебор по строкам
            for cur_row in used_rows:
                if not self._isTitleBand(rep_template_rows, cur_row):
                    # Не колонтитулы, добавить ячейки в общий лист
                    rep['sheet'].append([])
                    for cur_col in used_cols:
                        cell_attr = self._getCellAttr(rep_template_rows, rep_template_cols, styles, cur_row, cur_col)
                        if not self._isTag(cell_attr['value']):
                            rep['sheet'][-1].append(cell_attr)
                        else:
                            rep['sheet'][-1].append(None)

            # III. Определить бэнды в шаблоне
            # Перебрать все ячейки первой колонки
            self.__cur_band = None  # Тег текущего бенда
            title_row = 0   # Счетчик строк колонтитулов/заголовочных бендов
    
            # Перебор всех строк в шаблоне
            for cur_row in range(len(rep_template_rows)):
                tag = self._getTagBandRow(rep_template_rows, cur_row)
                # Если это ячейка с определенным тегом, значит новый бенд
                if tag:
                    # Определить текущий бэнд
                    self.__cur_band = tag
                    if tag in TITLE_TAGS:
                        # Обработка строк заголовочных тегов
                        parse_func = self._TitleTagParse.setdefault(tag, None)
                        try:
                            parse_func(self, rep, rep_template_rows[cur_row]['children'])
                        except:
                            log.fatal(u'Ошибка парсинга функции <%s>' % textfunc.toUnicode(parse_func))
                        title_row += 1
                    else:
                        # Определить бэнд внутри объекта
                        rep = self._defBand(self.__cur_band, cur_row, col_count, title_row, rep)
                else:
                    log.error(u'Не корректный тег <%s> строки [%d]' % (tag, cur_row))

            # Прочитать в шаблон параметры страницы
            rep['page_setup'] = copy.deepcopy(icrepgen.IC_REP_PAGESETUP)
            sheet_options = [rep_obj for rep_obj in self._rep_worksheet['children']
                             if rep_obj['name'] == 'WorksheetOptions']

            page_setup = [rep_obj for rep_obj in sheet_options[0]['children'] if rep_obj['name'] == 'PageSetup'][0]
            rep['page_setup'].update(self._getPageSetup(page_setup))
            print_setup = [rep_obj for rep_obj in sheet_options[0]['children'] if rep_obj['name'] == 'Print']
            if print_setup:
                rep['page_setup'].update(self._getPrintSetup(print_setup[0]))

            # Проверить заполнение генератора отчета
            if not rep['generator']:
                tmpl_filename = self.getTemplateFilename()
                rep['generator'] = os.path.splitext(tmpl_filename)[1].upper() if tmpl_filename else '.ODS'

            return rep
        except:
            log.fatal(u'Ошибка парсинга шаблона отчета <%s>' % textfunc.toUnicode(template_name))
        return None

    def _existTagBand(self):
        """
        Присутствует в шаблоне колонка тегов бендов?
            Если не существует, то далее считаем,
            что весь шаблон - это  заголовок отчета [header].

        :return: True - колонка тегов бендов есть в шаблоне / False - нет.
        """
        log.info(u'Колонка тегов бендов [%s]' % str(self._tag_band_col))
        return self._tag_band_col is not None

    def _getColumnCount(self, rows):
        """
        Определить количество колонок.

        :param rows: Список описаний строк.
        :return: Количество колонок шаблона отчета.
        """
        # Сначала предполагаем что в шаблоне имеется колонка тегов бендов
        col_count = self._getTagBandIdx(rows)
        if col_count <= 0:
            # В шаблоне нет колонки тегов бендов
            # Считаем по строкам
            max_col = 0
            for row in range(len(rows)):
                if 'children' in rows[row]:
                    for col in range(len(rows[row]['children'])):
                        max_col = max(max_col, col)
            col_count = max_col
        return col_count

    def _getTagBandIdx(self, rows):
        """
        Определить номер колонки тегов бэндов.

        :param rows: Список описаний строк.
        :return: Номер колонки тегов бендов.
        """
        if self._tag_band_col is None:
            # Это последняя колонка
            tag_col = 0
            for row in range(len(rows)):
                if 'children' in rows[row]:
                    for col in range(len(rows[row]['children'])):
                        # Определение данных ячейки
                        try:
                            cell_data = rows[row]['children'][col]['children']
                        except:
                            cell_data = None
                        # Если данные ячейки определены, то получить значение
                        if cell_data and 'value' in cell_data[0]:
                            value = cell_data[0]['value']
                        else:
                            value = None
                        if self._isTag(value):
                            tag_col = max(tag_col, col)
                        log.debug(u'Поиск индекса тега бенда. Ячейка [%d : %d]. Значение <%s>. Колонка тега бенда [%d]' % (row, col, value, tag_col))
            self._tag_band_col = tag_col
        return self._tag_band_col
        
    def _band(self, band, row, col_size):
        """
        Процедура заполнения бэнда.
        """
        new_band = band
        if 'row' not in new_band or new_band['row'] < 0:
            new_band['row'] = row
        if 'col' not in new_band or new_band['col'] < 0:
            new_band['col'] = 0
        if 'row_size' not in new_band or new_band['row_size'] < 0:
            new_band['row_size'] = 1
        else:
            new_band['row_size'] += 1
        if 'col_size' not in new_band or new_band['col_size'] < 0:
            new_band['col_size'] = col_size
        return new_band
     
    FIELD_NAMES = string.ascii_uppercase

    def _normDetail(self, detail, report):
        """
        Приведение к нормальному виду табличной части отчета.
            Если ячейки в табличной части не заполнены, то имеется ввиду,
            что ячейки будет заполняться по порядку.

        :param detail: Описание бенда табличной части.
        :param report: Описание данных отчета.
        """
        if detail['row_size'] == 1:
            ok = any([bool(cell['value']) for cell in report['sheet'][detail['row']]])
            if not ok:
                for i_row in range(detail['row'], detail['row'] + detail['row_size']):
                    for i_col in range(detail['col'], detail['col'] + detail['col_size']):
                        try:
                            report['sheet'][i_row][i_col]['value'] = '[\'%s\']' % (self.FIELD_NAMES[i_col - detail['col']])
                        except:
                            log.fatal('Ошибка. Функция _normDetail')
        return report
        
    def _defBand(self, band_tag, row, col_count, title_row, report):
        """
        Заполнить описание бенда.

        :param band_tag: Тег бэнда.
        :param row: Номер строки.
        :param title_row: Количество строк заголовочных бендов.
        :param col_count: Количество колонок.
        :param report: Описание данных отчета.
        :return: Описание данных отчета.
        """
        try:
            # Сделать копию данных отчета для возможного отката.
            rep = copy.deepcopy(report)
            
            log.debug(u'Определение бэнда. Тег: <%s>' % band_tag)
            if band_tag.strip() == HEADER_TAG:
                # Заполнить бэнд
                rep['header'] = self._band(rep['header'], row - title_row, col_count)
            elif band_tag.strip() == DETAIL_TAG:
                # Заполнить бэнд
                rep['detail'] = self._band(rep['detail'], row - title_row, col_count)
                self._normDetail(rep['detail'], rep)
            elif band_tag.strip() == FOOTER_TAG:
                # Заполнить бэнд
                rep['footer'] = self._band(rep['footer'], row - title_row, col_count)
            elif HEADER_GROUP_TAG in band_tag:
                # Определить имя поля группировки
                field_name = re.split(icrepgen.REP_FIELD_PATT, band_tag)[1].strip()[2:-2]
                # Если такой группы не зарегестрировано, то прописать ее
                is_grp = any([grp['field'] == field_name for grp in rep['groups']])
                if not is_grp:
                    # Записать в соответствии с положением относительно др. групп
                    rep['groups'].append(copy.deepcopy(icrepgen.IC_REP_GRP))
                    rep['groups'][-1]['field'] = field_name
                # Записать заголовок группы
                grp_field = [grp for grp in rep['groups'] if grp['field'] == field_name][0]
                # Заполнить бэнд
                grp_field['header'] = self._band(grp_field['header'], row - title_row, col_count)
            elif FOOTER_GROUP_TAG in band_tag:
                # Определить имя поля группировки
                field_name = re.split(icrepgen.REP_FIELD_PATT, band_tag)[1].strip()[2:-2]
                # Если такой группы не зарегестрировано, то прописать ее
                is_grp = any([grp['field'] == field_name for grp in rep['groups']])
                if not is_grp:
                    # Записать в соответствии с положением относительно др. групп
                    rep['groups'].append(copy.deepcopy(icrepgen.IC_REP_GRP))
                    rep['groups'][-1]['field'] = field_name
                # Записать примечание группы
                grp_field = [grp for grp in rep['groups'] if grp['field'] == field_name][0]
                # Заполнить бэнд
                grp_field['footer'] = self._band(grp_field['footer'], row - title_row, col_count)
            elif band_tag.strip() == UPPER_TAG:
                # Верхний колонтитул
                rep['upper'] = self._band(rep['upper'], row - title_row, col_count)
            elif band_tag.strip() == UNDER_TAG:
                # Нижний колонтитул
                rep['under'] = self._band(rep['under'], row - title_row, col_count)
            else:
                # Вывести сообщение об ошибке в лог
                log.warning(u'Не определенный тип бэнда <%s>.' % band_tag)
            # Заполнить колонтитулы
            rep['upper'] = self._bandUpper(rep['upper'], self._rep_worksheet)
            rep['under'] = self._bandUnder(rep['under'], self._rep_worksheet)
            
            return rep
        except:
            log.fatal(u'Ошибка определения бэнда <%s>.' % band_tag)
            return report
        
    def _bandUpper(self, band, worksheet_data):
        """
        Процедура заполнения верхнего колонтитула.

        :param band: Бэнд колонтитула.
        :param worksheet_data: Данные листа шаблона.
        """
        rep_upper = band
        # Заполнить данные и размер поля колонтитула
        if 'data' not in band:
            worksheet_options = [element for element in worksheet_data['children'] if element['name'] == 'WorksheetOptions']
            if worksheet_options:
                page_setup = [element for element in worksheet_options[0]['children'] if element['name'] == 'PageSetup']
                if page_setup:
                    header = [element for element in page_setup[0]['children'] if element['name'] == 'Header']
                    if header:
                        if 'Data' in header[0]:
                            rep_upper['data'] = header[0]['Data']
                        if 'Margin' in header[0]:
                            rep_upper['height'] = header[0]['Margin']
        return rep_upper
        
    def _bandUnder(self, band, worksheet_data):
        """
        Процедура заполнения нижнего колонтитула.

        :param band: Бэнд колонтитула.
        :param worksheet_data: Данные листа шаблона.
        """
        rep_under = band
        # Заполнить данные и размер поля колонтитула
        if 'data' not in band:
            worksheet_options = [element for element in worksheet_data['children'] if element['name'] == 'WorksheetOptions']
            if worksheet_options:
                page_setup = [element for element in worksheet_options[0]['children'] if element['name'] == 'PageSetup']
                if page_setup:
                    footer = [element for element in page_setup[0]['children'] if element['name'] == 'Footer']
                    if footer:
                        if 'Data' in footer[0]:
                            rep_under['data'] = footer[0]['Data']
                        if 'Margin' in footer[0]:
                            rep_under['height'] = footer[0]['Margin']
        return rep_under
        
    def _getParseRow(self, row, cur_band):
        """
        Подготовить для разбора строку шаблона.

        :param row: Описание строки.
        :param cur_band: Текуший тег бенда.
        """
        return row
    
    def _getCellStyle(self, rows, columns, styles, row, column):
        """
        Определить стиль ячейки.

        :param rows: Список строк.
        :param columns: Список колонок.
        :param styles: Словарь стилей.
        :param row: Номер строки ячейки.
        :param column: Номер колонки ячейки.
        """
        try:
            try:
                template_cell = rows[row]['children'][column]
            except:
                template_cell = {}
                cell_style = styles['Default']
            # Определение стиля ячейки
            if 'StyleID' in template_cell:
                cell_style = styles[template_cell['StyleID']]
            else:
                row = rows[row]
                if 'StyleID' in row:
                    cell_style = styles[row['StyleID']]
                else:
                    if columns and len(columns) > column:
                        col = columns[column]
                        if 'StyleID' in col:
                            cell_style = styles[col['StyleID']]
                        else:
                            cell_style = styles['Default']
                    else:
                        cell_style = styles['Default']
            # log.debug('Get new_cell style <%s>' % cell_style)
            return cell_style
        except:
            log.fatal(u'Ошибка определения стиля ячейки шаблона отчета')
        return styles['Default']

    def _getTypeCell(self, cell):
        """
        Определить тип ячейки.

        :param cell: Описание ячейки.
        """
        # В ячейке нет данных
        if 'children' not in cell or not cell['children']:
            return icrepgen.REP_FMT_NONE
            
        # Данные в ячейке имеются
        cell_data = cell['children'][0]
        if 'Type' in cell_data:
            if cell_data['Type'] == 'General':
                return icrepgen.REP_FMT_NONE
            elif cell_data['Type'] == 'String':
                return icrepgen.REP_FMT_STR
            elif cell_data['Type'] == 'Number':
                return icrepgen.REP_FMT_NUM
            else:
                return icrepgen.REP_FMT_MISC+cell_data['Type']
        return icrepgen.REP_FMT_NONE

    def _getCellValue(self, cell):
        """
        Значение ячейки.

        :param cell: Описание ячейки.
        """
        # Данных в ячейке нет
        if 'children' not in cell or not cell['children'] or \
           'value' not in cell['children'][0]:
            return None
        return cell['children'][0]['value']
        
    def _setDefaultCellSize(self, table):
        """
        Установка параметров по умолчанию для ячейки.

        :param table: Описание Таблицы.
        """
        if 'DefaultColumnWidth' in table:
            self._default_column_width = float(table['DefaultColumnWidth'])
            self._column_span_width = self._default_column_width
        if 'DefaultRowHeight' in table:
            self._default_row_height = float(table['DefaultRowHeight'])
            self._row_span_height = self._default_row_height
        
    def _getCellAttr(self, rows, columns, styles, row, column):
        """
        Функция возращает структуру атрибутов ячейки.

        :param rows: Список строк.
        :param columns: Список колонок.
        :param styles: Словарь стилей.
        :param row: Номер строки ячейки.
        :param column: Номер колонки ячейки.
        :return: Возвращает структуру icrepgen.IC_REP_CELL.
        """
        try:
            cell_style = self._getCellStyle(rows, columns, styles, row, column)
            cell = {}

            # Ширина колонок
            if not columns:
                cell_width = self._default_column_width     # 8.43
            elif len(columns) > column and 'Hidden' in columns[column]:
                cell_width = 0
            elif columns and len(columns) > column and 'Width' in columns[column]:
                cell_width = float(columns[column]['Width'])
                if 'Span' in columns[column]:
                    # Повторение атрибутов колонок
                    self._column_span_width = cell_width
            else:
                cell_width = self._column_span_width    # None=8.43

            # Высота строк
            if not rows:
                cell_height = self._default_row_height
            elif len(rows) > row and 'Hidden' in rows[row] and rows[row]['Hidden'] == '1':
                cell_height = 0
            elif rows and len(rows) > row and 'Height' in rows[row]:
                cell_height = float(rows[row]['Height'])
                if 'Span' in rows[row]:
                    # Повторение атрибутов строк
                    self._row_span_height = cell_height
            else:
                cell_height = self._row_span_height     # По умолчанию - 12.75

            # Объединение ячеек
            # Учет ширины и высоты ячеек для объединенных ячеек
            # Если ячейки объеденены в щаблоне, то и объеденить их в отчете
            cell['merge_row'] = 1
            cell['merge_col'] = 1

            try:            
                template_cell = rows[row]['children'][column]

                if 'MergeDown' in template_cell:
                    cell['merge_row'] = int(template_cell['MergeDown']) + 1
                if 'MergeAcross' in template_cell:
                    cell['merge_col'] = int(template_cell['MergeAcross']) + 1
            except:
                template_cell = None
                
            # Заполнение атрибутов ячейки
            # Размеры ячейки
            cell['width'] = cell_width
            cell['height'] = cell_height
            # Видимость ячейки
            cell['visible'] = True
    
            # Обрамление
            cell['border'] = self._getBordersStyle(cell_style)
            
            # Шрифт
            cell['font'] = self._getFontStyle(cell_style)
    
            # Установить цвет текста и фона
            cell['color'] = self._getColorStyle(cell_style)
    
            # Размещение
            cell['align'] = self._getAlignStyle(cell_style)
    
            # Формат вывода текста
            cell['format'] = self._getFmtStyle(cell_style)
            # Генерация текста ячейки
            # Перенести все ячейки из шаблона в выходной отчет
            if template_cell:
                cell['value'] = self._getCellValue(template_cell)
            else:
                cell['value'] = None

            # Инициализация данных суммирующих ячеек
            cell['sum'] = None
    
            return cell
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения атрибутов ячейки шаблона.')
        return None
    
    def _isTag(self, value):
        """
        Есть ли теги бендов в значении ячейки.

        :param value: Значение ячейки.
        :return: Возвращает True/False.
        """
        if not value:
            return False
        # Если хотя бы 1 тег есть в ячейке, то все ок
        for tag in ALL_TAGS:
            if value.find(tag) != -1:
                return True
        return False

    def _getTagBandRow(self, rows, row):
        """
        Определить тег бенда, к которому принадлежит строка.

        :param rows: Список строк.
        :param row: Номер строки.
        :return: Строка-тег бэнда или None  в случае ошибки.
        """
        try:
            row_data = rows[row]
            # Проверка корректности описания строки
            if 'children' not in row_data or not row_data['children']:
                log.warning(u'Ошибка наличия дочерних объектов строки <%s>' % row)
                return self.__cur_band
            i_tag = self._getTagBandIdx(rows)

            # ВНИМАНИЕ! Если колонки тегов бендов нет в шаблоне
            # то считаем что весь шаблон это шапка отчета
            # Используется для простого заполнения тегами
            if not self._existTagBand():
                self.__cur_band = HEADER_TAG
            else:
                if i_tag > 0:
                    i_tag, tag_value = self._findTagBandRow(row_data)
                    if i_tag >= 0:
                        # Если тег найден, то взять его
                        self.__cur_band = tag_value

            return self.__cur_band
        except:
            log.fatal(u'Ошибка в функции _getTagBandRow')
        return None

    def _findTagBandRow(self, row):
        """
        Поиск тега в текущем бэнде.

        :param row: Строка.
        :return: Кортеж: (Индекс ячейки в строке, в которой находится тег.
            Или -1, если тег в строке не найден,
            Сам тег).
        """
        try:
            for i in range(len(row['children'])-1, -1, -1):
                cell = row['children'][i]
                if 'children' in cell and cell['children'] and 'value' in cell['children'][0] and \
                   self._isTag(str(cell['children'][0]['value']).lower().strip()):
                    return i, cell['children'][0]['value'].lower().strip()
        except:
            log.fatal(u'Ошибка в функции _findTagBandRow')
        return -1, None

    def _isUpperBand(self, rows, row):
        """
        Проверить является текущая строка листа бэндом верхнего колонтитула.

        :param rows: Список строк.
        :param row: Номер строки.
        :return: Возвращает True/False.
        """
        try:
            tag = self._getTagBandRow(rows, row)
            return bool(tag == UPPER_TAG)
        except:
            log.fatal(u'Ошибка в функции _isUpperBand')
            return False
    
    def _isUnderBand(self, rows, row):
        """
        Проверить является текущая строка листа бэндом нижнего колонтитула.

        :param rows: Список строк.
        :param row: Номер строки.
        :return: Возвращает True/False.
        """
        try:
            tag = self._getTagBandRow(rows, row)
            return bool(tag == UNDER_TAG)
        except:
            log.fatal(u'Ошибка в функции _isUnderBand')
        return False

    def _isTitleBand(self, rows, row):
        """
        Проверить является текущая строка листа бэндом заголовочной части.

        :param rows: Список строк.
        :param row: Номер строки.
        :return: Возвращает True/False.
        """
        try:
            return bool(self._getTagBandRow(rows, row) in TITLE_TAGS)
        except:
            log.fatal(u'Ошибка в функции _isTitleBand')
        return False

    def _parseDescriptionTag(self, report, parse_row):
        """
        Разбор заголовочного тега описания.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            if not self._existTagBand():
                # Если теги бендов не указаны в шаблоне то
                # определяем описание как имя файла
                tmpl_filename = self.getTemplateFilename()
                report['description'] = os.path.splitext(os.path.basename(tmpl_filename))[0] if tmpl_filename else u''
            else:
                if 'value' in parse_row[0]['children'][0] and parse_row[0]['children'][0]['value']:
                    report['description'] = parse_row[0]['children'][0]['value']
                else:
                    report['description'] = None
        except:
            log.fatal(u'Ошибка в функции _parseDescriptionTag')

    def _parseVarTag(self, report, parse_row):
        """
        Разбор заголовочного тега переменных.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            name = parse_row[0]['children'][0]['value']
            value = parse_row[1]['children'][0]['value']
            if isinstance(value, str) and value.startswith(CODE_SIGNATURE):
                value = execfunc.exec_code(value.replace(CODE_SIGNATURE, u'').strip())
            elif isinstance(value, str) and value.startswith(PY_SIGNATURE):
                value = execfunc.exec_code(value.replace(PY_SIGNATURE, u'').strip())
            report['variables'][name] = value
        except:
            log.fatal(u'Ошибка в функции _parseVarTag')

    def _parseGeneratorTag(self, report, parse_row):
        """
        Разбор заголовочного тега генеаратора.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            if not self._existTagBand():
                # Если теги бендов не указаны в шаблоне то
                # определяем генератор по расширению имени файла
                tmpl_filename = self.getTemplateFilename()
                report['generator'] = os.path.splitext(tmpl_filename)[1].upper() if tmpl_filename else '.ODS'
            else:
                if 'value' in parse_row[0]['children'][0] and parse_row[0]['children'][0]['value']:
                    report['generator'] = parse_row[0]['children'][0]['value']
                else:
                    report['generator'] = None
        except:
            log.fatal(u'Ошибк в функции _parseGeneratorTag')

    def _parseDataSrcTag(self, report, parse_row):
        """
        Разбор заголовочного тега источника даных.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            report['data_source'] = parse_row[0]['children'][0]['value']
        except:
            report['data_source'] = None
            log.warning(u'Не указан источник данных!')

    def _parseQueryTag(self, report, parse_row):
        """
        Разбор заголовочного тега запроса.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            report['query'] = parse_row[0]['children'][0]['value']
        except:
            report['query'] = None
            log.warning(u'Не указан запрос!')
            
    def _parseStyleLibTag(self, report, parse_row):
        """
        Разбор заголовочного тега библиотеки стилей.

        :param report: Шаблон отчета.
        :param parse_row: Разбираемая строка шаблона отчета в виде списка.
        """
        try:
            from . import icstylelib
            xml_style_lib_file_name = parse_row[0]['children'][0]['value']
            report['style_lib'] = icstylelib.icXMLRepStyleLib().convert(xml_style_lib_file_name)
        except:
            log.fatal(u'Ошибка в функции _parseStyleLibTag')
            
    # Словарь функций разбора заголовочных тегов
    _TitleTagParse = {DESCRIPTION_TAG: _parseDescriptionTag,
                      VAR_TAG: _parseVarTag,
                      GENERATOR_TAG: _parseGeneratorTag,
                      DATASRC_TAG: _parseDataSrcTag,
                      QUERY_TAG: _parseQueryTag,
                      STYLELIB_TAG: _parseStyleLibTag,
                      }


from ic.virtual_excel import icexcel


class icODSReportTemplate(icExcelXMLReportTemplate):
    """
    Шаблон отчета в формате ODF Open Document Spreadsheet.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        icExcelXMLReportTemplate.__init__(self)

    def open(self, tmpl_filename):
        """
        Открыть файл шаблона отчета.

        :param tmpl_filename: Файл шаблона отчета.
        """
        v_excel = icexcel.icVExcel()
        result = v_excel.load(tmpl_filename)
        v_excel.saveAsXML(tmpl_filename.replace('.ods', '.xml'))
        return result


class icXLSReportTemplate(icODSReportTemplate):
    """
    Шаблон отчета в формате Excel XLS.
    """

    def __init__(self):
        """
        Конструктор класса.
        """
        icODSReportTemplate.__init__(self)

    def open(self, tmpl_filename):
        """
        Открыть файл шаблона отчета.

        :param tmpl_filename: Файл шаблона отчета.
        """
        try:
            ods_filename = os.path.splitext(tmpl_filename)[0] + '.ods'
            cmd = 'unoconv --format=ods %s' % tmpl_filename
            log.info(u'Выполнение комманды ОС <%s>' % cmd)
            os.system(cmd)

            return icODSReportTemplate.open(self, ods_filename)
        except:
            log.fatal(u'Ошибка открытия файла шаблона <%s>' % tmpl_filename)
        return None
