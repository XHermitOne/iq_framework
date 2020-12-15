#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XLS report generator system module.
"""

import copy
import os 
import os.path

from .dlg import report_action_dlg

from iq.util import log_func
from iq.dialog import dlg_func
from iq.util import global_func

from iq.components.virtual_spreadsheet import v_spreadsheet

from . import report_gen_system
from . import report_generator
from . import report_file

__version__ = (0, 0, 0, 1)

PDF_FILENAME_EXT = '.pdf'
XLS_FILENAME_EXT = '.xls'


class iqXLSReportGeneratorSystem(report_gen_system.iqReportGeneratorSystem):
    """
    XLS report generator system class.
    """
    def __init__(self, report=None, parent=None):
        """
        Constructor.

        :param report: Report template data.
        :param parent: Parent window.
        """
        report_gen_system.iqReportGeneratorSystem.__init__(self, report, parent)

        # Report template filename
        self.RepTmplFileName = None
        
        # Report folder
        self._report_dir = None
        if self._parent_window:
            self._report_dir = os.path.abspath(self._parent_window.getReportDir())
        
    def reloadRepData(self, tmpl_filename=None):
        """
        Reload report template data.

        :param tmpl_filename: Report template filename.
        """
        if tmpl_filename is None:
            tmpl_filename = self.RepTmplFileName
        report_gen_system.iqReportGeneratorSystem.reloadRepData(self, tmpl_filename)
        
    def getReportDir(self):
        """
        Get report folder path.
        """
        if self._report_dir is None:
            if self._parent_window:
                self._report_dir = os.path.abspath(self._parent_window.getReportDir())
            else:
                log_func.warning(u'Not define report directory')
                self._report_dir = ''
                                
        return self._report_dir

    def _genXLSReport(self, report, *args, **kwargs):
        """
        Generate a report and save it in an XLS file.

        :param report: Report template data.
        :return: Report XML file name or None if error.
        """
        if report is None:
            report = self._report_template
        data_rep = self.generateReport(report, *args, **kwargs)
        return self.save(data_rep)

    def selectAction(self, report=None, *args, **kwargs):
        """
        Start report generation and then select an action.

        :param report: Report template data.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            return self.doSelectAction(xls_rep_file_name)
        else:
            log_func.warning(u'Report file <%s> not exists' % xls_rep_file_name)
        return False

    def doSelectAction(self, data):
        """
        Select action.

        :param data: Report data.
        """
        action = report_action_dlg.getReportActionDlg(title=self.getReportDescription())
        if action == report_action_dlg.PRINT_ACTION_ID:
            return self.printOffice(data)
        elif action == report_action_dlg.PREVIEW_ACTION_ID:
            return self.previewOffice(data)
        elif action == report_action_dlg.EXPORT_ACTION_ID:
            return self.openOffice(data)
        else:
            log_func.warning(u'Not select action')
        return None

    def preview(self, report=None, *args, **kwargs):
        """
        Preview.

        :param report: Report template data.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            return self.previewOffice(xls_rep_file_name)
        return False
            
    def previewOffice(self, xls_filename):
        """
        Open preview in Office.

        :param xls_filename: Report XLS filename.
        """
        if not os.path.exists(xls_filename):
            log_func.warning(u'Preview. Report file <%s> not exists' % xls_filename)
            return False

        pdf_filename = os.path.splitext(xls_filename)[0] + PDF_FILENAME_EXT
        if os.path.exists(pdf_filename):
            try:
                os.remove(pdf_filename)
            except:
                log_func.fatal(u'Error delete file <%s>' % pdf_filename)

        cmd = 'unoconv --format=pdf %s' % xls_filename
        log_func.info(u'UNOCONV. Execute command <%s>' % cmd)
        os.system(cmd)

        cmd = 'evince %s&' % pdf_filename
        log_func.info(u'EVINCE. Execute command <%s>' % cmd)
        os.system(cmd)
        return True

    def print(self, report=None, *args, **kwargs):
        """
        Print.

        :param report: Report template data.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            return self.printOffice(xls_rep_file_name)
        return False

    def printOffice(self, xls_filename):
        """
        Print report by Office.

        :param xls_filename: Report XLS filename.
        """
        if xls_filename and os.path.exists(xls_filename):
            cmd = 'libreoffice -p %s&' % xls_filename
            log_func.info(u'Execute command <%s>' % cmd)
            os.system(cmd)
            return True
        else:
            log_func.warning(u'Print. Report file <%s> not exists' % xls_filename)
        return False

    def setPageSetup(self):
        """
        Set page setup.
        """
        pass

    def convert(self, report=None, to_filename=None, *args, **kwargs):
        """
        Convert report to Excel.

        :param report: Report template data.
        :param to_filename: Destination report filename.
        """
        rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if rep_file_name:
            return self.openOffice(rep_file_name)
        return False

    def openOffice(self, xls_filename):
        """
        Open XLS report in Office.

        :param xls_filename: Report XLS filename.
        """
        if xls_filename and os.path.exists(xls_filename):
            cmd = 'libreoffice %s&' % xls_filename
            log_func.info('Execute command <%s>' % cmd)
            os.system(cmd)
            return True
        else:
            log_func.warning(u'Open. Report file <%s> not exists' % xls_filename)
        return False

    def edit(self, rep_filename=None):
        """
        Edit report.

        :param rep_filename: Report template filename.
        """
        # Set *.xls filename
        xls_file = os.path.abspath(os.path.splitext(rep_filename)[0] + XLS_FILENAME_EXT)
        cmd = 'libreoffice \"%s\"&' % xls_file
        log_func.info('Execute command <%s>' % cmd)
        os.system(cmd)
        return True

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
            variables = kwargs.get('variables', None)
            if variables:
                kwargs.update(variables)

            query_tbl = self.getQueryTbl(self._report_template, *args, **kwargs)
            if self._isEmptyQueryTbl(query_tbl):
                if not global_func.isCUIEngine():
                    if not dlg_func.openAskBox(u'WARNING',
                                               u'Not report data\nQuery: %s\nContinue report generation' % self._report_template['query']):
                        return None
                else:
                    log_func.warning(u'Not report data. Continue generation')
                query_tbl = self.createEmptyQueryTbl()

            # 2. Generation
            rep = report_generator.iqReportGenerator()
            coord_fill = kwargs.get('coord_fill', None)
            data_rep = rep.generate(self._report_template, query_tbl,
                                    name_space=variables, coord_fill=coord_fill)

            return data_rep
        except:
            log_func.fatal(u'Error generate report <%s>' % self._report_template['name'])
        return None

    def generate(self, report=None, db_url=None, sql=None, stylelib=None, vars=None, *args, **kwargs):
        """
        Run report generator.

        :param report: Report template data.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param stylelib: Style library.
        :param vars: Report variables dictionary.
        :return: Generated report or None if error.
        """
        try:
            if report is not None:
                self._report_template = report

            if stylelib:
                self._report_template['style_lib'] = stylelib

            if vars:
                self._report_template['variables'] = vars

            # 1. Get query table
            _kwargs = copy.deepcopy(kwargs)
            _kwargs.update(dict(db_url=db_url, sql=sql, stylelib=stylelib, variables=vars))
            query_tbl = self.getQueryTbl(self._report_template, **_kwargs)
            if self._isEmptyQueryTbl(query_tbl):
                dlg_func.openWarningBox(u'WARNING',
                                        u'Not report data\nQuery <%s>' % self._report_template['query'],
                                        parent=self._parent_window)
                return None

            # 2. Run generator
            rep = report_generator.iqReportGenerator()
            data_rep = rep.generate(self._report_template, query_tbl,
                                    name_space=vars, *args, **kwargs)

            return data_rep
        except:
            log_func.fatal(u'Error generate report <%s>' % self._report_template['name'])
        return None

    def save(self, report_data=None, to_virtual_spreadsheet=True):
        """
        Save report result to file.

        :param report_data: Generated report data.
        :param to_virtual_spreadsheet: Save by Virtual SpreadSheet?
            True - yes,
            False - Save by UNOCONV convertation.
            When converting using UNOCONV, the cells are not dimensioned.
            Cell sizes remain by default.
            UNOCONV does not translate all cell styles and attributes.
        :return: Destination report filename or None if error.
        """
        if report_data:
            rep_file = report_file.iqXMLSpreadSheetReportFile()
            save_dir = self.getProfileDir()
            if not save_dir:
                save_dir = report_gen_system.DEFAULT_REPORT_DIR
            xml_rep_file_name = os.path.join(save_dir, '%s_report_result.xml' % report_data['name'])
            rep_file_name = os.path.join(save_dir, '%s_report_result.ods' % report_data['name'])

            rep_file.write(xml_rep_file_name, report_data)

            if to_virtual_spreadsheet:
                log_func.info(u'Convert report <%s> to file <%s>' % (xml_rep_file_name, rep_file_name))
                spreadsheet = v_spreadsheet.iqVSpreadsheet()
                spreadsheet.load(xml_rep_file_name)
                spreadsheet.saveAs(rep_file_name)
            else:
                cmd = 'unoconv -f ods %s' % xml_rep_file_name
                log_func.info(u'UNOCONV. Convert report <%s> to file <%s>' % (xml_rep_file_name,
                                                                              rep_file_name))
                log_func.info(u'Execute command <%s>' % cmd)
                os.system(cmd)
            return rep_file_name
        return None

    def previewResult(self, report_data=None):
        """
        Preview report.

        :param report_data: Generated report data.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.previewOffice(report_filename)

    def printResult(self, report_data=None):
        """
        Print report.

        :param report_data: Generated report data.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.printOffice(report_filename)

    def convertResult(self, report_data=None, to_filename=None):
        """
        Convert report.

        :param report_data: Generated report data.
        :param to_filename: Destination report filename.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.openOffice(report_filename)
