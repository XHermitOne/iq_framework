#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report template module.
"""

import os.path
import string
import copy
import pickle
import re

from iq.util import log_func
from iq.util import xml2dict
from iq.util import exec_func
from iq.util import str_func

from . import report_generator

from iq.components.virtual_spreadsheet import v_spreadsheet

__version__ = (0, 0, 0, 1)

# Report template tags
DESCRIPTION_TAG = '[description]'   # Description band
VAR_TAG = '[var]'                   # Variable band
GENERATOR_TAG = '[generator]'       # Generator type band
DATASRC_TAG = '[data_source]'       # Data source / DB band
QUERY_TAG = '[query]'               # Query table band
STYLELIB_TAG = '[style_lib]'        # Style labrary band

HEADER_TAG = '[header]'             # Report header band
FOOTER_TAG = '[footer]'             # Report footer band
DETAIL_TAG = '[detail]'             # Report data area band
HEADER_GROUP_TAG = '[head_grp]'     # Group header band
FOOTER_GROUP_TAG = '[foot_grp]'     # Group footer band
UPPER_TAG = '[upper]'               # Report upper band
UNDER_TAG = '[under]'               # Report under band

ALL_TAGS = (DESCRIPTION_TAG, VAR_TAG, GENERATOR_TAG, DATASRC_TAG, QUERY_TAG, STYLELIB_TAG,
            HEADER_TAG, FOOTER_TAG, DETAIL_TAG,
            HEADER_GROUP_TAG, FOOTER_GROUP_TAG, UPPER_TAG, UNDER_TAG)
    
# Title tags
TITLE_TAGS = (DESCRIPTION_TAG, VAR_TAG, GENERATOR_TAG, DATASRC_TAG, QUERY_TAG, STYLELIB_TAG)

# The coefficients for converting the width and height of
# the columns and rows are obtained experimentally
XL_COEF_WIDTH = 2
XL_COEF_HEIGHT = 2

DEFAULT_FIT_WIDTH = 1
DEFAULT_FIT_HEIGHT = 1

# Print density
DEFAULT_HORIZ_RESOLUTION = 300
DEFAULT_VERT_RESOLUTION = 300

DEFAULT_REPORT_FILE_EXT = '.rep'

TRANSPARENT_COLOR = 'transparent'

CODE_SIGNATURE = 'PRG:'
PY_SIGNATURE = 'PY:'


class iqReportTemplate(object):
    """
    Report template class.
    """
    def __init__(self):
        """
        Constructor.
        """
        # Report template data
        self._rep_template = None

        # Full report template filename
        self.template_filename = None

    def setTemplateFilename(self, template_filename):
        """
        Set report template filename.

        :param template_filename: Report template filename.
        """
        self.template_filename = template_filename

    def getTemplateFilename(self):
        """
        Get report template filename.
        """
        return self.template_filename

    def save(self, template_filename, template_name=None):
        """
        Save report template file as Pickle.

        :param template_filename:  XML report template filename.
        :param template_name: Template name.
        :return: True/False.
        """
        pickle_file_name = os.path.splitext(template_filename)[0] + DEFAULT_REPORT_FILE_EXT
        pickle_file = None
        try:
            pickle_file = open(pickle_file_name, 'wb')
            pickle.dump(self._rep_template, pickle_file)
            pickle_file.close()
            return True
        except:
            if pickle_file:
                pickle_file.close()
            log_func.fatal(u'Error save report template file')
        return False

    def load(self, template_filename, template_name=None):
        """
        Load report template data from Pickle file.

        :param template_filename: XML report template filename.
        :param template_name: Template name.
        :return: True/False.
        """
        self.setTemplateFilename(template_filename)
        pickle_file_name = os.path.splitext(template_filename)[0]+DEFAULT_REPORT_FILE_EXT
        pickle_file = None
        try:
            pickle_file = open(pickle_file_name, 'rb')
            self._rep_template = pickle.load(pickle_file)
            pickle_file.close()
            return True
        except:
            if pickle_file:
                pickle_file.close()
            log_func.fatal(u'Error load report template from file <%s>' % template_filename)
        return False

    def needUpdate(self, template_filename, template_name=None):
        """
        Need to update the Pickle report template file?

        :param template_filename: XML report template filename.
        :param template_name: Template name.
        :return: True-need update / False-no need to update.
        """
        pickle_file_name = os.path.splitext(template_filename)[0]+DEFAULT_REPORT_FILE_EXT
        if not os.path.exists(pickle_file_name) or os.path.getsize(pickle_file_name) < 10:
            # 1. Pickle file does not exist, so you need to update
            # 2. It is understood that the size of the template cannot be less
            # than 10 bytes, otherwise None or an empty dictionary is written there
            return True
        # Check creation time of xml template
        xml_create_time = os.path.getmtime(template_filename)
        rtp_create_time = os.path.getmtime(pickle_file_name)
        return xml_create_time > rtp_create_time
        
    def read(self, tmpl_filename, template_name=None):
        """
        Read report template data.

        :param tmpl_filename: Report template filename.
        :param template_name: Template name.
        """
        pass

    def get(self):
        """
        Get report template data.
        """
        return self._rep_template

    _LINE_STYLE = {
        'Continuous': report_generator.REP_LINE_SOLID,
        'Dash': report_generator.REP_LINE_SHORT_DASH,
        'DashDot': report_generator.REP_LINE_DOT_DASH,
        'Dot': report_generator.REP_LINE_DOT,
        }

    def _getLineStyle(self, line_style):
        """
        Recode style.
        """
        return self._LINE_STYLE.setdefault(line_style, report_generator.REP_LINE_TRANSPARENT)
        
    def _getBordersStyle(self, style):
        """
        Get borders from style.

        :param style: Style data.
        """
        style_border = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'Borders']
        if style_border:
            style_border = style_border[0]['_children_']
        else:
            style_border = list()
            
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

                if 'LineStyle' in border:
                    cur_border['style'] = self._getLineStyle(border['LineStyle'])
                if 'Weight' in border:
                    cur_border['weight'] = int(round(float(border['Weight'])))
    
        return tuple(borders)
        
    def _getFontStyle(self, style):
        """
        Get font data from style.

        :param style: Style data.
        """
        style_font = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'Font']
        log_func.debug('Font <%s> Style <%s>' % (style_font, style['ID']))
        if style_font:
            style_font = style_font[0]
        else:
            style_font = {}
        
        # Font data
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
        Convert color from #RRGGBB format to (R,G,B) format.
        """
        if color.strip().lower() == TRANSPARENT_COLOR:
            return None
        return int('0x'+color[1:3], 16), int('0x'+color[3:5], 16), int('0x'+color[5:7], 16)
        
    def _getColorStyle(self, style):
        """
        Get color data from style.

        :param style: Style data.
        """
        color = {}

        style_font = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'Font']
        if style_font:
            style_font = style_font[0]
        else:
            style_font = {}
            
        if 'Color' in style_font:
            color['text'] = self._getColorRGB(style_font['Color'])
        else:
            # Default text color is black
            color['text'] = (0, 0, 0)
            
        # Interior in style
        style_interior = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'Interior']
        if style_interior:
            style_interior = style_interior[0]
        else:
            style_interior = {}

        if 'Color' in style_interior:
            color['background'] = self._getColorRGB(style_interior['Color'])
        else:
            # Default background color is white
            color['background'] = None
        return color

    def _getAlignStyle(self, style):
        """
        Get alignment data from style.

        :param style: Style data.
        """
        style_align = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'Alignment']
        if style_align:
            style_align = style_align[0]
        else:
            style_align = {}
        
        align = {'align_txt': [report_generator.REP_HORIZ_ALIGN_LEFT,
                               report_generator.REP_VERT_ALIGN_CENTRE],
                 'wrap_txt': False,
                 }
        # Text alignment
        if 'Horizontal' in style_align:
            if style_align['Horizontal'] == 'Left':
                align['align_txt'][0] = report_generator.REP_HORIZ_ALIGN_LEFT
            elif style_align['Horizontal'] == 'Right':
                align['align_txt'][0] = report_generator.REP_HORIZ_ALIGN_RIGHT
            elif style_align['Horizontal'] == 'Center':
                align['align_txt'][0] = report_generator.REP_HORIZ_ALIGN_CENTRE
        if 'Vertical' in style_align:
            if style_align['Vertical'] == 'Top':
                align['align_txt'][1] = report_generator.REP_VERT_ALIGN_TOP
            elif style_align['Vertical'] == 'Bottom':
                align['align_txt'][1] = report_generator.REP_VERT_ALIGN_BOTTOM
            elif style_align['Vertical'] == 'Center':
                align['align_txt'][1] = report_generator.REP_VERT_ALIGN_CENTRE
        align['align_txt'] = tuple(align['align_txt'])
        # Wrap text
        if 'WrapText' in style_align and style_align['WrapText'] == '1':
            align['wrap_txt'] = True

        return align

    def _getFmtStyle(self, style):
        """
        Get number format from style.
        """
        style_fmt = [style_attr for style_attr in style['_children_'] if style_attr['name'] == 'NumberFormat']
        if style_fmt:
            style_fmt = style_fmt[0]
        else:
            style_fmt = {}
        
        if 'Format' in style_fmt:
            return report_generator.REP_FMT_EXCEL + style_fmt['Format']
        return report_generator.REP_FMT_NONE

    def _getPageSetup(self, page_setup):
        """
        Get page setup data.
        """
        new_page_setup = {}
        # Orientation
        layouts = [obj for obj in page_setup['_children_'] if obj['name'] == 'Layout']
        log_func.debug('Layout %s' % layouts)
        if layouts:
            layout = layouts[0]
            if 'Orientation' in layout:
                if layout['Orientation'] == 'Landscape':
                    new_page_setup['orientation'] = report_generator.REP_ORIENTATION_LANDSCAPE
                elif layout['Orientation'] == 'Portrait':
                    new_page_setup['orientation'] = report_generator.REP_ORIENTATION_PORTRAIT
            # Start page number
            if 'StartPageNumber' in layout:
                new_page_setup['start_num'] = int(layout['StartPageNumber'])
        # Margins
        page_margins = [obj for obj in page_setup['_children_'] if obj['name'] == 'PageMargins']
        log_func.debug('PageMargins %s' % page_margins)
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
        Get print setup data.
        """
        new_print_setup = {}
        # Paper size
        paper_sizes = [obj for obj in print_setup['_children_'] if obj['name'] == 'PaperSizeIndex']
        if paper_sizes:
            new_print_setup['paper_size'] = paper_sizes[0]['value']
        # Scale
        scales = [obj for obj in print_setup['_children_'] if obj['name'] == 'Scale']
        if scales:
            new_print_setup['scale'] = int(scales[0]['value'])
        else:
            try:
                h_fit = [obj for obj in print_setup['_children_'] if obj['name'] == 'FitWidth'][0]['value']
            except:
                h_fit = DEFAULT_FIT_WIDTH
            try:
                v_fit = [obj for obj in print_setup['_children_'] if obj['name'] == 'FitHeight'][0]['value']
            except:
                v_fit = DEFAULT_FIT_HEIGHT
            new_print_setup['fit'] = (int(h_fit), int(v_fit))

        try:
            h_resolution = [obj for obj in print_setup['_children_'] if obj['name'] == 'HorizontalResolution'][0]['value']
        except:
            h_resolution = DEFAULT_HORIZ_RESOLUTION
        try:    
            v_resolution = [obj for obj in print_setup['_children_'] if obj['name'] == 'VerticalResolution'][0]['value']
        except:
            v_resolution = DEFAULT_VERT_RESOLUTION
        new_print_setup['resolution'] = (int(h_resolution), int(v_resolution))

        return new_print_setup


class iqlXMLSpreadSheetReportTemplate(iqReportTemplate):
    """
    Report template in Excel XMLSpreadSheet format.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqReportTemplate.__init__(self)
        
        # Bend tag column number
        self._tag_band_col = None
        # Current band tag
        self.__cur_band = None
        
        # Current report template worksheet
        self._rep_worksheet = None

        # Duplicate column width
        self._column_span_width = None
        # Duplicate row height
        self._row_span_height = 12.75
        
        # Default column width
        self._default_column_width = None
        # Default row height
        self._default_row_height = 12.75

    def read(self, tmpl_filename, template_name=None):
        """
        Read report template file.

        :param tmpl_filename: Report template filename.
        :param template_name: Template name.
        """
        if self.needUpdate(tmpl_filename, template_name):
            # Need update template data
            template_data = self.open(tmpl_filename)
            self._rep_template = self.parse(template_data, template_name)
            self.save(tmpl_filename, template_name)
        else:
            self.load(tmpl_filename, template_name)
        return self._rep_template

    def open(self, tmpl_filename):
        """
        Open report template file.

        :param tmpl_filename: Report template filename.
        """
        return xml2dict.XmlFile2Dict(tmpl_filename)

    def _normList(self, data_list, element_name, length=None):
        """
        Normal list.

        :param length: Maximum list length, if specified, then
            the list is normalized to the maximum length.
        """
        element_template = {'name': element_name}
        lst = []
        for i in range(len(data_list)):
            element = data_list[i]
            # Check indexes
            if 'Index' in element:
                if int(element['Index']) > len(lst):
                    lst += [element_template] * (int(element['Index'])-len(lst)-1)
            lst.append(element)
            # Merge cells
            if 'MergeAcross' in element:
                lst += [element_template] * int(element['MergeAcross'])
                
        if length:
            if length > len(lst):
                lst += [element_template]*(length - len(lst))
        return lst
        
    def _normTable(self, table):
        """
        Normal table.
        """
        new_table = {}.fromkeys([key for key in table.keys() if key != '_children_'])
        for key in new_table.keys():
            new_table[key] = table[key]
        new_table['_children_'] = []

        # Columns
        cols = [element for element in table['_children_'] if element['name'] == 'Column']
        cols = self._normList(cols, 'Column')
        max_len = len(cols)
        # Rows
        rows = [element for element in table['_children_'] if element['name'] == 'Row']
        rows = self._normList(rows, 'Row')
        # Cells
        for i_row in range(len(rows)):
            row = rows[i_row]
            if '_children_' in row:
                rows[i_row]['_children_'] = self._normList(row['_children_'], 'Cell', max_len)

        new_table['_children_'] += cols
        new_table['_children_'] += rows
        return new_table

    def _defineSpan(self, obj_list):
        """
        Duplicate object descriptions with the Span attribute.

        :param obj_list: Object data list.
        :return: List with duplicate objects added.
        """
        result = list()
        for obj in obj_list:
            if 'Span' in obj:
                # This is an object account whose description we use
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
        Parse template data.

        :param template_data: Report template data.
        :param template_name: Template name, if None then first sheet.
        """
        try:
            # Create template
            rep = copy.deepcopy(report_generator.REPORT_TEMPLATE)

            workbook = template_data['_children_'][0]
            # Styles
            styles = dict([(style['ID'], style) for style in [element for element in workbook['_children_']
                                                              if element['name'] == 'Styles'][0]['_children_']])
            worksheets = [element for element in workbook['_children_'] if element['name'] == 'Worksheet']

            # I. Define all bands in the template
            # If the template name is not defined, then take the first sheet
            if template_name is None:
                template_name = worksheets[0]['Name']
                self._rep_worksheet = worksheets[0]
            else:
                # Set the page of the selected report template active
                self._rep_worksheet = [sheet for sheet in worksheets if sheet['Name'] == template_name][0]

            rep['name'] = template_name
            
            # Table
            rep_template_tabs = [rep_obj for rep_obj in self._rep_worksheet['_children_'] if rep_obj['name'] == 'Table']
            self._setDefaultCellSize(rep_template_tabs[0])
            # Normal table
            rep_template_tab = self._normTable(rep_template_tabs[0])

            # Column data
            rep_template_cols = [element for element in rep_template_tab['_children_'] if element['name'] == 'Column']
            rep_template_cols = self._defineSpan(rep_template_cols)
            # Row data
            rep_template_rows = [element for element in rep_template_tab['_children_'] if element['name'] == 'Row']
            rep_template_rows = self._defineSpan(rep_template_rows)

            # The number of columns without a column tag bands
            col_count = self._getColumnCount(rep_template_rows)
            log_func.debug(u'Column number [%d]' % col_count)

            # II. Define all sheet cells
            used_rows = range(len(rep_template_rows))
            used_cols = range(col_count)

            self.__cur_band = None  # Current band tag

            for cur_row in used_rows:
                if not self._isTitleBand(rep_template_rows, cur_row):
                    # No footers, add cells to the shared sheet
                    rep['sheet'].append([])
                    for cur_col in used_cols:
                        cell_attr = self._getCellAttr(rep_template_rows, rep_template_cols, styles, cur_row, cur_col)
                        if not self._isTag(cell_attr['value']):
                            rep['sheet'][-1].append(cell_attr)
                        else:
                            rep['sheet'][-1].append(None)

            # III. Define band in sheet
            self.__cur_band = None  # Current band tag
            title_row = 0   # Header / footer line counter
    
            for cur_row in range(len(rep_template_rows)):
                tag = self._getTagBandRow(rep_template_rows, cur_row)
                # If this is a cell with a specific tag, then a new band
                if tag:
                    self.__cur_band = tag
                    if tag in TITLE_TAGS:
                        parse_func = self._TITLE_TAG_PARSE_METHODS.setdefault(tag, None)
                        try:
                            parse_func(self, rep, rep_template_rows[cur_row]['_children_'])
                        except:
                            log_func.fatal(u'Error parse function <%s>' % str_func.toUnicode(parse_func))
                        title_row += 1
                    else:
                        rep = self._defBand(self.__cur_band, cur_row, col_count, title_row, rep)
                else:
                    log_func.warning(u'Not valid tag <%s> of row [%d]' % (tag, cur_row))

            # Page setup
            rep['page_setup'] = copy.deepcopy(report_generator.REP_PAGESETUP)
            sheet_options = [rep_obj for rep_obj in self._rep_worksheet['_children_']
                             if rep_obj['name'] == 'WorksheetOptions']

            page_setup = [rep_obj for rep_obj in sheet_options[0]['_children_'] if rep_obj['name'] == 'PageSetup'][0]
            rep['page_setup'].update(self._getPageSetup(page_setup))
            print_setup = [rep_obj for rep_obj in sheet_options[0]['_children_'] if rep_obj['name'] == 'Print']
            if print_setup:
                rep['page_setup'].update(self._getPrintSetup(print_setup[0]))

            if not rep['generator']:
                tmpl_filename = self.getTemplateFilename()
                rep['generator'] = os.path.splitext(tmpl_filename)[1].upper() if tmpl_filename else '.ODS'

            return rep
        except:
            log_func.fatal(u'Error parse report template <%s>' % str_func.toUnicode(template_name))
        return None

    def _existTagBand(self):
        """
        Exists band tag column in report template data?
        If it does not exist, then we further consider
        that the whole template is the header of the report [header].

        :return: True/False.
        """
        log_func.info(u'Band tag column [%s]' % str(self._tag_band_col))
        return self._tag_band_col is not None

    def _getColumnCount(self, rows):
        """
        Get column number.

        :param rows: Row data list.
        :return: Column number.
        """
        # First, we assume that the template has a column of bend tags
        col_count = self._getTagBandIdx(rows)
        if col_count <= 0:
            # The template does not have a column of tag tags
            max_col = 0
            for row in range(len(rows)):
                if '_children_' in rows[row]:
                    for col in range(len(rows[row]['_children_'])):
                        max_col = max(max_col, col)
            col_count = max_col
        return col_count

    def _getTagBandIdx(self, rows):
        """
        Get band tag column index.

        :param rows: Row data list.
        :return: Band tag column index.
        """
        if self._tag_band_col is None:
            # Last column
            tag_col = 0
            for row in range(len(rows)):
                if '_children_' in rows[row]:
                    for col in range(len(rows[row]['_children_'])):
                        try:
                            cell_data = rows[row]['_children_'][col]['_children_']
                        except:
                            cell_data = None
                        # If the cell data is defined, then get the value
                        if cell_data and 'value' in cell_data[0]:
                            value = cell_data[0]['value']
                        else:
                            value = None
                        if self._isTag(value):
                            tag_col = max(tag_col, col)
                        log_func.debug(u'Find band tag column index. Cell [%d : %d]. Value <%s>. Band tag column [%d]' % (row, col, value, tag_col))
            self._tag_band_col = tag_col
        return self._tag_band_col
        
    def _band(self, band, row, col_size):
        """
        Fill band.
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
        Normal report template data area.
        If the cells in the tabular section are not filled, then it means
        that the cells will be filled in order.

        :param detail: Detail band data.
        :param report: Report data.
        """
        if detail['row_size'] == 1:
            ok = any([bool(cell['value']) for cell in report['sheet'][detail['row']]])
            if not ok:
                for i_row in range(detail['row'], detail['row'] + detail['row_size']):
                    for i_col in range(detail['col'], detail['col'] + detail['col_size']):
                        try:
                            report['sheet'][i_row][i_col]['value'] = '[\'%s\']' % (self.FIELD_NAMES[i_col - detail['col']])
                        except:
                            log_func.fatal('Error normal detail')
        return report
        
    def _defBand(self, band_tag, row, col_count, title_row, report):
        """
        Define band data.

        :param band_tag: Band tag.
        :param row: Row number.
        :param title_row: Title row number.
        :param col_count: Column number.
        :param report: Report data.
        :return: Report data.
        """
        try:
            # Create copy report data
            rep = copy.deepcopy(report)
            
            log_func.debug(u'Define band. Band tag: <%s>' % band_tag)
            if band_tag.strip() == HEADER_TAG:
                rep['header'] = self._band(rep['header'], row - title_row, col_count)
            elif band_tag.strip() == DETAIL_TAG:
                rep['detail'] = self._band(rep['detail'], row - title_row, col_count)
                self._normDetail(rep['detail'], rep)
            elif band_tag.strip() == FOOTER_TAG:
                rep['footer'] = self._band(rep['footer'], row - title_row, col_count)
            elif HEADER_GROUP_TAG in band_tag:
                # Group field name
                field_name = re.split(report_generator.REP_FIELD_PATT, band_tag)[1].strip()[2:-2]
                # If such a group is not registered, then register it
                is_grp = any([grp['field'] == field_name for grp in rep['groups']])
                if not is_grp:
                    # Record in accordance with the regulations regarding other groups
                    rep['groups'].append(copy.deepcopy(report_generator.REP_GRP))
                    rep['groups'][-1]['field'] = field_name
                # Group title
                grp_field = [grp for grp in rep['groups'] if grp['field'] == field_name][0]
                grp_field['header'] = self._band(grp_field['header'], row - title_row, col_count)
            elif FOOTER_GROUP_TAG in band_tag:
                # Group field name
                field_name = re.split(report_generator.REP_FIELD_PATT, band_tag)[1].strip()[2:-2]
                # If such a group is not registered, then register it
                is_grp = any([grp['field'] == field_name for grp in rep['groups']])
                if not is_grp:
                    rep['groups'].append(copy.deepcopy(report_generator.REP_GRP))
                    rep['groups'][-1]['field'] = field_name
                grp_field = [grp for grp in rep['groups'] if grp['field'] == field_name][0]
                grp_field['footer'] = self._band(grp_field['footer'], row - title_row, col_count)
            elif band_tag.strip() == UPPER_TAG:
                # Upper
                rep['upper'] = self._band(rep['upper'], row - title_row, col_count)
            elif band_tag.strip() == UNDER_TAG:
                # Under
                rep['under'] = self._band(rep['under'], row - title_row, col_count)
            else:
                log_func.warning(u'Unsupported band type <%s>' % band_tag)
            rep['upper'] = self._bandUpper(rep['upper'], self._rep_worksheet)
            rep['under'] = self._bandUnder(rep['under'], self._rep_worksheet)
            
            return rep
        except:
            log_func.fatal(u'Error define band <%s>' % band_tag)
        return report
        
    def _bandUpper(self, band, worksheet_data):
        """
        Define upper band.

        :param band: Upper band data.
        :param worksheet_data: Report template worksheet data.
        """
        rep_upper = band

        if 'data' not in band:
            worksheet_options = [element for element in worksheet_data['_children_'] if element['name'] == 'WorksheetOptions']
            if worksheet_options:
                page_setup = [element for element in worksheet_options[0]['_children_'] if element['name'] == 'PageSetup']
                if page_setup:
                    header = [element for element in page_setup[0]['_children_'] if element['name'] == 'Header']
                    if header:
                        if 'Data' in header[0]:
                            rep_upper['data'] = header[0]['Data']
                        if 'Margin' in header[0]:
                            rep_upper['height'] = header[0]['Margin']
        return rep_upper
        
    def _bandUnder(self, band, worksheet_data):
        """
        Define under band.

        :param band: Under band data.
        :param worksheet_data: Report template worksheet data.
        """
        rep_under = band

        if 'data' not in band:
            worksheet_options = [element for element in worksheet_data['_children_'] if element['name'] == 'WorksheetOptions']
            if worksheet_options:
                page_setup = [element for element in worksheet_options[0]['_children_'] if element['name'] == 'PageSetup']
                if page_setup:
                    footer = [element for element in page_setup[0]['_children_'] if element['name'] == 'Footer']
                    if footer:
                        if 'Data' in footer[0]:
                            rep_under['data'] = footer[0]['Data']
                        if 'Margin' in footer[0]:
                            rep_under['height'] = footer[0]['Margin']
        return rep_under
        
    def _getParseRow(self, row, cur_band):
        """
        Get row data for parsing.

        :param row: Row data.
        :param cur_band: Current band tag.
        """
        return row
    
    def _getCellStyle(self, rows, columns, styles, row, column):
        """
        Get cell style.

        :param rows: Row data list.
        :param columns: Column data list.
        :param styles: Styles dictionary.
        :param row: Cell row index.
        :param column: Cell column index.
        """
        try:
            try:
                template_cell = rows[row]['_children_'][column]
            except:
                template_cell = {}
                cell_style = styles['Default']

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
            # log_func.debug('Get new_cell style <%s>' % cell_style)
            return cell_style
        except:
            log_func.fatal(u'Error define cell style')
        return styles['Default']

    def _getTypeCell(self, cell):
        """
        Get cell type.

        :param cell: Cell data.
        """
        if '_children_' not in cell or not cell['_children_']:
            return report_generator.REP_FMT_NONE
            
        cell_data = cell['_children_'][0]
        if 'Type' in cell_data:
            if cell_data['Type'] == 'General':
                return report_generator.REP_FMT_NONE
            elif cell_data['Type'] == 'String':
                return report_generator.REP_FMT_STR
            elif cell_data['Type'] == 'Number':
                return report_generator.REP_FMT_NUM
            else:
                return report_generator.REP_FMT_MISC + cell_data['Type']
        return report_generator.REP_FMT_NONE

    def _getCellValue(self, cell):
        """
        Get cell value.

        :param cell: Cell data.
        """
        if '_children_' not in cell or not cell['_children_'] or \
           'value' not in cell['_children_'][0]:
            return None
        return cell['_children_'][0]['value']
        
    def _setDefaultCellSize(self, table):
        """
        Set cell default data.

        :param table: Table data.
        """
        if 'DefaultColumnWidth' in table:
            self._default_column_width = float(table['DefaultColumnWidth'])
            self._column_span_width = self._default_column_width
        if 'DefaultRowHeight' in table:
            self._default_row_height = float(table['DefaultRowHeight'])
            self._row_span_height = self._default_row_height
        
    def _getCellAttr(self, rows, columns, styles, row, column):
        """
        Get cell attributes data.

        :param rows: Row data list.
        :param columns: Column data list.
        :param styles: Styles dictionary.
        :param row: Cell row index.
        :param column: Cell column index.
        :return: report_generator.REP_CELL structure.
        """
        try:
            cell_style = self._getCellStyle(rows, columns, styles, row, column)
            cell = {}

            # Column widths
            if not columns:
                cell_width = self._default_column_width     # 8.43
            elif len(columns) > column and 'Hidden' in columns[column]:
                cell_width = 0
            elif columns and len(columns) > column and 'Width' in columns[column]:
                cell_width = float(columns[column]['Width'])
                if 'Span' in columns[column]:
                    self._column_span_width = cell_width
            else:
                cell_width = self._column_span_width    # Default 8.43

            # Row heights
            if not rows:
                cell_height = self._default_row_height
            elif len(rows) > row and 'Hidden' in rows[row] and rows[row]['Hidden'] == '1':
                cell_height = 0
            elif rows and len(rows) > row and 'Height' in rows[row]:
                cell_height = float(rows[row]['Height'])
                if 'Span' in rows[row]:
                    self._row_span_height = cell_height
            else:
                cell_height = self._row_span_height     # Default 12.75

            # Merge cells
            # If cells are combined in a template, then merge them in a report
            cell['merge_row'] = 1
            cell['merge_col'] = 1

            try:            
                template_cell = rows[row]['_children_'][column]

                if 'MergeDown' in template_cell:
                    cell['merge_row'] = int(template_cell['MergeDown']) + 1
                if 'MergeAcross' in template_cell:
                    cell['merge_col'] = int(template_cell['MergeAcross']) + 1
            except:
                template_cell = None
                
            # Cell attributes
            # Cell size
            cell['width'] = cell_width
            cell['height'] = cell_height
            # Visible
            cell['visible'] = True
    
            # Borders
            cell['border'] = self._getBordersStyle(cell_style)
            
            # Font
            cell['font'] = self._getFontStyle(cell_style)
    
            # Set color
            cell['color'] = self._getColorStyle(cell_style)
    
            # Alignment
            cell['align'] = self._getAlignStyle(cell_style)
    
            # Number format
            cell['num_format'] = self._getFmtStyle(cell_style)
            # Cell text
            if template_cell:
                cell['value'] = self._getCellValue(template_cell)
            else:
                cell['value'] = None

            # Init sum
            cell['sum'] = None
    
            return cell
        except:
            log_func.fatal(u'Error get cell attributes')
        return None
    
    def _isTag(self, value):
        """
        Are there bend tags in the cell value?

        :param value: Cell value.
        :return: True/False.
        """
        if not value:
            return False
        # If at least 1 tag is in the cell, then everything is ok
        for tag in ALL_TAGS:
            if value.find(tag) != -1:
                return True
        return False

    def _getTagBandRow(self, rows, row):
        """
        Define the band tag to which the line belongs.

        :param rows: Row data list.
        :param row: Row index.
        :return: Band tag string or None in case of error.
        """
        try:
            row_data = rows[row]

            if '_children_' not in row_data or not row_data['_children_']:
                log_func.warning(u'Error having row children <%s>' % row)
                return self.__cur_band
            i_tag = self._getTagBandIdx(rows)

            # If the column of the tags of the bends is not in the template,
            # then we consider that the entire template is a report header
            if not self._existTagBand():
                self.__cur_band = HEADER_TAG
            else:
                if i_tag > 0:
                    i_tag, tag_value = self._findTagBandRow(row_data)
                    if i_tag >= 0:
                        # If tag found
                        self.__cur_band = tag_value

            return self.__cur_band
        except:
            log_func.fatal(u'Error get tag band row')
        return None

    def _findTagBandRow(self, row):
        """
        Search for a tag in the current band.

        :param row: Row data.
        :return: Tuple:
            (The index of the cell in the row where the tag is located.
             Or -1 if the tag is not found in the line,
             Tag).
        """
        try:
            for i in range(len(row['_children_'])-1, -1, -1):
                cell = row['_children_'][i]
                if '_children_' in cell and cell['_children_'] and 'value' in cell['_children_'][0] and \
                   self._isTag(str(cell['_children_'][0]['value']).lower().strip()):
                    return i, cell['_children_'][0]['value'].lower().strip()
        except:
            log_func.fatal(u'Error find tag in current band')
        return -1, None

    def _isUpperBand(self, rows, row):
        """
        Check is the current line row of the band header.

        :param rows: Row data list.
        :param row: Row index.
        :return: True/False.
        """
        try:
            tag = self._getTagBandRow(rows, row)
            return bool(tag == UPPER_TAG)
        except:
            log_func.fatal(u'Error check is row upper band')
            return False
    
    def _isUnderBand(self, rows, row):
        """
        Check is the current line row of the footer band.

        :param rows: Row data list.
        :param row: Row index.
        :return: True/False.
        """
        try:
            tag = self._getTagBandRow(rows, row)
            return bool(tag == UNDER_TAG)
        except:
            log_func.fatal(u'Error check is row under band')
        return False

    def _isTitleBand(self, rows, row):
        """
        Is the current row of the sheet a band of the header?

        :param rows: Row data list.
        :param row: Row index.
        :return: True/False.
        """
        try:
            return bool(self._getTagBandRow(rows, row) in TITLE_TAGS)
        except:
            log_func.fatal(u'Error check is row title band')
        return False

    def _parseDescriptionTag(self, report, parse_row):
        """
        Parse description tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            if not self._existTagBand():
                # If band tags are not specified in the template,
                # then we define the description as a file name
                tmpl_filename = self.getTemplateFilename()
                report['description'] = os.path.splitext(os.path.basename(tmpl_filename))[0] if tmpl_filename else u''
            else:
                if 'value' in parse_row[0]['_children_'][0] and parse_row[0]['_children_'][0]['value']:
                    report['description'] = parse_row[0]['_children_'][0]['value']
                else:
                    report['description'] = None
        except:
            log_func.fatal(u'Error parse description tag')

    def _parseVarTag(self, report, parse_row):
        """
        Parse variable tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            name = parse_row[0]['_children_'][0]['value']
            value = parse_row[1]['_children_'][0]['value']
            if isinstance(value, str) and value.startswith(CODE_SIGNATURE):
                value = exec_func.execTxtFunction(value.replace(CODE_SIGNATURE, u'').strip())
            elif isinstance(value, str) and value.startswith(PY_SIGNATURE):
                value = exec_func.execTxtFunction(value.replace(PY_SIGNATURE, u'').strip())
            report['variables'][name] = value
        except:
            log_func.fatal(u'Error parse variable tag')

    def _parseGeneratorTag(self, report, parse_row):
        """
        Parse generator tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            if not self._existTagBand():
                # If band tags are not specified in the template,
                # then we determine the generator by file name extension
                tmpl_filename = self.getTemplateFilename()
                report['generator'] = os.path.splitext(tmpl_filename)[1].upper() if tmpl_filename else '.ODS'
            else:
                if 'value' in parse_row[0]['_children_'][0] and parse_row[0]['_children_'][0]['value']:
                    report['generator'] = parse_row[0]['_children_'][0]['value']
                else:
                    report['generator'] = None
        except:
            log_func.fatal(u'Error parse generator tag')

    def _parseDataSrcTag(self, report, parse_row):
        """
        Parser data source tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            report['data_source'] = parse_row[0]['_children_'][0]['value']
        except:
            report['data_source'] = None
            log_func.warning(u'Not defined data source / database')

    def _parseQueryTag(self, report, parse_row):
        """
        Parse query tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            report['query'] = parse_row[0]['_children_'][0]['value']
        except:
            report['query'] = None
            log_func.warning(u'Not defined query')
            
    def _parseStyleLibTag(self, report, parse_row):
        """
        Parse style library tag.

        :param report: Report template data.
        :param parse_row: The parsed line of the report template as a list.
        """
        try:
            from . import style_library
            xml_style_lib_file_name = parse_row[0]['_children_'][0]['value']
            report['style_lib'] = style_library.iqXMLReportStyleLibrary().convert(xml_style_lib_file_name)
        except:
            log_func.fatal(u'Error parse style library tag')
            
    # Dictionary of header tag parsing functions
    _TITLE_TAG_PARSE_METHODS = {DESCRIPTION_TAG: _parseDescriptionTag,
                                VAR_TAG: _parseVarTag,
                                GENERATOR_TAG: _parseGeneratorTag,
                                DATASRC_TAG: _parseDataSrcTag,
                                QUERY_TAG: _parseQueryTag,
                                STYLELIB_TAG: _parseStyleLibTag,
                                }


