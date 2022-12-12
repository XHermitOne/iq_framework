#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report file module.
The report file is an XML format file Excel xmlss.
The documentation for this format is located:
http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dnexcl2k2/html/odc_xmlss.asp.
"""

import time
import copy
from xml.sax import saxutils
import os.path

from iq.util import log_func
from iq.util import str_func
from iq.util import file_func

from . import report_generator
from . import report_glob_data

__version__ = (0, 0, 3, 1)

SPC_XML_STYLE = {'style_id': '',  # Style ID
                 'align': {'align_txt': (0, 0), 'wrap_txt': False},  # Alignment
                 'font': None,  # Font
                 'border': (0, 0, 0, 0),  # Borders
                 'num_format': None,  # Cell num_format
                 'color': {},  # Colour
                 }


class iqReportFile(object):
    """
    Report file class.
    """
    def __init__(self):
        """
        Constructor.
        """
        pass
        
    def write(self, rep_filename, rec_data):
        """
        Save the completed report to a file.

        :param rep_filename: Report filename.
        :param rec_data: Report data.
        :return: Created xml filename or None if error.
        """
        pass


class iqXMLSpreadSheetReportFile(iqReportFile):
    """
    XML report file in Excel XMLSS format.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqReportFile.__init__(self)
        
    def write(self, rep_filename, rec_data):
        """
        Save the completed report to a file.

        :param rep_filename: Report filename.
        :param rec_data: Report data.
        :return: Created xml filename or None if error.
        """
        xml_file = None

        if not rep_filename:
            log_func.warning(u'Not define report file')
            return None

        try:
            rep_dirname = os.path.dirname(rep_filename)
            if not os.path.exists(rep_dirname):
                file_func.createDir(rep_dirname)

            xml_file = open(rep_filename, 'wt', encoding=report_glob_data.DEFAULT_REPORT_ENCODING)
            xml_gen = iqXMLSSGenerator(xml_file)
            xml_gen.startDocument()
            xml_gen.startBook()

            # Page setup
            # xml_gen.savePageSetup(rep_name,report)
        
            # Styles
            xml_gen.scanStyles(rec_data['sheet'])
            xml_gen.saveStyles()
        
            # Data
            xml_gen.startSheet(rec_data['name'], rec_data)
            xml_gen.saveColumns(rec_data['sheet'])
            for i_row in range(len(rec_data['sheet'])):
                xml_gen.startRow(rec_data['sheet'][i_row])
                # Reset cell index
                xml_gen.cell_idx = 1
                for i_col in range(len(rec_data['sheet'][i_row])):
                    cell = rec_data['sheet'][i_row][i_col]
                    xml_gen.saveCell(i_row+1, i_col+1, cell, rec_data['sheet'])
                xml_gen.endRow()
            
            xml_gen.endSheet(rec_data)
       
            xml_gen.endBook()
            xml_gen.endDocument()
            xml_file.close()
        
            return rep_filename
        except:
            if xml_file:
                xml_file.close()
            log_func.fatal(u'Error report write <%s>' % str_func.toUnicode(rep_filename))
        return None

    def writeBook(self, rep_filename, *rep_sheet_data):
        """
        Save the list of sheets of the completed report in a file.

        :param rep_filename: Report XML filename.
        :param rep_sheet_data: Report data sorted by sheets.
        :return: Report xml filename or None if error.
        """
        xml_file = None
        try:
            xml_file = open(rep_filename, 'wt', encoding=report_glob_data.DEFAULT_REPORT_ENCODING)
            xml_gen = iqXMLSSGenerator(xml_file)
            xml_gen.startDocument()
            xml_gen.startBook()
        
            for rep_sheet_data in rep_sheet_data:
                # Styles
                xml_gen.scanStyles(rep_sheet_data['sheet'])
            xml_gen.saveStyles()
        
            for rep_sheet_data in rep_sheet_data:
                #
                xml_gen.startSheet(rep_sheet_data['name'], rep_sheet_data)
                xml_gen.saveColumns(rep_sheet_data['sheet'])
                for i_row in range(len(rep_sheet_data['sheet'])):
                    xml_gen.startRow(rep_sheet_data['sheet'][i_row])

                    xml_gen.cell_idx = 1
                    for i_col in range(len(rep_sheet_data['sheet'][i_row])):
                        cell = rep_sheet_data['sheet'][i_row][i_col]
                        xml_gen.saveCell(i_row+1, i_col+1, cell, rep_sheet_data['sheet'])
                    xml_gen.endRow()
            
                xml_gen.endSheet(rep_sheet_data)
       
            xml_gen.endBook()
            xml_gen.endDocument()
            xml_file.close()
        
            return rep_filename
        except:
            if xml_file:
                xml_file.close()
            log_func.fatal(u'Error report write <%s>' % rep_filename)
        return None


