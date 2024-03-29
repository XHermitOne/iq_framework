#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RTF report generator system module.
"""

import os
import os.path
import copy
import re

from iq.util import log_func
from iq.dialog import dlg_func

from . import rtf_report
from . import report_gen_system


__version__ = (0, 0, 2, 1)

RTF_VAR_PATTERN = r'(#.*?#)'
# List of all patterns used in parsing cell values
ALL_PATERNS = (RTF_VAR_PATTERN, )

RTF_FILENAME_EXT = '.rtf'


class iqRTFReportGeneratorSystem(report_gen_system.iqReportGeneratorSystem):
    """
    RTF report generator system class.
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
        return self._report_dir

    def _genRTFReport(self, report):
        """
        Generate report and save it in RTF file.

        :param report: Report template data.
        :return: Report RTF filename or None if error.
        """
        if report is None:
            report = self._report_template
        data_rep = self.generateReport(report)
        if data_rep:
            rep_file_name = os.path.join(self.getReportDir(), '%s_report_result.rtf' % data_rep['name'])
            template_file_name = os.path.abspath(data_rep['generator'])
            log_func.info(u'Save report <%s> to file <%s>' % (template_file_name, rep_file_name))
            
            data = self._prevGenerateAllVariables(data_rep['__data__'])
            rtf_report.genRTFReport(data, rep_file_name, template_file_name)
            return rep_file_name
        return None
        
    def preview(self, report=None, *args, **kwargs):
        """
        Preview report.

        :param report: Report template data.
        """
        rtf_rep_file_name = self._genRTFReport(report)
        if rtf_rep_file_name:
            self.previewOffice(rtf_rep_file_name)
            
    def previewOffice(self, rtf_filename):
        """
        Open RTF report in word in preview mode.

        :param rtf_filename: Report RTF filename.
        """
        try:
            # Connect with Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Hide
            word_app.Visible = 0
            # Open RTF
            rep_tmpl_book = word_app.Documents.Open(rtf_filename)
            # Show
            word_app.Visible = 1
            
            rep_tmpl_book.PrintPreview()
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error preview report <%s>' % rtf_filename)
        return False

    def print(self, report=None, *args, **kwargs):
        """
        Print report.

        :param report: Report template data.
        """
        rtf_rep_file_name = self._genRTFReport(report)
        if rtf_rep_file_name:
            self.printOffice(rtf_rep_file_name)

    def printOffice(self, rtf_filename):
        """
        Print RTF report by word.

        :param rtf_filename: Report RTF filename.
        """
        try:
            # Connect with Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Hide
            word_app.Visible = 0
            # Open RTF
            rep_tmpl_book = word_app.Documents.Open(rtf_filename)
            # Show
            word_app.Visible = 1
            
            rep_tmpl_book.PrintOut()
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error print report <%s>' % rtf_filename)
        return False
            
    def setPageSetup(self):
        """
        Set page setup.
        """
        pass

    def convert(self, report=None, to_xls_filename=None, *args, **kwargs):
        """
        Convert generate report to Office.

        :param report: Report template data.
        :param to_xls_filename: Destination generated report filename.
        """
        pass

    def openOffice(self, rtf_filename):
        """
        Open RTF file in Word.

        :param rtf_filename: Report RTF filename.
        """
        try:
            # Connection with Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Hide
            word_app.Visible = 0
            # Open RTF
            rep_tmpl_book = word_app.Open(rtf_filename)
            # Show
            word_app.Visible = 1
            return True
        except pythoncom.com_error:
            log_func.fatal(u'Error open report <%s>' % rtf_filename)
        return False
    
    def edit(self, rep_filename=None):
        """
        Edit report.

        :param rep_filename: Report template filename.
        """
        # Set *.rtf filename
        rtf_file = os.path.abspath(os.path.splitext(rep_filename)[0] + RTF_FILENAME_EXT)
        cmd = 'start word.exe \'%s\'' % rtf_file
        log_func.info(u'Execute command <%s>' % cmd)
        # Run MSWord
        os.system(cmd)

    def generateReport(self, report=None, *args, **kwargs):
        """
        Generate report.

        :param report: Report template data.
        :return: Generated report or None if error.
        """
        try:
            if report is not None:
                self._report_template = report

            # 1. Get query table
            query_data = self.getQueryTable(self._report_template)
            if not query_data:
                dlg_func.openWarningBox(u'WARNING',
                                        u'Not report data\nQuery <%s>' % self._report_template['query'],
                                        parent=self._parent_window)
                return None

            # 2. Generate
            rep_data = copy.deepcopy(self._report_template)
            rep_data['__data__'] = query_data
            return rep_data
        except:
            log_func.fatal(u'Error generate report <%s>' % self._report_template['name'])
        return None

    def _prevGenerateAllVariables(self, data):
        """
        Prepare all variables.

        :return: Data with defined values.
        """
        if '__variables__' in data:
            # Prepare
            data['__variables__'] = self._prevGenerateVariable(data['__variables__'])
        if '__loop__' in data:
            for loop_name, loop_body in data['__loop__'].items():
                if loop_body:
                    for i_loop in range(len(loop_body)):
                        loop_body[i_loop] = self._prevGenerateAllVariables(loop_body[i_loop])
                    data['__loop__'][loop_name] = loop_body
        return data

    def _prevGenerateVariable(self, variables, value=None):
        """
        Prepare variable dictionary.

        :param variables: Valiable dictionary.
        :param value: Current value.
        """
        if value is None:
            for name, value in variables.items():
                variables[name] = self._prevGenerateVariable(variables, str(value))
            return variables
        else:
            # Replace
            value = value.replace('\r\n', '\n').strip()
            # Parse
            parsed = self._parseTextFunction(value)
            values = []
            for cur_var in parsed['func']:
                if re.search(RTF_VAR_PATTERN, cur_var):
                    if cur_var[1:-1] in variables:
                        values.append(self._prevGenerateVariable(variables,
                                                                 variables[cur_var[1:-1]]))
                    else:
                        values.append('')
                else:
                    log_func.warning(u'Unsupported tag <%s>' % cur_var)

            val_str = self._setValueFormat(parsed['fmt'], values)
            return val_str

    def _parseTextFunction(self, text, patterns=ALL_PATERNS):
        """
        Parse the string into format and executable code.

        :param text: Parsed text.
        :param patterns: A list of strings of patterns of tags
            to indicate the beginning and end of the functional.
        :return: Dictionary:
            {
            'fmt': The format of a line without lines of executable code is% s;
            'func': List of lines of executable code.
            }
            or None if error.
        """
        try:
            result = dict()
            result['fmt'] = ''
            result['func'] = list()
    
            if not text:
                return result
    
            pattern = r''
            for cur_sep in patterns:
                pattern += cur_sep
                if cur_sep != patterns[-1]:
                    pattern += r'|'
                    
            parsed_str = [x for x in re.split(pattern, text) if x is not None]
            for i_parse in range(len(parsed_str)):
                func_find = False
                for cur_patt in patterns:
                    if re.search(cur_patt, parsed_str[i_parse]):
                        result['func'].append(parsed_str[i_parse])
                        # Add %s in format
                        result['fmt'] += '%s'
                        func_find = True
                        break
                if not func_find:
                    result['fmt'] += parsed_str[i_parse]
            return result
        except:
            log_func.fatal(u'Error parse func text <%s>' % text)
        return None

    def _setValueFormat(self, fmt, data_list):
        """
        Set cell value format.
        
        :param fmt: Format.
        :param data_list: Data list.
        :return: Returns a string matching the format.
        """
        if data_list == list():
            value = fmt

        elif bool(None in data_list):
            data_lst = [{None: ''}.setdefault(val, val) for val in data_list]
            value = fmt % tuple(data_lst)
        else:
            value = fmt % tuple(data_list)
        return value
