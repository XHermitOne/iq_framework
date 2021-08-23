#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LimeReport report generator manager.

Official site: https://limereport.ru/ru/index.php
"""

import os
import os.path

from ...util import log_func
from ...util import exec_func
from ...util import file_func
from ...util import pdf_func
from ...util import pdf2svg
from ...util import svg_func

__version__ = (0, 0, 0, 1)

LIME_REPORT_PROJECT_FILE_EXT = '.lrxml'
LIME_REPORT_RESULT_FILE_EXT = pdf_func.PDF_FILENAME_EXT

LIME_REPORT_EXEC = 'limereport'
LIME_REPORT_DESIGNER_EXEC = 'LRDesigner'

ALTER_LIME_REPORT_EXEC = 'limereport'
ALTER_LIME_REPORT_DESIGNER_EXEC = 'LRDesigner'

DEFAULT_REPORT_BASENAME = 'default_report' + LIME_REPORT_PROJECT_FILE_EXT
DEFAULT_REPORT_FILENAME = os.path.join(os.path.dirname(__file__), DEFAULT_REPORT_BASENAME)


def isLimeReportProjectFile(filename):
    """
    Check if the file is LimeReport project.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, LIME_REPORT_PROJECT_FILE_EXT)


def getLimeReportEditorExecutable():
    """
    The path to the LimeReport designer program to run.
    """
    check_bin_path = '/bin/%s' % LIME_REPORT_DESIGNER_EXEC
    check_usr_bin_path = '/usr/bin/%s' % LIME_REPORT_DESIGNER_EXEC
    if os.path.exists(check_bin_path) or os.path.exists(check_usr_bin_path):
        return LIME_REPORT_DESIGNER_EXEC
    else:
        alter_limereport_designer_path = file_func.getNormalPath(ALTER_LIME_REPORT_DESIGNER_EXEC)
        log_func.info(u'Use alter LimeReport designer <%s>' % alter_limereport_designer_path)
        return alter_limereport_designer_path
    return None


def getLimeReportGeneratorExecutable():
    """
    The path to the LimeReport generator program to run.
    """
    check_bin_path = '/bin/%s' % LIME_REPORT_EXEC
    check_usr_bin_path = '/usr/bin/%s' % LIME_REPORT_EXEC
    if os.path.exists(check_bin_path) or os.path.exists(check_usr_bin_path):
        return LIME_REPORT_EXEC
    else:
        alter_limereport_path = file_func.getNormalPath(ALTER_LIME_REPORT_EXEC)
        log_func.info(u'Use alter LimeReport <%s>' % alter_limereport_path)
        return alter_limereport_path
    return None


def runLimeReportEditor(filename=None):
    """
    Run LimeReport designer.

    :param filename: LRXML file opened in designer.
    :return: True/False
    """
    if not os.path.exists(filename):
        log_func.warning(u'LimeReport project file <%s> not found' % filename)
        return False

    eclipse_exec = getLimeReportEditorExecutable()
    cmd = '%s %s' % (eclipse_exec, filename)
    return exec_func.execSystemCommand(cmd)


