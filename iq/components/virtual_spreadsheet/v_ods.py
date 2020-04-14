#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re
import uuid

import odf.opendocument
import odf.style
import odf.number
import odf.text
import odf.table

from ...util import log_func

__version__ = (0, 0, 0, 1)

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

# Default page margins
DEFAULT_XML_MARGIN_TOP = 0.787401575
DEFAULT_XML_MARGIN_BOTTOM = 0.787401575
DEFAULT_XML_MARGIN_LEFT = 0.787401575
DEFAULT_XML_MARGIN_RIGHT = 0.787401575


class iqODS(object):
    """
    Class for converting a VirtualExcel view to an ODS file.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._styles_ = {}
        self.ods_document = None

        # Internal data in xmlss representation
        self.xmlss_data = None
        
        # Dictionary number styles
        self._number_styles_ = {}

        # Style name generation index
        self._style_name_idx = 0
        
    def save(self, filename, data_dict=None):
        """
        Save to ODS file.

        :param filename: ODS filename.
        :param data_dict: Data dictionary.
        :return: True/False.
        """
        if not data_dict:
            log_func.error(u'ODS. Not save data defined')

        self.ods_document = None
        self._styles_ = {}
        
        workbooks = data_dict.get('__children__', None)
        if not workbooks:
            workbook = dict()
        else:
            workbook = workbooks[0]

        # log_func.debug(u'ODS.Save workbook - %s' % bool(workbook))
        self.setWorkbook(workbook)
        
        if self.ods_document:
            # if isinstance(filename, text):
            #    filename = unicode(filename, DEFAULT_ENCODE)

            # Add extension automatically to file name (True - yes)
            #                                    V
            self.ods_document.save(filename, addsuffix=False)
            self.ods_document = None
            
        return True
    
    def getChildrenByName(self, data_dict, name):
        """
        Get children by name.

        :param data_dict: Data dictionary.
        :param name: Child item name.
        """
        return [item for item in data_dict.get('__children__', []) if item.get('name') == name]
        
    def setWorkbook(self, data_dict):
        """
        Set workbook.

        :param data_dict: Data dictionary.
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
        Set styles.

        :param data_dict: Data dictionary.
        """
        styles = data_dict.get('__children__', [])
        for style in styles:
            ods_style = self.setStyle(style)
            self.ods_document.automaticstyles.addElement(ods_style)

    def setFont(self, data_dict):
        """
        Set style font.

        :param data_dict: Data dictionary.
        """
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
        Generating a style name for a numeric representation format.
        """
        # from services.ic_std.utils import uuid
        # return uuid.get_uuid()
        self._style_name_idx += 1
        return 'text%d' % self._style_name_idx

    def setNumberFormat(self, data_dict):
        """
        Fill in the format of the numeric representation.

        :param data_dict: Data dictionary.
        """
        number_format = {}
        format = data_dict.get('Format', '0')

        # Do not analyze sign %
        format = format.replace('%', '')
        decimalplaces = len(format[format.find(',')+1:]) if format.find(',') >= 0 else 0
        minintegerdigits = len([i for i in list(format[:format.find(',')]) if i == '0']) if format.find(',') >= 0 else len([i for i in list(format) if i == '0'])
        grouping = 'true' if format.find(' ') >= 0 else 'false'
                    
        number_format['decimalplaces'] = str(decimalplaces)
        number_format['minintegerdigits'] = str(minintegerdigits)
        number_format['grouping'] = str(grouping)
        
        return number_format

    _LINESTYLE_SPREADSHEETML2ODS = {None: 'solid',
                                    'Continuous': 'solid',
                                    'Double': 'double',
                                    'Dot': 'dotted',
                                    'Dash': 'dashed',
                                    'DashDot': 'dotted',
                                    'DashDotDot': 'dashed',
                                    'Solid': 'solid'}
    _LINESTYLE_ODS2SPREADSHEETML = {None: 'Continuous',
                                    'solid': 'Continuous',
                                    'double': 'Double',
                                    'dotted': 'Dot',
                                    'dashed': 'Dash'}

    def setBorders(self, data_dict):
        """
        Set borders.

        :param data_dict: Data dictionary.
        """
        borders = {}
        for border in data_dict['__children__']:
            if border:
                border_weight = border.get('Weight', '1')
                color = border.get('Color', '#000000')
                line_style = self._LINESTYLE_SPREADSHEETML2ODS.get(border.get('LineStyle', 'solid'), 'solid')
                if border['Position'] == 'Left':
                    borders['borderleft'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Right':
                    borders['borderright'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Top':
                    borders['bordertop'] = '%spt %s %s' % (border_weight, line_style, color)
                elif border['Position'] == 'Bottom':
                    borders['borderbottom'] = '%spt %s %s' % (border_weight, line_style, color)
                
        return borders
        
    _ALIGNHORIZSTYLE_SPREADSHEETML2ODS = {'Left': 'start',
                                          'Right': 'end',
                                          'Center': 'center',
                                          'Justify': 'justify',
                                          }
    _ALIGNVERTSTYLE_SPREADSHEETML2ODS = {'Top': 'top',
                                         'Bottom': 'bottom',
                                         'Center': 'middle',
                                         'Justify': 'justify',
                                         }

    def setAlignmentParagraph(self, data_dict):
        """
        Fill text alignment style.

        :param data_dict: Data dictionary.
        """
        align = {}
        horiz = data_dict.get('Horizontal', None)
        vert = data_dict.get('Vertical', None)

        if horiz:
            align['textalign'] = self._ALIGNHORIZSTYLE_SPREADSHEETML2ODS.get(horiz, 'start')
            
        if vert:
            align['verticalalign'] = self._ALIGNVERTSTYLE_SPREADSHEETML2ODS.get(vert, 'top')

        return align

    def setAlignmentCell(self, data_dict):
        """
        Fill text alignment style.

        :param data_dict: Data dictionary.
        """
        align = {}
        wrap_txt = data_dict.get('WrapText', 0)
        shrink_to_fit = data_dict.get('ShrinkToFit', 0)
        vert = data_dict.get('Vertical', None)
        
        if vert:
            align['verticalalign'] = self._ALIGNVERTSTYLE_SPREADSHEETML2ODS.get(vert, 'top')
        
        if wrap_txt:
            align['wrapoption'] = 'wrap'
            
        if shrink_to_fit:
            align['shrinktofit'] = 'true'
        
        return align

    def setInteriorCell(self, data_dict):
        """
        Fill the cell style interior.

        :param data_dict: Data dictionary.
        """
        interior = {}
        color = data_dict.get('Color', None)

        if color:
            interior['backgroundcolor'] = color

        return interior

    def setStyle(self, data_dict):
        """
        Set style.

        :param data_dict: Data dictionary.
        """
        properties_args = {}
        number_format = self.getChildrenByName(data_dict, 'NumberFormat')
        if number_format:
            # Filling in a numeric representation format
            number_properties = self.setNumberFormat(number_format[0])
            number_style_name = self._genNumberStyleName()
            properties_args['datastylename'] = number_style_name
            
            num_format = number_format[0].get('Format', '0')
            if '%' in num_format:
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
        # log_func.warning('Set font <%s>' % fonts)
        if fonts:
            # Set font
            properties_args = self.setFont(fonts[0])

        if properties_args:
            ods_properties = odf.style.TextProperties(**properties_args)
            ods_style.addElement(ods_properties)
        
        properties_args = {}
        borders = self.getChildrenByName(data_dict, 'Borders')
        if borders:
            # Set borders
            args = self.setBorders(borders[0])
            properties_args.update(args)

        alignments = self.getChildrenByName(data_dict, 'Alignment')
        if alignments:
            # Set alignment
            args = self.setAlignmentCell(alignments[0])
            properties_args.update(args)

        interiors = self.getChildrenByName(data_dict, 'Interior')
        if interiors:
            # Set interior
            args = self.setInteriorCell(interiors[0])
            properties_args.update(args)

        if properties_args:
            ods_properties = odf.style.TableCellProperties(**properties_args)
            ods_style.addElement(ods_properties)            
            
        properties_args = {}
        if alignments:
            # Set alignment
            args = self.setAlignmentParagraph(alignments[0])
            properties_args.update(args)

        if properties_args:
            ods_properties = odf.style.ParagraphProperties(**properties_args)
            ods_style.addElement(ods_properties)            

        # Register style in cache by name
        self._styles_[style_id] = ods_style
        return ods_style

    def setWorksheet(self, data_dict):
        """
        Set worksheet.

        :param data_dict: Data dictionary.
        """
        sheet_name = data_dict.get('Name', 'Лист')
        if not isinstance(sheet_name, str):
            sheet_name = str(sheet_name)    # DEFAULT_ENCODE)
        ods_table = odf.table.Table(name=sheet_name)
        tables = self.getChildrenByName(data_dict, 'Table')
        if tables:
            self.setTable(tables[0], ods_table)
            
        # Set worksheet options
        worksheet_options = self.getChildrenByName(data_dict, 'WorksheetOptions')
        if worksheet_options:
            self.setWorksheetOptions(worksheet_options[0])

        # Set page breaks
        page_breaks = self.getChildrenByName(data_dict, 'PageBreaks')
        if page_breaks:
            self.setPageBreaks(page_breaks[0], ods_table)
        return ods_table

    def _setRowBreak(self, row, ods_table):
        """
        Set line break.

        :param row: Row number.
        :param ods_table: ODS table object.
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
        Set page breaks.

        :param data_dict: Data dictionary.
        :param ods_table: ODS table object.
        """
        row_breaks = data_dict['__children__'][0]['__children__']
        for row_break in row_breaks:
            i_row = row_break['__children__'][0]['value']
            self._setRowBreak(i_row, ods_table)

    def setWorksheetOptions(self, data_dict):
        """
        Set worksheet options.

        :param data_dict: Data dictionary.
        """
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
                ods_properties['margintop'] = self._dimensionInch2Cm(margin_top, True)
            if margin_bottom:
                ods_properties['marginbottom'] = self._dimensionInch2Cm(margin_bottom, True)
            if margin_left:
                ods_properties['marginleft'] = self._dimensionInch2Cm(margin_left, True)
            if margin_right:
                ods_properties['marginright'] = self._dimensionInch2Cm(margin_right, True)
        else:
            log_func.warning(u'Параметры страницы не определены')
        if print_setup:
            paper_size_idx = self.getChildrenByName(print_setup[0], 'PaperSizeIndex')
            if paper_size_idx:
                width, height = self._getPageSizeByExcelIndex(paper_size_idx[0]['value'])
                if orientation == LANDSCAPE_ORIENTATION:
                    variable = height
                    height = width
                    width = variable
                # Convert to string type
                ods_properties['pagewidth'] = '%scm' % str(width)
                ods_properties['pageheight'] = '%scm' % str(height)
        else:
            log_func.error(u'Worksheet options not defined')

        if fit_to_page:
            ods_properties['scaletopages'] = '1'

        ods_pagelayout = odf.style.PageLayout(name='MyPageLayout')
        ods_pagelayoutproperties = odf.style.PageLayoutProperties(**ods_properties)
        ods_pagelayout.addElement(ods_pagelayoutproperties)
        if self.ods_document:
            self.ods_document.automaticstyles.addElement(ods_pagelayout)
                
            masterpage = odf.style.MasterPage(name=DEFAULT_STYLE_ID, pagelayoutname=ods_pagelayout)
            self.ods_document.masterstyles.addElement(masterpage)
        else:
            log_func.error(u'ODS document not defined')
        return ods_pagelayout

    def _getPageSizeByExcelIndex(self, paper_size_idx):
        """
        Get sheet size by its index in Excel.

        :param paper_size_idx: Index 9-A4 8-A3.
        :return: Tuple (Width in cm, Height in cm).
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
        Set table.

        :param data_dict: Data dictionary.
        :param ods_table: ODS table object.
        """
        # Columns
        i = 1
        columns = self.getChildrenByName(data_dict, 'Column')
        for column in columns:
            # Column index accounting
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
        
        # Rows
        i = 1
        rows = self.getChildrenByName(data_dict, 'Row')
        for row in rows:
            # Row index accounting
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
        Generating a column style name.
        """
        return str(uuid.uuid4())

    def _genRowStyleName(self):
        """
        Generating a row style name.
        """
        return str(uuid.uuid4())

    def setColumn(self, data_dict):
        """
        Set column.

        :param data_dict: Data dictionary.
        """
        kwargs = {}
        
        width = data_dict.get('Width', None)

        if width:
            width = self._dimensionXML2ODS(width)
            # Create automatic styles for column widths
            ods_col_style = odf.style.Style(name=self._genColumnStyleName(), family='table-column')
            ods_col_properties = odf.style.TableColumnProperties(columnwidth=width, breakbefore='auto')
            ods_col_style.addElement(ods_col_properties)
            self.ods_document.automaticstyles.addElement(ods_col_style)
            
            kwargs['stylename'] = ods_col_style
        else:
            # Column width not defined
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
        Set row.

        :param data_dict: Data dictionary.
        """
        kwargs = dict()
        height = data_dict.get('Height', None)

        style_name = u''
        if height:
            height = self._dimensionXML2ODS(height)
            # Create automatic styles for line heights
            style_name = self._genRowStyleName()
            ods_row_style = odf.style.Style(name=style_name, family='table-row')
            ods_row_properties = odf.style.TableRowProperties(rowheight=height, breakbefore='auto')
            ods_row_style.addElement(ods_row_properties)
            self.ods_document.automaticstyles.addElement(ods_row_style)
            
            kwargs['stylename'] = ods_row_style
        else:
            # Line height not defined
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

        # Register style
        if ods_row_style:
            self._styles_[style_name] = ods_row_style

        ods_row = odf.table.TableRow(**kwargs)
        
        # Cells
        i = 1
        cells = self.getChildrenByName(data_dict, 'Cell')
        for i_cell, cell in enumerate(cells):
            idx = int(cell.get('Index', i))
            if idx > i:
                kwargs = dict()
                kwargs['numbercolumnsrepeated'] = (idx-i)

                style_id = self._findPrevStyle(cells[:i_cell])
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

            # Combined cell accounting
            merge = int(cell.get('MergeAcross', 0))
            if merge > 0:
                kwargs = dict()
                kwargs['numbercolumnsrepeated'] = merge

                style_id = self._findPrevStyle(cells[:i_cell])
                if style_id:
                    kwargs['stylename'] = self._styles_.get(style_id, None)
                
                ods_cell = odf.table.CoveredTableCell(**kwargs)
                ods_row.addElement(ods_cell)
                i += merge
            
        return ods_row

    def _findPrevStyle(self, cells):
        """
        Search for the style defined in the previous cell.

        :param cells: List of previous cells.
        :return: The identifier of the current style or None if the style is not defined.
        """
        for cell in reversed(cells):
            if 'StyleID' in cell:
                return cell.get('StyleID', None)
        return None
        
    def getCellValue(self, data_dict):
        """
        Get cell value.

        :param data_dict: Data dictionary.
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
        Get cell type.

        :param data_dict: Data dictionary.
        """
        dates = self.getChildrenByName(data_dict, 'Data')
        type = 'string'
        if dates:
            type = dates[0].get('Type', 'string').lower()
        
        if type == 'number':
            type = 'float'
        elif type == 'percentage':
            # It is necessary to check the compliance of the data with the percentage type
            str_value = dates[0].get('value', 'None')
            try:
                value = float(str_value)
            except:
                log_func.warning(u'Value <%s> not [percentage] type' % str_value)
                type = 'string'
        return type            
    
    # Excel column names in A1 format
    COLS_A1 = None

    def _getColsA1(self):
        """
        Excel column names in A1 format.
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
        Convert an address from the format R1C1 to A1.
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
        Convert an address from A1 format to R1C1.
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
        Transfer formulas from R1C1 format to A1 format.

        :param formula: The formula in a string.
        :return: String of translated formula.
        """
        parse_all = re.findall(self.R1C1_FORMAT, formula)
        for replace_addr in parse_all:
            a1 = self._getA1(replace_addr)
            if self._isSheetAddress(replace_addr, formula):
                a1 = '.'+a1
            formula = formula.replace(replace_addr, a1)
        return formula

    def _isSheetAddress(self, address, formula):
        """
        Addressing a cell indicating a sheet? For example, Sheet1.A1

        :param address: Cell address.
        :param formula: The formula in a string.
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
        Translation of a formula from A1 format to R1C1 format.

        :param formula: The formula as a string.
        :return: String of translated formula.
        """
        parse_all = re.findall(self.A1_FORMAT, formula)
        for replace_addr in parse_all:
            r1c1 = self._getR1C1(replace_addr)
            formula = formula.replace(replace_addr, r1c1)
        return formula
        
    def _translateR1C1Formula(self, formula):
        """
        Transfer formulas from R1C1 format to ODS file format.

        :param formula: The formula as a string.
        :return: String of translated formula.
        """
        return self._R1C1Fmt2A1Fmt(formula)

    def _translateA1Formula(self, formula):
        """
        Translation of a formula from ODS (A1) format to R1C1 format.

        :param formula: The formula as a string.
        :return: String of translated formula.
        """
        return self._A1Fmt2R1C1Fmt(formula)
        
    def setCell(self, data_dict):
        """
        Set cell.

        :param data_dict: Data dictionary.
        """
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
        ods_cell = odf.table.TableCell(**properties)
            
        dates = self.getChildrenByName(data_dict, 'Data')
        values = self.getDataValues(data_dict)
        for data in dates:
            for val in values:
                ods_data = self.setData(data, style_id, val)
                if ods_data:
                    ods_cell.addElement(ods_data)
            
        return ods_cell
        
    def getDataValues(self, data_dict):
        """
        Get the value of a row-wise cell.

        :param data_dict: Data dictionary.
        """
        dates = self.getChildrenByName(data_dict, 'Data')
        value = ''
        if dates:
            value = str(dates[0].get('value', ''))  # DEFAULT_ENCODE)
        return value.split(SPREADSHEETML_CR)
    
    def setData(self, data_dict, style_id=None, value=None):
        """
        Set cell data.

        :param data_dict: Data dictionary.
        :param style_id: Style id.
        :param value: Value.
        """
        ods_style = None
        if style_id:
            ods_style = self._styles_.get(style_id, None)

        ods_data = None
        if value:
            # Text
            if style_id and style_id != DEFAULT_STYLE_ID:
                ods_data = odf.text.P()
                style_span = odf.text.Span(stylename=ods_style, text=value)
                ods_data.addElement(style_span)
            else:
                ods_data = odf.text.P(text=value)
        return ods_data
        
    def load(self, filename):
        """
        Load from ODS file.

        :param filename: ODS filename.
        :return: Data dictionary or None if error.
        """
        if not os.path.exists(filename):
            # If the file does not exist then return None
            log_func.error(u'ODS. File <%s> not found' % filename)
            return None
        else:
            try:
                return self._loadODS(filename)
            except:
                log_func.fatal(u'Error file open <%s>' % filename)
                raise                
        
    def _loadODS(self, filename):
        """
        Load from ODS file.

        :param filename: ODS filename.
        :return: Data dictionary or None if error.
        """
        self.ods_document = odf.opendocument.load(filename)
        
        self.xmlss_data = {'name': 'Calc', '__children__': []}
        ods_workbooks = self.ods_document.getElementsByType(odf.opendocument.Spreadsheet)
        if ods_workbooks:
            workbook_data = self.readWorkbook(ods_workbooks[0])
            self.xmlss_data['__children__'].append(workbook_data)
        return self.xmlss_data
    
    def readWorkbook(self, ods_element=None):
        """
        Read workbook data from ODS file.

        :param ods_element: ODS element corresponding to an Excel workbook.
        """
        data = {'name': 'Workbook', '__children__': []}
        
        styles_data = self.readStyles()
        data['__children__'].append(styles_data)
        
        ods_tables = ods_element.getElementsByType(odf.table.Table)
        if ods_tables:
            for ods_table in ods_tables:
                worksheet_data = self.readWorksheet(ods_table)
                data['__children__'].append(worksheet_data)
        
        return data

    def readNumberStyles(self, *ods_styles):
        """
        Read data on number format styles.

        :param ods_styles: Style list.
        """
        if not ods_styles:
            log_func.error(u'ODS styles not defined')
            return {}
            
        result = {}
        for ods_styles in ods_styles:
            num_styles = ods_styles.getElementsByType(odf.number.NumberStyle)
            percentage_styles = ods_styles.getElementsByType(odf.number.PercentageStyle)
            styles = num_styles + percentage_styles
            if styles:
                for style in styles:
                    result[style.getAttribute('name')] = style
    
        return result
        
    def readStyles(self, ods_element=None):
        """
        Read styles data from ODS file.

        :param ods_element: An ODS element that matches the styles of an Excel workbook.
        """
        data = {'name': 'Styles', '__children__': []}
        ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style) + \
            self.ods_document.styles.getElementsByType(odf.style.Style) + \
            self.ods_document.masterstyles.getElementsByType(odf.style.Style)

        # Number format styles
        self._number_styles_ = self.readNumberStyles(self.ods_document.automaticstyles,
                                                     self.ods_document.styles,
                                                     self.ods_document.masterstyles)
        
        for ods_style in ods_styles:
            style = self.readStyle(ods_style)
            data['__children__'].append(style)
                        
        return data

    def readStyle(self, ods_element=None):
        """
        Read style data ODS from file.

        :param ods_element: ODS element corresponding to the style of Excel.
        """
        data = {'name': 'Style', '__children__': []}
        id = ods_element.getAttribute('name')
        data['ID'] = id
        
        data_style_name = ods_element.getAttribute('datastylename')
        if data_style_name:
            number_style = self._number_styles_.get(data_style_name, None)
            if number_style:
                number_format_data = self.readNumberFormat(number_style)
                if number_format_data:
                    data['__children__'].append(number_format_data)

        # Read font
        txt_properties = ods_element.getElementsByType(odf.style.TextProperties)
        if txt_properties:
            font_data = self.readFont(txt_properties[0])
            if font_data:
                data['__children__'].append(font_data)

        # Read borders
        tab_cell_properties = ods_element.getElementsByType(odf.style.TableCellProperties)
        if tab_cell_properties:
            borders_data = self.readBorders(tab_cell_properties[0])
            if borders_data:
                data['__children__'].append(borders_data)

        # Read interior
        if tab_cell_properties:
            interior_data = self.readInterior(tab_cell_properties[0])
            if interior_data:
                data['__children__'].append(interior_data)

        # Read align
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
            data['__children__'].append(align_data)
        
        return data
    
    def readNumberFormat(self, ods_element=None):
        """
        Read number format data from ODS file.

        :param ods_element: ODS element corresponding to the style of numerical representation.
        """
        if ods_element is None:
            log_func.error('Not define ods_element <%s>' % ods_element)
            return None
        
        numbers = ods_element.getElementsByType(odf.number.Number)
        if not numbers:
            log_func.error('Not define numbers in ods_element <%s>' % ods_element)
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
            grp_format = list(grouping_format + minintegerdigits_format)
            format_result = []
            count = 3
            for i in range(len(grp_format)-1, -1, -1):
                format_result = [grp_format[i]] + format_result
                count = count - 1
                if not count:
                    format_result = [' '] + format_result
                    count = 3
            number_format = ''.join(format_result) + decimalplaces_format + percentage_format
        else:
            number_format = minintegerdigits_format + decimalplaces_format + percentage_format
            
        log_func.debug('NUMBER FORMAT %s : %s' % (decimalplaces_str, number_format))
        data = {'name': 'NumberFormat', '__children__': [], 'Format': number_format}
        return data
        
    def readFont(self, ods_element=None):
        """
        Read font data from ODS file.

        :param ods_element: ODS element corresponding to style text properties.
        """
        name = ods_element.getAttribute('fontname')
        name = name if name else ods_element.getAttribute('fontfamily')
        size = ods_element.getAttribute('fontsize')
        bold = ods_element.getAttribute('fontweight')
        italic = ods_element.getAttribute('fontstyle')
        # Through
        through_style = ods_element.getAttribute('textlinethroughstyle')
        # through_type = ods_element.getAttribute('textlinethroughtype')
        # Underline
        underline_style = ods_element.getAttribute('textunderlinestyle')
        # underline_width = ods_element.getAttribute('textunderlinewidth')

        data = {'name': 'Font', '__children__': []}
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

        # log_func.debug('Read FONT: %s : %s : %s : %s : %s : %s' % (name, size, bold, italic, through_style, underline_style))
        
        return data
        
    def readInterior(self, ods_element=None):
        """
        Read interior data from ODS file.

        :param ods_element: An ODS element corresponding to the properties of a style sheet cell.
        """
        data = {'name': 'Interior', '__children__': []}

        color = ods_element.getAttribute('backgroundcolor')

        # log_func.debug('Read INTERIOR: color <%s>' % color)

        if color and (color not in ('None', 'none', 'NONE')):
            data['Color'] = color.strip()

        return data

    def readBorders(self, ods_element=None):
        """
        Read borders data from ODS file.

        :param ods_element: An ODS element corresponding to the properties of a style sheet cell.
        """
        data = {'name': 'Borders', '__children__': []}
        
        all_border = ods_element.getAttribute('border')
        left = ods_element.getAttribute('borderleft')
        right = ods_element.getAttribute('borderright')
        top = ods_element.getAttribute('bordertop')
        bottom = ods_element.getAttribute('borderbottom')
        
        # log_func.debug('BORDERS: border %s Left: %s Right: %s Top: %s Bottom: %s' % (all_border, left, right, top, bottom))
        
        if all_border and (all_border not in ('None', 'none', 'NONE')):
            border = self.parseBorder(all_border, 'Left')
            if border:
                data['__children__'].append(border)
            border = self.parseBorder(all_border, 'Right')
            if border:
                data['__children__'].append(border)
            border = self.parseBorder(all_border, 'Top')
            if border:
                data['__children__'].append(border)
            border = self.parseBorder(all_border, 'Bottom')
            if border:
                data['__children__'].append(border)
                
        if left and (left not in ('None', 'none', 'NONE')):
            border = self.parseBorder(left, 'Left')
            if border:
                data['__children__'].append(border)
            
        if right and (right not in ('None', 'none', 'NONE')):
            border = self.parseBorder(right, 'Right')
            if border:
                data['__children__'].append(border)
        
        if top and (top not in ('None', 'none', 'NONE')):
            border = self.parseBorder(top, 'Top')
            if border:
                data['__children__'].append(border)
            
        if bottom and (bottom not in ('None', 'none', 'NONE')):
            border = self.parseBorder(bottom, 'Bottom')
            if border:
                data['__children__'].append(border)
            
        return data
        
    def readAlignmentParagraph(self, ods_element=None):
        """
        Read alignment data from ODS file.

        :param ods_element: ODS element corresponding to the properties of the paragraph.
        """
        data = {'name': 'Alignment', '__children__': []}

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
            
        # log_func.debug('ALIGNMENT PARAGRAPH: %s:%s' % (text_align, vert_align))
        
        return data
        
    def readAlignmentCell(self, ods_element=None):
        """
        Read alignment cell text data from ODS file.

        :param ods_element: ODS element corresponding to the properties of the cell.
        """
        data = {'name': 'Alignment', '__children__': []}

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
            
        # log_func.debug('ALIGNMENT CELL: %s' % vert_align)
        
        return data
        
    def parseBorder(self, data_string, position=None):
        """
        Parse border.

        :param data_string: Data text as <1pt solid #000000>.
        :param position: Border position.
        :return: Border data dictionary.
        """
        border = None
        if data_string:
            border_data = self.parseBorderData(data_string)
            if border_data:
                border = {'name': 'Border', 'Position': position,
                          'Weight': border_data.get('weight', '1'),
                          'LineStyle': self._LINESTYLE_ODS2SPREADSHEETML.get(border_data.get('line', None), 'Continuous'),
                          'Color': border_data.get('color', '000000')}
            # log_func.debug('PARSE BORDER: %s : %s' % (data_string, border))
            
        return border
            
    def parseBorderData(self, data_string):
        """
        Parse border data.

        :param data_string: Data text as <1pt solid #000000>.
        :return: Dictionary {'weight':1,'line':'solid','color':'#000000'}.
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
            # The width can be set in cm, so you need to convert to pt
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
        Read worksheet data from ODS file.

        :param ods_element: ODS element corresponding to the sheet.
        """
        data = {'name': 'Worksheet', '__children__': []}
        name = ods_element.getAttribute('name')

        # log_func.debug('WORKSHEET: <%s : %s>' % (type(name), name))
        
        data['Name'] = name
        
        table = {'name': 'Table', '__children__': []}
        
        # Columns
        ods_columns = ods_element.getElementsByType(odf.table.TableColumn)
        for ods_column in ods_columns:
            column_data = self.readColumn(ods_column)
            table['__children__'].append(column_data)
            
        # Rows
        ods_rows = ods_element.getElementsByType(odf.table.TableRow)
        for i, ods_row in enumerate(ods_rows):
            row_data = self.readRow(ods_row, table, data, i)
            table['__children__'].append(row_data)
      
        data['__children__'].append(table)
        
        # Worksheet options
        ods_pagelayouts = self.ods_document.automaticstyles.getElementsByType(odf.style.PageLayout)
        worksheet_options = self.readWorksheetOptions(ods_pagelayouts)
        if worksheet_options:
            data['__children__'].append(worksheet_options)
        
        return data
    
    def readWorksheetOptions(self, ods_page_layouts):
        """
        Read worksheet options from ODS file.

        :param ods_page_layouts: List of found page parameters.
        """
        if not ods_page_layouts:
            log_func.error(u'Not define page layout')
            return None

        # log_func.debug(u'Set default worksheet options')
        options = {'name': 'WorksheetOptions',
                   '__children__': [{'name': 'PageSetup',
                                 '__children__': [{'name': 'Layout',
                                               'Orientation': PORTRAIT_ORIENTATION},
                                              {'name': 'PageMargins',
                                               'Top': str(DEFAULT_XML_MARGIN_TOP),
                                               'Bottom': str(DEFAULT_XML_MARGIN_BOTTOM),
                                               'Left': str(DEFAULT_XML_MARGIN_LEFT),
                                               'Right': str(DEFAULT_XML_MARGIN_RIGHT)},
                                              ]
                                 },
                                {'name': 'Print',
                                 '__children__': [{'name': 'PaperSizeIndex',
                                               'value': '9'}
                                              ]
                                 }
                                ]
                   }
        
        for pagelayout in ods_page_layouts:
            properties = pagelayout.getElementsByType(odf.style.PageLayoutProperties)
            # log_func.debug(u'Properties: %s' % text(properties))
            if properties:
                properties = properties[0]
                orientation = properties.getAttribute('printorientation')
                margin = properties.getAttribute('margin')
                # log_func.debug(u'Margin: %s' % margin)
                margin_top = properties.getAttribute('margintop')
                # log_func.debug(u'Margin Top: %s' % margin_top)
                margin_bottom = properties.getAttribute('marginbottom')
                # log_func.debug(u'Margin Bottom: %s' % margin_bottom)
                margin_left = properties.getAttribute('marginleft')
                # log_func.debug(u'Margin Left: %s' % margin_left)
                margin_right = properties.getAttribute('marginright')
                # log_func.debug(u'Margin Right: %s' % margin_right)
                page_width = properties.getAttribute('pagewidth')
                # log_func.debug(u'Page Width: %s' % page_width)
                page_height = properties.getAttribute('pageheight')
                # log_func.debug(u'Page Height: %s' % page_height)
                fit_to_page = properties.getAttribute('scaletopages')
                # log_func.debug(u'Fit To Pages: %s' % fit_to_page)
                scale_to = properties.getAttribute('scaleto')
                # log_func.debug(u'Scale To: %s' % scale_to)

                if orientation:
                    options['__children__'][0]['__children__'][0]['Orientation'] = orientation.title()
                if margin:
                    options['__children__'][0]['__children__'][1]['Top'] = self._dimensionCm2Inch(margin)
                    options['__children__'][0]['__children__'][1]['Bottom'] = self._dimensionCm2Inch(margin)
                    options['__children__'][0]['__children__'][1]['Left'] = self._dimensionCm2Inch(margin)
                    options['__children__'][0]['__children__'][1]['Right'] = self._dimensionCm2Inch(margin)
                if margin_top:
                    options['__children__'][0]['__children__'][1]['Top'] = self._dimensionCm2Inch(margin_top)
                if margin_bottom:
                    options['__children__'][0]['__children__'][1]['Bottom'] = self._dimensionCm2Inch(margin_bottom)
                if margin_left:
                    options['__children__'][0]['__children__'][1]['Left'] = self._dimensionCm2Inch(margin_left)
                if margin_right:
                    options['__children__'][0]['__children__'][1]['Right'] = self._dimensionCm2Inch(margin_right)
                if fit_to_page or (scale_to == (1, 1)):
                    options['__children__'].append({'name': 'FitToPage'})

                if page_width and page_height:
                    # Set page size
                    options['__children__'][1]['__children__'][0]['value'] = self._getExcelPaperSizeIndex(page_width, page_height)
                # Typically, the print options indicated at the beginning are
                # the default settings. Therefore, we skip all the others
                break
            else:
                # log_func.debug(u'Not define worksheet options')
                continue
        return options

    def _getExcelPaperSizeIndex(self, page_width, page_height):
        """
        Determine its index in the Excel list by the size of the sheet.
        """
        paper_format = self._getPaperSizeFormat(page_width, page_height)
        
        if paper_format is None:
            # Default A4
            return '9'
        elif paper_format == A4_PAPER_FORMAT:
            return '9'
        elif paper_format == A3_PAPER_FORMAT:
            return '8'
        return None
        
    def _getPaperSizeFormat(self, page_width, page_height):
        """
        Determine the size of the sheet format.

        :param page_width: Page width in cm.
        :param page_height: Page height in cm.
        :return: A4 or A3.
        """
        if isinstance(page_width, str):
            page_width_txt = page_width.replace('cm', '').replace('mm', '')
            page_width = float(page_width_txt)
        if isinstance(page_height, str):
            page_height_txt = page_height.replace('cm', '').replace('mm', '')
            page_height = float(page_height_txt)

        # If in cm
        if round(page_width, 1) == 21.0 and round(page_height, 1) == 29.7:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 29.7 and round(page_height, 1) == 21.0:
            return A4_PAPER_FORMAT
        elif round(page_width, 1) == 29.7 and round(page_height, 1) == 42.0:
            return A3_PAPER_FORMAT
        elif round(page_width, 1) == 42.0 and round(page_height, 1) == 29.7:
            return A3_PAPER_FORMAT
        # If in mm
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
        Read column data from ODS file.

        :param ods_element: ODS item corresponding column.
        """
        data = {'name': 'Column', '__children__': []}
        style_name = ods_element.getAttribute('stylename')
        default_cell_style_name = ods_element.getAttribute('defaultcellstylename')
        repeated = ods_element.getAttribute('numbercolumnsrepeated')
        hidden = ods_element.getAttribute('visibility')

        if style_name:
            # Column width
            column_width = None
            ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style)
            find_style = [ods_style for ods_style in ods_styles if ods_style.getAttribute('name') == style_name]
            if find_style:
                ods_style = find_style[0]
                ods_column_properties = ods_style.getElementsByType(odf.style.TableColumnProperties)
                if ods_column_properties:
                    ods_column_property = ods_column_properties[0]
                    column_width = self._dimensionODS2XML(ods_column_property.getAttribute('columnwidth'))
                    if column_width:
                        data['Width'] = column_width
            # log_func.debug('COLUMN: %s Width: %s Cell style: %s' % (style_name, column_width, default_cell_style_name))
        
        if default_cell_style_name and (default_cell_style_name not in ('Default', 'None', 'none', 'NONE')):
            data['StyleID'] = default_cell_style_name

        if repeated and repeated != 'None':
            repeated = str(int(repeated)-1)
            data['Span'] = repeated

        if hidden and hidden == 'collapse':
            data['Hidden'] = True

        return data
    
    def _dimensionODS2XML(self, dimension):
        """
        Translating dimensions from an ODS view to XML.

        :param dimension: Dimension as string.
        """
        if not dimension:
            return None
        elif (len(dimension) > 2) and (dimension[-2:] == 'cm'):
            # Is the size in centimeters?
            return str(float(dimension[:-2]) * 28)
        elif (len(dimension) > 2) and (dimension[-2:] == 'mm'):
            # Size in millimeters?
            return str(float(dimension[:-2]) * 2.8)
        else:
            # Size indicated in points
            return str(float(dimension) / DIMENSION_CORRECT)

    def _dimensionXML2ODS(self, dimension):
        """
        Translating dimensions from an XML view into ODS.

        :param dimension: String representation of the size in inches.
        """
        return str(float(dimension) * DIMENSION_CORRECT)

    def _dimensionInch2Cm(self, dimension, is_postfix=False):
        """
        Convert dimensions from representation in inches to centimeters.

        :param dimension: String representation of the size in inches.
        :param is_postfix: Add cm as a postfix in a string?
        """
        return str(float(dimension) * INCH2CM) + (' cm' if is_postfix else '')

    def _dimensionCm2Inch(self, dimension):
        """
        Convert dimensions from view in centimeters / mm to inches.

        :param dimension: String representation of the size in centimeters / mm.
        """
        if not dimension:
            return None
        elif (len(dimension) > 2) and (dimension[-2:] == 'cm'):
            # Is the size in centimeters?
            return str(float(dimension[:-2]) / INCH2CM)
        elif (len(dimension) > 2) and (dimension[-2:] == 'mm'):
            # Size in millimeters?
            return str(float(dimension[:-2]) / 10.0 / INCH2CM)
        else:
            # Size indicated in points
            return str(float(dimension) / DIMENSION_CORRECT)

    def _addPageBreak(self, worksheet, row):
        """
        Add page break.

        :param worksheet: Worksheet data dictionary.
        :param row: Row number.
        """
        find_page_breaks = [child for child in worksheet['__children__'] if child['name'] == 'PageBreaks']
        if find_page_breaks:
            data = find_page_breaks[0]
        else:
            data = {'name': 'PageBreaks', '__children__': [{'name': 'RowBreaks', '__children__': []}]}
            worksheet['__children__'].append(data)

        row_break = {'name': 'RowBreak', '__children__': [{'name': 'Row', 'value': row}]}
        data['__children__'][0]['__children__'].append(row_break)
        return data

    def readRow(self, ods_element=None, table=None, worksheet=None, row=-1):
        """
        Read row data from ODS file.

        :param ods_element: ODS element corresponding to the string.
        :param table: Table data dictionary.
        :param worksheet: Worksheet data dictionary.
        :param row: Row number.
        """
        data = {'name': 'Row', '__children__': []}
        style_name = ods_element.getAttribute('stylename')
        repeated = ods_element.getAttribute('numberrowsrepeated')
        hidden = ods_element.getAttribute('visibility')

        if style_name:
            # Row height
            row_height = None
            ods_styles = self.ods_document.automaticstyles.getElementsByType(odf.style.Style)
            find_style = [ods_style for ods_style in ods_styles if ods_style.getAttribute('name') == style_name]
            if find_style:
                ods_style = find_style[0]
                ods_row_properties = ods_style.getElementsByType(odf.style.TableRowProperties)
                if ods_row_properties:
                    ods_row_property = ods_row_properties[0]
                    row_height = self._dimensionODS2XML(ods_row_property.getAttribute('rowheight'))
                    if row_height:
                        data['Height'] = row_height
                    # Page breaks
                    page_break = ods_row_property.getAttribute('breakbefore')
                    if page_break and page_break == 'page' and worksheet:
                        self._addPageBreak(worksheet, row)
                    # log_func.debug('ROW: %s \tHeight: %s \tPageBreak: %s \tStyle: %s' % (style_name, row_height, page_break, style_name))
        
        if repeated and (repeated not in ('None', 'none', 'NONE')):
            # An additional condition is necessary to eliminate
            # an error situation when the row parameters are duplicated
            # on all subsequent lines (in LibreOffice this is done
            # to duplicate the style of cells line by line at
            # the end of the sheet)
            i_repeated = int(repeated)
            if i_repeated <= LIMIT_ROWS_REPEATED:
                repeated = i_repeated-1
                if table:
                    for i in range(repeated):
                        table['__children__'].append(self.readRow(ods_element))
                else:
                    data['Span'] = str(repeated)

        if hidden and hidden == 'collapse':
            data['Hidden'] = True

        # Cells
        ods_cells = ods_element.childNodes
        
        i = 1
        set_idx = False
        for ods_cell in ods_cells:
            if ods_cell.qname[-1] == 'covered-table-cell':
                repeated = ods_cell.getAttribute('numbercolumnsrepeated')
                if repeated and (repeated not in ('None', 'none', 'NONE')):
                    # Accounting for index and missing cells
                    i += int(repeated)  # +1
                    set_idx = True
                else:
                    i += 1
                    set_idx = True
            elif ods_cell.qname[-1] == 'table-cell':
                cell_data = self.readCell(ods_cell, i if set_idx else None)
                data['__children__'].append(cell_data)
                if set_idx:
                    set_idx = False

                repeated = ods_cell.getAttribute('numbercolumnsrepeated')
                if repeated and (repeated not in ('None', 'none', 'NONE')):
                    # Accounting for index and missing cells
                    i_repeated = int(repeated)
                    if i_repeated < LIMIT_COLUMNS_REPEATED:
                        for ii in range(i_repeated-1):
                            cell_data = self.readCell(ods_cell)
                            data['__children__'].append(cell_data)
                            i += 1
                        # Here you need to add 1 otherwise the tables / stamps can "float"
                        i += 1
                    else:
                        i += i_repeated     # +1
                        set_idx = True
                else:
                    i += 1
                        
        return data
    
    def hasODSAttribute(self, ods_element, attr_name):
        """
        Does an ODS element have an attribute with that name?

        :param ods_element: ODS element.
        :param attr_name: Attribute name.
        :return: True/False.
        """
        return attr_name in [attr[-1].replace('-', '') for attr in ods_element.attributes.keys()]
        
    def readCell(self, ods_element=None, index=None):
        """
        Read cell data from ODS file.

        :param ods_element: ODS element corresponding to the cell.
        :type index: C{int}
        :param index: Cell index, if necessary.
        """
        data = {'name': 'Cell', '__children__': []}
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
            cur_data = None
            for i, ods_txt in enumerate(ods_data):
                data_data = self.readData(ods_txt, value, valuetype)
                if not i:
                    cur_data = data_data
                else:
                    cur_data['value'] += SPREADSHEETML_CR+data_data['value']
            data['__children__'].append(cur_data)
        
        # log_func.debug('CELL Style: %s MergeAcross: %s MergeDown: %s' % (style_name, merge_across, merge_down))
        
        return data
   
    def readData(self, ods_element=None, value=None, value_type=None):
        """
        Reade data from ODS file.

        :param ods_element: ODS element corresponding to cell data.
        :param value: Value as string.
        :param value_type: Cell value type as string.
        """
        data = {'name': 'Data', '__children__': []}
        if value and value != 'None':
            data['value'] = value
        else:
            txt = u''.join([str(child) for child in ods_element.childNodes])
            value = txt
            data['value'] = value

        if value_type:
            data['Type'] = str(value_type).title()
        
        # log_func.debug('DATA: %s' % value_type)
        return data
