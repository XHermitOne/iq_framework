#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
iqReport manager module.
"""

import os
import os.path
import wx

from iq.util import log_func
from iq.util import file_func
from iq.util import txtfile_func
from iq.util import res_func
from iq.util import str_func

from .report.dlg import report_action_dlg
from .report import do_report

__version__ = (0, 0, 0, 1)

DEFAULT_REPORT_DIRNAME = 'reports'

DEFAULT_REPORT_FILE_EXT = do_report.DEFAULT_REPORT_FILE_EXT

DEFAULT_INIT_PY_FMT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Reports package <%s>.
\"\"\"

__version__ = (0, 0, 0, 1)

'''

# Post-processing commands for the generated report
DO_COMMAND_PRINT = 'print'
DO_COMMAND_PREVIEW = 'preview'
DO_COMMAND_EXPORT = 'export'
DO_COMMAND_SELECT = 'select'

DEFAULT_REPORTS_PATH = os.path.join(file_func.getFrameworkPath(), 'reports')

# Report manager object
REPORT_MANAGER = None


class iqReportManager(object):
    """
    iqReport manager class.
    """
    def __init__(self, report_dir=None):
        """
        Constructor.

        :param report_dir: Report folder path.
        """
        self._report_dir = None
        if report_dir and os.path.exists(report_dir):
            self._report_dir = report_dir

    def design(self):
        """
        Report design mode.
        """
        try:
            do_report.openReportEditor(report_dir=self.getReportDir())
        except:
            log_func.fatal(u'Error run report design mode')

    def setReportDir(self, report_dir=None):
        """
        Set report folder path.

        :param report_dir: Report folder path.
        """
        self._report_dir = report_dir

    def getReportDir(self):
        """
        Get report folder path.

        :return: Report folder path.
        """
        if self._report_dir is None:
            prj_dir = file_func.getProjectPath()
            prj_dir = prj_dir if prj_dir else DEFAULT_REPORTS_PATH
            self._report_dir = os.path.join(prj_dir, DEFAULT_REPORT_DIRNAME)

            if not os.path.exists(self._report_dir):
                try:
                    os.makedirs(self._report_dir)
                    log_func.info(u'Create folder <%s>' % self._report_dir)
                    description_filename = os.path.join(self._report_dir, 'descript.ion')
                    prj_name = os.path.basename(prj_dir)
                    txtfile_func.saveTextFile(description_filename,
                                              u'<%s> project reports' % prj_name)
                    init_filename = os.path.join(self._report_dir, '__init__.py')
                    txtfile_func.saveTextFile(init_filename,
                                              DEFAULT_INIT_PY_FMT % prj_name)
                except IOError:
                    log_func.warning(u'Error create folder <%s>' % self._report_dir)
        return self._report_dir

    def printReport(self, report_filename,
                    db_url=None, sql=None, command=None,
                    stylelib_filename=None, variables=None):
        """
        Start report generation and print it.

        :param report_filename: The name of the report template file.
             Paths are relative to the report folder.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param command: Command after generation (print/preview/export).
        :param stylelib_filename: Style library file.
        :param variables: Dictionary of variables to populate the report.
        :return: True/False.
        """
        try:
            return do_report.printReport(report_filename=report_filename,
                                         report_dir=self.getReportDir(),
                                         db_url=db_url,
                                         sql=sql,
                                         command=command,
                                         stylelib_filename=stylelib_filename,
                                         variables=variables)
        except:
            log_func.fatal(u'Error print report <%s>' % report_filename)

    def previewReport(self, report_filename,
                      db_url=None, sql=None, command=None,
                      stylelib_filename=None, variables=None):
        """
        Start report generation with preview.

        :param report_filename: The name of the report template file.
             Paths are relative to the report folder.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param command: Command after generation (print/preview/export).
        :param stylelib_filename: Style library file.
        :param variables: Dictionary of variables to populate the report.
        :return: True/False.
        """
        try:
            return do_report.previewReport(report_filename=report_filename,
                                           report_dir=self.getReportDir(),
                                           db_url=db_url,
                                           sql=sql,
                                           command=command,
                                           stylelib_filename=stylelib_filename,
                                           variables=variables)
        except:
            log_func.fatal(u'Error preview report <%s>' % report_filename)

    def exportReport(self, report_filename,
                     db_url=None, sql=None, command=None,
                     stylelib_filename=None, variables=None):
        """
        Start generating a report with conversion to an office program.

        :param report_filename: The name of the report template file.
             Paths are relative to the report folder.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param command: Command after generation (print/preview/export).
        :param stylelib_filename: Style library file.
        :param variables: Dictionary of variables to populate the report.
        :return: True/False.
        """
        try:
            return do_report.exportReport(report_filename=report_filename,
                                          report_dir=self.getReportDir(),
                                          db_url=db_url,
                                          sql=sql,
                                          command=command,
                                          stylelib_filename=stylelib_filename,
                                          variables=variables)
        except:
            log_func.fatal(u'Error export report <%s>' % report_filename)

    def selectPostAction(self, report_filename, parent=None,
                         db_url=None, sql=None, command=None,
                         stylelib_filename=None, variables=None):
        """
        Select the action we want to do with the report after generating the report.

        :param report_filename: The name of the report template file.
             Paths are relative to the report folder.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param command: Command after generation (print/preview/export).
        :param stylelib_filename: Style library file.
        :param variables: Dictionary of variables to populate the report.
        :return: True/False.
        """
        try:
            return do_report.selectReport(report_filename=report_filename,
                                          report_dir=self.getReportDir(),
                                          db_url=db_url,
                                          sql=sql,
                                          command=command,
                                          stylelib_filename=stylelib_filename,
                                          variables=variables)
        except:
            log_func.fatal(u'Error select post action report <%s>' % report_filename)

    def selectPrevAction(self, report_filename, parent=None,
                         db_url=None, sql=None, command=None,
                         stylelib_filename=None, variables=None):
        """
        First, select the action we want to do with the report.

        :param parent: Parent window.
        :param report_filename: The name of the report template file.
             Paths are relative to the report folder.
        :param db_url: Connection string as url.
            For example:
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: SQL query.
        :param command: Command after generation (print/preview/export).
        :param stylelib_filename: Style library file.
        :param variables: Dictionary of variables to populate the report.
        :return: True/False.
        """
        try:
            if parent is None:
                parent = wx.GetApp().GetTopWindow()

            description = self.getReportDescription(report_filename)
            dlg = None
            try:
                dlg = report_action_dlg.iqReportActionDialog(parent)
                dlg.setReportNameTitle(description)
                dlg.ShowModal()
                result = dlg.getSelectedAction()
                dlg.Destroy()
                dlg = None

                if result == report_action_dlg.PRINT_ACTION_ID:
                    return self.printReport(report_filename, db_url=db_url, sql=sql,
                                            command=command, stylelib_filename=stylelib_filename, variables=variables)
                elif result == report_action_dlg.PREVIEW_ACTION_ID:
                    return self.previewReport(report_filename, db_url=db_url, sql=sql,
                                              command=command, stylelib_filename=stylelib_filename, variables=variables)
                elif result == report_action_dlg.EXPORT_ACTION_ID:
                    return self.exportReport(report_filename, db_url=db_url, sql=sql,
                                             command=command, stylelib_filename=stylelib_filename, variables=variables)
            except:
                if dlg:
                    dlg.Destroy()
                log_func.fatal(u'Error select prev action report <%s>' % report_filename)
        except:
            log_func.fatal(u'Error select prev action report <%s>' % report_filename)
        return False

    def getReportTemplateFilename(self, report_filename='', report_dir=''):
        """
        Get the full file name of the report template.

        :param report_filename: Relative report template filename.
        :param report_dir: Report folder path.
        :return: Full report template filename.
        """
        if not report_filename.endswith(DEFAULT_REPORT_FILE_EXT):
            report_filename = os.path.splitext(report_filename)[0] + DEFAULT_REPORT_FILE_EXT

        if os.path.exists(report_filename):
            # If absolute path
            filename = report_filename
        else:
            filename = os.path.join(report_dir, report_filename)
            if not os.path.exists(filename):
                log_func.error(u'Report template file <%s> not exists' % filename)
                filename = None
        return filename

    def loadReportTemplate(self, report_filename=''):
        """
        Load report template data.

        :param report_filename: Report template filename.
        :return: Report template data or None if error.
        """
        return res_func.loadResource(report_filename)

    def getReportDescription(self, report_filename):
        """
        Get report description.

        :param report_filename: Report template filename.
        :return: Report description or base report template file name if description not defined.
        """
        res_filename = self.getReportTemplateFilename(report_filename, self.getReportDir())
        report_res = self.loadReportTemplate(res_filename)
        description = report_res.get('description', u'') if report_res and report_res.get('description', None) else report_filename
        return str_func.toUnicode(description)


def getReportManager():
    """
    Get report manager object.

    :return:
    """
    if globals()['REPORT_MANAGER'] is None:
        globals()['REPORT_MANAGER'] = iqReportManager()
    return globals()['REPORT_MANAGER']
