# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
import uuid

# from . import config

try:
    # Если Virtual Excel работает в окружении icReport
    from ic.std.log import log
except ImportError:
    # Если Virtual Excel работает в окружении DEFIS
    from ic.log import log

# log.init(config)
    
try:
    import odf.opendocument
    import odf.style
    import odf.number
    import odf.text
    import odf.table
except ImportError:
    log.error(u'Ошибка импорта ODFpy')

__version__ = (0, 1, 2, 1)

DIMENSION_CORRECT = 35
DEFAULT_STYLE_ID = 'Default'

CM2PT_CORRECT = 25

INCH2CM = 2.54

SPREADSHEETML_CR = '&#10;'

LIMIT_ROWS_REPEATED = 1000000
LIMIT_COLUMNS_REPEATED = 100

ODS_LANDSCAPE_ORIENTATION = 'landscape'
ODS_PORTRAIT_ORIENTATION = 'portrait'
LANDSCAPE_ORIENTATION = ODS_LANDSCAPE_ORIENTATION.title()
PORTRAIT_ORIENTATION = ODS_PORTRAIT_ORIENTATION.title()

A4_PAPER_FORMAT = 'A4'
A3_PAPER_FORMAT = 'A3'

DEFAULT_ENCODE = 'utf-8'

# Поля страницы по умолчанию
DEFAULT_XML_MARGIN_TOP = 0.787401575
DEFAULT_XML_MARGIN_BOTTOM = 0.787401575
DEFAULT_XML_MARGIN_LEFT = 0.787401575
DEFAULT_XML_MARGIN_RIGHT = 0.787401575


