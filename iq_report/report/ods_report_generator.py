#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ODS file report generator system module.
"""

import copy
import os 
import os.path

from .dlg import report_action_dlg

import iq
from iq.util import log_func
from iq.dialog import dlg_func
from iq.util import str_func
from iq.util import global_func
from iq.util import sys_func

from iq.components.virtual_spreadsheet import v_spreadsheet

from . import report_gen_system
from . import report_generator
from . import report_file


__version__ = (0, 0, 2, 1)

ODS_FILENAME_EXT = '.ods'
PDF_FILENAME_EXT = '.pdf'


class iqODSReportGeneratorSystem(report_gen_system.iqReportGeneratorSystem):
    """
    ODS file report generator system class.
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
                log_func.warning(u'Not define report directory')
                self._report_dir = ''
                                
        return self._report_dir

    def _genODSReport(self, report, *args, **kwargs):
        """
        Generate report and save it in ODS file.

        :param report: Report template data.
        :return: Report ODS filename or None if error.
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
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            return self.doSelectAction(ods_rep_file_name)
        else:
            log_func.warning(u'Report file <%s> not exists' % ods_rep_file_name)

    def doSelectAction(self, data):
        """
        Start select action.

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
            log_func.warning(u'Not define action')
        return None

    def preview(self, report=None, *args, **kwargs):
        """
        Preview report.

        :param report: Report template data.
        """
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            return self.previewOffice(ods_rep_file_name)
        return False
            
    def previewOffice(self, ods_filename):
        """
        Open ODS file in Office preview mode.

        :param ods_filename: Report ODS filename.
        """
        if not os.path.exists(ods_filename):
            log_func.warning(u'Preview. Report file <%s> not exists' % ods_filename)
            return False

        pdf_filename = os.path.splitext(ods_filename)[0] + PDF_FILENAME_EXT

        if os.path.exists(pdf_filename):
            try:
                os.remove(pdf_filename)
            except:
                log_func.fatal(u'Delete file <%s>' % pdf_filename)

        if sys_func.isLinuxPlatform():
            cmd = report_gen_system.UNIX_CONV_TO_PDF_FMT % ods_filename
            log_func.info(u'Convert to PDF. Execute command <%s>' % cmd)
            os.system(cmd)

            if os.path.exists(pdf_filename):
                cmd = report_gen_system.UNIX_OPEN_PDF_FMT % pdf_filename
                log_func.info(u'Open PDF. Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            else:
                log_func.warning(u'Open PDF. PDF file <%s> not found' % pdf_filename)
        elif sys_func.isWindowsPlatform():
            win_conv_to_pdf_fmt = iq.KERNEL.settings.THIS.SETTINGS.win_conv_to_pdf_fmt.get()
            if not win_conv_to_pdf_fmt:
                win_conv_to_pdf_fmt = report_gen_system.WIN_CONV_TO_PDF_FMT
            cmd = win_conv_to_pdf_fmt % (ods_filename, os.path.dirname(ods_filename))
            log_func.info(u'Convert to PDF. Execute command <%s>' % cmd)
            os.system(cmd)

            if os.path.exists(pdf_filename):
                win_open_pdf_fmt = iq.KERNEL.settings.THIS.SETTINGS.win_open_pdf_fmt.get()
                if not win_open_pdf_fmt:
                    win_open_pdf_fmt = report_gen_system.WIN_OPEN_PDF_FMT

                cmd = win_open_pdf_fmt % pdf_filename
                log_func.info(u'Open PDF. Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            else:
                log_func.warning(u'Open PDF. PDF file <%s> not found' % pdf_filename)
        else:
            log_func.warning(u'Unsupported <%s> platform' % sys_func.getPlatform())
        return False

    def print(self, report=None, *args, **kwargs):
        """
        Print report.

        :param report: Report template data.
        """
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            return self.printOffice(ods_rep_file_name)
        return False

    def printOffice(self, ods_filename):
        """
        Print report by Office.

        :param ods_filename: Report ODS filename.
        """
        if ods_filename and os.path.exists(ods_filename):
            if sys_func.isLinuxPlatform():
                cmd = '%s -p %s&' % (report_gen_system.UNIX_OFFICE_OPEN, ods_filename)
                log_func.info(u'Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            elif sys_func.isWindowsPlatform():
                win_office_open = iq.KERNEL.settings.THIS.SETTINGS.win_libreoffice_run.get()
                cmd = '%s -p %s&' % (win_office_open if win_office_open else report_gen_system.WIN_OFFICE_OPEN,
                                     ods_filename)
                log_func.info(u'Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            else:
                log_func.warning(u'Unsupported platform <%s>' % sys_func.getPlatform())
        else:
            log_func.warning(u'Print. Report file <%s> not exists' % ods_filename)
        return False

    def setPageSetup(self):
        """
        Set page setup.
        """
        pass

    def convert(self, report=None, to_filename=None, *args, **kwargs):
        """
        Convert report data to Office.

        :param report: Report template data.
        :param to_filename: Destination report filename.
        """
        rep_file_name = self._genODSReport(report, *args, **kwargs)
        if rep_file_name:
            return self.openOffice(rep_file_name)
        return False

    def openOffice(self, ods_filename):
        """
        Open report.

        :param ods_filename: Report ODS filename.
        """
        if ods_filename and os.path.exists(ods_filename):
            if sys_func.isLinuxPlatform():
                cmd = '%s %s&' % (report_gen_system.UNIX_OFFICE_OPEN, ods_filename)
                log_func.info('Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            elif sys_func.isWindowsPlatform():
                win_office_open = iq.KERNEL.settings.THIS.SETTINGS.win_libreoffice_run.get()
                cmd = '%s %s&' % (win_office_open if win_office_open else report_gen_system.WIN_OFFICE_OPEN,
                                  ods_filename)
                log_func.info(u'Execute command <%s>' % cmd)
                os.system(cmd)
                return True
            else:
                log_func.warning(u'Unsupported platform <%s>' % sys_func.getPlatform())
        else:
            log_func.warning(u'Open. Report file <%s> not exists' % ods_filename)
        return False

    def edit(self, rep_filename=None):
        """
        Edit report.

        :param rep_filename: Report template filename.
        """
        # Set *.ods filename
        ods_filename = os.path.abspath(os.path.splitext(rep_filename)[0]+'.ods')

        if sys_func.isLinuxPlatform():
            cmd = '%s \"%s\"&' % (report_gen_system.UNIX_OFFICE_OPEN, ods_filename)
            log_func.info(u'Execute command <%s>' % cmd)
            os.system(cmd)
            return True
        elif sys_func.isWindowsPlatform():
            win_office_open = iq.KERNEL.settings.THIS.SETTINGS.win_libreoffice_run.get()
            cmd = '%s \"%s\"&' % (win_office_open if win_office_open else report_gen_system.WIN_OFFICE_OPEN,
                                  ods_filename)
            log_func.info(u'Execute command <%s>' % cmd)
            os.system(cmd)
            return True
        else:
            log_func.warning(u'Unsupported platform <%s>' % sys_func.getPlatform())

        return False

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

            query_tbl = self.getQueryTable(self._report_template, *args, **kwargs)
            if self._isEmptyQueryTable(query_tbl):
                if not global_func.isCUIEngine():
                    if not dlg_func.openAskBox(u'WARNING',
                                               u'No report data\nQuery <%s>\nContinue report generation?' % self._report_template['query']):
                        return None
                else:
                    log_func.warning(u'No report data. Continue generation')
                query_tbl = self.createEmptyQueryTable()

            # 2. Generate
            rep = report_generator.iqReportGenerator()
            coord_fill = kwargs.get('coord_fill', None)
            data_rep = rep.generate(self._report_template, query_tbl,
                                    name_space=variables, coord_fill=coord_fill)

            return data_rep
        except:
            log_func.fatal(u'Error generate report <%s>.' % self._report_template['name'])
        return None

    def generate(self, report=None, db_url=None, sql=None, stylelib=None, vars=None, *args, **kwargs):
        """
        Generate report.

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
            query_tbl = self.getQueryTable(self._report_template, **_kwargs)
            if self._isEmptyQueryTable(query_tbl):
                dlg_func.openWarningBox(u'WARNING',
                                        u'No report data\nQuery <%s>' % self._report_template['query'],
                                        parent=self._parent_window)
                return None

            # 2. Generate
            rep = report_generator.iqReportGenerator()
            data_rep = rep.generate(self._report_template, query_tbl,
                                    name_space=vars, *args, **kwargs)

            return data_rep
        except:
            log_func.fatal(u'Error generate report <%s>.' % str_func.toUnicode(self._report_template['name']))
        return None

    def save(self, report_data=None, to_virtual_spreadsheet=True):
        """
        Save generated report to file.

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
                log_func.info(u'Convert report <%s> to file <%s>' % (str_func.toUnicode(xml_rep_file_name),
                                                                     str_func.toUnicode(rep_file_name)))
                spreadsheet = v_spreadsheet.iqVSpreadsheet()
                spreadsheet.load(xml_rep_file_name)
                spreadsheet.saveAs(rep_file_name)
            else:
                cmd = 'unoconv --format=ods %s' % xml_rep_file_name
                log_func.info(u'UNOCONV. Convert report <%s> to file <%s>' % (str_func.toUnicode(xml_rep_file_name),
                                                                              str_func.toUnicode(rep_file_name)))
                log_func.info(u'Execute command <%s>' % cmd)
                os.system(cmd)

            return rep_file_name
        return None

    def previewResult(self, report_data=None):
        """
        Preview report result.

        :param report_data: Generated report data.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.previewOffice(report_filename)
        return False

    def printResult(self, report_data=None):
        """
        Print report result.

        :param report_data: Generated report data.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.printOffice(report_filename)
        return False

    def convertResult(self, report_data=None, to_filename=None):
        """
        Convert report result.

        :param report_data: Generated report data.
        :param to_filename: Destination report filename.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.openOffice(report_filename)
        return False
