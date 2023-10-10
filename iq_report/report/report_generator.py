#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report generator module.

Report cell tags:
['...'] - Access to the query table field.

[&...&] - Accessing a report variable.
Report variables are set in the query table
in the form of a dictionary by key '__variables__'.

[@package.module.function()@] - Python function call.

[=...=] - Execution of a code block.
Code block system variables:
    value - The value written to the cell
    record - Dictionary of the current query table entry
For example:
    [=value=record['dt'].strftime('%B')=]
    [=cell['color']=dict(background=(128, 0 , 0)) if record['is_alarm'] else None; value=record['field_name']=]

[^...^] - Generator system functions.
For example:
    [^N^] - Tabular line number.
    [^SUM(record['...'])^] or [^SUM({имя поля})^] - Field summation.
    [^AVG(record['...'])^] or [^AVG({имя поля})^] - Field average calculation.

[*...*] - Setting the generation style.
"""

import time
import datetime
import re
import copy

from iq.util import log_func
from iq.util import str_func
from iq.util import exec_func
from iq.util import dt_func

__version__ = (0, 0, 3, 4)

# Report cell tags:
# query table field values
REP_FIELD_PATT = r'(\[\'.*?\'\])'
# function
REP_FUNC_PATT = r'(\[@.*?@\])'
# expression
REP_EXP_PATT = r'(\[#.*?#\])'
# lambda
REP_LAMBDA_PATT = r'(\[~.*?~\])'
# variable
REP_VAR_PATT = r'(\[&.*?&\])'
# code block
REP_EXEC_PATT = r'(\[=.*?=\])'
# system function
REP_SYS_PATT = r'(\[\^.*?\^\])'
# Tags are used in the SUM summation
# system function to indicate field values
REP_SUM_FIELD_START = '{'
REP_SUM_FIELD_STOP = '}'
# style
REP_STYLE_PATT = r'(\[\*.*?\*\])'
# sub report
REP_SUBREPORT_PATT = r'(\[$.*?$\])'

ALL_PATTERNS = (REP_FIELD_PATT,
                REP_FUNC_PATT,
                REP_EXP_PATT,
                REP_LAMBDA_PATT,
                REP_VAR_PATT,
                REP_EXEC_PATT,
                REP_SYS_PATT,
                REP_STYLE_PATT,
                REP_SUBREPORT_PATT,
                )
    
REPORT_TEMPLATE = {
    'name': '',             # Report name
    'description': '',      # Description
    'variables': dict(),    # Report variables
    'generator': None,      # Generator
    'data_source': None,    # Data source / BD
    'query': None,          # Report query
    'style_lib': None,      # Style library
    'template': None,       # Template modification
    'header': dict(),       # Header band (coordinates and sizes)
    'footer': dict(),       # Footer band (coordinates and sizes)
    'detail': dict(),       # Data area band (coordinates and sizes)
    'groups': list(),       # Group band list (coordinates and sizes)
    'upper': dict(),        # Upper band (coordinates and sizes)
    'under': dict(),        # Under band (coordinates and sizes)
    'sheet': list(),        # Report cells
    'args': dict(),         # Extended arguments
    'page_setup': None,     # Page setup
    }


# Page orientation
REP_ORIENTATION_PORTRAIT = 0     # Portrait
REP_ORIENTATION_LANDSCAPE = 1    # Landscape

# Page setup
REP_PAGESETUP = {
    'orientation': REP_ORIENTATION_PORTRAIT,  # Page orientation
    'start_num': 1,                           # Start numbering from page...
    'page_margins': (0, 0, 0, 0),             # Margins
    'scale': 100,                             # Print scale (in %)
    'paper_size': 9,                          # Page size - 9-A4
    'resolution': (600, 600),                 # Density / print quality
    'fit': (1, 1),                            # Parameters for filling out a report on sheets
    }

# Band data structure
REP_BAND = {
    'row': -1,          # Band row
    'col': -1,          # Band column
    'row_size': -1,     # Band size in rows
    'col_size': -1,     # Band size in columns
    }

# Cell formats
REP_FMT_NONE = None     # Do not set format
REP_FMT_STR = 'S'       # String/Text
REP_FMT_TIME = 'T'      # Time
REP_FMT_DATE = 'D'      # Date
REP_FMT_NUM = 'N'       # Number
REP_FMT_FLOAT = 'F'     # Float
REP_FMT_MISC = 'M'      # Abstract format
REP_FMT_EXCEL = 'X'     # Excel format

# Структура ячейки отчета
REP_CELL = {
    'merge_row': 0,         # Merge row number
    'merge_col': 0,         # Merge column number
    'left': 0,              # X coordinate
    'top': 0,               # Y coordinate
    'width': 10,            # Cell width
    'height': 10,           # Cell height
    'value': None,          # Cell text
    'font': None,           # Font
    'color': None,          # Color
    'border': None,         # Border
    'align': None,          # Alignment text
    'sum': None,            # Sum list
    'visible': True,        # Cell visible
    'exist': True,          # Exist cell?
    'num_format': None,     # Cell format
    }

# At each iteration, the current value of the sum is calculated
# as value=value+eval(formul)
REP_SUM = {
    'value': 0.0,   # Current sum value
    'formul': '0',  # Formula for calculating the amount
    }

# Color
REP_COLOR = {
    'text': (0, 0, 0),      # Foreground color
    'background': None,     # Background color
    }

# Borders
REP_BORDER_LEFT = 0
REP_BORDER_TOP = 1
REP_BORDER_BOTTOM = 2
REP_BORDER_RIGHT = 3
REP_BORDER_LINE = {
    'color': (0, 0, 0),
    'style': None,
    'weight': 0,
    }

# Line styles
REP_LINE_SOLID = 0
REP_LINE_SHORT_DASH = 1
REP_LINE_DOT_DASH = 2
REP_LINE_DOT = 3
REP_LINE_TRANSPARENT = None

# Alignment
REP_ALIGN = {
    'align_txt': (0, 0),
    'wrap_txt': False,
    }
REP_ALIGN_HORIZ = 0
REP_ALIGN_VERT = 1

REP_HORIZ_ALIGN_LEFT = 0
REP_HORIZ_ALIGN_CENTRE = 1
REP_HORIZ_ALIGN_RIGHT = 2

REP_VERT_ALIGN_TOP = 3
REP_VERT_ALIGN_CENTRE = 4
REP_VERT_ALIGN_BOTTOM = 5

# Group
REP_GRP = {
    'header': {},       # Group header
    'footer': {},       # Group footer
    'field': None,      # Group field name
    'old_rec': None,    # Old query table record
    }

DEFAULT_ENCODING = 'utf-8'


class iqReportGenerator(object):
    """
    Report generator class.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._report_name = None
        self._query_table = None
        # Query table record number
        self._query_table_rec_count = -1
        # Current query table record
        self._current_record = dict()
        # Report template
        self._template = None
        # Report template sheet
        self._template_sheet = None
        # Result report data
        self._report = None

        # Group list
        self._report_groups = list()

        # Current Y coordinate for redistributing cell coordinates
        self._cur_top = 0

        # Report name space
        self._variables = dict()

        # Cell attributes by default. If None, then attributes are not set
        self.default_cell_attributes = None

        self._style_library = None
        
        # Coordinate replacement of cell values
        self._coord_replacements = None

        # Cell format dictionary
        self._cell_format = dict()

    def generate(self, rep_template, query_table, name_space=None, coord_fill=None):
        """
        Generate report.

        :param rep_template: Report template data.
        :param query_table: Query table:
                {
                    '__name__': query table name,
                    '__fields__': [field names],
                    '__data__': [query table data],
                    '__sub__': {sub report data},
                }.
        :param name_space: Report name space.
                {
                    'variable name': variable value,
                }.
            This dictionary can be transmitted in the query table key __variables__.
        :param coord_fill: Coordinate filling in cell values.
            Format:
                {
                    (row, col): 'value',
                }.
            This dictionary can be transmitted in the query table key __coord_fill__.
        :return: Generated report data.
        """
        try:
            # Coordinate filling in cell values
            self._coord_replacements = coord_fill
            if query_table and '__coord_fill__' in query_table:
                if self._coord_replacements is None:
                    self._coord_replacements = dict()
                self._coord_replacements.update(query_table['__coord_fill__'])

            # Group list
            self._report_groups = list()

            # I. Define all bands in the template and amount cells
            if isinstance(rep_template, dict):
                # Template modify
                if 'template' in rep_template and rep_template['template']:
                    rep_template = self._modifyTemplate(rep_template, rep_template['template'])
                self._template = rep_template
            else:
                log_func.warning(u'Error report template type <%s>.' % type(rep_template))
                return None

            # Init report name
            if 'name' in query_table and query_table['name']:
                # If the query table is named, then this is the name of the finished report
                self._report_name = str(query_table['name'])
            elif 'name' in self._template:
                self._report_name = self._template['name']
            
            # Init name space
            self._variables = name_space
            if self._variables is None:
                self._variables = dict()
            self._variables.update(self._template['variables'])
            if query_table and '__variables__' in query_table:
                self._variables.update(query_table['__variables__'])
            if self._variables:
                log_func.debug(u'Report variables: %s' % str(list(self._variables.keys())))

            # Style library
            self._style_library = None
            if 'style_lib' in self._template:
                self._style_library = self._template['style_lib']

            self._template_sheet = self._template['sheet']
            self._template_sheet = self._initSumCells(self._template_sheet)

            # II. Init query table
            self._query_table = query_table
            # Determine the number of records in the query table
            self._query_table_rec_count = 0
            if self._query_table and '__data__' in self._query_table:
                self._query_table_rec_count = len(self._query_table['__data__'])

            # Init group band
            for grp in self._template['groups']:
                grp['old_rec'] = None

            time_start = time.time()
            log_func.info(u'Report <%s>. Generate start' % str_func.toUnicode(self._report_name))

            # III. Fill report
            # Create report
            self._report = copy.deepcopy(REPORT_TEMPLATE)
            self._report['name'] = self._report_name

            # Init variables
            field_idx = dict()      # Field indexes
            i = 0
            i_rec = 0
            # Iterate through the fields of a query table
            if self._query_table and '__fields__' in self._query_table:
                for cur_field in self._query_table['__fields__']:
                    field_idx[cur_field] = i
                    i += 1

            if self._query_table_rec_count:
                # Init current record
                rec = self._query_table['__data__'][i_rec]
                for field_name in field_idx.keys():
                    val = rec[field_idx[field_name]]
                    self._current_record[field_name] = val
                # Current record index
                self._current_record['sys_num_rec_idx'] = i_rec

            # Upper
            if self._template['upper']:
                self._genUpper(self._template['upper'])
            
            # Header
            self._genHeader(self._template['header'])

            # Main loop
            while i_rec < self._query_table_rec_count:
                # Group
                # Check group change and find the index of the most common change group
                i_grp_out = -1
                # Start generate flag
                start_gen = False
                for i_grp in range(len(self._template['groups'])):
                    grp = self._template['groups'][i_grp]
                    if grp['old_rec']:
                        # Check group note output condition
                        if self._current_record[grp['field']] != grp['old_rec'][grp['field']]:
                            i_grp_out = i_grp
                            break
                    else:
                        i_grp_out = 0
                        start_gen = True
                        break
                if i_grp_out != -1:
                    # Display notes
                    if start_gen is False:
                        for i_grp in range(len(self._template['groups']) - 1, i_grp_out - 1, -1):
                            grp = self._template['groups'][i_grp]
                            self._genGroupFooter(grp)
                    # Show headers
                    for i_grp in range(i_grp_out, len(self._template['groups'])):
                        grp = self._template['groups'][i_grp]
                        grp['old_rec'] = copy.deepcopy(self._current_record)
                        self._genGroupHeader(grp)
                    
                # Data area
                self._genDetail(self._template['detail'])

                # Increase the sum of summing cells
                self._sumIterate(self._template_sheet, self._current_record)

                # Next record
                i_rec += 1
                # Set current record
                if i_rec < self._query_table_rec_count:
                    rec = self._query_table['__data__'][i_rec]
                    for field_name in field_idx.keys():
                        val = rec[field_idx[field_name]]
                        self._current_record[field_name] = val
                    # Set current record index
                    self._current_record['sys_num_rec_idx'] = i_rec

            # Footer
            for i_grp in range(len(self._template['groups']) - 1, -1, -1):
                grp = self._template['groups'][i_grp]
                if grp['old_rec']:
                    self._genGroupFooter(grp)
                else:
                    break
            self._genFooter(self._template['footer'])
            # Under
            if self._template['under']:
                self._genUnder(self._template['under'])

            # Page setup
            self._report['page_setup'] = self._template['page_setup']

            log_func.info(u'Report <%s>. Generate end. Time: %d sec.' % (str_func.toUnicode(self._report_name),
                                                                         time.time()-time_start))

            return self._report
        except:
            log_func.fatal(u'Error report generate')
        return None

    def _genHeader(self, header):
        """
        Generate report header.

        :param header: Header band.
        :return: True/False.
        """
        try:
            # log_func.debug(u'Generate header')
            # We will add to the end of the report, therefore, determine the maximum line
            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(header['row'], header['row'] + header['row_size']):
                for col in range(header['col'], header['col'] + header['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1
                # Current coordinate Y
                self._cur_top += cur_height

            self._report['header'] = {'row': max_row,
                                   'col': header['col'],
                                   'row_size': i_row,
                                   'col_size': header['col_size'],
                                      }
            # Clear sums
            self._template_sheet = self._clearSum(self._template_sheet, 0, len(self._template_sheet))
            return True
        except:
            log_func.fatal(u'Error report header generate <%s>.' % str_func.toUnicode(self._report_name))
        return False
            
    def _genFooter(self, footer):
        """
        Generate report footer.

        :param footer: Footer band.
        :return: True/False.
        """
        try:
            if not footer:
                return True

            # We will add to the end of the report, therefore, determine the maximum line
            max_row = len(self._report['sheet'])
            i_row = 0       # Row band count
            cur_height = 0

            for row in range(footer['row'], footer['row'] + footer['row_size']):
                for col in range(footer['col'], footer['col'] + footer['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1
                # Current Y coordinate
                self._cur_top += cur_height

            self._report['footer'] = {'row': max_row,
                                   'col': footer['col'],
                                   'row_size': i_row,
                                   'col_size': footer['col_size'],
                                      }
            return True
        except:
            log_func.fatal(u'Error report footer generate <%s>.' % self._report_name)
        return False

    def _genDetail(self, detail):
        """
        Generate report detail.

        :param detail: Detail band.
        :return: True/False.
        """
        try:
            # We will add to the end of the report, therefore, determine the maximum line
            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(detail['row'], detail['row'] + detail['row_size']):
                for col in range(detail['col'], detail['col'] + detail['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1
                # Current Y coordinate
                self._cur_top += cur_height

            if self._report['detail'] == {}:
                self._report['detail'] = {'row': max_row,
                                       'col': detail['col'],
                                       'row_size': i_row,
                                       'col_size': detail['col_size'],
                                          }
            else:
                self._report['detail']['row_size'] += i_row

            return True
        except:
            log_func.fatal(u'Error report detail generate <%s>.' % self._report_name)
        return False

    def _genGroupHeader(self, rep_group):
        """
        Generate group header.

        :param rep_group: REP_GRP dictionary.
        :return: True/False.
        """
        try:
            band = rep_group['header']
            if not band:
                return False
            # We will add to the end of the report, therefore, determine the maximum line
            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(band['row'], band['row']+band['row_size']):
                for col in range(band['col'], band['col']+band['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1
                # Current Y coordinate
                self._cur_top += cur_height
            # Clear sums. There are no summary cells in the headers
            band = rep_group['footer']
            if band:
                self._template_sheet = self._clearSum(self._template_sheet, band['row'], band['row'] + band['row_size'])
            return True
        except:
            log_func.fatal(u'Error group header generate <%s> of report <%s>.' % (rep_group['field'], self._report_name))
        return False

    def _genGroupFooter(self, rep_group):
        """
        Generate group footer.

        :param rep_group: REP_GRP dictionary.
        :return: True/False.
        """
        try:
            band = rep_group['footer']
            if not band:
                return False

            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(band['row'], band['row']+band['row_size']):
                for col in range(band['col'], band['col']+band['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, rep_group['old_rec'])
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1
                # Current Y coordinate
                self._cur_top += cur_height
            return True
        except:
            log_func.fatal(u'Error group footer generate <%s> of report <%s>.' % (rep_group['field'], self._report_name))
        return False

    def _genUpper(self, upper):
        """
        Generate report upper.

        :param upper: Upper band.
        :return: True/False.
        """
        try:
            if 'row' not in upper or 'col' not in upper or \
               'row_size' not in upper or 'col_size' not in upper:
                self._report['upper'] = upper
                return True
                
            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(upper['row'], upper['row'] + upper['row_size']):
                for col in range(upper['col'], upper['col'] + upper['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1

                self._cur_top += cur_height

            self._report['upper'] = copy.deepcopy(upper)
            self._report['upper']['row'] = max_row
            self._report['upper']['row_size'] = i_row
            
            return True
        except:
            log_func.fatal(u'Error report upper generate <%s>' % self._report_name)
        return False

    def _genUnder(self, under):
        """
        Generate report under.

        :param under: Under band.
        :return: True/False.
        """
        try:
            if 'row' not in under or 'col' not in under or \
               'row_size' not in under or 'col_size' not in under:
                self._report['under'] = under
                return True
                
            max_row = len(self._report['sheet'])
            i_row = 0
            cur_height = 0

            for row in range(under['row'], under['row'] + under['row_size']):
                for col in range(under['col'], under['col'] + under['col_size']):
                    if self._template_sheet[row][col]:
                        self._genCell(self._template_sheet, row, col,
                                      self._report, max_row + i_row, col, self._current_record)
                        cur_height = self._template_sheet[row][col]['height']
                i_row += 1

                self._cur_top += cur_height

            self._report['under'] = copy.deepcopy(under)
            self._report['under']['row'] = max_row
            self._report['under']['row_size'] = i_row
            return True
        except:
            log_func.fatal(u'Error report under generate <%s>' % self._report_name)
        return False
            
    def _genSubReport(self, sub_rep_name, row):
        """
        Generate sub report.

        :param sub_rep_name: Sub report name.
        :param row: Rown number for insert sub report.
        :return: True/False.
        """
        try:
            if '__sub__' in self._query_table and self._query_table['__sub__']:
                if sub_rep_name in self._query_table['__sub__']:
                    # If there is sub-report data, then start the generation
                    report = self._query_table['__sub__'][sub_rep_name]['report']
                    if isinstance(report, str):
                        from . import report_template
                        template = report_template.iqlXMLSpreadSheetReportTemplate()

                        self._query_table['__sub__'][sub_rep_name]['report'] = template.read(report)

                    # Generate sub report
                    rep_gen = iqReportGenerator()
                    rep_result = rep_gen.generate(self._query_table['__sub__'][sub_rep_name]['report'],
                                                  self._query_table['__sub__'][sub_rep_name],
                                                  self._query_table['__sub__'][sub_rep_name]['__variables__'],
                                                  self._query_table['__sub__'][sub_rep_name]['__coord_fill__'])

                    self._report['sheet'] = self._report['sheet'][:row] + rep_result['sheet'] + self._report['sheet'][row:]
            return True
        except:
            log_func.fatal(u'Error sub report generate <%s> of report <%s>.' % (sub_rep_name, self._report_name))
        return False

    def _genCell(self, from_sheet, from_row, from_col, to_report, to_row, to_col, record):
        """
        Generate report cell.

        :param from_sheet: From report template sheet.
        :param from_row: Report template cell row.
        :param from_col: Report template cell column.
        :param to_report: To report.
        :param to_row: Result report cell row.
        :param to_col: Result report cell column.
        :param record: Current record.
        :return: True/False.
        """
        try:
            cell = copy.deepcopy(from_sheet[from_row][from_col])

            # Correct cell coordinate
            cell['top'] = self._cur_top
            # Generate cell value
            if self._coord_replacements and (to_row, to_col) in self._coord_replacements:
                # Coordinate replacements
                fill_val = str(self._coord_replacements[(to_row, to_col)])
                cell['value'] = self._genText({'value': fill_val}, record, to_row, to_col)
            else:
                # Transfer all cells from the template to the output report
                cell['value'] = self._genText(cell, record, to_row, to_col)

            # log_func.debug(u'Value <%s>' % text(new_cell['value']))

            # Set default cell atiributes
            # Filling some default cell attributes
            if self.default_cell_attributes and isinstance(self.default_cell_attributes, dict):
                cell.update(self.default_cell_attributes)
                
            # Set report cell description
            if len(to_report['sheet']) <= to_row:
                # Expand rows
                for i_row in range(len(to_report['sheet']), to_row + 1):
                    to_report['sheet'].append([])
            if len(to_report['sheet'][to_row]) <= to_col:
                # Expand columns
                for i_col in range(len(to_report['sheet'][to_row]), to_col + 1):
                    to_report['sheet'][to_row].append(None)

            if not cell['visible']:
                cell['width'] = 0
                cell['height'] = 0

            if cell.get('exist', True):
                to_report['sheet'][to_row][to_col] = cell
            return True
        except:
            log_func.fatal(u'Error report cell generate <%s>' % self._report_name)
        return False
        
    def _genText(self, cell, record=None, cell_row=None, cell_col=None):
        """
        Generate text.

        :param cell: Cell.
        :param record: Current record data.
            Format:
                { <field name> : <value>, ...}
        :param cell_row: Cell row number.
        :param cell_col: Cell column number.
        :return: Generated text value or None if error.
        """
        value = u''
        try:
            cell_val = cell['value']
            if cell_val is not None and not isinstance(cell_val, str):
                cell_val = str(cell_val)
            elif cell_val in (None, 'None'):
                cell_val = ''

            if cell_val not in self._cell_format:
                parsed_fmt = self.parseFunctionText(cell_val)
                self._cell_format[cell_val] = parsed_fmt
            else:
                parsed_fmt = self._cell_format[cell_val]

            # vvv For use records in generate cell text vvv
            query_table = self._query_table
            records = [{field_name: table_rec[i_field] for i_field, field_name in enumerate(query_table.get('__fields__', list()))} for table_rec in query_table.get('__data__', list())]
            variables = self._variables

            i_record = self._current_record.get('sys_num_rec_idx', 0)
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            func_str = list()   # Result value list
            i_sum = 0

            for cur_func in parsed_fmt['func']:

                # Function
                if re.search(REP_FUNC_PATT, cur_func):
                    value = self._execFunction(cur_func, locals(), globals())

                # Expression
                elif re.search(REP_EXP_PATT, cur_func):
                    value = self._execExpression(cur_func, locals(), globals())

                # Lambda
                elif re.search(REP_LAMBDA_PATT, cur_func):
                    value = self._execLambda(cur_func, locals(), globals())

                # Variable
                elif re.search(REP_VAR_PATT, cur_func):
                    value = self._getVariable(cur_func, locals(), globals())

                # Code block
                elif re.search(REP_EXEC_PATT, cur_func):
                    value = self._execCodeBlock(cur_func, locals(), globals())

                # System function
                elif re.search(REP_SYS_PATT, cur_func):
                    # Sum function
                    if cur_func[2:6].lower() == 'sum(':
                        if isinstance(cell['sum'][i_sum]['value'], datetime.timedelta):
                            value = dt_func.strfdelta(cell['sum'][i_sum]['value'])
                        else:
                            value = str(cell['sum'][i_sum]['value'])
                        i_sum += 1  # Next sum
                    # Average calculation function
                    elif cur_func[2:6].lower() == 'avg(':
                        if 'sys_num_rec_idx' not in record:
                            record['sys_num_rec_idx'] = 0
                        value = str(cell['sum'][i_sum]['value'] / (record['sys_num_rec_idx'] + 1))
                        i_sum += 1  # Next sum
                    elif cur_func[2:-2].lower() == 'n':
                        if 'sys_num_rec_idx' not in record:
                            record['sys_num_rec_idx'] = 0
                        sys_num_rec = record['sys_num_rec_idx']
                        value = str(sys_num_rec + 1)
                    else:
                        log_func.warning(u'Unknown system function <%s> in <%s>' % (str_func.toUnicode(cur_func),
                                                                                    self._report_name))
                        value = ''
                        
                # Style
                elif re.search(REP_STYLE_PATT, cur_func):
                    value = self._setStyle(cur_func, locals(), globals())

                # Field
                elif re.search(REP_FIELD_PATT, cur_func):
                    value = self._getFieldValue(cur_func, locals(), globals())

                # Sub report
                elif re.search(REP_SUBREPORT_PATT, cur_func):
                    value = self._genSubReportBlock(cur_func, locals(), globals())

                else:
                    log_func.warning(u'Unsupported function <%s>' % str(cur_func))

                # The cell value may also contain control codes
                value = self._genText({'value': value}, record)
                func_str.append(value)

            return self._setValueFormat(parsed_fmt['fmt'], func_str)
        except:
            log_func.fatal(u'Error cell text generate <%s> in <%s>.' % (str_func.toUnicode(cell['value']),
                                                                        self._report_name))
        return None

    def _execFunction(self, cur_func, locals, globals):
        """
        Execute external function.
        A function in a template can have 1 argument; this is a dictionary of entries.
        For example:
            [@package_name.module_name.function_name(record)@]

        :param cur_func: Call function text.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: The calculated value as a string or an empty string in case of an error.
        """
        value = u''
        func_body = cur_func[2:-2]
        try:
            value = str(self._execTextFunction(func_body, locals))
        except:
            log_func.fatal(u'Error execute function <%s>' % func_body)
        return value

    def _execExpression(self, cur_func, locals, globals):
        """
        Execute expression.
        For example:
            [#record["dt"].strftime("%B")#]

        :param cur_func: Expression text.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: The calculated value as a string or an empty string in case of an error.
        """
        value = u''
        exp_body = cur_func[2:-2]
        try:
            value = eval(exp_body, globals, locals)
        except:
            log_func.fatal(u'Error expression execute <%s>' % exp_body)
        log_func.debug(u'Execute expression <%s>. Value <%s>' % (exp_body, str(value)))
        return value

    def _execLambda(self, cur_func, locals, globals):
        """
        Execute lambda.
        Lambda haa 1 argument. It is record.
        For example:
            [~rec: rec['name']=='My name'~]

        :param cur_func: Call lambda text.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: The calculated value as a string or an empty string in case of an error.
        """
        value = u''
        lambda_body = cur_func[2:-2]
        lambda_func = None
        try:
            lambda_func = eval('lambda ' + cur_func[2:-2])
        except:
            log_func.fatal(u'Error lambda format <%s>' % lambda_body)

        if lambda_func:
            try:
                record = locals['record'] if 'record' in locals else globals.get('record', dict())
                value = str(lambda_func(record))
            except:
                log_func.fatal(u'Error lambda execute <%s>' % lambda_body)

        return value

    def _execCodeBlock(self, cur_func, locals, globals):
        """
        Execute code block.
        In the code block, new_cell and record objects are available.
        If you need to display information, then it must be displayed in the variable value.
        For example:
            [=value = '-' if record['name']=='My name' else ''=]

        :param cur_func: Code block text.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: The calculated value as a string or an empty string in case of an error.
        """
        value = u''
        exec_func = cur_func[2:-2].strip()

        try:
            exec(exec_func, globals, locals)
            # When the code block is executed, the value of the variable is located in the locals namespace.
            # Therefore, after executing the code block, it is necessary
            # to return the variable back to the current function
            value = locals.get('value', u'')
            log_func.debug(u'Execute code block <%s>. Value [%s]' % (exec_func, value))
        except:
            log_func.fatal(u'Error code block execute <%s>' % exec_func)
        return str(value)

    def _getVariable(self, cur_func, locals, globals):
        """
        Get variable from report name space.

        :param cur_func: Get variable text.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: The variable value as a string or an empty string in case of an error.
        """
        var_name = cur_func[2:-2]
        if var_name in self._variables:
            log_func.debug(u'Get variable <%s>' % var_name)
        else:
            log_func.warning(u'Variable <%s> not found in report name space' % var_name)
        value = str(self._variables.setdefault(var_name, u''))
        return value

    def _setStyle(self, cur_func, locals, globals):
        """
        Set style.

        :param cur_func: Style name.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: Empty string.
        """
        value = u''
        style_name = cur_func[2:-2]
        self._setStyleAttr(style_name)
        return value

    def _getFieldValue(self, cur_func, locals, globals):
        """
        Get field value of current record.

        :param cur_func: Field name.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: Value as string.
        """
        value = u''
        field_name = str((cur_func[2:-2]))
        record = locals['record'] if 'record' in locals else globals.get('record', dict())
        try:
            value = record[field_name]
        except KeyError:
            log_func.warning(u'In record (%s) field <%s> not found' % (str_func.toUnicode(record),
                                                                     str_func.toUnicode(field_name)))
        return value

    def _genSubReportBlock(self, cur_func, locals, globals):
        """
        Generate sub report.

        :param cur_func: Sub report name.
        :param locals: Local name space.
        :param globals: Global name space.
        :return: Empty string.
        """
        value = u''
        subreport_name = cur_func[2:-2]
        cell_row = locals['cell_row'] if 'cell_row' in locals else globals.get('cell_row', dict())
        self._genSubReport(subreport_name, cell_row)
        return value

    def _setValueFormat(self, fmt, data_list):
        """
        Set value format.

        :param fmt: Format.
        :param data_list: Format data.
        :return: A string that matches the format.
        """
        # Set format
        if data_list is []:
            if fmt:
                value = fmt
            else:
                return None
        elif data_list == [None] and fmt == '%s':
            return None

        # None value
        elif bool(None in data_list):
            data_lst = [{None: ''}.setdefault(val, val) for val in data_list]
            value = fmt % tuple(data_lst)
        else:
            value = fmt % tuple(data_list)
        return value
        
    def _setStyleAttr(self, style_name):
        """
        Set the default attributes of cells by style name from the style library.

        :param style_name: Style name.
        """
        if self._style_library and style_name in self._style_library:
            self.default_cell_attributes = self._style_library[style_name]
        else:
            self.default_cell_attributes = None
        
    def _getSum(self, formula):
        """
        Get sum by formula.

        :param formula: Formula.
        :return: Sum as string.
        """
        return '0'

    def _initSumCells(self, sheet):
        """
        Init cell sums.

        :param sheet: Report sheet data.
        :return: Returns a description of a sheet with a correct description of cells with sums.
             The error returns the old sheet description.
        """
        try:
            new_sheet = sheet

            for row in range(len(new_sheet)):
                for col in range(len(new_sheet[row])):
                    if new_sheet[row][col]:
                        new_sheet[row][col] = self._initSumCell(new_sheet[row][col])
            return new_sheet
        except:
            log_func.fatal(u'Error sum cells init <%s>.' % self._report_name)
        return sheet

    def _initSumCell(self, cell):
        """
        Init cell sum.

        :param cell: Cell data.
        :return: Returns the corrected cell description.
             In case of an error, returns the old description of the cell.
        """
        try:
            new_cell = cell

            cell_val = new_cell['value']
            if cell_val is not None and not isinstance(cell_val, str):
                cell_val = str(cell_val)
            parsed_fmt = self.parseFunctionText(cell_val, [REP_SYS_PATT])

            for cur_func in parsed_fmt['func']:
                # System function
                if re.search(REP_SYS_PATT, cur_func):
                    # Sum function
                    if cur_func[2:6].lower() in ('sum(', 'avg('):
                        # Init sum
                        if new_cell['sum'] is None:
                            new_cell['sum'] = []

                        new_cell['sum'].append(copy.deepcopy(REP_SUM))
                        new_cell['sum'][-1]['formul'] = cur_func[6:-3].replace(REP_SUM_FIELD_START, 'record[\'').replace(REP_SUM_FIELD_STOP, '\']')
            return new_cell
        except:
            log_func.fatal(u'Error init cell sum <%s>' % cell)
        return cell

    def _sumIterate(self, sheet, record):
        """
        Sum step.

        :param sheet: Report sheet data.
        :param record: Current record.
        :return: Returns a description of a sheet with a correct description of cells with sums.
             The error returns the old sheet description.
        """
        try:
            new_sheet = sheet

            # vvv For use records in generate cell text vvv
            query_table = self._query_table
            records = [{field_name: table_rec[i_field] for i_field, field_name in enumerate(query_table.get('__fields__', list()))} for table_rec in query_table.get('__data__', list())]
            variables = self._variables
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            for row in range(len(new_sheet)):
                for col in range(len(new_sheet[row])):

                    if new_sheet[row][col]:
                        if new_sheet[row][col]['sum'] is not None and new_sheet[row][col]['sum'] is not []:
                            for cur_sum in new_sheet[row][col]['sum']:
                                try:
                                    value = eval(cur_sum['formul'], globals(), locals())
                                except:
                                    log_func.fatal(u'Error SUM by formula <%s>.' % cur_sum)
                                    value = 0.0
                                try:
                                    if value is None:
                                        value = 0.0
                                    elif isinstance(value, str):
                                        value = float(value)
                                    if isinstance(cur_sum['value'], value.__class__):
                                        cur_sum['value'] += value
                                    else:
                                        cur_sum['value'] = value
                                except:
                                    log_func.fatal(u'Error SUM iteration: <%s> + <%s>' % (cur_sum['value'], value))

            return new_sheet
        except:
            log_func.fatal(u'Error step sum. Report <%s>' % self._report_name)
        return sheet

    def _clearSum(self, sheet, start_row, stop_row):
        """
        Clear sum.

        :param sheet: Report sheet data.
        :param start_row: Start row band for clear.
        :param stop_row: End row band for clear.
        :return: Returns a description of a sheet with a correct description of cells with sums.
            The error returns the old sheet description.
        """
        try:
            new_sheet = sheet

            for row in range(start_row, stop_row):
                for col in range(len(new_sheet[row])):
                    if new_sheet[row][col]:
                        if new_sheet[row][col]['sum'] is not None and new_sheet[row][col]['sum'] is not []:
                            for cur_sum in new_sheet[row][col]['sum']:
                                cur_sum['value'] = 0
            return new_sheet
        except:
            log_func.fatal(u'Error clear sum. Report <%s>.' % self._report_name)
        return sheet
        
    def getCurrentRecord(self):
        return self._current_record

    def parseFunctionText(self, text, patterns=ALL_PATTERNS):
        """
        Parse a text into format and executable code.

        :param text: Parse text.
        :param patterns: List of string patterns of tags to indicate the beginning and end of the functional.
        :return: Dictionary:
            {
            'fmt': The format of a line without lines of executable code is %s;
            'func': List of lines of executable code.
            }
            None if error.
        """
        try:
            # Init
            ret = {'fmt': '', 'func': []}

            if not text:
                return ret

            # Set pattern
            pattern = r''
            for cur_sep in patterns:
                pattern += cur_sep
                if cur_sep != patterns[-1]:
                    pattern += r'|'
                    
            # Parse
            parsed_str = [x for x in re.split(pattern, text) if x is not None]

            for i_parse in range(len(parsed_str)):
                func_find = False
                for cur_patt in patterns:
                    # Functional
                    if re.search(cur_patt, parsed_str[i_parse]):
                        ret['func'].append(parsed_str[i_parse])
                        # Set %s
                        ret['fmt'] += '%s'
                        func_find = True
                        break
                # String
                if func_find is False:
                    ret['fmt'] += parsed_str[i_parse]
            return ret
        except:
            log_func.fatal(u'Error text format <%s> in report <%s>.' % (text, self._report_name))
        return None

    def _execTextFunction(self, function, locals):
        """
        Execute function.
        """
        return exec_func.execTxtFunction(function)

    def _modifyTemplate(self, template, modify_expression=None):
        """
        Modify template before generating.

        :param template: Template structure.
        :param modify_expression: Modify expression.
        :return: Modified template structure or None if error.
        """
        if modify_expression is None:
            log_func.warning(u'Not define modify template expression')
            return None
        try:
            from . import report_template

            if modify_expression.startswith(report_template.PY_SIGNATURE):
                modify_expression = modify_expression.replace(report_template.PY_SIGNATURE, u'').strip()
            elif modify_expression.startswith(report_template.CODE_SIGNATURE):
                modify_expression = modify_expression.replace(report_template.CODE_SIGNATURE, u'').strip()

            TEMPLATE = report_template.iqReportTemplate()
            TEMPLATE.setTemplate(template)

            template = exec_func.execTxtFunction(function=modify_expression,
                                                 context=locals())
            return template
        except:
            log_func.fatal(u'Error modify template by expression:\n%s' % str(modify_expression))
        return None