class icODS(object):
    """
    Класс конвертации представления VirtualExcel в ODS файл.
    """
    def __init__(self):
        """
        Конструктор.
        """
        self._styles_ = {}
        self.ods_document = None

        # Внутренние данные в xmlss представлении
        self.xmlss_data = None
        
        # Стили числовых форматов в виде словаря
        self._number_styles_ = {}

        # Индекс генерации имен стилей
        self._style_name_idx = 0
        
    def save(self, filename, data_dict=None):
        """
        Сохранить в ODS файл.

        :param filename: Имя ODS файла.
        :param data_dict: Словарь данных.
        :return: True/False.
        """
        if data_dict is None:
            log.warning(u'ODS. Не определены данные для сохранения')

        self.ods_document = None
        self._styles_ = {}
        
        workbooks = data_dict.get('children', None)
        if not workbooks:
            workbook = {}
        else:
            workbook = workbooks[0]
        
        self.setWorkbook(workbook)
        
        if self.ods_document:
            # if isinstance(filename, text):
            #    # ВНИМАНИЕ! Перед сохранением надо имя файла сделать
            #    # Юникодной иначе падает по ошибке в функции save
            #    filename = unicode(filename, DEFAULT_ENCODE)
            # Добавлять автоматически расширение-+
            # к имени файла (True - да)          |
            #                                    V
            self.ods_document.save(filename, addsuffix=False)
            self.ods_document = None
            
        return True
    
    def getChildrenByName(self, data_dict, name):
        """
        Дочерние элементы по имени.

        :param data_dict: Словарь данных.
        :param name: Имя дочернего элемента.
        """
        return [item for item in data_dict.get('children', []) if item['name'] == name]
        
    def setWorkbook(self, data_dict):
        """
        Заполнить книгу.

        :param data_dict: Словарь данных.
        """
        self.ods_document = odf.opendocument.OpenDocumentSpreadsheet()
        
        if data_dict:
            styles = self.getChildrenByName(data_dict, 'Styles')
            if styles:
                self.setStyles(styles[0])

            sheets = self.getChildrenByName(data_dict, 'Worksheet')
            if sheets:
                for sheet in sheets:
                    ods_table = self.setWorksheet(sheet)
                    self.ods_document.spreadsheet.addElement(ods_table)

    def setStyles(self, data_dict):
        """
        Заполнить стили.

        :param data_dict: Словарь данных.
        """
        # log.info(u'Стили <%s>' % data_dict)
        
        styles = data_dict.get('children', [])
        for style in styles:
            ods_style = self.setStyle(style)
            self.ods_document.automaticstyles.addElement(ods_style)

    def setFont(self, data_dict):
        """
        Заполнить шрифт стиля.

        :param data_dict: Словарь данных.
        """
        # log.debug(u'Установка шрифта <%s>' % data_dict)
        font = {}
        font_name = data_dict.get('FontName', 'Arial')
        font_size = data_dict.get('Size', '10')
        font_bold = 'bold' if data_dict.get('Bold', '0') in (True, '1') else None
        font_italic = 'italic' if data_dict.get('Italic', '0') in (True, '1') else None

        through = 'solid' if data_dict.get('StrikeThrough', '0') in (True, '1') else None
        underline = 'solid' if data_dict.get('Underline', 'None') != 'None' else None

        font['fontfamily'] = font_name
        font['fontsize'] = font_size
        font['fontweight'] = font_bold
        font['fontstyle'] = font_italic

        if through:
            font['textlinethroughstyle'] = 'solid'
            font['textlinethroughtype'] = 'single'
        if underline:
            font['textunderlinestyle'] = 'solid'
            font['textunderlinewidth'] = 'auto'

        return font

    def _genNumberStyleName(self):
        """
        Генерация имени стиля формата числового представления.
        """
        # from services.ic_std.utils import uuid
        # return uuid.get_uuid()
        self._style_name_idx += 1
        return 'text%d' % self._style_name_idx

    def setNumberFormat(self, data_dict):
        """
        Заполнить формат числового представления.

        :param data_dict: Словарь данных.
        """
        number_format = {}
        format = data_dict.get('Format', '0')

        # Не анализировать знак %
        format = format.replace('%', '')
        decimalplaces = len(format[format.find(',')+1:]) if format.find(',') >= 0 else 0
        minintegerdigits = len([i for i in list(format[:format.find(',')]) if i == '0']) if format.find(',') >= 0 else len([i for i in list(format) if i == '0'])
        grouping = 'true' if format.find(' ') >= 0 else 'false'
                    
        number_format['decimalplaces'] = str(decimalplaces)
        number_format['minintegerdigits'] = str(minintegerdigits)
        number_format['grouping'] = str(grouping)
        
        # log.debug(u'Установка числового формата <%s>' % number_format)
        return number_format

    _lineStyles_SpreadsheetML2ODS = {None: 'solid',
                                     'Continuous': 'solid',
                                     'Double': 'double',
                                     'Dot': 'dotted',
                                     'Dash': 'dashed',
                                     'DashDot': 'dotted',
                                     'DashDotDot': 'dashed',
                                     'solid': 'solid'}
    _lineStyles_ODS2SpreadsheetML = {None: 'Continuous',
                                     'solid': 'Continuous',
                                     'double': 'Double',
                                     'dotted': 'Dot',
                                     'dashed': 'Dash'}

    def setBorders(self, data_dict):
        """
        Заполнить бордеры.

        :param data_dict: Словарь данных.
        """
        borders = {}
        for border in data_dict['children']:
            if border:
                border_weight = border.get('Weight', '1')
                color = border.get('Color', '#000000')
                line_style = self._lineStyles_SpreadsheetML2ODS.get(border.get('LineStyle', 'solid'), 'solid')
                if border['Position'] == 'Left':
                    borders['borderleft'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Right':
                    borders['borderright'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Top':
                    borders['bordertop'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Bottom':
                    borders['borderbottom'] = '%spt %s %s' % (border_weight, line_style, color)
                
        return borders
        
    _alignHorizStyle_SpreadsheetML2ODS = {'Left': 'start',
                                          'Right': 'end',
                                          'Center': 'center',
                                          'Justify': 'justify',
                                          }
    _alignVertStyle_SpreadsheetML2ODS = {'Top': 'top',
                                         'Bottom': 'bottom',
                                         'Center': 'middle',
                                         'Justify': 'justify',
                                         }

    def setAlignmentParagraph(self, data_dict):
        """
        Заполнить выравнивания текста стиля.

        :param data_dict: Словарь данных.
        """
        align = {}
        horiz = data_dict.get('Horizontal', None)
        vert = data_dict.get('Vertical', None)

        if horiz:
            align['textalign'] = self._alignHorizStyle_SpreadsheetML2ODS.get(horiz, 'start')
            
        if vert:
            align['verticalalign'] = self._alignVertStyle_SpreadsheetML2ODS.get(vert, 'top')

        return align

    def setAlignmentCell(self, data_dict):
        """
        Заполнить выравнивания текста стиля.

        :param data_dict: Словарь данных.
        """
        align = {}
        wrap_txt = data_dict.get('WrapText', 0)
        shrink_to_fit = data_dict.get('ShrinkToFit', 0)
        vert = data_dict.get('Vertical', None)
        
        if vert:
            align['verticalalign'] = self._alignVertStyle_SpreadsheetML2ODS.get(vert, 'top')
        
        if wrap_txt:
            align['wrapoption'] = 'wrap'
            
        if shrink_to_fit:
            align['shrinktofit'] = 'true'
        
        return align

    def setInteriorCell(self, data_dict):
        """
        Заполнить интерьер ячейки стиля.

        :param data_dict: Словарь данных.
        """
        interior = {}
        color = data_dict.get('Color', None)

        if color:
            interior['backgroundcolor'] = color

        return interior

    def setStyle(self, data_dict):
        """
        Заполнить стиль.

        :param data_dict: Словарь данных.
        """
        # log.info(u'Установка стиля <%s>' % data_dict)

        properties_args = {}
        number_format = self.getChildrenByName(data_dict, 'NumberFormat')
        if number_format:
            # Заполнениние формата числового представления
            number_properties = self.setNumberFormat(number_format[0])
            number_style_name = self._genNumberStyleName()
            properties_args['datastylename'] = number_style_name
            
            format = number_format[0].get('Format', '0')
            # log.debug(u'Установка числового формата <%s>' % format)
            if '%' in format:
                ods_number_style = odf.number.PercentageStyle(name=number_style_name)
                ods_number_style.addElement(odf.number.Number(**number_properties))
                ods_number_style.addElement(odf.number.Text(text='%'))
                self.ods_document.styles.addElement(ods_number_style)
            else:
                ods_number_style = odf.number.NumberStyle(name=number_style_name)
                ods_number_style.addElement(odf.number.Number(**number_properties))
                self.ods_document.automaticstyles.addElement(ods_number_style)
    
        style_id = data_dict['ID']
        properties_args['name'] = style_id
        properties_args['family'] = 'table-cell'
        ods_style = odf.style.Style(**properties_args)

        properties_args = {}
        fonts = self.getChildrenByName(data_dict, 'Font')
        # log.warning('Set font <%s>' % fonts)
        if fonts:
            # Заполнениние шрифта
            properties_args = self.setFont(fonts[0])
            # log.debug(u'Шрифт. Аргументы <%s>' % properties_args)

        if properties_args:
            ods_properties = odf.style.TextProperties(**properties_args)
            ods_style.addElement(ods_properties)
        
        properties_args = {}
        borders = self.getChildrenByName(data_dict, 'Borders')
        if borders:
            # Заполнение бордеров
            args = self.setBorders(borders[0])
            properties_args.update(args)
            # log.debug(u'Обрамление. Аргументы <%s>' % args)

        alignments = self.getChildrenByName(data_dict, 'Alignment')
        if alignments:
            # Заполнение выравнивания текста
            args = self.setAlignmentCell(alignments[0])
            properties_args.update(args)
            # log.debug(u'Выравнивание. Аргументы %s' % args)

        interiors = self.getChildrenByName(data_dict, 'Interior')
        if interiors:
            # Заполнение интерьера
            args = self.setInteriorCell(interiors[0])
            properties_args.update(args)
            # log.debug(u'Интеръер. Аргументы %s' % args)

        if properties_args:
            ods_properties = odf.style.TableCellProperties(**properties_args)
            ods_style.addElement(ods_properties)            
            
        properties_args = {}
        if alignments:
            # Заполнение выравнивания текста
            args = self.setAlignmentParagraph(alignments[0])
            properties_args.update(args)
            # log.debug(u'Выравнивание параграфа. Аргументы <%s>' % args)

        if properties_args:
            ods_properties = odf.style.ParagraphProperties(**properties_args)
            ods_style.addElement(ods_properties)            

        # Зарегистрировать стиль в кеше по имени
        self._styles_[style_id] = ods_style
        return ods_style

    def setWorksheet(self, data_dict):
        """
        Заполнить лист.

        :param data_dict: Словарь данных.
        """
        # log.info(u'Установка листа <%s>' % data_dict)
        # log.debug(u'Установка листа <%s : %s>' % (type(data_dict.get('Name', None)), data_dict.get('Name', None)))
        sheet_name = data_dict.get('Name', 'Лист')
        if not isinstance(sheet_name, str):
            sheet_name = str(sheet_name)    # DEFAULT_ENCODE)
        ods_table = odf.table.Table(name=sheet_name)
        tables = self.getChildrenByName(data_dict, 'Table')
        if tables:
            self.setTable(tables[0], ods_table)
            
        # Установка параметров страницы
        worksheet_options = self.getChildrenByName(data_dict, 'WorksheetOptions')
        if worksheet_options:
            self.setWorksheetOptions(worksheet_options[0])

        # Установка разрывов страницы
        page_breaks = self.getChildrenByName(data_dict, 'PageBreaks')
        if page_breaks:
            self.setPageBreaks(page_breaks[0], ods_table)
        return ods_table

    def _set_row_break(self, row, ods_table):
        """
        Установить разрыв по строке.

        :param row: Номер строки.
        :param ods_table: Объект ODS таблицы.
        """
        if ods_table:
            rows = ods_table.getElementsByType(odf.table.TableRow)
            if rows:
                style_name = rows[row].getAttribute('stylename')
                style = self._styles_[style_name]
                if style:
                    row_properties = style.getElementsByType(odf.style.TableRowProperties)
                    if row_properties:
                        row_properties[0].setAttribute('breakbefore', 'page')

    def setPageBreaks(self, data_dict, ods_table):
        """
        Установить разрывы страниц.

        :param data_dict: Словарь данных.
        :param ods_table: Объект ODS таблицы.
        """
        row_breaks = data_dict['children'][0]['children']
        for row_break in row_breaks:
            i_row = row_break['children'][0]['value']
            # log.debug(u'Разрыв страницы <%s>' % i_row)
            self._set_row_break(i_row, ods_table)

    def setWorksheetOptions(self, data_dict):
        """
        Установить параметры страницы.

        :param data_dict: Словарь данных.
        """
        # log.debug(u'Параметры листа <%s>' % data_dict)
        page_setup = self.getChildrenByName(data_dict, 'PageSetup')
        print_setup = self.getChildrenByName(data_dict, 'Print')
        fit_to_page = self.getChildrenByName(data_dict, 'FitToPage')
        ods_properties = {'writingmode': 'lr-tb'}
        orientation = None
        if page_setup:
            
            layout = self.getChildrenByName(page_setup[0], 'Layout')
            orientation = layout[0].get('Orientation', None) if layout else None
            if orientation:
                ods_properties['printorientation'] = orientation.lower()
                
            page_margins = self.getChildrenByName(page_setup[0], 'PageMargins')
            margin_top = page_margins[0].get('Top', DEFAULT_XML_MARGIN_TOP) if page_margins else DEFAULT_XML_MARGIN_TOP
            margin_bottom = page_margins[0].get('Bottom', DEFAULT_XML_MARGIN_BOTTOM) if page_margins else DEFAULT_XML_MARGIN_BOTTOM
            margin_left = page_margins[0].get('Left', DEFAULT_XML_MARGIN_LEFT) if page_margins else DEFAULT_XML_MARGIN_LEFT
            margin_right = page_margins[0].get('Right', DEFAULT_XML_MARGIN_RIGHT) if page_margins else DEFAULT_XML_MARGIN_RIGHT
            if margin_top:
                ods_properties['margintop'] = self._dimension_inch2cm(margin_top, True)
            if margin_bottom:
                ods_properties['marginbottom'] = self._dimension_inch2cm(margin_bottom, True)
            if margin_left:
                ods_properties['marginleft'] = self._dimension_inch2cm(margin_left, True)
            if margin_right:
                ods_properties['marginright'] = self._dimension_inch2cm(margin_right, True)
        else:
            log.warning(u'Параметры страницы не определены')
        if print_setup:
            paper_size_idx = self.getChildrenByName(print_setup[0], 'PaperSizeIndex')
            if paper_size_idx:
                width, height = self._getPageSizeByExcelIndex(paper_size_idx[0]['value'])
                if orientation == LANDSCAPE_ORIENTATION:
                    variable = height
                    height = width
                    width = variable
                # Преобразовать к строковому типу
                ods_properties['pagewidth'] = '%scm' % str(width)
                ods_properties['pageheight'] = '%scm' % str(height)
        else:
            log.warning(u'Параметры печати не определены')

        if fit_to_page:
            ods_properties['scaletopages'] = '1'

        ods_pagelayout = odf.style.PageLayout(name='MyPageLayout')
        # log.debug(u'[ODS] Свойства ориентации страницы <%s>' % ods_properties)
        ods_pagelayoutproperties = odf.style.PageLayoutProperties(**ods_properties)
        ods_pagelayout.addElement(ods_pagelayoutproperties)
        if self.ods_document:
            self.ods_document.automaticstyles.addElement(ods_pagelayout)
                
            masterpage = odf.style.MasterPage(name=DEFAULT_STYLE_ID, pagelayoutname=ods_pagelayout)
            self.ods_document.masterstyles.addElement(masterpage)
        else:
            log.warning(u'Не определен ODS документ')
        return ods_pagelayout

    def _getPageSizeByExcelIndex(self, paper_size_idx):
        """
        Получить размер листа по его индуксу в Excel.

        :param paper_size_idx: Индекс 9-A4 8-A3.
        :return: Кортеж (Ширина в см, Высота в см).
        """
        if type(paper_size_idx) != int:
            paper_size_idx = int(paper_size_idx)
            
        if paper_size_idx == 9:
            # A4
            return 21.0, 29.7
        elif paper_size_idx == 8:
            # A3
            return 42.0, 29.7
        else:
            # По умолчанию A4
            return 21.0, 29.7

    def setTable(self, data_dict, ods_table):
        """
        Заполнить таблицу.

        :param data_dict: Словарь данных.
        :param ods_table: Объект таблицы ODS файла.
        """
        # log.info('table: <%s>' % data_dict)

        # колонки
        i = 1
        columns = self.getChildrenByName(data_dict, 'Column')
        for column in columns:
            # Учет индекса колонки
            idx = int(column.get('Index', i))
            if idx > i:
                for ii in range(idx-i):
                    ods_column = odf.table.TableColumn()
                    ods_table.addElement(ods_column)
                i = idx+1
            else:
                i += 1
            ods_column = self.setColumn(column)
            ods_table.addElement(ods_column)
            
            span = column.get('Span', None)
            if span:
                i += int(span)
        
        # строки
        i = 1
        rows = self.getChildrenByName(data_dict, 'Row')
        for row in rows:
            # Учет индекса строки
            idx = int(row.get('Index', i))
            if idx > i:
                for ii in range(idx-i):
                    ods_row = odf.table.TableRow()
                    ods_table.addElement(ods_row)
                i = idx+1
            else:
                i += 1
                
            ods_row = self.setRow(row)
            ods_table.addElement(ods_row)

            span = row.get('Span', None)
            if span:
                i += int(span)

    def _genColumnStyleName(self):
        """
        Генерация имени стиля колонки.
        """
        return str(uuid.uuid4())

    def _genRowStyleName(self):
        """
        Генерация имени стиля cтроки.
        """
        return str(uuid.uuid4())

    def setColumn(self, data_dict):
        """
        Заполнить колонку.

        :param data_dict: Словарь данных.
        """
        # log.info('column: <%s>' % data_dict)
        
        kwargs = {}
        
        width = data_dict.get('Width', None)

        if width:
            width = self._dimension_xml2ods(width)
            # Создать автоматические стили дбя ширин колонок
            ods_col_style = odf.style.Style(name=self._genColumnStyleName(), family='table-column')
            ods_col_properties = odf.style.TableColumnProperties(columnwidth=width, breakbefore='auto')
            ods_col_style.addElement(ods_col_properties)
            self.ods_document.automaticstyles.addElement(ods_col_style)
            
            kwargs['stylename'] = ods_col_style
        else:
            # Ширина колонки не определена
            ods_col_style = None

        cell_style = data_dict.get('StyleID', None)
        kwargs['defaultcellstylename'] = cell_style

        repeated = data_dict.get('Span', None)
        if repeated:
            repeated = str(int(repeated)+1)
            kwargs['numbercolumnsrepeated'] = repeated

        hidden = data_dict.get('Hidden', False)
        if hidden:
            kwargs['visibility'] = 'collapse'

        ods_column = odf.table.TableColumn(**kwargs)
        return ods_column

    def setRow(self, data_dict):
        """
        Заполнить строку.

        :param data_dict: Словарь данных.
        """
        # log.info(u'Установка строки <%s>' % data_dict)
        
        kwargs = dict()
        height = data_dict.get('Height', None)

        style_name = u''
        if height:
            height = self._dimension_xml2ods(height)
            # Создать автоматические стили дбя высот строк
            style_name = self._genRowStyleName()
            ods_row_style = odf.style.Style(name=style_name, family='table-row')
            ods_row_properties = odf.style.TableRowProperties(rowheight=height, breakbefore='auto')
            ods_row_style.addElement(ods_row_properties)
            self.ods_document.automaticstyles.addElement(ods_row_style)
            
            kwargs['stylename'] = ods_row_style
        else:
            # Высота строки не определена
            ods_row_style = None

        # repeated=data_dict.get('Span',None)
        # if repeated:
        #     self._row_repeated=int(repeated)+1
        #     self._row_repeated_style=ods_row_style
        #
        # if self._row_repeated>0:
        #     self._row_repeated=self._row_repeated-1
        #     if self._row_repeated_style:
        #         kwargs['stylename']=self._row_repeated_style

        hidden = data_dict.get('Hidden', False)
        if hidden:
            kwargs['visibility'] = 'collapse'

        # Зарегистрировать стиль
        if ods_row_style:
            self._styles_[style_name] = ods_row_style

        ods_row = odf.table.TableRow(**kwargs)
        
        # Ячейки
        i = 1
        cells = self.getChildrenByName(data_dict, 'Cell')
        for i_cell, cell in enumerate(cells):
            # Учет индекса ячейки
            idx = int(cell.get('Index', i))
            if idx > i:
                kwargs = dict()
                kwargs['numbercolumnsrepeated'] = (idx-i)

                style_id = self._find_prev_style(cells[:i_cell])
                if style_id:
                    kwargs['stylename'] = self._styles_.get(style_id, None)
                    
                ods_cell = odf.table.CoveredTableCell(**kwargs)
                ods_row.addElement(ods_cell)
                
                i = idx+1
            else:
                i += 1

            ods_cell = self.setCell(cell)
            if ods_cell:
                ods_row.addElement(ods_cell)

            # Учет объединенных ячеек
            merge = int(cell.get('MergeAcross', 0))
            if merge > 0:
                kwargs = dict()
                kwargs['numbercolumnsrepeated'] = merge

                style_id = self._find_prev_style(cells[:i_cell])
                if style_id:
                    kwargs['stylename'] = self._styles_.get(style_id, None)
                
                ods_cell = odf.table.CoveredTableCell(**kwargs)
                ods_row.addElement(ods_cell)
                i += merge
            
        return ods_row

    def _find_prev_style(self, cells):
        """
        Поиск стиля определенного в предыдущей ячейке.

        :param cells: Список предыдущих ячеек.
        :return: Идентификатор исокмого стиля или None если стиль не определен.
        """
        for cell in reversed(cells):
            if 'StyleID' in cell:
                return cell.get('StyleID', None)
        return None
        
    def getCellValue(self, data_dict):
        """
        Получить значение ячейки.

        :param data_dict: Словарь данных.
        """
        type = self.getCellType(data_dict)
        
        if type != 'string':
            dates = self.getChildrenByName(data_dict, 'Data')
            value = ''
            if dates:
                value = str(dates[0].get('value', ''))  # DEFAULT_ENCODE)
            return value
        return None
        
    def getCellType(self, data_dict):
        """
        Тип значения ячейки.

        :param data_dict: Словарь данных.
        """
        dates = self.getChildrenByName(data_dict, 'Data')
        type = 'string'
        if dates:
            type = dates[0].get('Type', 'string').lower()
        
        if type == 'number':
            type = 'float'
        elif type == 'percentage':
            # ВНИМЕНИЕ! Здесь необходимо сделать проверку
            # на соответствие данных процентному типу
            str_value = dates[0].get('value', 'None')
            try:
                value = float(str_value)
            except:
                log.warning(u'Значение <%s> не [percentage] типа' % str_value)
                type = 'string'
        return type            
    
    # Имена колонок Excel в формате A1
    COLS_A1 = None

    def _getColsA1(self):
        """
        Имена колонок Excel в формате A1.
        """
        if self.COLS_A1:
            return self.COLS_A1

        sAlf1 = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        sAlf2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.COLS_A1 = []
        for s1 in sAlf1:
            for s2 in sAlf2:
                self.COLS_A1.append((s1+s2).strip())
                if len(self.COLS_A1) == 256:
                    return self.COLS_A1
        return self.COLS_A1
        
    R1_FORMAT = r'R[0-9]{1,5}'
    C1_FORMAT = r'C[0-9]{1,5}'

    def _getA1(self, r1c1):
        """
        Преабразовать адрес из формата R1C1 в A1.
        """
        parse = re.findall(self.R1_FORMAT, r1c1)
        row = 1
        if parse:
            row = int(parse[0][1:])
        parse = re.findall(self.C1_FORMAT, r1c1)
        col = 1
        if parse:
            col = int(parse[0][1:])
        cols_a1 = self._getColsA1()
        return cols_a1[col-1]+str(row)

    ALPHA_FORMAT = r'[A-Z]{1,2}'
    DIGIT_FORMAT = r'[0-9]{1,5}'

    def _getR1C1(self, a1):
        """
        Преабразовать адрес из формата A1 в R1C1.
        """
        parse = re.findall(self.DIGIT_FORMAT, a1)
        row = 1
        if parse:
            row = int(parse[0])
        parse = re.findall(self.ALPHA_FORMAT, a1)
        col = 1
        if parse:
            cols_a1 = self._getColsA1()
            try:
                col = cols_a1.index(parse[0]) + 1
            except:
                pass
        return 'R%dC%d' % (row, col)
        
    R1C1_FORMAT = r'R[0-9]{1,5}C[0-9]{1,5}'

    def _R1C1Fmt2A1Fmt(self, formula):
        """
        Перевод формулы из формата R1C1 в формат A1.

        :param formula: Формула в строковом представлении.
        :return: Строка транслированной формулы.
        """
        parse_all = re.findall(self.R1C1_FORMAT, formula)
        for replace_addr in parse_all:
            a1 = self._getA1(replace_addr)
            if self._is_sheetAddress(replace_addr, formula):
                a1 = '.'+a1
            formula = formula.replace(replace_addr, a1)
        return formula

    def _is_sheetAddress(self, address, formula):
        """
        Адресация ячейки с указанием листа? Например Лист1.A1

        :param address: Адресс ячейки.
        :param formula: Формула в строковом представлении.
        :return: True/False.
        """
        if address in formula:
            i = formula.index(address)
            if i > 0:
                return formula[i - 1].isalnum()
            else:
                return False
        return None

    A1_FORMAT = r'\.[A-Z]{1,2}[0-9]{1,5}'

    def _A1Fmt2R1C1Fmt(self, formula):
        """
        Перевод формулы из формата A1 в формат R1C1.

        :param formula: Формула в строковом представлении.
        :return: Строка транслированной формулы.
        """
        parse_all = re.findall(self.A1_FORMAT, formula)
        for replace_addr in parse_all:
            r1c1 = self._getR1C1(replace_addr)
            formula = formula.replace(replace_addr, r1c1)
        return formula
        
    def _translateR1C1Formula(self, formula):
        """
        Перевод формулы из формата R1C1 в формат ODS файла.

        :param formula: Формула в строковом представлении.
        :return: Строка транслированной формулы.
        """
        return self._R1C1Fmt2A1Fmt(formula)

    def _translateA1Formula(self, formula):
        """
        Перевод формулы из формата ODS(A1) в формат R1C1.

        :param formula: Формула в строковом представлении.
        :return: Строка транслированной формулы.
        """
        return self._A1Fmt2R1C1Fmt(formula)
        
    def setCell(self, data_dict):
        """
        Заполнить ячейку.

        :param data_dict: Словарь данных.
        """
        # log.info('new_cell: <%s>' % data_dict)

        properties = {}
        ods_type = self.getCellType(data_dict)
        properties['valuetype'] = ods_type
        style_id = data_dict.get('StyleID', None)
        if style_id:
            ods_style = self._styles_.get(style_id, None)
            properties['stylename'] = ods_style
        
        merge_across = int(data_dict.get('MergeAcross', 0))
        if merge_across:
            merge_across = str(merge_across+1)
            properties['numbercolumnsspanned'] = merge_across
            
        merge_down = int(data_dict.get('MergeDown', 0))
        if merge_down:
            merge_down = str(merge_down+1)
            properties['numberrowsspanned'] = merge_down
            
        formula = data_dict.get('Formula', None)
        if formula:
            properties['formula'] = self._translateR1C1Formula(formula)
        else:
            value = self.getCellValue(data_dict)
            properties['value'] = value
        # log.debug(u'Ячейка. Свойства <%s>' % properties)
        ods_cell = odf.table.TableCell(**properties)
            
        dates = self.getChildrenByName(data_dict, 'Data')
        # Разбить на строки
        values = self.getDataValues(data_dict)
        # log.info(u'Ячейка. Значение <%s>' % values)
        for data in dates:
            for val in values:
                ods_data = self.setData(data, style_id, val)
                if ods_data:
                    ods_cell.addElement(ods_data)
            
        return ods_cell
        
    def getDataValues(self, data_dict):
        """
        Получить значение ячейки с разбитием по строкам.

        :param data_dict: Словарь данных.
        """
        dates = self.getChildrenByName(data_dict, 'Data')
        value = ''
        if dates:
            value = str(dates[0].get('value', ''))  # DEFAULT_ENCODE)
        return value.split(SPREADSHEETML_CR)
    
    def setData(self, data_dict, style_id=None, value=None):
        """
        Заполнить ячейку данными.

        :param data_dict: Словарь данных.
        :param style_id: Идентификатор стиля.
        :param value: Значение строки.
        """
        # log.info(u'Установка данных <%s>. Стиль <%s>' % (data_dict, style_id))
        
        ods_style = None
        if style_id:
            ods_style = self._styles_.get(style_id, None)

        ods_data = None
        if value:
            # Просто текст
            if style_id and style_id != DEFAULT_STYLE_ID:
                ods_data = odf.text.P()
                style_span = odf.text.Span(stylename=ods_style, text=value)
                ods_data.addElement(style_span)
            else:
                ods_data = odf.text.P(text=value)
        return ods_data
        
    def load(self, filename):
        """
        Загрузить из ODS файла.

        :param filename: Имя ODS файла.
        :return: Словарь данных или None в случае ошибки.
        """
        if not os.path.exists(filename):
            # Если файл не существует то верноть None
            log.warning(u'Файл <%s> не существует' % filename)
            return None
        else:
            try:
                return self._loadODS(filename)
            except:
                log.fatal(u'Ошибка открытия файла <%s>' % filename)
                raise                
        
    def _loadODS(self, filename):
        """
        Загрузить из ODS файла.

        :param filename: Имя ODS файла.
        :return: Словарь данных или None в случае ошибки.
        """
        self.ods_document = odf.opendocument.load(filename)
        
        self.xmlss_data = {'name': 'Calc', 'children': []}
        ods_workbooks = self.ods_document.getElementsByType(odf.opendocument.Spreadsheet)
        if ods_workbooks:
            workbook_data = self.readWorkbook(ods_workbooks[0])
            self.xmlss_data['children'].append(workbook_data)
        return self.xmlss_data
    
    def readWorkbook(self, ods_element=None):
        """
        Прочитать из ODS файла данные о книге.

        :param ods_element: ODS элемент соответствующий книги Excel.
        """
        data = {'name': 'Workbook', 'children': []}
        
        styles_data = self.readStyles()
        data['children'].append(styles_data)
        
        ods_tables = ods_element.getElementsByType(odf.table.Table)
        if ods_tables:
            for ods_table in ods_tables:
                worksheet_data = self.readWorksheet(ods_table)
                data['children'].append(worksheet_data)
        
        return data

    def readNumberStyles(self, *ods_styles):
        """
        Прочитать данные о стилях числовых форматов.

        :param ods_styles: Список стилей.
        """
        if not ods_styles:
            log.warning(u'Не определены ODS стили для чтения числовых стилей')
            return {}
            
        result = {}
        for ods_styles in ods_styles:
            num_styles = ods_styles.getElementsByType(odf.number.NumberStyle)
            percentage_styles = ods_styles.getElementsByType(odf.number.PercentageStyle)
            styles = num_styles + percentage_styles
            if styles:
                for style in styles:
                    result[style.getAttribute('name')] = style
    
        # log.debug(u'Числовые стили <%s>' % result)
        return result
        
    def readStyles(self, ods_element=None):
        """
        Прочитать из ODS файла данные о стилях.

        :param ods_element: ODS элемент соответствующий стилям книги Excel.
        """
        data = {'name': 'Styles', 'children': []}
        ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style) + \
            self.ods_document.styles.getElementsByType(odf.style.Style) + \
            self.ods_document.masterstyles.getElementsByType(odf.style.Style)

        # Стили числовых форматов
        self._number_styles_ = self.readNumberStyles(self.ods_document.automaticstyles,
                                                     self.ods_document.styles,
                                                     self.ods_document.masterstyles)
        
        # log.debug('STYLES <%s>' % ods_styles)
        
        for ods_style in ods_styles:
            style = self.readStyle(ods_style)
            data['children'].append(style)
                        
        return data

    def readStyle(self, ods_element=None):
        """
        Прочитать из ODS файла данные о стиле.

        :param ods_element: ODS элемент соответствующий стилю Excel.
        """
        data = {'name': 'Style', 'children': []}
        id = ods_element.getAttribute('name')
        data['ID'] = id
        
        data_style_name = ods_element.getAttribute('datastylename')
        if data_style_name:
            number_style = self._number_styles_.get(data_style_name, None)
            if number_style:
                number_format_data = self.readNumberFormat(number_style)
                if number_format_data:
                    data['children'].append(number_format_data)

        # Чтение шрифта
        txt_properties = ods_element.getElementsByType(odf.style.TextProperties)
        if txt_properties:
            font_data = self.readFont(txt_properties[0])
            if font_data:
                data['children'].append(font_data)

        # Чтение бордеров
        tab_cell_properties = ods_element.getElementsByType(odf.style.TableCellProperties)
        if tab_cell_properties:
            borders_data = self.readBorders(tab_cell_properties[0])
            if borders_data:
                data['children'].append(borders_data)

        # Чтение интерьера
        if tab_cell_properties:
            interior_data = self.readInterior(tab_cell_properties[0])
            if interior_data:
                data['children'].append(interior_data)

        # Чтение выравнивания
        align_data = {}
        paragraph_properties = ods_element.getElementsByType(odf.style.ParagraphProperties)
        if paragraph_properties:
            paragraph_align_data = self.readAlignmentParagraph(paragraph_properties[0])
            if paragraph_align_data:
                align_data.update(paragraph_align_data)

        if tab_cell_properties:
            cell_align_data = self.readAlignmentCell(tab_cell_properties[0])
            if cell_align_data:
                align_data.update(cell_align_data)
                
        if align_data:
            data['children'].append(align_data)
        
        # log.debug(u'Чтение стиля %s : %s : %s' % (style_id, txt_properties, tab_cell_properties))
        
        return data        
    
    def readNumberFormat(self, ods_element=None):
        """
        Прочитать из ODS файла данные о формате числового представления.

        :param ods_element: ODS элемент соответствующий стилю числового представления.
        """
        if ods_element is None:
            log.warning('Not define ods_element <%s>' % ods_element)
            return None
        
        numbers = ods_element.getElementsByType(odf.number.Number)
        if not numbers:
            log.warning('Not define numbers in ods_element <%s>' % ods_element)
            return None
        else:
            number = numbers[0]

        decimalplaces_str = number.getAttribute('decimalplaces')
        decimalplaces = int(decimalplaces_str) if decimalplaces_str not in ('None', 'none', 'NONE', None) else 0
        minintegerdigits_str = number.getAttribute('minintegerdigits')
        minintegerdigits = int(minintegerdigits_str) if minintegerdigits_str not in ('None', 'none', 'NONE', None) else 0
        grouping = number.getAttribute('grouping')
        percentage = 'percentage-style' in ods_element.tagName

        decimalplaces_format = ','+'0' * decimalplaces if decimalplaces else ''
        minintegerdigits_format = '0' * minintegerdigits
        grouping_format = '#' * (4 - minintegerdigits) if minintegerdigits<4 else ''
        percentage_format = '%' if percentage else ''
        
        if grouping and (grouping not in ('None', 'none', 'NONE', 'false')):
            format = list(grouping_format + minintegerdigits_format)
            format_result = []
            count = 3
            for i in range(len(format)-1, -1, -1):
                format_result = [format[i]] + format_result
                count = count - 1
                if not count:
                    format_result = [' '] + format_result
                    count = 3
            number_format = ''.join(format_result) + decimalplaces_format + percentage_format
        else:
            number_format = minintegerdigits_format + decimalplaces_format + percentage_format
            
        # log.debug('NUMBER FORMAT %s' % (number_format))
        data = {'name': 'NumberFormat', 'children': [], 'Format': number_format}
        return data
        
    def readFont(self, ods_element=None):
        """
        Прочитать из ODS файла данные о шрифте.

        :param ods_element: ODS элемент соответствующий ствойствам текста стиля.
        """
        name = ods_element.getAttribute('fontname')
        name = name if name else ods_element.getAttribute('fontfamily')
        size = ods_element.getAttribute('fontsize')
        bold = ods_element.getAttribute('fontweight')
        italic = ods_element.getAttribute('fontstyle')
        # Зачеркивание
        through_style = ods_element.getAttribute('textlinethroughstyle')
        # through_type = ods_element.getAttribute('textlinethroughtype')
        # Подчеркивание
        underline_style = ods_element.getAttribute('textunderlinestyle')
        # underline_width = ods_element.getAttribute('textunderlinewidth')

        data = {'name': 'Font', 'children': []}
        if name and (name not in ('None', 'none', 'NONE')):
            data['FontName'] = name
            
        if size and (size not in ('None', 'none', 'NONE')):
            if size[-2:] == 'pt':
                size = size[:-2]
            data['Size'] = size
        if bold and (bold not in ('None', 'none', 'NONE', 'normal')):
            data['Bold'] = '1'
        if italic and (italic not in ('None', 'none', 'NONE', 'normal')):
            data['Italic'] = '1'

        if through_style and (through_style not in ('None', 'none', 'NONE', 'normal')):
            data['StrikeThrough'] = '1'
        if underline_style and (underline_style not in ('None', 'none', 'NONE', 'normal')):
            data['Underline'] = 'Single'

        # log.debug('Read FONT: %s : %s : %s : %s : %s : %s' % (name, size, bold, italic, through_style, underline_style))
        
        return data
        
    def readInterior(self, ods_element=None):
        """
        Прочитать из ODS файла данные о бордерах.

        :param ods_element: ODS элемент соответствующий ствойствам ячейки таблицы стиля.
        """
        data = {'name': 'Interior', 'children': []}

        color = ods_element.getAttribute('backgroundcolor')

        # log.debug('Read INTERIOR: color <%s>' % color)

        if color and (color not in ('None', 'none', 'NONE')):
            data['Color'] = color.strip()

        return data

    def readBorders(self, ods_element=None):
        """
        Прочитать из ODS файла данные о бордерах.

        :param ods_element: ODS элемент соответствующий ствойствам ячейки таблицы стиля.
        """
        data = {'name': 'Borders', 'children': []}
        
        all_border = ods_element.getAttribute('border')
        left = ods_element.getAttribute('borderleft')
        right = ods_element.getAttribute('borderright')
        top = ods_element.getAttribute('bordertop')
        bottom = ods_element.getAttribute('borderbottom')
        
        # log.debug('BORDERS: border %s Left: %s Right: %s Top: %s Bottom: %s' % (all_border, left, right, top, bottom))
        
        if all_border and (all_border not in ('None', 'none', 'NONE')):
            border = self.parseBorder(all_border, 'Left')
            if border:
                data['children'].append(border)
            border = self.parseBorder(all_border, 'Right')
            if border:
                data['children'].append(border)
            border = self.parseBorder(all_border, 'Top')
            if border:
                data['children'].append(border)
            border = self.parseBorder(all_border, 'Bottom')
            if border:
                data['children'].append(border)
                
        if left and (left not in ('None', 'none', 'NONE')):
            border = self.parseBorder(left, 'Left')
            if border:
                data['children'].append(border)
            
        if right and (right not in ('None', 'none', 'NONE')):
            border = self.parseBorder(right, 'Right')
            if border:
                data['children'].append(border)
        
        if top and (top not in ('None', 'none', 'NONE')):
            border = self.parseBorder(top, 'Top')
            if border:
                data['children'].append(border)
            
        if bottom and (bottom not in ('None', 'none', 'NONE')):
            border = self.parseBorder(bottom, 'Bottom')
            if border:
                data['children'].append(border)
            
        return data
        
    def readAlignmentParagraph(self, ods_element=None):
        """
        Прочитать из ODS файла данные о выравнивании текста.

        :param ods_element: ODS элемент соответствующий ствойствам параграфа.
        """
        data = {'name': 'Alignment', 'children': []}

        text_align = ods_element.getAttribute('textalign')
        vert_align = ods_element.getAttribute('verticalalign')
        
        if text_align == 'start':
            data['Horizontal'] = 'Left'
        elif text_align == 'end':
            data['Horizontal'] = 'Right'
        elif text_align == 'center':
            data['Horizontal'] = 'Center'
        elif text_align == 'justify':
            data['Horizontal'] = 'Justify'

        if vert_align == 'top':
            data['Vertical'] = 'Top'
        elif vert_align == 'bottom':
            data['Vertical'] = 'Bottom'
        elif vert_align == 'middle':
            data['Vertical'] = 'Center'
        elif vert_align == 'justify':
            data['Vertical'] = 'Justify'
            
        # log.debug('ALIGNMENT PARAGRAPH: %s:%s' % (text_align, vert_align))
        
        return data
        
    def readAlignmentCell(self, ods_element=None):
        """
        Прочитать из ODS файла данные о выравнивании текста.

        :param ods_element: ODS элемент соответствующий ствойствам ячейки.
        """
        data = {'name': 'Alignment', 'children': []}

        vert_align = ods_element.getAttribute('verticalalign')
        wrap_txt = ods_element.getAttribute('wrapoption')

        if vert_align == 'top':
            data['Vertical'] = 'Top'
        elif vert_align == 'bottom':
            data['Vertical'] = 'Bottom'
        elif vert_align == 'middle':
            data['Vertical'] = 'Center'
            
        if wrap_txt and wrap_txt == 'wrap':
            data['WrapText'] = '1'
            
        # log.debug('ALIGNMENT CELL: %s' % vert_align)
        
        return data
        
    def parseBorder(self, data_string, position=None):
        """
        Распарсить бордер.

        :param data_string: Строка данных в виде <1pt solid #000000>.
        :param position: Позиция бордера.
        :return: Заполненный словарь бордера.
        """
        border = None
        if data_string:
            border_data = self.parseBorderData(data_string)
            if border_data:
                border = {'name': 'Border', 'Position': position,
                          'Weight': border_data.get('weight', '1'),
                          'LineStyle': self._lineStyles_ODS2SpreadsheetML.get(border_data.get('line', None), 'Continuous'),
                          'Color': border_data.get('color', '000000')}
            # log.debug('PARSE BORDER: %s : %s' % (data_string, border))
            
        return border
            
    def parseBorderData(self, data_string):
        """
        Распарсить данные бордера.

        :param data_string: Строка данных в виде <1pt solid #000000>.
        :return: Словарь {'weight':1,'line':'solid','color':'#000000'}.
        """
        if data_string in ('None', 'none', 'NONE'):
            return None
        
        weight_pattern_pt = r'([\.\d]+)pt'
        weight_pattern_cm = r'([\.\d]+)cm'
        line_style_pattern = r' [a-zA-Z]* '
        color_pattern = r'#......'
        
        result = {}

        weight_pt = re.findall(weight_pattern_pt, data_string)
        weight_cm = re.findall(weight_pattern_cm, data_string)
        if weight_pt:
            result['weight'] = weight_pt[0]
        elif weight_cm:
            # Ширина может задаватся в см поэтому нужно преобразовать в пт
            result['weight'] = str(float(weight_cm[0])*CM2PT_CORRECT)
            
        line_style = re.findall(line_style_pattern, data_string)
        if line_style:
            result['line'] = line_style[0].strip()

        color = re.findall(color_pattern, data_string)
        if color:
            result['color'] = color[0]
        
        return result

    def readWorksheet(self, ods_element=None):
        """
        Прочитать из ODS файла данные о листе.

        :param ods_element: ODS элемент соответствующий листу.
        """
        data = {'name': 'Worksheet', 'children': []}
        name = ods_element.getAttribute('name')

        # log.debug('WORKSHEET: <%s : %s>' % (type(name), name))
        
        data['Name'] = name
        
        table = {'name': 'Table', 'children': []}
        
        # Колонки
        ods_columns = ods_element.getElementsByType(odf.table.TableColumn)
        for ods_column in ods_columns:
            column_data = self.readColumn(ods_column)
            table['children'].append(column_data)
            
        # Строки
        ods_rows = ods_element.getElementsByType(odf.table.TableRow)
        for i, ods_row in enumerate(ods_rows):
            row_data = self.readRow(ods_row, table, data, i)
            table['children'].append(row_data)
      
        data['children'].append(table)
        
        # Параметры страницы
        ods_pagelayouts = self.ods_document.automaticstyles.getElementsByType(odf.style.PageLayout)
        worksheet_options = self.readWorksheetOptions(ods_pagelayouts)
        if worksheet_options:
            data['children'].append(worksheet_options)
        
        return data
    
    def readWorksheetOptions(self, ods_page_layouts):
        """
        Прочитать из ODS файла данные о параметрах страницы.

        :param ods_page_layouts: Список найденных параметров страницы.
        """
        # log.debug(u'Чтение данных параметров страницы из ODS')
        if not ods_page_layouts:
            log.warning(u'Not define page layout')
            return None

        # log.debug(u'Set default worksheet options')
        options = {'name': 'WorksheetOptions',
                   'children': [{'name': 'PageSetup',
                                 'children': [{'name': 'Layout',
                                               'Orientation': PORTRAIT_ORIENTATION},
                                              {'name': 'PageMargins',
                                               'Top': str(DEFAULT_XML_MARGIN_TOP),
                                               'Bottom': str(DEFAULT_XML_MARGIN_BOTTOM),
                                               'Left': str(DEFAULT_XML_MARGIN_LEFT),
                                               'Right': str(DEFAULT_XML_MARGIN_RIGHT)},
                                              ]
                                 },
                                {'name': 'Print',
                                 'children': [{'name': 'PaperSizeIndex',
                                               'value': '9'}
                                              ]
                                 }
                                ]
                   }
        
        # for pagelayout in ods_page_layouts:
        #    log.debug(u'Чтение значения параметров страницы <%s> : %s' % (text(pagelayout.getAttribute('name')),
        #                                                                  text(pagelayout.getAttribute('pageusage'))))
        for pagelayout in ods_page_layouts:
            # log.debug(u'Чтение значения параметров страницы <%s>' % text(pagelayout.getAttribute('name')))
            properties = pagelayout.getElementsByType(odf.style.PageLayoutProperties)
            # log.debug(u'Properties: %s' % text(properties))
            if properties:
                properties = properties[0]
                orientation = properties.getAttribute('printorientation')
                margin = properties.getAttribute('margin')
                # log.debug(u'Margin: %s' % margin)
                margin_top = properties.getAttribute('margintop')
                # log.debug(u'Margin Top: %s' % margin_top)
                margin_bottom = properties.getAttribute('marginbottom')
                # log.debug(u'Margin Bottom: %s' % margin_bottom)
                margin_left = properties.getAttribute('marginleft')
                # log.debug(u'Margin Left: %s' % margin_left)
                margin_right = properties.getAttribute('marginright')
                # log.debug(u'Margin Right: %s' % margin_right)
                page_width = properties.getAttribute('pagewidth')
                # log.debug(u'Page Width: %s' % page_width)
                page_height = properties.getAttribute('pageheight')
                # log.debug(u'Page Height: %s' % page_height)
                fit_to_page = properties.getAttribute('scaletopages')
                # log.debug(u'Fit To Pages: %s' % fit_to_page)
                scale_to = properties.getAttribute('scaleto')
                # log.debug(u'Scale To: %s' % scale_to)

                if orientation:
                    options['children'][0]['children'][0]['Orientation'] = orientation.title()
                if margin:
                    options['children'][0]['children'][1]['Top'] = self._dimension_cm2inch(margin)
                    options['children'][0]['children'][1]['Bottom'] = self._dimension_cm2inch(margin)
                    options['children'][0]['children'][1]['Left'] = self._dimension_cm2inch(margin)
                    options['children'][0]['children'][1]['Right'] = self._dimension_cm2inch(margin)
                if margin_top:
                    options['children'][0]['children'][1]['Top'] = self._dimension_cm2inch(margin_top)
                if margin_bottom:
                    options['children'][0]['children'][1]['Bottom'] = self._dimension_cm2inch(margin_bottom)
                if margin_left:
                    options['children'][0]['children'][1]['Left'] = self._dimension_cm2inch(margin_left)
                if margin_right:
                    options['children'][0]['children'][1]['Right'] = self._dimension_cm2inch(margin_right)
                if fit_to_page or (scale_to == (1, 1)):
                    options['children'].append({'name': 'FitToPage'})

                if page_width and page_height:
                    # Установить размер листа
                    options['children'][1]['children'][0]['value'] = self._getExcelPaperSizeIndex(page_width, page_height)
                # ВНИМАНИЕ! Обычно параметры печати указанные в начале и являются
                # параметрами по умолчанию. Поэтому пропускаем все остальные
                break
            else:
                # log.debug(u'Not define worksheet options')
                continue
        return options

    def _getExcelPaperSizeIndex(self, page_width, page_height):
        """
        Определить по размеру листа его индекс в списке Excel.
        """
        paper_format = self._getPaperSizeFormat(page_width, page_height)
        
        if paper_format is None:
            # По умолчанию A4
            return '9'
        elif paper_format == A4_PAPER_FORMAT:
            return '9'
        elif paper_format == A3_PAPER_FORMAT:
            return '8'
        return None
        
    def _getPaperSizeFormat(self, page_width, page_height):
        """
        Определить по размеру листа его формат.

        :param page_width: Ширина листа в см.
        :param page_height: Высота листа в см.
        :return: A4 или A3.
        """
        if isinstance(page_width, str):
            page_width_txt = page_width.replace('cm', '').replace('mm', '')
            page_width = float(page_width_txt)
        if isinstance(page_height, str):
            page_height_txt = page_height.replace('cm', '').replace('mm', '')
            page_height = float(page_height_txt)

        # Если задается в сантиметрах
        if round(page_width, 1) == 21.0 and round(page_height, 1) == 29.7:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 29.7 and round(page_height, 1) == 21.0:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 29.7 and round(page_height, 1) == 42.0:
            return A3_PAPER_FORMAT
        elif round(page_width, 1) == 42.0 and round(page_height, 1) == 29.7:
            return A3_PAPER_FORMAT
        # Если задается в миллиметрах
        elif round(page_width, 1) == 210.0 and round(page_height, 1) == 297.0:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 297.0 and round(page_height, 1) == 210.0:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 297.0 and round(page_height, 1) == 420.0:
            return A3_PAPER_FORMAT
        elif round(page_width, 1) == 420.0 and round(page_height, 1) == 297.0:
            return A3_PAPER_FORMAT
        return None
        
    def readColumn(self, ods_element=None):
        """
        Прочитать из ODS файла данные о колонке.

        :param ods_element: ODS элемент соответствующий колонке.
        """
        data = {'name': 'Column', 'children': []}
        style_name = ods_element.getAttribute('stylename')
        default_cell_style_name = ods_element.getAttribute('defaultcellstylename')
        repeated = ods_element.getAttribute('numbercolumnsrepeated')
        hidden = ods_element.getAttribute('visibility')

        if style_name:
            # Определение ширины колонки
            column_width = None
            ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style)
            find_style = [ods_style for ods_style in ods_styles if ods_style.getAttribute('name') == style_name]
            if find_style:
                ods_style = find_style[0]
                ods_column_properties = ods_style.getElementsByType(odf.style.TableColumnProperties)
                if ods_column_properties:
                    ods_column_property = ods_column_properties[0]
                    column_width = self._dimension_ods2xml(ods_column_property.getAttribute('columnwidth'))
                    if column_width:
                        data['Width'] = column_width
            # log.debug('COLUMN: %s Width: %s Cell style: %s' % (style_name, column_width, default_cell_style_name))
        
        if default_cell_style_name and (default_cell_style_name not in ('Default', 'None', 'none', 'NONE')):
            data['StyleID'] = default_cell_style_name

        if repeated and repeated != 'None':
            repeated = str(int(repeated)-1)
            data['Span'] = repeated

        if hidden and hidden == 'collapse':
            data['Hidden'] = True

        return data
    
    def _dimension_ods2xml(self, dimension):
        """
        Перевод размеров из представления ODS в XML.

        :param dimension: Строковое представление размера.
        """
        if not dimension:
            return None
        elif (len(dimension) > 2) and (dimension[-2:] == 'cm'):
            # Размер указан в сентиметрах?
            return str(float(dimension[:-2]) * 28)
        elif (len(dimension) > 2) and (dimension[-2:] == 'mm'):
            # Размер указан в миллиметрах?
            return str(float(dimension[:-2]) * 2.8)
        else:
            # Размер указан в точках
            return str(float(dimension) / DIMENSION_CORRECT)

    def _dimension_xml2ods(self, dimension):
        """
        Перевод размеров из представления XML в ODS.

        :param dimension: Строковое представление размера в дюймах.
        """
        return str(float(dimension) * DIMENSION_CORRECT)

    def _dimension_inch2cm(self, sDimension, is_postfix=False):
        """
        Перевод размеров из представления в дюймах в сантиментры.

        :param sDimension: Строковое представление размера в дюймах.
        :param is_postfix: Добавить cm в качестве постфикса в строке?
        """
        return str(float(sDimension) * INCH2CM) + (' cm' if is_postfix else '')

    def _dimension_cm2inch(self, dimension):
        """
        Перевод размеров из представления в сантиментрах/мм в дюймы.

        :param dimension: Строковое представление размера в сантиметрах/мм.
        """
        if not dimension:
            return None
        elif (len(dimension) > 2) and (dimension[-2:] == 'cm'):
            # Размер указан в сентиметрах?
            return str(float(dimension[:-2]) / INCH2CM)
        elif (len(dimension) > 2) and (dimension[-2:] == 'mm'):
            # Размер указан в миллиметрах?
            return str(float(dimension[:-2]) / 10.0 / INCH2CM)
        else:
            # Размер указан в точках
            return str(float(dimension) / DIMENSION_CORRECT)

    def _add_page_break(self, worksheet, row):
        """
        Добавить разрыв страницы.

        :param worksheet: Словарь, описывающий лист.
        :param row: Номер строки.
        """
        find_page_breaks = [child for child in worksheet['children'] if child['name'] == 'PageBreaks']
        if find_page_breaks:
            data = find_page_breaks[0]
        else:
            data = {'name': 'PageBreaks', 'children': [{'name': 'RowBreaks', 'children': []}]}
            worksheet['children'].append(data)

        row_break = {'name': 'RowBreak', 'children': [{'name': 'Row', 'value': row}]}
        data['children'][0]['children'].append(row_break)
        return data

    def readRow(self, ods_element=None, table=None, worksheet=None, row=-1):
        """
        Прочитать из ODS файла данные о строке.

        :param ods_element: ODS элемент соответствующий строке.
        :param table: Словарь, описывающий таблицу.
        :param worksheet: Словарь, описывающий лист.
        :param row: Номер строки.
        """
        data = {'name': 'Row', 'children': []}
        style_name = ods_element.getAttribute('stylename')
        repeated = ods_element.getAttribute('numberrowsrepeated')
        hidden = ods_element.getAttribute('visibility')

        if style_name:
            # Определение высоты строки
            row_height = None
            ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style)
            find_style = [ods_style for ods_style in ods_styles if ods_style.getAttribute('name') == style_name]
            if find_style:
                ods_style = find_style[0]
                ods_row_properties = ods_style.getElementsByType(odf.style.TableRowProperties)
                if ods_row_properties:
                    ods_row_property = ods_row_properties[0]
                    row_height = self._dimension_ods2xml(ods_row_property.getAttribute('rowheight'))
                    if row_height:
                        data['Height'] = row_height
                    # Разрывы страниц
                    page_break = ods_row_property.getAttribute('breakbefore')
                    if page_break and page_break == 'page' and worksheet:
                        self._add_page_break(worksheet, row)
                    # log.debug('ROW: %s \tHeight: %s \tPageBreak: %s \tStyle: %s' % (style_name, row_height, page_break, style_name))
        
        if repeated and (repeated not in ('None', 'none', 'NONE')):
            # Дополниетельное условие необходимо для
            # исключения ошибочной ситуации когда параметры строки
            # дублируются на все последующие строки
            # (в LibreOffice это сделано для дублирования стиля ячеек
            # построчно в конце листа)
            i_repeated = int(repeated)
            if i_repeated <= LIMIT_ROWS_REPEATED:
                repeated = i_repeated-1
                if table:
                    for i in range(repeated):
                        table['children'].append(self.readRow(ods_element))
                else:
                    data['Span'] = str(repeated)

        if hidden and hidden == 'collapse':
            data['Hidden'] = True

        # Обработка ячеек
        ods_cells = ods_element.childNodes
        
        i = 1
        set_idx = False
        # log.debug(u'Количество ячеек строки [%d]' % len(ods_cells))
        for ods_cell in ods_cells:
            # log.debug(u'Обработка ячейки <%s>' % ods_cell.qname[-1])
            if ods_cell.qname[-1] == 'covered-table-cell':
                repeated = ods_cell.getAttribute('numbercolumnsrepeated')
                if repeated and (repeated not in ('None', 'none', 'NONE')):
                    # Учет индекса и пропущенных ячеек
                    i += int(repeated)  # +1
                    set_idx = True
                else:
                    # Стоит просто ячейка и ее надо учесть
                    i += 1
                    set_idx = True
            elif ods_cell.qname[-1] == 'table-cell':
                cell_data = self.readCell(ods_cell, i if set_idx else None)
                data['children'].append(cell_data)
                if set_idx:
                    set_idx = False

                repeated = ods_cell.getAttribute('numbercolumnsrepeated')
                if repeated and (repeated not in ('None', 'none', 'NONE')):
                    # Учет индекса и пропущенных ячеек
                    i_repeated = int(repeated)
                    if i_repeated < LIMIT_COLUMNS_REPEATED:
                        for ii in range(i_repeated-1):
                            cell_data = self.readCell(ods_cell)
                            data['children'].append(cell_data)
                            i += 1
                        # ВНИМАНИЕ! Здесь необходимо добавить 1 иначе таблицы/штампы могут "плыть"
                        i += 1
                    else:
                        i += i_repeated     # +1
                        set_idx = True
                else:
                    i += 1
                        
        return data
    
    def hasODSAttribute(self, ods_element, attr_name):
        """
        Имеется в ODS элементе атрибут с таким именем?

        :param ods_element: ODS элемент.
        :param attr_name: Имя атрибута.
        :return: True/False.
        """
        return attr_name in [attr[-1].replace('-', '') for attr in ods_element.attributes.keys()]
        
    def readCell(self, ods_element=None, index=None):
        """
        Прочитать из ODS файла данные о ячейке.

        :param ods_element: ODS элемент соответствующий ячейке.
        :type index: C{int}
        :param index: Индекс ячейки, если необходимо указать.
        """
        data = {'name': 'Cell', 'children': []}
        if index:
            data['Index'] = str(index)

        style_name = ods_element.getAttribute('stylename')
        if style_name:
            data['StyleID'] = style_name

        formula = ods_element.getAttribute('formula')
        if formula:
            data['Formula'] = self._translateA1Formula(formula)
            
        merge_across = None
        if self.hasODSAttribute(ods_element, 'numbercolumnsspanned'):
            numbercolumnsspanned = ods_element.getAttribute('numbercolumnsspanned')
            if numbercolumnsspanned:
                merge_across = int(numbercolumnsspanned)-1
                data['MergeAcross'] = merge_across
            
        merge_down = None
        if self.hasODSAttribute(ods_element, 'numberrowsspanned'):
            numberrowsspanned = ods_element.getAttribute('numberrowsspanned')
            if numberrowsspanned:
                merge_down = int(numberrowsspanned)-1
                data['MergeDown'] = merge_down
        
        ods_data = ods_element.getElementsByType(odf.text.P)
        if ods_data:
            value = ods_element.getAttribute('value')
            valuetype = ods_element.getAttribute('valuetype')
            # log.debug(u'Значение ячейки <%s : %s>' % (value, valuetype))
            cur_data = None
            for i, ods_txt in enumerate(ods_data):
                data_data = self.readData(ods_txt, value, valuetype)
                if not i:
                    cur_data = data_data
                else:
                    cur_data['value'] += SPREADSHEETML_CR+data_data['value']
            data['children'].append(cur_data)
        
        # log.debug('CELL Style: %s MergeAcross: %s MergeDown: %s' % (style_name, merge_across, merge_down))
        
        return data
   
    def readData(self, ods_element=None, value=None, value_type=None):
        """
        Прочитать из ODS файла данные.

        :param ods_element: ODS элемент соответствующий данным ячейки.
        :param value: Строковое значение ячейки.
        :param value_type: Строковое представление типа значения ячейки.
        """
        data = {'name': 'Data', 'children': []}
        if value and value != 'None':
            data['value'] = value
        else:
            txt = u''.join([str(child) for child in ods_element.childNodes])
            value = txt
            data['value'] = value

        if value_type:
            data['Type'] = str(value_type).title()
        
        # log.debug('DATA: %s' % value_type)
        return data