class iqLimeReportManager(object):
    """
    LimeReport report generator manager.
    """
    def openProject(self, prj_filename):
        """
        Open project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False
        try:
            return runLimeReportEditor(prj_filename)
        except:
            log_func.fatal(u'Error opening LimeReport project file <%s>' % prj_filename)
        return False

    def createProject(self, default_prj_filename=None, new_prj_filename=None, auto_open=False):
        """
        Create a new project file.

        :param default_prj_filename: The default project file name.
        :param new_prj_filename: New project filename.
        :param auto_open: Automatic open new file in designer?
        :return: True/False.
        """
        try:
            if default_prj_filename is None:
                default_prj_filename = DEFAULT_REPORT_FILENAME
            if new_prj_filename is None:
                new_prj_filename = default_prj_filename
            result = file_func.copyFile(src_filename=default_prj_filename,
                                        dst_filename=new_prj_filename)

            if result and auto_open:
                return runLimeReportEditor(new_prj_filename)
            return result
        except:
            log_func.fatal(u'Error creating LimeReport project file <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, dst_filename=None, **kwargs):
        """
        Generate report by LimeReport tool.

        :param prj_filename: LRXML project filename.
        :param dst_filename: Result filename.
        :param kwargs:
            Extended parameters.
        :return: True/False.
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False
        if dst_filename is None:
            dst_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(), LIME_REPORT_RESULT_FILE_EXT)

        try:
            if not os.path.exists(prj_filename):
                log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
                return False

            generate_exec = getLimeReportGeneratorExecutable()
            cmd = '%s --source %s' % (generate_exec, prj_filename)
            if dst_filename:
                cmd += ' --destination %s' % dst_filename
            if kwargs:
                for param_name, param_value in kwargs.items():
                    cmd += ' --param %s=%s' % (param_name, param_value)
            return exec_func.execSystemCommand(cmd)
        except:
            log_func.fatal(u'Error generate LimeReport report <%s>' % prj_filename)
        return False

    def preview(self, prj_filename, **kwargs):
        """
        Preview report.

        :param prj_filename: LRXML project filename.
        :param kwargs: Extended parameters.
        :return: True/False.
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False
        dst_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(), LIME_REPORT_RESULT_FILE_EXT)
        if self.generate(prj_filename=prj_filename, dst_filename=dst_filename, **kwargs):
            return pdf_func.viewPDF(pdf_filename=dst_filename)
        return False

    def print(self, prj_filename, printer_name=None, **kwargs):
        """
        Print report.

        :param prj_filename: LRXML project filename.
        :param printer_name: Printer name.
        :param kwargs: Extended parameters.
        :return: True/False.
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False
        dst_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(), LIME_REPORT_RESULT_FILE_EXT)
        if self.generate(prj_filename=prj_filename, dst_filename=dst_filename, **kwargs):
            return pdf_func.printPDF(pdf_filename=dst_filename, printer_name=printer_name)
        return False

    def convertToSVG(self, prj_filename, svg_filename=None, page=1, auto_open=False, **kwargs):
        """
        Convert report to SVG file.

        :param prj_filename: LRXML project filename.
        :param svg_filename: Result SVG filename.
        :param page: Number of PDF page.
        :param auto_open: Automatic open SVG file in viewer?
        :param kwargs: Extended parameters.
        :return: True/False.
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False
        if svg_filename is None:
            svg_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(),
                                                    svg_func.SVG_FILENAME_EXT)

        pdf_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(), LIME_REPORT_RESULT_FILE_EXT)
        if self.generate(prj_filename=prj_filename, dst_filename=pdf_filename, **kwargs):
            if pdf2svg.pdf2svg(pdf_filename=pdf_filename, svg_filename=svg_filename, page=page):
                if auto_open:
                    svg_func.viewSVG(svg_filename=svg_filename)
                return True
        return False

    def convert(self, prj_filename, convert_to='PDF', dst_filename=None, auto_open=False, **kwargs):
        """
        Convert report to...

        :param prj_filename: LRXML project filename.
        :param convert_to: Convert to file type.
        :param dst_filename: Result filename.
        :param kwargs: Extended parameters.
        :return: True/False.
        """
        if not os.path.exists(prj_filename):
            log_func.warning(u'LimeReport project file <%s> not found' % prj_filename)
            return False

        if convert_to.upper().endswith('PDF'):
            if dst_filename is None:
                dst_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(),
                                                        pdf_func.PDF_FILENAME_EXT)
            return self.generate(prj_filename=prj_filename, dst_filename=dst_filename, **kwargs)
        elif convert_to.upper().endswith('SVG'):
            if dst_filename is None:
                dst_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(),
                                                        svg_func.SVG_FILENAME_EXT)
            return self.convertToSVG(prj_filename=prj_filename, svg_filename=dst_filename,
                                     auto_open=auto_open, **kwargs)
        else:
            log_func.warning(u'Not supported convert file <%s> to <%s>' % (prj_filename, convert_to))
        return False


def createLimeReportProjectFile(prj_filename, auto_open=False):
    """
    Create LimeReport LRXML project file.

    :param prj_filename: New LRXML project filename.
    :param auto_open: Automatic open new file in designer?
    :return: True/False.
    """
    manager = iqLimeReportManager()
    return manager.createProject(new_prj_filename=prj_filename, auto_open=auto_open)
