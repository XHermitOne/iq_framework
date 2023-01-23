#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JasperReport report generator manager.
"""

import os
import os.path

from ...util import log_func
from ...util import exec_func
from ...util import py_func
from ...util import file_func

__version__ = (0, 0, 0, 1)

JASPER_REPORT_PROJECT_FILE_EXT = '.jrxml'

ALTER_ECLIPSE_RUN = '~/dev/ide/eclipse/java-2021-06/eclipse/eclipse'
ALTER_JASPERSTARTER_RUN = '~/dev/ide/jasperstarter/bin/jasperstarter'

DEFAULT_REPORT_PORTRAIT_BASENAME = 'default_report_portrait' + JASPER_REPORT_PROJECT_FILE_EXT
DEFAULT_REPORT_PORTRAIT_FILENAME = os.path.join(os.path.dirname(__file__),
                                                DEFAULT_REPORT_PORTRAIT_BASENAME)
DEFAULT_REPORT_LANDSCAPE_BASENAME = 'default_report_landscape' + JASPER_REPORT_PROJECT_FILE_EXT
DEFAULT_REPORT_LANDSCAPE_FILENAME = os.path.join(os.path.dirname(__file__),
                                                 DEFAULT_REPORT_LANDSCAPE_BASENAME)


def isJasperReportProjectFile(filename):
    """
    Check if the file is JasperReport project.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, JASPER_REPORT_PROJECT_FILE_EXT)


def getEclipseExecutable():
    """
    The path to the Eclipse program to run.
    """
    if os.path.exists('/bin/eclipse') or os.path.exists('/usr/bin/eclipse'):
        return 'eclipse'
    else:
        alter_eclipse_path = file_func.getNormalPath(ALTER_ECLIPSE_RUN)
        return alter_eclipse_path
    return None


# Alter function name
getJasperReportEditorExecutable = getEclipseExecutable


def getJasperStarterExecutable():
    """
    The path to the JasperStarter program to run.
    """
    if os.path.exists('/bin/jasperstarter') or os.path.exists('/usr/bin/jasperstarter'):
        return 'jasperstarter'
    else:
        alter_path = file_func.getNormalPath(ALTER_JASPERSTARTER_RUN)
        return alter_path
    return None


# Alter function name
getJasperReportGeneratorExecutable = getJasperStarterExecutable


def runEclipse(filename=None):
    """
    Run Eclipse as JasperReport editor.

    :param filename: JRXML file opened in Eclipse.
    :return: True/False
    """
    if not os.path.exists(filename):
        log_func.warning(u'JasperReport project file <%s> not found' % filename)
        return False

    eclipse_exec = getJasperReportEditorExecutable()
    cmd = '%s %s' % (eclipse_exec, filename)
    return exec_func.execSystemCommand(cmd)


# Alter function name
runJasperReportEditor = runEclipse


class iqJasperReportManager(object):
    """
    JasperReport report generator manager.
    """
    def openProject(self, prj_filename):
        """
        Open project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        try:
            return runJasperReportEditor(prj_filename)
        except:
            log_func.fatal(u'Error opening JasperReport project file <%s>' % prj_filename)
        return False

    def createProject(self, default_prj_filename=None, new_prj_filename=None, auto_open=False):
        """
        Create a new project file.

        :param default_prj_filename: The default project file name.
        :param new_prj_filename: New project filename.
        :param auto_open: Automatic open new file.
        :return: True/False.
        """
        try:
            if default_prj_filename is None:
                default_prj_filename = DEFAULT_REPORT_LANDSCAPE_FILENAME
            if new_prj_filename is None:
                new_prj_filename = default_prj_filename
            result = file_func.copyFile(src_filename=default_prj_filename,
                                        dst_filename=new_prj_filename)

            if result and auto_open:
                return runJasperReportEditor(new_prj_filename)
            return result
        except:
            log_func.fatal(u'Error creating JasperReport project file <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, command='process', fmt='view', **kwargs):
        """
        Generate report by JasperReport JasperStarter tool.

        :param prj_filename: JRXML project filename.
        :param command: Command:
            compile - compile reports
            process - view, print or export an existing report
            list_printers - lists available printers
            list_parameters - list parameters from a given report

        :param fmt: Format:
            view, print, pdf, rtf, xls, xlsMeta, xlsx, docx, odt, ods, pptx, csv, csvMeta, html, xhtml, xml, jrprint.
        :param kwargs:
            Extended parameters.
        :return: True/False.
        """
        try:
            if not os.path.exists(prj_filename):
                log_func.warning(u'JasperReport project file <%s> not found' % prj_filename)
                return False

            generate_exec = getJasperReportGeneratorExecutable()
            cmd = '%s %s %s -f %s' % (generate_exec, command, prj_filename, fmt)
            return exec_func.execSystemCommand(cmd)
        except:
            log_func.fatal(u'Error generate JasperReport report <%s>' % prj_filename)
        return False


def createJasperReportProjectFile(prj_filename, auto_open=False):
    """
    Create JasperReport JRXML project file.

    :param prj_filename: New JRXML project filename.
    :param auto_open: Automatic open new file.
    :return: True/False.
    """
    manager = iqJasperReportManager()
    return manager.createProject(new_prj_filename=prj_filename, auto_open=auto_open)
