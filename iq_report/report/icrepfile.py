#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль файла отчета.
    Файл отчета преставляет собой XML файл формата Excel xmlss.
    Документация по данному формату находится:
    http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dnexcl2k2/html/odc_xmlss.asp.
"""

# Подключение библиотек
import time
import copy
from xml.sax import saxutils

from ic.std.log import log
from ic.std.utils import textfunc

from ic.report import icrepgen

__version__ = (0, 1, 1, 2)

# Спецификации и структуры
# Спецификация стиля ячеек
SPC_IC_XML_STYLE = {'style_id': '',                                           # Идентификатор стиля
                    'align': {'align_txt': (0, 0), 'wrap_txt': False},  # Выравнивание
                    'font': None,                                       # Шрифт
                    'border': (0, 0, 0, 0),                             # Обрамление
                    'format': None,                                     # Формат ячейки
                    'color': {},                                        # Цвет
                    }


class icReportFile:
    """
    Класс файла отчета.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        pass
        
    def write(self, rep_filename, rec_data):
        """
        Сохранить заполненный отчет в файле.

        :param rep_filename: Имя файла отчета.
        :param rec_data: Данные отчета.
        :return: Функция возвращает имя созданного xml файла,
            или None в случае ошибки.
        """
        pass


class icExcelXMLReportFile(icReportFile):
    """
    Файл *.XML отчета, в формат Excel XMLSS.
    """
    
    def __init__(self):
        """
        Конструктор.
        """
        icReportFile.__init__(self)
        
    def write(self, rep_filename, rec_data):
        """
        Сохранить заполненный отчет в файле.

        :param rep_filename: Имя файла отчета XML.
        :param rec_data: Данные отчета.
        :return: Функция возвращает имя созданного xml файла,
            или None в случае ошибки.
        """
        xml_file = None
        try:
            # Начать запись
            xml_file = open(rep_filename, 'wt')
            xml_gen = icXMLSSGenerator(xml_file)
            xml_gen.startDocument()
            xml_gen.startBook()

            # Параметры страницы
            # xml_gen.savePageSetup(rep_name,report)
        
            # Стили
            xml_gen.scanStyles(rec_data['sheet'])
            xml_gen.saveStyles()
        
            # Данные
            xml_gen.startSheet(rec_data['name'], rec_data)
            xml_gen.saveColumns(rec_data['sheet'])
            for i_row in range(len(rec_data['sheet'])):
                xml_gen.startRow(rec_data['sheet'][i_row])
                # Сбросить индекс ячейки
                xml_gen.cell_idx = 1
                for i_col in range(len(rec_data['sheet'][i_row])):
                    cell = rec_data['sheet'][i_row][i_col]
                    xml_gen.saveCell(i_row+1, i_col+1, cell, rec_data['sheet'])
                xml_gen.endRow()
            
            xml_gen.endSheet(rec_data)
       
            # Закончить запись
            xml_gen.endBook()
            xml_gen.endDocument()
            xml_file.close()
        
            return rep_filename
        except:
            if xml_file:
                xml_file.close()
            log.error(u'Ошибка сохранения отчета <%s>.' % textfunc.toUnicode(rep_filename))
            raise
        return None

    def write_book(self, rep_filename, *rep_sheet_data):
        """
        Сохранить список листов заполненного отчета в файле.

        :param rep_filename: Имя файла отчета XML.
        :param rep_sheet_data: Данные отчета, разобранные по листам.
        :return: Функция возвращает имя созданного xml файла,
            или None в случае ошибки.
        """
        xml_file = None
        try:
            # Начать запись
            xml_file = open(rep_filename, 'wt')
            xml_gen = icXMLSSGenerator(xml_file)
            xml_gen.startDocument()
            xml_gen.startBook()
        
            for rep_sheet_data in rep_sheet_data:
                # Стили
                xml_gen.scanStyles(rep_sheet_data['sheet'])
            xml_gen.saveStyles()
        
            for rep_sheet_data in rep_sheet_data:
                # Данные
                xml_gen.startSheet(rep_sheet_data['name'], rep_sheet_data)
                xml_gen.saveColumns(rep_sheet_data['sheet'])
                for i_row in range(len(rep_sheet_data['sheet'])):
                    xml_gen.startRow(rep_sheet_data['sheet'][i_row])
                    # Сбросить индекс ячейки
                    xml_gen.cell_idx = 1
                    for i_col in range(len(rep_sheet_data['sheet'][i_row])):
                        cell = rep_sheet_data['sheet'][i_row][i_col]
                        xml_gen.saveCell(i_row+1, i_col+1, cell, rep_sheet_data['sheet'])
                    xml_gen.endRow()
            
                xml_gen.endSheet(rep_sheet_data)
       
            # Закончить запись
            xml_gen.endBook()
            xml_gen.endDocument()
            xml_file.close()
        
            return rep_filename
        except:
            if xml_file:
                xml_file.close()
            log.error(u'Ошибка сохранения отчета %s.' % rep_filename)
            raise
        return None


