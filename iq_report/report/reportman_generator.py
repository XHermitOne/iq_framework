#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReportManager generator system module.

https://reportman.sourceforge.io
"""

import os
import os.path
import tempfile

from iq.util import res_func
# from iq.util import util_func
from iq.util import exec_func
from iq.util import log_func
from iq.dialog import dlg_func

from . import report_gen_system

from . import reportman


__version__ = (0, 0, 2, 1)

DEFAULT_REP_FILE_NAME = os.path.join(tempfile.gettempdir(), 'new_report.rep')


class iqReportManagerGeneratorSystem(report_gen_system.iqReportGeneratorSystem):
    """
    ReportManager generator system class.
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
        
    def getReportDir(self):
        """
        Get report folder path.
        """
        return self._report_dir

    def preview(self, report=None, *args, **kwargs):
        """
        Preview report.

        :param report: Report template data.
        """
        if report is None:
            report = self._report_template
        # Connect with ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Report parameters
            params = self._getReportParameters(report)
            # Set parameters
            self._setReportParameters(report_manager, params)

            report_manager.preview(u'Preview: %s' % report_file)
            return True
        except:
            log_func.fatal(u'Error preview report <%s>' % report_file)
        return False
            
    def print(self, report=None, *args, **kwargs):
        """
        Print report.

        :param report: Report template data.
        """
        if report is None:
            report = self._Rep
        # Create with ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Report parameters
            params = self._getReportParameters(report)
            # Set parameters
            self._setReportParameters(report_manager, params)

            report_manager.printout(u'Print: %s' % report_file, True, True)
            return True
        except:
            log_func.fatal(u'Error print report <%s>' % report_file)
        return False

    def setPageSetup(self):
        """
        Set page setup.
        """
        pass

    def convert(self, report=None, to_xls_filename=None, *args, **kwargs):
        """
        Convert report data to Office.

        :param report: Report template data.
        :param to_xls_filename: Destination report filename.
        """
        if report is None:
            report = self._Rep
        # Connection with ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Report parameters
            params = self._getReportParameters(report)
            # Set parameters
            self._setReportParameters(report_manager, params)

            report_manager.execute()
            return True
        except:
            log_func.fatal(u'Error convert report <%s>' % report_file)
        return False

    def edit(self, rep_filename=None):
        """
        Edit report.

        :param rep_filename: Report template filename.
        """
        rprt_file_name = os.path.abspath(rep_filename)
        rep = res_func.loadResource(rprt_file_name)
        report_dir = os.path.abspath(self.getReportDir())
        rep_file = os.path.join(report_dir, rep['generator'])
        
        reportman_designer_key = utilfunc.getRegValue('Software\\Classes\\Report Manager Designer\\shell\\open\\command',
                                                      None)
        if reportman_designer_key:
            reportman_designer_run = reportman_designer_key.replace('\'%1\'', '\'%s\'') % rep_file
            cmd = 'start %s' % reportman_designer_run
            log_func.debug(u'Execute command <%s>' % cmd)
            # Run Report Manager Designer
            os.system(cmd)
        else:
            msg = u'Not define Report Manager Designer <%s>' % reportman_designer_key
            log_func.warning(msg)
            dlg_func.openWarningBox(u'WARNING', msg)

        xml_file = os.path.normpath(os.path.abspath(os.path.splitext(rep_filename)[0]+'.xml'))
        cmd = 'start excel.exe \'%s\'' % xml_file
        log_func.debug(u'Execute command <%s>' % cmd)
        os.system(cmd)

    def _getReportParameters(self, report=None):
        """
        Get report parameters.

        :param report: Report template data.
        :return: Report parameters dictionary:
            {'report_parameter_name': report_parameter_value,
            ...
            }.
        """
        try:
            if report is not None:
                self._Rep = report
            else:
                report = self._Rep

            # 1. Get query table
            query = report['query']
            if query is not None:
                if self._isQueryFunction(query):
                    query = self._execQueryFunction(query)
                else:
                    query = exec_func.execTxtFunction(query)
                
            return query
        except:
            log_func.fatal(u'Error get report parameters <%s>' % report['name'])
        return None

    def _setReportParameters(self, report_obj, parameters):
        """
        Set report parameters.

        :param report_obj: ReportManger report object.
        :param parameters: Report parameters dictionary:
            {'report_parameter_name': report_parameter_value,
            ...
            }.
        :return: True/False.
        """
        try:
            if parameters:
                for param_name, param_value in parameters.items():
                    report_obj.set_param(param_name, param_value)
            return True
        except:
            log_func.fatal(u'Error set report parameters <%s> in report <%s>' % (parameters,
                                                                                 report_obj._report_filename))
        return False
