#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XML report generator system module.
"""

import os 
import os.path

import iq
from iq.util import log_func
from iq.dialog import dlg_func
from iq.util import global_func
from iq.util import sys_func

from . import report_gen_system
from . import report_generator
from . import report_file


__version__ = (0, 0, 2, 1)

XML_FILENAME_EXT = '.xml'


class iqXMLReportGeneratorSystem(report_gen_system.iqReportGeneratorSystem):
    """
    XML report generator system class.
    """
    def __init__(self, report=None, parent=None):
        """
        Constructor.

        :param report: Report template data.
        :param parent: Parent window.
        """
        report_gen_system.iqReportGeneratorSystem.__init__(self, report, parent)

        # Report folder
        self._report_dir = None
        if self._parent_window:
            self._report_dir = os.path.abspath(self._parent_window.getReportDir())
        
    def reloadReportData(self, tmpl_filename=None):
        """
        Reload report template data.

        :param tmpl_filename: Report template filename.
        """
        if tmpl_filename is None:
            tmpl_filename = self._report_template_filename
        report_gen_system.iqReportGeneratorSystem.reloadReportData(self, tmpl_filename)
        
    def getReportDir(self):
        """
        Get report folder path.
        """
        if self._report_dir is None:
            if self._parent_window:
                self._report_dir = os.path.abspath(self._parent_window.getReportDir())
            else:
                dlg_func.openErrBox(u'ERROR', u'Not defined report folder')
                                
        return self._report_dir

    def _genXMLReport(self, report):
        """
        Generate a report and save it in an XML file.

        :param report: Report template data.
        :return: XML filename or None if error.
        """
        if report is None:
            report = self._report_template
        data_rep = self.generateReport(report)
        if data_rep:
            rep_file = report_file.iqXMLSpreadSheetReportFile()
            rep_file_name = os.path.join(self.getReportDir(),
                                         '%s_report_result.xml' % str(data_rep['name']))
            rep_file.write(rep_file_name, data_rep)
            log_func.info(u'Save report file <%s>' % rep_file_name)
            return rep_file_name
        return None
        
    def preview(self, report=None, *args, **kwargs):
        """
        Preview.

        :param report: Report template data.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            self.previewExcel(xml_rep_file_name)
            
    def previewExcel(self, xml_filename):
        """
        Open excel in preview mode.

        :param xml_filename: Report XML filename.
        """
        try:
            # Connect with Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Hide Excel
            excel_app.Visible = 0
            # Close all
            excel_app.Workbooks.Close()
            # Open XML
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Visible Excel
            excel_app.Visible = 1
            
            excel_app.ActiveWindow.ActiveSheet.PrintPreview()
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error preview Excel')
        return False

    def print(self, report=None, *args, **kwargs):
        """
        Print.

        :param report: Report template data.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            self.printOffice(xml_rep_file_name)

    def printOffice(self, xml_filename):
        """
        Print report  by excel.

        :param xml_filename: Report XML filename.
        """
        try:
            # Connect with Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Hide Excel
            excel_app.Visible = 0
            # Close all workbooks
            excel_app.Workbooks.Close()
            # Open XML
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Show Excel
            excel_app.Visible = 1
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error print report by Excel')
        return False
            
    def setPageSetup(self):
        """
        Set page setup.
        """
        pass

    def convert(self, report=None, to_xls_filename=None, *args, **kwargs):
        """
        Convert report to Excel.

        :param report: Report template data.
        :param to_xls_filename: Report XLS filename.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            # Excel
            self.openOffice(xml_rep_file_name)

    def openOffice(self, xml_filename):
        """
        Open excel.

        :param xml_filename: Report XML filename.
        """
        try:
            # Connect with Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Hide Excel
            excel_app.Visible = 0
            # Close all workbooks
            excel_app.Workbooks.Close()
            # Open XML
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Show Excel
            excel_app.Visible = 1
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error open report in Excel')
        return False

    def edit(self, rep_filename=None):
        """
        Edit report.

        :param rep_filename: Report template filename.
        """
        # Set *.xml filename
        xml_file = os.path.abspath(os.path.splitext(rep_filename)[0] + XML_FILENAME_EXT)
        cmd = 'start excel.exe \"%s\"' % xml_file
        # Run MSExcel
        os.system(cmd)

    def generateReport(self, report=None, *args, **kwargs):
        """
        Run report generator.

        :param report: Report template data.
        :return: Generated report or None if error.
        """
        try:
            if report is not None:
                self._report_template = report

            # 1. Get query table
            # Variables
            variables = kwargs.get('variables', None)
            if variables:
                kwargs.update(variables)

            query_tbl = self.getQueryTable(self._report_template)
            if not query_tbl or not query_tbl['__data__']:
                if not global_func.isCUIEngine():
                    if dlg_func.openAskBox(u'WARNING',
                                           u'No report data\nQuery: %s\nContinue report generation?' % self._report_template['query']):
                        return None
                else:
                    log_func.warning(u'No report data. Continue generation.')
                query_tbl = self.createEmptyQueryTable()

            # 2. Run generation
            rep = report_generator.iqReportGenerator()
            data_rep = rep.generate(self._report_template, query_tbl)

            return data_rep
        except:
            log_func.fatal(u'Error generate report <%s>' % self._report_template['name'])
        return None