class iqODSReportTemplate(iqlXMLSpreadSheetReportTemplate):
    """
    Report template in ODF Open Document Spreadsheet format.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqlXMLSpreadSheetReportTemplate.__init__(self)

    def open(self, tmpl_filename):
        """
        Open report template file.

        :param tmpl_filename: Report template filename.
        """
        spreadsheet = v_spreadsheet.iqVSpreadsheet()
        result = spreadsheet.load(tmpl_filename)
        spreadsheet.saveAsXML(tmpl_filename.replace('.ods', '.xml'))
        return result


class iqXLSReportTemplate(iqODSReportTemplate):
    """
    Report template in Excel XLS format.
    """

    def __init__(self):
        """
        Конструктор класса.
        """
        iqODSReportTemplate.__init__(self)

    def open(self, tmpl_filename):
        """
        Open report template file.

        :param tmpl_filename: Report template filename.
        """
        try:
            ods_filename = os.path.splitext(tmpl_filename)[0] + '.ods'
            cmd = 'unoconv --format=ods %s' % tmpl_filename
            log_func.info(u'Execute command <%s>' % cmd)
            os.system(cmd)

            return iqODSReportTemplate.open(self, ods_filename)
        except:
            log_func.fatal(u'Error open report template file <%s>' % tmpl_filename)
        return None