def test_save(xml_filename):
    """
    Функция тестирования.
    """
    from . import v_excel
    excel = v_excel.iqVExcel()
    excel.load(xml_filename)
    data = excel.getData()
    
    ods = icODS()
    ods.save('./testfiles/test.ods', data)


def test_load(ods_filename):
    """
    Функция тестирования.
    """
    ods = icODS()
    ods.load(ods_filename)


def test_complex(src_ods_filename, dst_ods_filename):
    """
    Функция тестирования чтения/записи ODS файла.
    """
    ods = icODS()
    data = ods.load(src_ods_filename)
    
    from . import v_excel
    excel = v_excel.iqVExcel()
    excel._data = data
    excel.saveAs(dst_ods_filename)


def test_1(src_ods_filename, dst_ods_filename):
    """
    Функция тестирования чтения/записи ODS файла.
    """
    ods = icODS()
    data = ods.load(src_ods_filename)
    
    if data:
        ods.save(dst_ods_filename, data)


def test_2(src_ods_filename, dst_xml_filename, dst_ods_filename):
    """
    Функция тестирования чтения/записи ODS файла.
    """
    ods = icODS()
    data = ods.load(src_ods_filename)

    if data:
        import icexcel
        excel = icexcel.icVExcel()
        excel._data = data
        cell = excel.getWorkbook().getWorksheetIdx().getTable().getCell(40, 61)
        # log.debug('Cell: %s : %s' % (new_cell.getAddress(), new_cell.getRegion()))
        cell.setValue('123456')

        excel.saveAs(dst_xml_filename)
        ods.save(dst_ods_filename, data)


if __name__ == '__main__':
    test_complex('./testfiles/test.ods', './testfiles/result.ods')