class iqXMLSSGenerator(saxutils.XMLGenerator):
    """
    Report converter generator class in xml representation.
    """
    def __init__(self, out=None, encoding=report_glob_data.DEFAULT_REPORT_ENCODING):
        """
        Constructor.
        """
        saxutils.XMLGenerator.__init__(self, out, encoding)

        self._encoding = encoding
        
        # Indentation for tagging
        self.break_line = ''
        
        # Cell styles
        self._styles = []
        
        # Current cell index in row
        self.cell_idx = 0
        # Index setting flag in row
        self._idx_set = False

        # Create file start time
        self.time_start = 0

    def startElementLevel(self, name, attrs):
        """
        Start element.

        :param name: Element name.
        :param attrs: Element attributes (dictionary).
        """
        self._write(u'\n' + str(self.break_line))

        saxutils.XMLGenerator.startElement(self, name, attrs)
        self.break_line += ' '

    def endElementLevel(self, name):
        """
        End element.

        :param name: Element name.
        """
        self._write(u'\n' + str(self.break_line))

        saxutils.XMLGenerator.endElement(self, name)

        if self.break_line:
            self.break_line = self.break_line[:-1]

    def startElement(self, name, attrs):
        """
        Start element.

        :param name: Element name.
        :param attrs: Element attributes (dictionary).
        """
        self._write(u'\n' + str(self.break_line))

        saxutils.XMLGenerator.startElement(self, name, attrs)

    def endElement(self, name):
        """
        End element.

        :param name: Element name.
        """
        saxutils.XMLGenerator.endElement(self, name)

        if self.break_line:
            self.break_line = self.break_line[:-1]

    _REPORT_ORIENTATION2XML = {0: 'Portrait',
                               1: 'Landscape',
                               '0': 'Portrait',
                               '1': 'Landscape',
                               }

    def savePageSetup(self, report):
        """
        Write page parameters in the xml file.

        :param report: Report data.
        """
        self.startElementLevel('WorksheetOptions', {'xmlns': 'urn:schemas-microsoft-com:office:excel'})
        if 'page_setup' in report:
            # Page setup
            self.startElementLevel('PageSetup', {})

            # Page orientation
            if 'orientation' in report['page_setup']:
                self.startElementLevel('Layout',
                                       {'x:Orientation': self._REPORT_ORIENTATION2XML[report['page_setup']['orientation']],
                                        'x:StartPageNum': str(report['page_setup'].setdefault('start_num', 1))})
                self.endElementLevel('Layout')

            # Page margins
            if 'page_margins' in report['page_setup']:
                self.startElementLevel('PageMargins',
                                       {'x:Left': str(report['page_setup']['page_margins'][0]),
                                        'x:Right': str(report['page_setup']['page_margins'][1]),
                                        'x:Top': str(report['page_setup']['page_margins'][2]),
                                        'x:Bottom': str(report['page_setup']['page_margins'][3])})
                self.endElementLevel('PageMargins')
        
            # Upper
            if 'data' in report['upper']:
                data = str(report['upper']['data'])   # , 'CP1251').encode('UTF-8')
                self.startElementLevel('Header', 
                                       {'x:Margin': str(report['upper']['height']),
                                        'x:Data': data})
                self.endElementLevel('Header')
                
            # Under
            if 'data' in report['under']:
                data = str(report['under']['data'])  # , 'CP1251').encode('UTF-8')
                self.startElementLevel('Footer', 
                                       {'x:Margin': str(report['under']['height']),
                                        'x:Data': data})
                self.endElementLevel('Footer')
                
            self.endElementLevel('PageSetup')

            # Print options
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
        Start workbook.
        """
        self.time_start = time.time()

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
        End workbook.
        """
        self.endElementLevel('Workbook')

    def startSheet(self, rep_name, report):
        """
        Start worksheet.

        :param rep_name: Report name.
        :param report: Report data.
        """
        rep_name = str(rep_name)
        self.startElementLevel('Worksheet', {'ss:Name': rep_name})

        try:
            if report['upper']:
                refers_to = self._getUpperRangeStr(report['upper'])

                self.startElementLevel('Names', {})
                self.startElementLevel('NamedRange', {'ss:Name': 'Print_Titles',
                                       'ss:RefersTo': refers_to})
                self.endElementLevel('NamedRange')
                self.endElementLevel('Names')
        except:
            log_func.fatal('Names SAVE <%s>' % report['upper'])
            raise

        self.startElementLevel('Table', {})

    def _getUpperRangeStr(self, upper):
        """
        Present a range of header cells as a string.
        """
        return '=C%d:C%d,R%d:R%d' % (upper['col'] + 1, upper['col'] + upper['col_size'],
                                     upper['row'] + 1, upper['row'] + upper['row_size'])
        
    def endSheet(self, report):
        """
        End worksheet.

        :param report: Report data.
        """
        self.endElementLevel('Table')
        self.savePageSetup(report)
        self.endElementLevel('Worksheet')
    
    def scanStyles(self, sheet):
        """
        Worksheet styles scan.
        """
        for i_row in range(len(sheet)):
            for i_col in range(len(sheet[i_row])):
                cell = sheet[i_row][i_col]
                if cell is not None:
                    self.setStyle(cell)
        return self._styles
        
    def setStyle(self, cell):
        """
        Set cell style.

        :param cell: Cell attributes.
        :return: Style index in style list.
        """
        cell_style_idx = self.getStyle(cell)
        if cell_style_idx is None:
            # Create style
            new_idx = len(self._styles)
            cell_style = copy.deepcopy(SPC_XML_STYLE)
            cell_style['align'] = cell['align']
            cell_style['font'] = cell['font']
            cell_style['border'] = cell['border']
            cell_style['num_format'] = cell['num_format']
            cell_style['color'] = cell['color']
            cell_style['style_id'] = 'x'+str(new_idx)
            # Set style in cell
            cell['style_id'] = cell_style['style_id']
            self._styles.append(cell_style)
            return new_idx
        return cell_style_idx
      
    def getStyle(self, cell):
        """
        Define a cell style from existing ones.

        :param cell: Cell attributes.
        :return: Style index in style list.
        """
        find_style = [style for style in self._styles if self._equalStyles(style, cell)]

        if find_style:
            cell['style_id'] = find_style[0]['style_id']
            return self._styles.index(find_style[0])
        return None
        
    def _equalStyles(self, style1, style2):
        """
        The function of checking the equality of styles.
        """
        return bool(self._equalAlign(style1['align'], style2['align']) and
                    self._equalFont(style1['font'], style2['font']) and
                    self._equalBorder(style1['border'], style2['border']) and
                    self._equalFormat(style1['num_format'], style2['num_format']) and
                    self._equalColor(style1['color'], style2['color']))

    def _equalAlign(self, align1, align2):
        """
        Equal alignments.
        """
        return bool(align1 == align2)
        
    def _equalFont(self, font1, font2):
        """
        Equal fonts.
        """
        return bool(font1 == font2)
        
    def _equalBorder(self, border1, border2):
        """
        Equal border.
        """
        return bool(border1 == border2)
        
    def _equalFormat(self, format1, format2):
        """
        Equal format.
        """
        return bool(format1 == format2)
        
    def _equalColor(self, color1, color2):
        """
        Equal color.
        """
        return bool(color1 == color2)
        
    def saveStyles(self):
        """
        Save styles.
        """
        self.startElementLevel('Styles', {})
        
        # Default style
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
        
        # Additional styles
        for style in self._styles:
            self.startElementLevel('Style', {'ss:ID': style['style_id']})
            # Alignment
            align = dict()
            h_align = self._REPORT_ALIGNMENT2XML[style['align']['align_txt'][report_generator.REP_ALIGN_HORIZ]]
            v_align = self._REPORT_ALIGNMENT2XML[style['align']['align_txt'][report_generator.REP_ALIGN_VERT]]
            if h_align:
                align['ss:Horizontal'] = h_align
            if v_align:
                align['ss:Vertical'] = v_align
            # Word wrap
            if style['align']['wrap_txt']:
                align['ss:WrapText'] = '1'
            
            self.startElement('Alignment', align)
            self.endElement('Alignment')
            
            # Borders
            self.startElementLevel('Borders', {})
            for border_pos in range(4):
                border = self._borderReport2XML(style['border'], border_pos)
                if border:
                    border_element = {'ss:'+stl_name: border[stl_name] for stl_name in [stl_name for stl_name in border.keys() if border[stl_name] is not None]}
                    self.startElement('Border', border_element)
                    self.endElement('Border')
            self.endElementLevel('Borders')
               
            # Font
            font = dict()
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
            
            # Interior
            interior = dict()
            if style['color']:
                if 'background' in style['color'] and style['color']['background']:
                    interior['ss:Color'] = self._getRGBColor(style['color']['background'])
                    interior['ss:Pattern'] = 'Solid'

            self.startElement('Interior', interior)
            self.endElement('Interior')

            # Format
            fmt = dict()
            if style['num_format']:
                fmt['ss:Format'] = self._getNumberFormat(style['num_format'])
                self.startElement('NumberFormat', fmt)
                self.endElement('NumberFormat')

            self.endElementLevel('Style')
            
        self.endElementLevel('Styles')
        
    def _getRGBColor(self, color):
        """
        Convert (R,G,B) color to #RRGGBB color.
        """
        if type(color) in (list, tuple):
            return '#%02X%02X%02X' % (color[0], color[1], color[2])
        # If the color is specified in a non-RGB format, then leave it unchanged
        return color

    def _getNumberFormat(self, num_format):
        """
        Number format.
        """
        if num_format[0] == report_generator.REP_FMT_EXCEL:
            return num_format[1:]
        elif num_format[0] == report_generator.REP_FMT_STR:
            return '@'
        elif num_format[0] == report_generator.REP_FMT_NUM:
            return '0'
        elif num_format[0] == report_generator.REP_FMT_FLOAT:
            return '0.'
        return '0'

    _REPORT_ALIGNMENT2XML = {report_generator.REP_HORIZ_ALIGN_LEFT: 'Left',
                             report_generator.REP_HORIZ_ALIGN_CENTRE: 'Center',
                             report_generator.REP_HORIZ_ALIGN_RIGHT: 'Right',
                             report_generator.REP_VERT_ALIGN_TOP: 'Top',
                             report_generator.REP_VERT_ALIGN_CENTRE: 'Center',
                             report_generator.REP_VERT_ALIGN_BOTTOM: 'Bottom',
                             }
        
    def _borderReport2XML(self, border, position):
        """
        Convert framing to xml representation.
        """
        if border[position]:
            return {'Position': self._REPORT_POSITION2XML.setdefault(position, 'Left'),
                    'Color': self._colorRep2XML(border[position].setdefault('color', None)),
                    'LineStyle': self._REPORT_LINE2XML.setdefault(border[position].setdefault('style', report_generator.REP_LINE_TRANSPARENT), 'Continuous'),
                    'Weight': str(border[position].setdefault('weight', 1)),
                    }

    _REPORT_POSITION2XML = {report_generator.REP_BORDER_LEFT: 'Left',
                            report_generator.REP_BORDER_RIGHT: 'Right',
                            report_generator.REP_BORDER_TOP: 'Top',
                            report_generator.REP_BORDER_BOTTOM: 'Bottom',
                            }
        
    _REPORT_LINE2XML = {report_generator.REP_LINE_SOLID: 'Continuous',
                        report_generator.REP_LINE_SHORT_DASH: 'Dash',
                        report_generator.REP_LINE_DOT_DASH: 'DashDot',
                        report_generator.REP_LINE_DOT: 'Dot',
                        report_generator.REP_LINE_TRANSPARENT: None,
                        }
    
    def _colorRep2XML(self, color):
        """
        Convert color to xml representation.
        """
        return None

    def saveColumns(self, sheet):
        """
        Save column attributes.
        """
        width_cols = self.getWidthColumns(sheet)
        for width_col in width_cols:
            if width_col is not None:
                self.startElement('Column', {'ss:Width': str(width_col), 'ss:AutoFitWidth': '0'})
            else:
                self.startElement('Column', {'ss:AutoFitWidth': '0'})
            self.endElement('Column')
            
    def getColumnCount(self, sheet):
        """
        Get column number.
        """
        if sheet:
            return max([len(row) for row in sheet])
        return 0

    def getWidthColumns(self, sheet):
        """
        Get column width list.
        """
        col_count = self.getColumnCount(sheet)
        col_width = []
        row = [row for row in sheet if len(row) == col_count][0] if sheet else list()
        for cell in row:
            if cell:
                # log_func.debug('Column width <%s>' % new_cell['width'])
                col_width.append(cell['width'])
            else:
                # log_func.debug('Column default width')
                col_width.append(8.43)
        return col_width

    def getRowHeight(self, row):
        """
        Get row height.
        """
        cells = [cell for cell in row if isinstance(cell, dict) and 'height' in cell]
        return min([cell['height'] for cell in cells]) if cells else 0

    def getRowHidden(self, row):
        """
        Get row hidden.
        """
        cells = [cell for cell in row if isinstance(cell, dict) and 'visible' in cell]
        return (not any([cell['visible'] for cell in cells])) if cells else True

    def startRow(self, row):
        """
        Start row.
        """
        height_row = self.getRowHeight(row)
        hidden_row = self.getRowHidden(row)
        row_dict = {'ss:Height': str(height_row)}
        if hidden_row:
            row_dict['ss:Hidden'] = str(hidden_row)
        self.startElementLevel('Row', row_dict)
        self._idx_set = False       # Clear the index setting flag
        self.cell_idx = 1
            
    def endRow(self):
        """
        End row.
        """
        self.endElementLevel('Row')
        
    def _saveCellStyleID(self, cell):
        """
        Cell style id for save.
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
        Save cell.

        :param row: Row data.
        :param column: Column data.
        :param cell: Cell attributes.
        """
        if cell is None:
            self._idx_set = False   # Clear the index setting flag
            self.cell_idx += 1
            return 

        if 'hidden' in cell and cell['hidden']:
            self._idx_set = False   # Clear the index setting flag
            # Here you need to increase the index by 1
            # because in Excel indexing starts at 1
            self.cell_idx += 1
            return 

        cell_attr = {}
        if self.cell_idx > 1:
            if not self._idx_set:
                cell_attr = {'ss:Index': str(self.cell_idx)}
                self._idx_set = True    # Set the index setting flag

        # Merge cells
        if cell['merge_col'] > 1:
            cell_attr['ss:MergeAcross'] = str(cell['merge_col'] - 1)
            # Process top row of join area
            self._setCellMergeAcross(row, column, cell['merge_col'], sheet)
            if cell['merge_row'] > 1:
                # Process additional join area
                self._setCellMerge(row, column, cell['merge_col'], cell['merge_row'], sheet)
            self._idx_set = False   # Clear the index setting flag
        # Here you need to increase the index by 1
        # because in Excel indexing starts at 1
        self.cell_idx = column+1
    
        if cell['merge_row'] > 1:
            cell_attr['ss:MergeDown'] = str(cell['merge_row'] - 1)
            # Edit left column of join area
            self._setCellMergeDown(row, column, cell['merge_row'], sheet)

        # Style
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
        Get cell value.
        """
        if self._getCellType(value) == 'Number':
            # Number
            value = value.strip()
        else:
            # Not number
            value = value

        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                value = str(value)
        if value:
            value = saxutils.escape(value)
            
        return value

    def _getCellType(self, value):
        """
        Get cell type.
        """
        try:
            # Number
            float(value)
            return 'Number'
        except:
            # Not number
            return 'String'

    def _setCellMergeAcross(self, row, column, merge_across, sheet):
        """
        Reset all cells that fall into the horizontal pool area.

        :param row: Row.
        :param column: Column.
        :param merge_across: Merge cell number.
        :param sheet: Worksheet struct data.
        """
        for i in range(1, merge_across):
            try:
                cell = sheet[row - 1][column + i - 1]
            except IndexError:
                continue
            if cell and (not cell['value']):
                sheet[row - 1][column + i - 1]['hidden'] = True
        return sheet

    def _setCellMergeDown(self, row, column, merge_down, sheet):
        """
        Reset all cells that fall into the vertical pool area.

        :param row: Row.
        :param column: Column.
        :param merge_down: Merge cell number.
        :param sheet: Worksheet struct data.
        """
        for i in range(1, merge_down):
            try:
                cell = sheet[row + i - 1][column - 1]
            except IndexError:
                continue
            if cell and (not cell['value']):
                sheet[row + i - 1][column - 1]['hidden'] = True
        return sheet

    def _setCellMerge(self, row, column, merge_across, merge_down, sheet):
        """
        Reset all cells that fall into the pool zone.

        :param row: Row.
        :param column: Column.
        :param merge_across: Merge cell number.
        :param merge_down: Merge cell number.
        :param sheet: Worksheet struct data.
        """
        for x in range(1, merge_across):
            for y in range(1, merge_down):
                try:
                    cell = sheet[row + y - 1][column + x - 1]
                except IndexError:
                    continue
                if cell is not None and (not cell['value']):
                    sheet[row + y - 1][column + x - 1]['hidden'] = True
        return sheet