class icXMLSSGenerator(saxutils.XMLGenerator):
    """
    Класс генератора конвертора отчетов в xml представление.
    """
    def __init__(self, out=None, encoding='utf-8'):
        """
        Конструктор.
        """
        saxutils.XMLGenerator.__init__(self, out, encoding)

        self._encoding = encoding
        
        # Отступ, определяющий вложение тегов
        self.break_line = ''
        
        # Стили ячеек
        self._styles = []
        
        # Текущий индекс ячейки в строке
        self.cell_idx = 0
        # Флаг установки индекса в строке
        self._idx_set = False

        # Время начала создания файла
        self.time_start = 0

    def startElementLevel(self, name, attrs):
        """
        Начало тега.

        :param name: Имя тега.
        :param attrs: Атрибуты тега (словарь).
        """
        # Дописать новый отступ
        self._write(u'\n' + str(self.break_line))    # self._encoding

        saxutils.XMLGenerator.startElement(self, name, attrs)
        self.break_line += ' '

    def endElementLevel(self, name):
        """
        Конец тега.

        :param name: Имя, закрываемого тега.
        """
        # Дописать новый отступ
        self._write(u'\n' + str(self.break_line))    # self._encoding

        saxutils.XMLGenerator.endElement(self, name)

        if self.break_line:
            self.break_line = self.break_line[:-1]

    def startElement(self, name, attrs):
        """
        Начало тега.

        :param name: Имя тега.
        :param attrs: Атрибуты тега (словарь).
        """
        # Дописать новый отступ
        self._write(u'\n' + str(self.break_line))    # self._encoding

        saxutils.XMLGenerator.startElement(self, name, attrs)

    def endElement(self, name):
        """
        Конец тега.

        :param name: Имя, закрываемого тега.
        """
        saxutils.XMLGenerator.endElement(self, name)

        if self.break_line:
            self.break_line = self.break_line[:-1]

    _orientationRep2XML = {0: 'Portrait',
                           1: 'Landscape',
                           '0': 'Portrait',
                           '1': 'Landscape',
                           }

    def savePageSetup(self, report):
        """
        Записать в xml файле параметры страницы.

        :param report: Тело отчета.
        """
        self.startElementLevel('WorksheetOptions', {'xmlns': 'urn:schemas-microsoft-com:office:excel'})
        if 'page_setup' in report:
            # Параметры страницы
            self.startElementLevel('PageSetup', {})

            # Ориентация листа
            if 'orientation' in report['page_setup']:
                self.startElementLevel('Layout',
                                       {'x:Orientation': self._orientationRep2XML[report['page_setup']['orientation']],
                                        'x:StartPageNum': str(report['page_setup'].setdefault('start_num', 1))})
                self.endElementLevel('Layout')

            # Поля
            if 'page_margins' in report['page_setup']:
                self.startElementLevel('PageMargins',
                                       {'x:Left': str(report['page_setup']['page_margins'][0]),
                                        'x:Right': str(report['page_setup']['page_margins'][1]),
                                        'x:Top': str(report['page_setup']['page_margins'][2]),
                                        'x:Bottom': str(report['page_setup']['page_margins'][3])})
                self.endElementLevel('PageMargins')
        
            # Обработка верхнего колонтитула
            if 'data' in report['upper']:
                data = str(report['upper']['data'])   # , 'CP1251').encode('UTF-8')
                self.startElementLevel('Header', 
                                       {'x:Margin': str(report['upper']['height']),
                                        'x:Data': data})
                self.endElementLevel('Header')
                
            # Обработка нижнего колонтитула
            if 'data' in report['under']:
                data = str(report['under']['data'])  # , 'CP1251').encode('UTF-8')
                self.startElementLevel('Footer', 
                                       {'x:Margin': str(report['under']['height']),
                                        'x:Data': data})
                self.endElementLevel('Footer')
                
            self.endElementLevel('PageSetup')

            # Параметры печати
            self.startElementLevel('Print', {})

            if 'paper_size' in report['page_setup']:
                self.startElementLevel('PaperSizeIndex', {})
                self.characters(str(report['page_setup']['paper_size']))
                self.endElementLevel('PaperSizeIndex')

            if 'scale' in report['page_setup']:
                self.startElementLevel('Scale', {})
                self.characters(str(report['page_setup']['scale']))
                self.endElementLevel('Scale')
        
            if 'resolution' in report['page_setup']:
                self.startElementLevel('HorizontalResolution', {})
                self.characters(str(report['page_setup']['resolution'][0]))
                self.endElementLevel('HorizontalResolution')
                self.startElementLevel('VerticalResolution', {})
                self.characters(str(report['page_setup']['resolution'][1]))
                self.endElementLevel('VerticalResolution')

            if 'fit' in report['page_setup']:
                self.startElementLevel('FitWidth', {})
                self.characters(str(report['page_setup']['fit'][0]))
                self.endElementLevel('FitWidth')
                self.startElementLevel('FitHeight', {})
                self.characters(str(report['page_setup']['fit'][1]))
                self.endElementLevel('FitHeight')
        
            self.endElementLevel('Print')

        self.endElementLevel('WorksheetOptions')

    def startBook(self):
        """
        Начало книги.
        """
        # Время начала создания фала
        self.time_start = time.time()

        # ВНИМАНИЕ! Неоходимо наличие следующих ключей
        # иначе некоторыетеги не будут пониматься библиотекой
        # и будет генерироваться ошибка чтения файла
        # <Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
        # xmlns:o="urn:schemas-microsoft-com:office:office"
        # xmlns:x="urn:schemas-microsoft-com:office:excel"
        # xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">

        self.startElementLevel('Workbook', {'xmlns': 'urn:schemas-microsoft-com:office:spreadsheet',
                                            'xmlns:o': 'urn:schemas-microsoft-com:office:office',
                                            'xmlns:x': 'urn:schemas-microsoft-com:office:excel',
                                            'xmlns:ss': 'urn:schemas-microsoft-com:office:spreadsheet'})
            
    def endBook(self):
        """
        Конец книги.
        """
        self.endElementLevel('Workbook')

    def startSheet(self, rep_name, report):
        """
        Теги начала страницы.

        :param rep_name: Имя отчета.
        :param report: Тело отчета.
        """
        rep_name = str(rep_name)    # , self._encoding)
        self.startElementLevel('Worksheet', {'ss:Name': rep_name})
        # Диапазон ячеек верхнего колонтитула
        try:
            if report['upper']:
                refers_to = self._getUpperRangeStr(report['upper'])

                self.startElementLevel('Names', {})
                self.startElementLevel('NamedRange', {'ss:Name': 'Print_Titles',
                                       'ss:RefersTo': refers_to})
                self.endElementLevel('NamedRange')
                self.endElementLevel('Names')
        except:
            log.error('Names SAVE <%s>' % report['upper'])
            raise
        
        # Начало таблицы
        self.startElementLevel('Table', {})

    def _getUpperRangeStr(self, upper):
        """
        Представить диапазон ячеек верхнего колонтитула в виде строки.
        """
        return '=C%d:C%d,R%d:R%d' % (upper['col'] + 1, upper['col'] + upper['col_size'],
                                     upper['row'] + 1, upper['row'] + upper['row_size'])
        
    def endSheet(self, report):
        """
        Теги начала страницы.

        :param report: Тело отчета.
        """
        self.endElementLevel('Table')
        self.savePageSetup(report)
        self.endElementLevel('Worksheet')
    
    def scanStyles(self, sheet):
        """
        Сканирование стилей на листе.
        """
        for i_row in range(len(sheet)):
            for i_col in range(len(sheet[i_row])):
                cell = sheet[i_row][i_col]
                if cell is not None:
                    self.setStyle(cell)
        return self._styles
        
    def setStyle(self, cell):
        """
        Определить стиль ячейки.

        :param cell: Атрибуты ячейки.
        :return: Возвращает индекс стиля в списке стилей.
        """
        cell_style_idx = self.getStyle(cell)
        if cell_style_idx is None:
            # Создать новый стиль
            new_idx = len(self._styles)
            cell_style = copy.deepcopy(SPC_IC_XML_STYLE)
            cell_style['align'] = cell['align']
            cell_style['font'] = cell['font']
            cell_style['border'] = cell['border']
            cell_style['format'] = cell['format']
            cell_style['color'] = cell['color']
            cell_style['style_id'] = 'x'+str(new_idx)
            # Прописать в ячейке идентификатор стиля
            cell['style_id'] = cell_style['style_id']
            self._styles.append(cell_style)
            return new_idx
        return cell_style_idx
      
    def getStyle(self, cell):
        """
        Определить стиль ячейки из уже имеющихся.

        :param cell: Атрибуты ячейки.
        :return: Возвращает индекс стиля в списке стилей.
        """
        # сначала поискать в списке стилей
        find_style = [style for style in self._styles if self._equalStyles(style, cell)]

        # Если такой стиль найден, то вернуть его
        if find_style:
            cell['style_id'] = find_style[0]['style_id']
            return self._styles.index(find_style[0])
        return None
        
    def _equalStyles(self, style1, style2):
        """
        Функция проверки равенства стилей.
        """
        return bool(self._equalAlign(style1['align'], style2['align']) and
                    self._equalFont(style1['font'], style2['font']) and
                    self._equalBorder(style1['border'], style2['border']) and
                    self._equalFormat(style1['format'], style2['format']) and
                    self._equalColor(style1['color'], style2['color']))

    def _equalAlign(self, align1, align2):
        """
        Равенство выравниваний.
        """
        return bool(align1 == align2)
        
    def _equalFont(self, font1, font2):
        """
        Равенство шрифтов.
        """
        return bool(font1 == font2)
        
    def _equalBorder(self, border1, border2):
        """
        Равенство обрамлений.
        """
        return bool(border1 == border2)
        
    def _equalFormat(self, format1, format2):
        """
        Равенство форматов.
        """
        return bool(format1 == format2)
        
    def _equalColor(self, color1, color2):
        """
        Равенство цветов.
        """
        return bool(color1 == color2)
        
    def saveStyles(self):
        """
        Записать стили.
        """
        self.startElementLevel('Styles', {})
        
        # Стиль по умолчанию
        self.startElementLevel('Style', {'ss:ID': 'Default', 'ss:Name': 'Normal'})
        self.startElement('Alignment', {'ss:Vertical': 'Bottom'})
        self.endElement('Alignment')    
        self.startElement('Borders', {})
        self.endElement('Borders')    
        self.startElement('Font', {'ss:FontName': 'Arial Cyr'})
        self.endElement('Font')    
        self.startElement('Interior', {})
        self.endElement('Interior')    
        self.startElement('NumberFormat', {})
        self.endElement('NumberFormat')    
        self.startElement('Protection', {})
        self.endElement('Protection')    
        self.endElementLevel('Style')
        
        # Дополнительные стили
        for style in self._styles:
            self.startElementLevel('Style', {'ss:ID': style['style_id']})
            # Выравнивание
            align = {}
            h_align = self._alignRep2XML[style['align']['align_txt'][icrepgen.IC_REP_ALIGN_HORIZ]]
            v_align = self._alignRep2XML[style['align']['align_txt'][icrepgen.IC_REP_ALIGN_VERT]]
            if h_align:
                align['ss:Horizontal'] = h_align
            if v_align:
                align['ss:Vertical'] = v_align
            # Перенос по словам
            if style['align']['wrap_txt']:
                align['ss:WrapText'] = '1'
            
            self.startElement('Alignment', align)
            self.endElement('Alignment')
            
            # Обрамление
            self.startElementLevel('Borders', {})
            for border_pos in range(4):
                border = self._borderRep2XML(style['border'], border_pos)
                if border:
                    border_element = dict([('ss:'+stl_name, border[stl_name]) for stl_name in
                                          [stl_name for stl_name in border.keys() if border[stl_name] is not None]])
                    self.startElement('Border', border_element)
                    self.endElement('Border')
            self.endElementLevel('Borders')
               
            # Шрифт
            font = {}
            font['ss:FontName'] = style['font']['name']
            font['ss:Size'] = str(int(style['font']['size']))
            if style['font']['style'] == 'bold' or style['font']['style'] == 'boldItalic':
                font['ss:Bold'] = '1'
            elif style['font']['style'] == 'italic' or style['font']['style'] == 'boldItalic':
                font['ss:Italic'] = '1'
            if style['color']:
                if 'text' in style['color'] and style['color']['text']:
                    font['ss:Color'] = self._getRGBColor(style['color']['text'])
                
            self.startElement('Font', font)
            self.endElement('Font')
            
            # Интерьер
            interior = {}
            if style['color']:
                if 'background' in style['color'] and style['color']['background']:
                    interior['ss:Color'] = self._getRGBColor(style['color']['background'])
                    interior['ss:Pattern'] = 'Solid'

            self.startElement('Interior', interior)
            self.endElement('Interior')

            # Формат
            fmt = {}
            if style['format']:
                fmt['ss:Format'] = self._getNumFmt(style['format'])
                self.startElement('NumberFormat', fmt)
                self.endElement('NumberFormat')

            self.endElementLevel('Style')
            
        self.endElementLevel('Styles')
        
    def _getRGBColor(self, color):
        """
        Преобразование цвета из (R,G,B) в #RRGGBB.
        """
        if type(color) in (list, tuple):
            return '#%02X%02X%02X' % (color[0], color[1], color[2])
        # ВНИМАНИЕ! Если цвет задается не RGB форматом, тогда оставить его без изменения
        return color

    def _getNumFmt(self, format):
        """
        Формат чисел.
        """
        if format[0] == icrepgen.REP_FMT_EXCEL:
            return format[1:]
        elif format[0] == icrepgen.REP_FMT_STR:
            return '@'
        elif format[0] == icrepgen.REP_FMT_NUM:
            return '0'
        elif format[0] == icrepgen.REP_FMT_FLOAT:
            return '0.'
        return '0'

    # Преобразование выравнивания из нашего представления
    # в xml представление.
    _alignRep2XML = {icrepgen.IC_HORIZ_ALIGN_LEFT: 'Left',
                     icrepgen.IC_HORIZ_ALIGN_CENTRE: 'Center',
                     icrepgen.IC_HORIZ_ALIGN_RIGHT: 'Right',
                     icrepgen.IC_VERT_ALIGN_TOP: 'Top',
                     icrepgen.IC_VERT_ALIGN_CENTRE: 'Center',
                     icrepgen.IC_VERT_ALIGN_BOTTOM: 'Bottom',
                     }
        
    def _borderRep2XML(self, border, position):
        """
        Преобразование обрамления из нашего представления
            в xml представление.
        """
        if border[position]:
            return {'Position': self._positionRep2XML.setdefault(position, 'Left'),
                    'Color': self._colorRep2XML(border[position].setdefault('color', None)),
                    'LineStyle': self._lineRep2XML.setdefault(border[position].setdefault('style', icrepgen.IC_REP_LINE_TRANSPARENT), 'Continuous'),
                    'Weight': str(border[position].setdefault('weight', 1)),
                    }

    # Преобразование позиции линии обрамления из нашего представления
    # в xml представление.
    _positionRep2XML = {icrepgen.IC_REP_BORDER_LEFT: 'Left',
                        icrepgen.IC_REP_BORDER_RIGHT: 'Right',
                        icrepgen.IC_REP_BORDER_TOP: 'Top',
                        icrepgen.IC_REP_BORDER_BOTTOM: 'Bottom',
                        }
        
    _lineRep2XML = {icrepgen.IC_REP_LINE_SOLID: 'Continuous',
                    icrepgen.IC_REP_LINE_SHORT_DASH: 'Dash',
                    icrepgen.IC_REP_LINE_DOT_DASH: 'DashDot',
                    icrepgen.IC_REP_LINE_DOT: 'Dot',
                    icrepgen.IC_REP_LINE_TRANSPARENT: None,
                    }
    
    def _colorRep2XML(self, color):
        """
        Преобразование цвета из нашего представления
            в xml представление.
        """
        return None

    def saveColumns(self, sheet):
        """
        Запись атрибутов колонок.
        """
        width_cols = self.getWidthColumns(sheet)
        for width_col in width_cols:
            # Если ширина колонки определена
            if width_col is not None:
                self.startElement('Column', {'ss:Width': str(width_col), 'ss:AutoFitWidth': '0'})
            else:
                self.startElement('Column', {'ss:AutoFitWidth': '0'})
            self.endElement('Column')
            
    def getColumnCount(self, sheet):
        """
        Определить количество колонок.
        """
        if sheet:
            return max([len(row) for row in sheet])
        return 0

    def getWidthColumns(self, sheet):
        """
        Ширины колонок.
        """
        col_count = self.getColumnCount(sheet)
        col_width = []
        # Выбрать строку по которой будыт выставяться ширины колонок
        row = [row for row in sheet if len(row) == col_count][0] if sheet else list()
        for cell in row:
            if cell:
                # log.debug('Column width <%s>' % new_cell['width'])
                col_width.append(cell['width'])
            else:
                # log.debug('Column default width')
                col_width.append(8.43)
        return col_width

    def getRowHeight(self, row):
        """
        Высота строки.
        """
        return min([cell['height'] for cell in [cell_ for cell_ in row if type(cell_) == dict and 'height' in cell_]])
            
    def startRow(self, row):
        """
        Начало строки.
        """
        height_row = self.getRowHeight(row)
        self.startElementLevel('Row', {'ss:Height': str(height_row)})
        self._idx_set = False       # Сбросить флаг установки индекса
        self.cell_idx = 1
            
    def endRow(self):
        """
        Конец строки.
        """
        self.endElementLevel('Row')
        
    def _saveCellStyleID(self, cell):
        """
        Определить идентификатор стиля ячейки для записи.
        """
        if 'style_id' in cell:
            return cell['style_id']
        else:
            style_idx = self.getStyle(cell)
            if style_idx is not None:
                style_id = self._styles[style_idx]['style_id']
            else:
                style_id = 'Default'
            return style_id
        
    def saveCell(self, row, column, cell, sheet=None):
        """
        Записать ячейку.

        :param row: НОмер строки.
        :param column: Номер колонки.
        :param cell: Атрибуты ячейки.
        """
        if cell is None:
            self._idx_set = False   # Сбросить флаг установки индекса
            self.cell_idx += 1
            return 

        if 'hidden' in cell and cell['hidden']:
            self._idx_set = False   # Сбросить флаг установки индекса
            # ВНИМАНИЕ!!! Здесь надо увеличивать индекс на 1
            # потому что в Excel индексирование начинается с 1 !!!
            self.cell_idx += 1
            return 

        cell_attr = {}
        if self.cell_idx > 1:
            if not self._idx_set:
                cell_attr = {'ss:Index': str(self.cell_idx)}
                self._idx_set = True    # Установить флаг установки индекса

        # Объединение ячеек
        if cell['merge_col'] > 1:
            cell_attr['ss:MergeAcross'] = str(cell['merge_col'] - 1)
            # Обработать верхнюю строку области объединения
            self._setCellmerge_across(row, column, cell['merge_col'], sheet)
            if cell['merge_row'] > 1:
                # Обработать дополнительную область объединения
                self._setCellMerge(row, column, cell['merge_col'], cell['merge_row'], sheet)
            self._idx_set = False   # Сбросить флаг установки индекса
        # ВНИМАНИЕ!!! Здесь надо увеличивать индекс на 1
        # потому что в Excel индексирование начинается с 1 !!!
        self.cell_idx = column+1
    
        if cell['merge_row'] > 1:
            cell_attr['ss:MergeDown'] = str(cell['merge_row'] - 1)
            # Обработать левый столбец области объединения
            self._setCellMergeDown(row, column, cell['merge_row'], sheet)

        # Стиль
        cell_attr['ss:StyleID'] = self._saveCellStyleID(cell)

        self.startElement('Cell', cell_attr)
        if cell['value'] is not None:
            self.startElement('Data', {'ss:Type': self._getCellType(cell['value'])})
            value = self._getCellValue(cell['value'])
            self.characters(value)
        
            self.endElement('Data')

        self.endElement('Cell')
        
    def _getCellValue(self, value):
        """
        Подготовить значение для записи в файл.
        """
        if self._getCellType(value) == 'Number':
            # Это число
            value = value.strip()
        else:
            # Это не число
            value = value

        if not isinstance(value, str):
            try:
                value = str(value)  #, self._encoding)
            except:
                value = str(value)  #, 'cp1251')
        if value:
            value = saxutils.escape(value)
            
        return value

    def _getCellType(self, value):
        """
        Тип ячейки.
        """
        try:
            # Это число
            float(value)
            return 'Number'
        except:
            # Это не число
            return 'String'

    def _setCellmerge_across(self, row, column, merge_across_, sheet):
        """
        Сбросить все ячейки, которые попадают в горизонтальную зону объединения.

        :param row: НОмер строки.
        :param column: Номер колонки.
        :param merge_across_: Количество ячеек, объединенных с текущей.
        :param sheet: Структура листа.
        """
        for i in range(1, merge_across_):
            try:
                cell = sheet[row - 1][column + i - 1]
            except IndexError:
                continue
            if cell and (not cell['value']):
                sheet[row - 1][column + i - 1]['hidden'] = True
        return sheet

    def _setCellMergeDown(self, row, column, merge_down, sheet):
        """
        Сбросить все ячейки, которые попадают в вертикальную зону объединения.

        :param row: НОмер строки.
        :param column: Номер колонки.
        :param merge_down: Количество ячеек, объединенных с текущей.
        :param sheet: Структура листа.
        """
        for i in range(1, merge_down):
            try:
                cell = sheet[row + i - 1][column - 1]
            except IndexError:
                continue
            if cell and (not cell['value']):
                sheet[row + i - 1][column - 1]['hidden'] = True
        return sheet

    def _setCellMerge(self, row, column, merge_across_, merge_down, sheet):
        """
        Сбросить все ячейки, которые попадают в зону объединения.

        :param row: НОмер строки.
        :param column: Номер колонки.
        :param merge_across_: Количество ячеек, объединенных с текущей.
        :param merge_down: Количество ячеек, объединенных с текущей.
        :param sheet: Структура листа.
        """
        for x in range(1, merge_across_):
            for y in range(1, merge_down):
                try:
                    cell = sheet[row + y - 1][column + x - 1]
                except IndexError:
                    continue
                if cell is not None and (not cell['value']):
                    sheet[row + y - 1][column + x - 1]['hidden'] = True
        return sheet
