#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

from . import v_prototype
from . import v_worksheet
from . import v_style


__version__ = (0, 0, 0, 1)


class iqVWorkbook(v_prototype.iqVPrototype):
    """
    Workbook.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Workbook', 'children': []}
        # Dictionary of sheets by name
        self._worksheet_dict = {}

        self.Name = None
        
        # Managing styles
        self.styles = None

    def load(self, name):
        """
        Load workbook.
        """
        self.Name = os.path.abspath(name.strip())
        return self._parent.load(name)

    def save(self):
        """
        Save workbook.
        """
        return self._parent.save()

    def saveAs(self, name):
        """
        Save as...
        """
        self.Name = os.path.abspath(name.strip())
        return self._parent.saveAs(self.Name)
    
    def getWorksheetDict(self):
        """
        Dictionary of sheets by name.
        """
        return self._worksheet_dict

    def initWorksheetDict(self):
        """
        Initializing the dictionary of sheets.
        """
        self._worksheet_dict = dict([(worksheet['Name'], worksheet) for worksheet in \
                                    [element for element in self._attributes['children'] if element['name'] == 'Worksheet']])
        return self._worksheet_dict
        
    worksheet_dict = property(getWorksheetDict)

    def create(self):
        """
        Create workbook.
        """
        attrs = self._parent.getAttributes()
        # Since there is only one book in the XML file m. b.,
        # you can not add it here, but only replace the description of the book
        attrs['children'] = [self._attributes]
        return self._attributes

    def createWorksheet(self):
        """
        Create worksheet.
        """
        work_sheet = v_worksheet.iqVWorksheet(self)
        attrs = work_sheet.create()
        self.initWorksheetDict()
        return work_sheet

    def _findWorksheetAttrName(self, worksheets, name):
        """
        Find a sheet in the list by name.
        """
        work_sheet_attr = None

        if not isinstance(name, str):
            name = str(name)
            
        for sheet in worksheets:
            if not isinstance(sheet['Name'], str):
                sheet_name = str(sheet['Name'])
            else:
                sheet_name = sheet['Name']
            if sheet_name == name:
                work_sheet_attr = sheet
                break
        return work_sheet_attr
            
    def findWorksheet(self, name):
        """
        Search for a sheet by name.
        """
        work_sheet = None
        if name in self._worksheet_dict:
            work_sheet = v_worksheet.iqVWorksheet(self)
            work_sheet.setAttributes(self._worksheet_dict[name])
        else:
            # Try searching in the list
            find_worksheet = self._findWorksheetAttrName([element for element in self._attributes['children'] \
                                                          if element['name'] == 'Worksheet'], name)
            if find_worksheet:
                work_sheet = v_worksheet.iqVWorksheet(self)
                work_sheet.setAttributes(find_worksheet)
                # The dictionary was out of
                self.initWorksheetDict()
        return work_sheet

    def getWorksheetIdx(self, idx=0):
        """
        Get sheet by index.
        """    
        work_sheets = [element for element in self._attributes['children'] if element['name'] == 'Worksheet']
        try:
            worksheet_attr = work_sheets[idx]
            work_sheet = v_worksheet.iqVWorksheet(self)
            work_sheet.setAttributes(worksheet_attr)
            return work_sheet
        except:
            print('Error getWorksheetIdx')
            raise
    
    def createStyles(self):
        """
        Create styles.
        """
        styles = v_style.iqVStyles(self)
        attrs = styles.create()
        return styles

    def getStylesAttrs(self):
        """
        Get styles attributes.
        """
        styles = [element for element in self._attributes['children'] if element['name'] == 'Styles']
        if styles:
            return styles[0]
        return None

    def getStyles(self):
        """
        Get styles.
        """
        if self.styles:
            return self.styles
        
        styles_data = self.getStylesAttrs()
        if styles_data is None:
            self.styles = self.createStyles()
        else:
            self.styles = v_style.iqVStyles(self)
            self.styles.setAttributes(styles_data)
        return self.styles

    def getWorksheetNames(self):
        """
        List of sheet names in the book.
        """
        return [work_sheet['Name'] for work_sheet in self._attributes['children'] if work_sheet['name'] == 'Worksheet']
