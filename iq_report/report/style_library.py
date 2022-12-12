#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report style library module.
"""

import copy
import string

from iq.util import log_func
from iq.util import xml2dict

from . import report_template

__version__ = (0, 0, 2, 1)

# Style data structure
REP_STYLE = {
    'font': None,
    'color': None,
    # 'border': None,
    # 'align': None,
    # 'num_format': None,
    }


class iqReportStyleLibrary(report_template.iqReportTemplate):
    """
    Report style library class.
    """
    def __init__(self):
        """
        Constructor.
        """
        report_template.iqReportTemplate.__init__(self)
        self._style_lib = dict()
        
    def convert(self, src_data):
        """
        Convert XML style library data to report style library data.

        :param src_data: Source data.
        """
        pass
        
    def get(self):
        """
        Get converted report style library data.
        """
        return self._style_lib


class iqXMLReportStyleLibrary(iqReportStyleLibrary):
    """
    XML report style library class.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqReportStyleLibrary.__init__(self)

    def open(self, xml_filename):
        """
        Open XML file.

        :param xml_filename: XML report style library filename.
        """
        return xml2dict.XmlFile2Dict(xml_filename)

    def convert(self, xml_filename):
        """
        Convert from XML file to report style library.

        :param xml_filename: XML report style library filename.
        """
        xml_data = self.open(xml_filename)
        self._style_lib = self.covertData(xml_data)
        return self._style_lib

    def covertData(self, data):
        """
        Convert from XML file to report style library.
        """
        try:
            # Get workbook
            workbook = data['_children_'][0]
            # Styles as dictionary
            styles = dict()
            styles_lst = [element for element in workbook['_children_'] if element['name'] == 'Styles']
            if styles_lst:
                styles = {style['ID']: style for style in styles_lst[0]['_children_']}

            worksheets = [element for element in workbook['_children_'] if element['name'] == 'Worksheet']

            # Get worksheet
            rep_worksheet = worksheets[0]
            rep_data_tab = rep_worksheet['_children_'][0]
            # Row data list
            rep_data_rows = [element for element in rep_data_tab['_children_'] if element['name'] == 'Row']

            style_lib = self._getStyles(rep_data_rows, styles)
            return style_lib
        except:
            log_func.fatal(u'Error convert report style library data')
        return None

    # Allowed characters in style tag names
    LATIN_CHARSET = string.ascii_uppercase+string.ascii_lowercase + string.digits + '_'

    def _isStyleTag(self, value):
        """
        Is tag as style tag?

        :param value: Cell value as string.
        :return: True/False.
        """
        for symbol in value:
            if symbol not in self.LATIN_CHARSET:
                return False
        return True

    def _getStyles(self, rows, styles):
        """
        Get styles dictionary.

        :param rows: Row list in XML.
        :param styles: Style dictionary in XML.
        """
        new_styles = dict()
        for row in rows:
            for cell in row['_children_']:
                # Get value
                value = cell['_children_'][0]['value']

                if value and isinstance(value, str):
                    if self._isStyleTag(value):
                        style_id = cell['StyleID']
                        new_styles[value] = self._getStyle(style_id, styles)
        return new_styles
                            
    def _getStyle(self, style_id, styles):
        """
        Get style data by ID.

        :param style_id: Style ID in XML data.
        :param styles: Style dictionary in XML.
        """
        style = copy.deepcopy(REP_STYLE)
        
        if style_id in styles:
            style['font'] = self._getFontStyle(styles[style_id])
            style['color'] = self._getColorStyle(styles[style_id])
            # style['border']=self._getBordersStyle(styles[style_id])
            # style['align']=self._getAlignStyle(styles[style_id])
            # style['num_format']=self._getNumberFormatStyle(styles[style_id])
        return style
