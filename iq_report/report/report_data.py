#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report data preparation module.

Data format:

data={
    '__fields__': [('field_name1',), ('field_name2',) ,...],    # Field data
    '__data__': [('value1', 'value2', ...), ...],               # Table data
    '__variables__': {
                    'variable_name1': 'variable_value1',
                    'variable_name2': 'variable_value2',
                    ...},   # Name space
    '__coord_fill__': {
                        (row1, column1): 'value1',
                        (row2, columns2): 'value2',
                       ...},    # Coordinate cell value replacements
    }

For example:
data={
        '__variables__':
            {
                'form_torg': 'Text1',
                'name_torg': 'Text2',

                'm_email': 'ss@mail.ru',
                'm_phone': '5-40-33',
            },
        '__fields__': (('n_lot',), ('predmet_lot',), ('cena_lot',)),
        '__data__': [('1', 'Picture', '123.45')],
    }

Values may multi-line. In this case, they are enclosed in triple quotation marks.
"""

import copy
import string

from iq.util import log_func

from iq.util import xml2dict

__version__ = (0, 0, 0, 1)

# Report data structure
REPORT_DATA = {
    '__fields__': list(),       # Field data
    '__data__': list(),         # Table data
    '__variables__': dict(),    # Name space
    '__coord_fill__': None,     # Coordinate cell value replacements
    '__sub__': dict(),          # Sub reports data
    }

# Sub report data structure
SUB_REPORT_DATA = {
    'report': '',           # Report template file or report description in REPORT_TEMPLATE
    'rep_data': dict(),     # REPORT_DATA
    }


class iqReportData(object):
    """
    Data preparation class for reports.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._rep_data = None
        
    def convert(self, src_data):
        """
        Converting from initial data presentation to report data presentation.

        :param src_data: Source data.
        """
        pass
        
    def get(self):
        """
        Get converted report data.
        """
        return self._rep_data


class iqXMLReportData(iqReportData):
    """
    A class for converting XML data to primary.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqReportData.__init__(self)
        
    def convert(self, xml_filename):
        """
        Converting from initial data presentation to report data presentation.

        :param xml_filename: Source xml filename.
        """
        xml_data = self.open(xml_filename)
        self._rep_data = self.data_convert(xml_data)
        return self._rep_data
    
    def open(self, xml_filename):
        """
        Open XML file.

        :param xml_filename: Report XML filename.
        """
        return xml2dict.XmlFile2Dict(xml_filename)

    def data_convert(self, src_rep_data):
        """
        Convert data from one view to another.
        """
        try:
            rep_data = copy.deepcopy(REPORT_DATA)

            workbook = src_rep_data['_children_'][0]
            # Styles
            styles = dict()
            styles_lst = [element for element in workbook['_children_'] if element['name'] == 'Styles']
            if styles_lst:
                styles = dict([(style['ID'], style) for style in styles_lst[0]['_children_']])

            worksheets = [element for element in workbook['_children_'] if element['name'] == 'Worksheet']
            # Variables
            variables = [element for element in workbook['_children_'] if element['name'] == 'Variables']
            #
            coord_values = [element for element in workbook['_children_'] if element['name'] == 'CoordFill']

            rep_worksheet = worksheets[0]
            rep_data_tab = rep_worksheet['_children_'][0]
            # Rows
            rep_data_rows = [element for element in rep_data_tab['_children_'] if element['name'] == 'Row']
            # Columns
            rep_data_cols = [element for element in rep_data_tab['_children_'] if element['name'] == 'Column']
            if not rep_data_cols:
                # If the columns are not defined in the data file,
                # then automatically generate a list of columns
                col_count = max([len(row['_children_']) for row in rep_data_rows])
                for col in range(col_count):
                    rep_data_cols.append({'name': 'Column'})

            rep_data['fields'] = self._getFields(rep_data_cols)
            rep_data['data'] = self._getData(rep_data_rows)
            rep_data['__variables__'] = self._getVariables(variables[0]['_children_'])
            rep_data['__coord_fill__'] = self._getCoordFill(coord_values[0]['_children_'])
            
            return rep_data
        except:
            log_func.fatal(u'Error report data convert')
        return None
        
    FIELD_NAMES = string.ascii_uppercase

    def _getFields(self, columns):
        """
        Get field descriptions. Fields are filled in columns.
        """
        try:
            fields = list()
            i_name = 0
            for col in columns:
                field = list()
                # Field name
                if 'Name' in col:
                    name = col['Name']
                else:
                    name = self.FIELD_NAMES[i_name]
                i_name += 1
                field.append(name)
                # Field type
                field.append('String')
                fields.append(tuple(field))
            return fields
        except:
            log_func.fatal(u'Error get fields data')
        return None
        
    def _getData(self, rows):
        """
        Get data.
        """
        try:
            data = list()
            i_rec = 0
            for row in rows:
                rec = list()
                
                # Empty cells
                if 'Index' in row:
                    idx = int(row['Index'])
                    if idx > i_rec:
                        data += [[]]*(idx-i_rec)

                for cell in row['_children_']:
                    cell_data = None
                    if 'value' in cell['_children_'][0]:
                        cell_data = cell['_children_'][0]['value']
                    rec.append(cell_data)
                    
                data.append(rec)
                i_rec = len(data)
                
            return data
        except:
            log_func.fatal(u'Error report data')
            return None
        
    def _getVariables(self, variables):
        """
        Name space variables.
        """
        try:
            variables = dict([(var['Name'], var['value']) for var in variables])
            return variables
        except:
            log_func.fatal(u'Error name space variables')
        return None

    def _getCoordFill(self, coord_values):
        """
        Coordinate replacements of cell values.
        """
        try:
            coord_fill = dict([((int(fill['Row']), int(fill['Col'])),
                                fill['value']) for fill in coord_values])
            return coord_fill
        except:
            log_func.fatal(u'Error determining coordinate report replacements')
        return None
