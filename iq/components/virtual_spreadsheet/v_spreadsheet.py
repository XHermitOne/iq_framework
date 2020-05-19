#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import copy

from . import v_prototype
from . import v_workbook
from . import v_ods

from ...util import xml2dict
from ...util import dict2xml
from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqVSpreadsheet(v_prototype.iqVPrototype):
    """
    A virtual representation of the Excel object model.
    """
    def __init__(self, encoding='utf-8', *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, None, *args, **kwargs)

        # Active workbook Data
        self._data = {'name': 'Excel', '__children__': []}

        # Dictionary of open books
        self._workbooks = {}

        # Filename
        self.SpreadsheetFileName = None

        self.encoding = encoding

        # Internal clipboard for sheet operations
        self._worksheet_clipboard = {}
        # Sign that after insertion the old sheet needs to be deleted
        self._is_cut_worksheet = False
        # List of group operations with sheets
        self._worksheet_list_clipboard = []

    def _regWorkbook(self, xml_filename=None, workbook_data=None):
        """
        Register book as open.
        """
        self._workbooks[xml_filename] = workbook_data

    def _unregWorkbook(self, xml_filename=None):
        """
        Remove book from registered.
        """
        if xml_filename in self._workbooks:
            del self._workbooks[xml_filename]

    def _reregWorkbook(self, old_xml_filename=None, new_xml_filename=None):
        """
        Register a registered book with a new name.
        """
        if old_xml_filename in self._workbooks:
            self._workbooks[new_xml_filename] = self._workbooks[old_xml_filename]
            del self._workbooks[old_xml_filename]

    def createNew(self):
        """
        Create new.
        """
        self._data = {'name': 'Excel', '__children__': []}

        self.SpreadsheetFileName = None

        self._regWorkbook(self.SpreadsheetFileName, self._data)

    def getFileName(self):
        """
        File name.
        """
        return self.SpreadsheetFileName
    
    def convertXLS2XML(self, xls_filename=None):
        """
        Convert XLS file to XML.
        Conversion will occur only when Excel is installed.

        :return: True - was converted normally, False - error.
        """
        try:
            import win32com.client
            xlXMLSpreadsheet = 46   # 0x2e # from enum XlFileFormat
        except ImportError:
            print('import win32com error!')
            return False
        try:
            excel_app = win32com.client.Dispatch('Excel.Application')
            excel_app.Workbooks.Close()
            wrkbook = excel_app.Workbooks.Open(xls_filename)
            xml_file_name = os.path.splitext(xls_filename)[0] + '.xml'
            wrkbook.saveAs(xml_file_name,
                           FileFormat=xlXMLSpreadsheet,
                           ReadOnlyRecommended=False,
                           CreateBackup=False)
            excel_app.Workbooks.Close()
            return True
        except:
            log_func.fatal('convertXLS2XML function')
        return False

    def loadXML(self, xml_filename=None):
        """
        Load from XML file.
        """
        if xml_filename:
            self.SpreadsheetFileName = os.path.abspath(xml_filename)
            xls_file_name = os.path.splitext(self.SpreadsheetFileName)[0]+'.xls'
            if not os.path.exists(self.SpreadsheetFileName) and os.path.exists(xls_file_name):
                if not self.convertXLS2XML(xls_file_name):
                    return None
        self._data = xml2dict.XmlFile2Dict(self.SpreadsheetFileName, encoding=self.encoding)

        # Register an open book
        self._regWorkbook(self.SpreadsheetFileName, self._data)

        return self._data

    def loadODS(self, ods_filename=None):
        """
        Load from ODS file.

        :param ods_filename: ODS filename.
        """
        if ods_filename:
            self.SpreadsheetFileName = os.path.abspath(ods_filename)
        
            ods = v_ods.iqODS()
            self._data = ods.load(ods_filename)
        
            # Register an open book
            self._regWorkbook(self.SpreadsheetFileName, self._data)
        
        return self._data
        
    def load(self, filename):
        """
        Load data from a file. File type is determined by extension.

        :param filename: File name.
        """
        if filename:
            filename = os.path.abspath(filename)
        else:
            filename = os.path.abspath(self.SpreadsheetFileName)
            
        if (not filename) or (not os.path.exists(filename)):
            log_func.error(u'Unable to load file <%s>' % filename)
            return None
        
        ext = os.path.splitext(filename)[1]
        if ext in ('.ODS', '.ods', '.Ods'):
            return self.loadODS(filename)
        elif ext in ('.XML', '.xml', '.Xml'):
            return self.loadXML(filename)
        else:
            log_func.error(u'Unsupported file type <%s>' % ext)
        return None
            
    def save(self):
        """
        Save data.
        """
        return self.saveAs()
        
    def saveAs(self, filename=None):
        """
        Save data to file.

        :param filename: Destination file name.
        """
        if not filename:
            filename = self.SpreadsheetFileName
        
        ext = os.path.splitext(filename)[1]
        if ext in ('.ODS', '.ods', '.Ods'):
            return self.saveAsODS(filename)
        elif ext in ('.XML', '.xml', '.Xml'):
            return self.saveAsXML(filename)
        else:
            log_func.error(u'Unsupported file type <%s>' % ext)
        return None
        
    def saveAsODS(self, ods_filename=None):
        """
        Save to ODS file.

        :param ods_filename: ODS filename.
        """
        if ods_filename is None:
            ods_filename = os.path.splitext(self.SpreadsheetFileName)[0] + '.ods'
            
        if ods_filename:
            self._reregWorkbook(self.SpreadsheetFileName, ods_filename.strip())
            self.SpreadsheetFileName = ods_filename.strip()
            
        if os.path.exists(ods_filename):
            # If the file exists, delete it
            os.remove(ods_filename)
            
        ods = v_ods.iqODS()
        return ods.save(ods_filename, self._data)

    def saveODS(self):
        """
        Save ODS file.
        """
        return self.saveAsODS()
        
    def saveXML(self):
        """
        Save XML file.
        """
        return self.saveAsXML()

    def saveAsXML(self, xml_filename=None):
        """
        Save XML file.
        """
        if xml_filename:
            self._reregWorkbook(self.SpreadsheetFileName, xml_filename.strip())
            self.SpreadsheetFileName = xml_filename.strip()

        work_book = self.getActiveWorkbook()

        # Set ExpandedRowCount and ExpandedColumnCount if necessary
        work_sheet_names = work_book.getWorksheetNames()
        for name in work_sheet_names:
            work_sheet = work_book.findWorksheet(name)
            if work_sheet:
                tab = work_sheet.getTable()
                tab.setExpandedRowCount()
                tab.setExpandedColCount()

        # Delete unused styles
        styles = work_book.getStyles()
        styles.clearUnUsedStyles()

        save_data = self.getData()['__children__'][0]
        try:
            return dict2xml.dict2XmlssFile(save_data, self.SpreadsheetFileName, encoding=self.encoding)
        except IOError:
            return self.saveCopyXml(save_data, self.SpreadsheetFileName)

    def saveCopyXml(self, save_data, xml_filename, n_copy=0):
        """
        Saving the XML file, if not, then save a copy.

        :param save_data: Saved data.
        :param xml_filename: XML filename.
        :param n_copy: Copy number.
        """
        try:
            xml_copy_name = os.path.splitext(xml_filename)[0] + '_' + str(n_copy) + '.xml'
            return dict2xml.dict2XmlssFile(save_data, xml_copy_name, encoding=self.encoding)
        except IOError:
            log_func.warning(u'XML copy <%s> <%d>' % (xml_filename, n_copy + 1))
            return self.saveCopyXml(save_data, xml_filename, n_copy + 1)

    def getData(self):
        """
        Get data.
        """
        return self._data

    def getAttributes(self):
        """
        Get attributes.
        """
        return self._data

    def createWorkbook(self):
        """
        Create workbook.
        """
        if self._data is None:
            self._data = {'name': 'Excel', '__children__': []}
            # Register an open book
            self._regWorkbook(self.SpreadsheetFileName, self._data)
        work_book = v_workbook.iqVWorkbook(self)
        attrs = work_book.create()
        return work_book

    def getWorkbook(self, name=None):
        """
        Get workbook.

        :param name: Workbook name - XML file name.
        """
        if name is None:
            if self._data['__children__']:
                attrs = [element for element in self._data['__children__'] if element['name'] == 'Workbook']
                if attrs:
                    work_book = v_workbook.iqVWorkbook(self)
                    work_book.setAttributes(attrs[0])
                    return work_book
            else:
                return self.createWorkbook()
        else:
            self.load(name)
            work_book = self.getWorkbook()
            work_book.Name = name
            return work_book
        return None

    def getActiveWorkbook(self):
        """
        Get active workbook.
        """
        return self.getWorkbook()

    def openWorkbook(self, xml_filename=None):
        """
        Open workbook.
        Workbook - XML file of Spreadsheet table.
        """
        return self.load(xml_filename)

    def closeWorkbook(self, xml_filename=None):
        """
        Close workbook.

        :param xml_filename: Specifies the XML file of the book to be closed.
            If not specified, the current book closes.
        """
        xml_file_name = xml_filename
        if xml_file_name is None:
            xml_file_name = self.SpreadsheetFileName

        self._unregWorkbook(xml_file_name)

        # If the active book is closed, then change the active book
        if self.SpreadsheetFileName.lower() == xml_file_name.lower():
            if self._workbooks:
                # Replace the active book with any of the registered
                reg_workbook_xml_file_name = self._workbooks.keys()[0]
                self.activeWorkbook(reg_workbook_xml_file_name)
            else:
                # If there are no more books registered,
                # then create a new book
                self.createNew()

    def activeWorkbook(self, xml_filename=None):
        """
        Make a book active.
        """
        xml_file_name = u''
        try:
            xml_file_name = os.path.abspath(xml_filename)
            if os.path.exists(xml_file_name):
                self.SpreadsheetFileName = xml_file_name
                self._data = self._workbooks[xml_file_name]
            else:
                log_func.error(u'SpreadSheet. File <%s> not found' % xml_file_name)

        except KeyError:
            log_func.error(u'Workbook <%s> not registred in <%s>' % (xml_file_name, self._workbooks.keys()))
            raise

    def _findWorkbookData(self, xml_filename=None):
        """
        Find data for the specified book.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        """
        if xml_filename is None:
            workbook_data = self._data
        else:
            xml_file_name = os.path.abspath(xml_filename)
            try:
                workbook_data = self._workbooks[xml_file_name]
            except KeyError:
                log_func.error(u'Workbook <%s> not registered in <%s>' % (xml_file_name, self._workbooks.keys()))
                raise
        workbook_data = [data for data in workbook_data['__children__'] if 'name' in data and data['name'] == 'Workbook']
        if workbook_data:
            workbook_data = workbook_data[0]
        else:
            log_func.error(u'Workbook not defined in <%s>' % xml_filename)
            return None
        return workbook_data

    def _findWorksheetData(self, xml_filename=None, sheet_name=None):
        """
        Find the data of the specified sheet.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: Имя листа в указанной книге.
            If not specified, then the first sheet is meant.
        """
        workbook_data = self._findWorkbookData(xml_filename)
        if workbook_data is None:
            return None

        worksheet_data = [data for data in workbook_data['__children__'] if data['name'] == 'Worksheet']
        if worksheet_data:
            if sheet_name is None:
                worksheet_data = worksheet_data[0]
            else:
                worksheet_data = [data for data in worksheet_data if data['Name'] == sheet_name]
                if worksheet_data:
                    worksheet_data = worksheet_data[0]
                else:
                    log_func.error(u'Workbook <%s> not found' % sheet_name)
                    return None
        else:
            log_func.error(u'Workbook not defined in <%s>' % xml_filename)
            return None
        return worksheet_data

    def _getWorkbookStyles(self, xml_filename=None):
        """
        Style data for the specified book.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        """
        workbook_data = self._findWorkbookData(xml_filename)
        if workbook_data is None:
            return None

        styles_data = [data for data in workbook_data['__children__'] if data['name'] == 'Styles']
        if not styles_data:
            log_func.warning(u'Styles not defined in workbook <%s>' % xml_filename)
            return None
        else:
            styles_data = styles_data[0]
        return styles_data

    def _genNewStyleID(self, style_id, reg_styles_id):
        """
        Generate style id when working with sheets.

        :param style_id: Style identifier.
        :param reg_styles_id: List of identifiers already registered styles.
        """
        i = 0
        new_style_id = style_id
        while new_style_id in reg_styles_id:
            new_style_id = style_id+str(i)
            i += 1
        return new_style_id

    def copyWorksheet(self, xml_filename=None, sheet_name=None):
        """
        Положить в внутренний буфер обмена копию листа.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: The name of the sheet in the specified book.
            If not specified, then the first sheet is meant.
        """
        xml_filename = self._unificXMLFileName(xml_filename)

        sheet_name = self._unicode2str(sheet_name)

        worksheet_data = self._findWorksheetData(xml_filename, sheet_name)
        styles_data = self._getWorkbookStyles(xml_filename)
        if worksheet_data:
            # Make copy
            self._worksheet_clipboard = dict()
            self._worksheet_clipboard[(xml_filename, sheet_name)] = copy.deepcopy(worksheet_data)
            self._worksheet_clipboard['styles'] = copy.deepcopy(styles_data)
            self._is_cut_worksheet = False
            return self._worksheet_clipboard[(xml_filename, sheet_name)]
        return None

    def cutWorksheet(self, xml_filename=None, sheet_name=None):
        """
        Cut sheet.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: The name of the sheet in the specified book.
            If not specified, then the first sheet is meant.
        """
        xml_filename = self._unificXMLFileName(xml_filename)

        sheet_name = self._unicode2str(sheet_name)

        worksheet_data = self._findWorksheetData(xml_filename, sheet_name)
        styles_data = self._getWorkbookStyles(xml_filename)
        if worksheet_data:
            # Make copy
            self._worksheet_clipboard = dict()
            self._worksheet_clipboard[(xml_filename, sheet_name)] = copy.deepcopy(worksheet_data)
            self._worksheet_clipboard['styles'] = copy.deepcopy(styles_data)
            self._is_cut_worksheet = True
            return self._worksheet_clipboard[[(xml_filename, sheet_name)]]
        return None

    def delWorksheet(self, xml_filename=None, sheet_name=None):
        """
        Delete the sheet permanently.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: The name of the sheet in the specified book.
            If not specified, then the first sheet is meant.
        :return: True/False.
        """
        xml_filename = self._unificXMLFileName(xml_filename)

        sheet_name = self._unicode2str(sheet_name)

        workbook_data = self._findWorkbookData(xml_filename)
        if workbook_data is None:
            log_func.error(u'Workbook <%s> not found' % xml_filename)
            return False
        # Find and delete sheet
        result = False
        for i, data in enumerate(workbook_data['__children__']):
            if data['name'] == 'Worksheet':
                if sheet_name is None:
                    # If the sheet name is not defined, then simply delete the first leaf
                    del workbook_data['__children__'][i]
                    result = True
                    break
                else:
                    # If a sheet name is specified, then check for matching sheet names
                    if data['Name'] == sheet_name:
                        log_func.info(u'Delete worksheet <%s>' % sheet_name)
                        del workbook_data['__children__'][i]
                        result = True
                        break
        return result

    def delWithoutWorksheet(self, xml_filename=None, sheet_name_=None):
        """
        Delete irrevocably all sheets from the book except the specified.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: The name of the sheet in the specified book.
            If not specified, then the first sheet is meant.
        :return: True/False.
        """
        sheet_name_ = self._unicode2str(sheet_name_)

        workbook_data = self._findWorkbookData(xml_filename)
        if workbook_data is None:
            return False

        not_del_first = True
        for i, data in enumerate(workbook_data['__children__']):
            if data['name'] == 'Worksheet':
                if sheet_name_ is None:
                    # If the sheet name is not defined, then simply delete the first leaf
                    if not not_del_first:
                        del workbook_data['__children__'][i]
                    not_del_first = False
                else:
                    # If a sheet name is specified, then check for matching sheet names
                    if data['Name'] != sheet_name_:
                        del workbook_data['__children__'][i]

        return True

    def delSelectedWorksheetList(self, xml_filename=None):
        """
        Delete selected sheets.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        """
        xml_filename = self._unificXMLFileName(xml_filename)

        if type(self._worksheet_list_clipboard) in (list, tuple):
            for i, worksheet_src in enumerate(self._worksheet_list_clipboard):
                workbook_name, worksheet_name = worksheet_src

                if xml_filename == workbook_name:
                    self.delWorksheet(workbook_name, worksheet_name)

        # After the option, clear the list of selected sheets
        self._worksheet_list_clipboard = []

    def delWithoutSelectedWorksheetList(self, xml_filename=None):
        """
        Delete all unselected sheets from the book.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        """
        xml_filename = self._unificXMLFileName(xml_filename)

        not_deleted_worksheet_names = [worksheet_src[1] for worksheet_src in self._worksheet_list_clipboard if xml_filename == worksheet_src[0]]

        # Define the data of the book from which to be deleted
        workbook_name = xml_filename
        workbook_data = self._findWorkbookData(workbook_name)
        if workbook_data is None:
            return None
        # List of book sheet names
        worksheet_name_list = [data['Name'] for data in workbook_data['__children__'] if data['name'] == 'Worksheet']

        if type(self._worksheet_list_clipboard) in (list, tuple):
            for i, worksheet_name in enumerate(worksheet_name_list):
                if worksheet_name not in not_deleted_worksheet_names:
                    self.delWorksheet(workbook_name,worksheet_name)

    def _pasteStyleIntoWorkbook(self, style, workbook_data):
        """
        Paste the style in the finished structure of the book.

        :param style: Paste style data.
        :param workbook_data: Book data.
        :return: Returns the style identifier or None
            in case of an error.
        """
        try:
            workbook_styles = [data for data in workbook_data['__children__'] if data['name'] == 'Styles'][0]
            if style not in workbook_styles['__children__']:
                workbook_styles_id = [data['ID'] for data in workbook_styles['__children__'] if data['name'] == 'Style']

                new_style_id = self._genNewStyleID(style['ID'], workbook_styles_id)
                style['ID'] = new_style_id
                workbook_styles['__children__'].append(style)
                return new_style_id
            else:
                # Exactly such a style already exists and therefore you do not need to add it
                return style['ID']
        except:
            log_func.error(u'Error paste style')
            raise
        return None

    def _replaceStyleID(self, data, old_style_id, new_style_id):
        """
        Replace style identifiers in inserted data.

        :param data: Data to insert.
        :param old_style_id: Old style identifier.
        :param new_style_id: New style identifier.
        :return: Returns data with a corrected style.
        """
        if old_style_id == new_style_id:
            # Identifiers are mask - no replacement required
            return data
        if 'StyleID' in data and data['StyleID'] == old_style_id:
            data['StyleID'] = new_style_id
        if '__children__' in data and data['__children__']:
            for i, child in enumerate(data['__children__']):
                data['__children__'][i] = self._replaceStyleID(child, old_style_id, new_style_id)
        return data

    def _genNewWorksheetName(self, worksheet_name, worksheet_names):
        """
        Choose a name for the sheet so that it does not overlap with existing ones
        """
        new_sheet_name = worksheet_name

        i = 1
        while new_sheet_name in worksheet_names:
            new_sheet_name = worksheet_name+'_'+str(i)
            i += 1
        return new_sheet_name

    def pasteWorksheet(self, xml_filename=None, is_cut=None, new_worksheet_name=None):
        """
        Paste the sheet from the clipboard into the specified book.

        :param xml_filename: The name of the XML file of the book to insert.
            If not defined, it means an active book.
        :param is_cut: A sign that the old sheet needs to be deleted.
            If None, then take the system attribute.
        :param new_worksheet_name: The new sheet name.
        :return: True/False.
        """
        xml_filename = self._unificXMLFileName(xml_filename)
        new_worksheet_name = self._unicode2str(new_worksheet_name)

        # If there is nothing in the clipboard, then do not paste
        if not self._worksheet_clipboard:
            return False

        # Identify the book in which to insert the sheet
        workbook_data = self._findWorkbookData(xml_filename)
        if workbook_data is None:
            return False

        if is_cut is None:
            is_cut = self._is_cut_worksheet
        # Define a new sheet name
        sheet_names = [data['Name'] for data in workbook_data['__children__'] if data['name'] == 'Worksheet']
        worksheet_source, worksheet_data = [(key, value) for key, value in self._worksheet_clipboard.items()
                                            if isinstance(key, tuple)][0]
        if new_worksheet_name:
            sheet_name = new_worksheet_name
        else:
            sheet_name = worksheet_data['Name']
        worksheet_data['Name'] = self._genNewWorksheetName(sheet_name, sheet_names)
        # Paste styles
        if 'styles' in self._worksheet_clipboard:
            for i, style in enumerate(self._worksheet_clipboard['styles']['__children__']):
                old_style_id = style['ID']
                new_style_id = self._pasteStyleIntoWorkbook(style, workbook_data)
                worksheet_data = self._replaceStyleID(worksheet_data, old_style_id, new_style_id)
        # Insert data
        workbook_data['__children__'].append(worksheet_data)

        # If necessary, delete the old sheet.
        if is_cut:
            self.delWorksheet(*worksheet_source)
        # Clear clipboard
        self._worksheet_clipboard = {}
        return True

    def moveWorksheet(self, old_xml_filename=None, sheet_name=None, new_xml_filename=None):
        """
        Move a sheet from one book to another.
        """
        self.cutWorksheet(old_xml_filename, sheet_name)
        return self.pasteWorksheet(new_xml_filename)

    def selectWorksheet(self, xml_filename=None, sheet_name=None):
        """
        Select a sheet for group operations with sheets.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param sheet_name: The name of the sheet in the specified book.
            If not specified, then the first sheet is meant.
        """
        xml_filename = self._unificXMLFileName(xml_filename)
        sheet_name = self._unicode2str(sheet_name)

        self._worksheet_list_clipboard.append((xml_filename, sheet_name))

    def getLastSelectedWorksheet(self):
        """
        The last selected sheet.
        """
        if self._worksheet_list_clipboard:
            worksheet_src = self._worksheet_list_clipboard[-1]
            self.activeWorkbook(worksheet_src[0])
            active_workbook = self.getActiveWorkbook()
            if active_workbook:
                return active_workbook.findWorksheet(worksheet_src[1])
        return None

    def copyWorksheetListTo(self, xml_filename=None, new_worksheet_names=None):
        """
        Copy a list of selected sheets to a book.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param new_worksheet_names: List of new sheet names.
        """
        if type(self._worksheet_list_clipboard) in (list, tuple):
            for i, worksheet_src in enumerate(self._worksheet_list_clipboard):
                workbook_name, worksheet_name = worksheet_src
                new_worksheet_name = None
                if new_worksheet_names:
                    if i < len(new_worksheet_names):
                        new_worksheet_name = new_worksheet_names[i]
                self.copyWorksheet(workbook_name, worksheet_name)
                self.pasteWorksheet(xml_filename, new_worksheet_name=new_worksheet_name)

        # After the operation, clear the list of selected sheets
        self._worksheet_list_clipboard = []

    def moveWorksheetListTo(self, xml_filename=None, new_worksheet_names=None):
        """
        Transfer the list of selected sheets to the book.

        :param xml_filename: Workbook XML file name.
            If not defined, it means an active book.
        :param new_worksheet_names: List of new sheet names.
        """
        if type(self._worksheet_list_clipboard) in (list, tuple):
            for i, worksheet_src in enumerate(self._worksheet_list_clipboard):
                workbook_name, worksheet_name = worksheet_src
                new_worksheet_name = None
                if new_worksheet_names:
                    if i < len(new_worksheet_names):
                        new_worksheet_name = new_worksheet_names[i]
                self.cutWorksheet(workbook_name, worksheet_name)
                self.pasteWorksheet(xml_filename, new_worksheet_name=new_worksheet_name)

        # After the operation, clear the list of selected sheets
        self._worksheet_list_clipboard = []

    def _unicode2str(self, UnicodeStr_):
        """
        Convert unicode string to regular string.
        """
        # if isinstance(UnicodeStr_, unicode):
        #    return UnicodeStr_.encode(self.encoding)
        return UnicodeStr_

    def _unificXMLFileName(self, xml_filename):
        """
        Bring in the name of the XML file name of the book.
        If no name is specified, the file name of the active workbook is taken.
        As the internal name of the book XML file
        The ABSOLUTE PATH to the file is taken.
        """
        if xml_filename:
            xml_filename = os.path.abspath(xml_filename)
        else:
            xml_filename = self.SpreadsheetFileName
        return xml_filename

    def mergeCell(self, sheet_name, row, column, merge_down, merge_across_, xml_filename=None):
        """
        Merge cells.
        """
        if xml_filename is not None:
            self.activeWorkbook(xml_filename)
        work_book = self.getActiveWorkbook()
        work_sheet = work_book.findWorksheet(sheet_name)
        table = work_sheet.getTable()
        cell = table.getCell(row, column)
        return cell.setMerge(merge_across_, merge_down)

    def setCellValue(self, sheet_name, row, column, value, xml_filename=None):
        """
        Set value to cell.
        """
        if xml_filename is not None:
            self.activeWorkbook(xml_filename)
        work_book = self.getActiveWorkbook()
        work_sheet = work_book.findWorksheet(sheet_name)
        table = work_sheet.getTable()
        cell = table.getCell(row, column)
        return cell.setValue(value)

    def setCellStyle(self, sheet_name, row, col, alignment=None,
                     left_border=None, right_border=None, top_border=None, bottom_border=None,
                     font=None, interior=None, number_format=None, xml_filename=None):
        """
        Set cell style.
        """
        if xml_filename is not None:
            self.activeWorkbook(xml_filename)
        work_book = self.getActiveWorkbook()
        work_sheet = work_book.findWorksheet(sheet_name)
        table = work_sheet.getTable()
        cell = table.getCell(row, col)
        borders = {'name': 'Borders', '__children__': []}
        if left_border:
            left_border['Position'] = 'Left'
            borders['__children__'].append(left_border)
        if right_border:
            right_border['Position'] = 'Right'
            borders['__children__'].append(right_border)
        if top_border:
            top_border['Position'] = 'Top'
            borders['__children__'].append(top_border)
        if bottom_border:
            bottom_border['Position'] = 'Bottom'
            borders['__children__'].append(bottom_border)

        return cell.setStyle(alignment=alignment, borders=borders, font=font,
                             interior=interior, number_format=number_format)

    def execCmdScript(self, cmd_script=None, auto_save=True):
        """
        Run script - a list of commands.

        :param cmd_script: List of format commands
        [
        ('CommandName', (tuple of unnamed arguments), {dictionary of named arguments}),
        ...
        ]
        :param auto_save: Save automatically upon completion of work.
        """
        if cmd_script:
            for cmd in cmd_script:
                try:
                    args = ()
                    len_cmd = len(cmd)
                    if len_cmd >= 2:
                        args = cmd[1]
                    kwargs = {}
                    if len_cmd >= 3:
                        kwargs = cmd[2]
                    # Direct function call
                    getattr(self, cmd[0])(*args, **kwargs)
                except:
                    log_func.error(u'Error execute command <%s>' % cmd)
                    raise
        if auto_save:
            self.save()
