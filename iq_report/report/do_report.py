#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report generator launch function module.
"""

import os
import os.path

from iq.util import log_func
from iq.util import res_func
from iq.util import str_func
from iq.util import file_func

from . import report_browser
from . import report_gen_func
from . import style_library


__version__ = (0, 0, 0, 1)

DEFAULT_REPORT_FILE_EXT = report_browser.REPORT_FILENAME_EXT


def getReportResourceFilename(report_filename='', report_dir=''):
    """
    Get the full file name of the report template.

    :param report_filename:The name of the report file in short form.
    :param report_dir: Report folder.
    :return: The full name of the report file.
    """
    # Check extension
    rprt_filename = report_filename
    if not rprt_filename.endswith(DEFAULT_REPORT_FILE_EXT):
        rprt_filename = os.path.splitext(rprt_filename)[0]+DEFAULT_REPORT_FILE_EXT

    # Check the relevance of the template
    full_src_filename = getPathFilename(report_filename, report_dir)
    full_rprt_filename = getPathFilename(rprt_filename, report_dir)
    if isNewReportTemplateFile(full_src_filename, full_rprt_filename):
        # If the original template is changed later than the working
        # template file <rprt> then you need to make changes
        updateReportTemplateFile(full_src_filename, full_rprt_filename)

    if os.path.exists(rprt_filename):
        # Check can be given an absolute file name
        filename = rprt_filename
    else:
        # The relative file name relative to the report
        # folder is most likely set
        filename = full_rprt_filename
        if not os.path.exists(filename):
            log_func.error(u'Report template file <%s> not found' % str(filename))
            filename = createReportResourceFile(filename)
    log_func.debug(u'Report te,plate filename <%s>' % str(filename))
    return filename


def getPathFilename(filename='', report_dir=''):
    """
    Get absolute report template filename.

    :param filename: Short report file name.
    :param report_dir: Report folder.
    :return: Absolute report template filename.
    """
    return file_func.getAbsolutePath(os.path.join(report_dir, filename))


def isNewReportTemplateFile(src_filename, rprt_filename):
    """
    Check the relevance of the template.
    If the original template is changed later than the working * .rprt
    template file, then you need to make changes.

    :return: True-changes to the original template/False-no changes.
    """
    src_modify_dt = file_func.getFileModifyDatetime(src_filename)
    rprt_modify_dt = file_func.getFileModifyDatetime(rprt_filename)
    if src_modify_dt and rprt_modify_dt:
        return src_modify_dt > rprt_modify_dt
    return False


def updateReportTemplateFile(src_filename, rprt_filename):
    """
    Update the report template.

    :param src_filename: The name of the source template file.
    :param rprt_filename: The name of the resulting template file is * .rprt.
    :return: Corrected name of the created template file or None in case of error.
    """
    # Delete destination file
    file_func.removeFile(rprt_filename)
    # Delete all intermediate files
    for ext in report_gen_func.SRC_REPORT_EXT:
        src_ext = os.path.splitext(src_filename)[1].lower()
        if src_ext != ext:
            filename = os.path.splitext(src_filename)[0] + ext
            if os.path.exists(filename):
                file_func.removeFile(filename)
    # Recreate template
    return createReportResourceFile(rprt_filename)


def createReportResourceFile(template_filename):
    """
    Create a resource file for the template by the name of the requested.

    :param template_filename: The name of the requested template file.
    :return: Corrected name of created template file or None in case of error.
    """
    dir_name = os.path.dirname(template_filename)
    base_filename = os.path.basename(template_filename).replace(' ', '_')
    base_filename = str_func.rus2lat(base_filename) if str_func.isRUSText(base_filename) else base_filename
    norm_tmpl_filename = os.path.join(dir_name, base_filename)

    log_func.info(u'Create new template file <%s>' % norm_tmpl_filename)
    # We consistently check which file can be taken as the basis for the template
    for ext in report_gen_func.SRC_REPORT_EXT:
        src_filename = os.path.splitext(template_filename)[0] + ext
        unicode_src_filename = str_func.toUnicode(src_filename)
        if os.path.exists(src_filename):
            # Yes, there is such a file and it can act as a source for the template
            log_func.info(u'Report template source found <%s>' % unicode_src_filename)
            try:
                rep_generator = report_gen_func.createReportGeneratorSystem(ext)
                return rep_generator.update(src_filename)
            except:
                log_func.fatal(u'Error converting report template <%s> -> <%s>' % (unicode_src_filename,
                                                                                   norm_tmpl_filename))
            return None

    log_func.error(u'Report template sources not found in folder <%s> for <%s>' % (dir_name,
                                                                                   str_func.toUnicode(os.path.basename(template_filename))))
    return None


def loadStyleLib(stylelib_filename=None):
    """
    Download style library from file.

    :param stylelib_filename: Style library file.
    :return: Style library.
    """
    stylelib = None
    if stylelib_filename:
        stylelib_filename = os.path.abspath(stylelib_filename)
        if os.path.exists(stylelib_filename):
            xml_stylelib = style_library.icXMLRepStyleLib()
            stylelib = xml_stylelib.convert(stylelib_filename)
    return stylelib


def openReportBrowser(parent_form=None, report_dir='', mode=report_browser.REPORT_EDITOR_MODE):
    """
    Launch report browser.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_dir: Directory where reports are stored.
    :return: True/False.
    """
    dlg = None
    try:
        dlg = report_browser.iqReportBrowserDialog(parent=parent_form, mode=mode,
                                                   report_dir=report_dir)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error starting report browser')
    return False


def openReportEditor(parent_form=None, report_dir=''):
    """
    Starting the report editor. Editor - browser mode.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_dir: Directory where reports are stored.
    :return: True/False.
    """
    return openReportBrowser(parent_form, report_dir, report_browser.REPORT_EDITOR_MODE)


def openReportViewer(parent_form=None, report_dir=''):
    """
    Starting the report viewer. Viewer - browser mode.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_dir: Directory where reports are stored.
    :return: True/False.
    """
    return openReportBrowser(parent_form, report_dir, report_browser.REPORT_VIEWER_MODE)


def printReport(parent_form=None, report_filename='', report_dir='',
                db_url=None, sql=None, command=None,
                stylelib_filename=None, variables=None):
    """
    The function starts the report generator and print output.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_filename: Report filename.
    :param report_dir: Directory where reports are stored.
    :param db_url: URL Connection string.
        For example:
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: SQL query text.
    :param command: After generation command. print/preview/export.
    :param stylelib_filename: Style library filename.
    :param variables: A dictionary of variables to populate the report.
    :return: True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            repgen_system = report_gen_func.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.Print(res_func.loadResource(report_filename),
                                       stylelib=stylelib,
                                       variables=variables)
    except:
        log_func.fatal(u'Report printing error <%s>' % report_filename)
    return False


def previewReport(parent_form=None, report_filename='', report_dir='',
                  db_url=None, sql=None, command=None,
                  stylelib_filename=None, variables=None):
    """
    The function starts the report generator and displays the preview screen.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_filename: Report filename.
    :param report_dir: Directory where reports are stored.
    :param db_url: URL Connection string.
        For example:
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: SQL query text.
    :param command: After generation command. print/preview/export.
    :param stylelib_filename: Style library filename.
    :param variables: A dictionary of variables to populate the report.
    :return: True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            repgen_system = report_gen_func.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.preview(res_func.loadResource(report_filename),
                                         stylelib=stylelib,
                                         variables=variables)
    except:
        log_func.fatal(u'Report preview error <%s>' % report_filename)
    return False


def exportReport(parent_form=None, report_filename='', report_dir='',
                 db_url=None, sql=None, command=None,
                 stylelib_filename=None, variables=None):
    """
    The function launches the report generator and output in Office.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_filename: Report filename.
    :param report_dir: Directory where reports are stored.
    :param db_url: URL Connection string.
        For example:
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: SQL query text.
    :param command: After generation command. print/preview/export.
    :param stylelib_filename: Style library filename.
    :param variables: A dictionary of variables to populate the report.
    :return: True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            repgen_system = report_gen_func.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.convert(res_func.loadResource(report_filename),
                                         stylelib=stylelib,
                                         variables=variables)
    except:
        log_func.fatal(u'Report export error <%s>' % report_filename)
    return False


def selectReport(parent_form=None, report_filename='', report_dir='',
                 db_url=None, sql=None, command=None,
                 stylelib_filename=None, variables=None):
    """
    The function starts the report generator with the subsequent choice of action.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_filename: Report filename.
    :param report_dir: Directory where reports are stored.
    :param db_url: URL Connection string.
        For example:
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: SQL query text.
    :param command: After generation command. print/preview/export.
    :param stylelib_filename: Style library filename.
    :param variables: A dictionary of variables to populate the report.
    :return: True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            repgen_system = report_gen_func.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.selectAction(res_func.loadResource(report_filename),
                                              stylelib=stylelib,
                                              variables=variables)
    except:
        log_func.fatal(u'Error generating report with action selection <%s>' % report_filename)
    return False


# Post-processing commands for the generated report
DO_COMMAND_PRINT = 'print'
DO_COMMAND_PREVIEW = 'preview'
DO_COMMAND_EXPORT = 'export'
DO_COMMAND_SELECT = 'select'


def doReport(parent_form=None, report_filename='', report_dir='', db_url='', sql='', command=None,
             stylelib_filename=None, variables=None):
    """
    The function starts the report generator.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_filename: Report filename.
    :param report_dir: Directory where reports are stored.
    :param db_url: URL Connection string.
        For example:
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: SQL query text.
    :param command: After generation command. print/preview/export.
    :param stylelib_filename: Style library filename.
    :param variables: A dictionary of variables to populate the report.
    :return: True/False.
    """
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            repgen_system = report_gen_func.getReportGeneratorSystem(report_filename, parent_form)
            stylelib = loadStyleLib(stylelib_filename)

            data = repgen_system.generate(res_func.loadResource(report_filename), db_url, sql,
                                          stylelib=stylelib, vars=variables)

            if command:
                command = command.lower()
                if command == DO_COMMAND_PRINT:
                    repgen_system.printResult(data)
                elif command == DO_COMMAND_PREVIEW:
                    repgen_system.previewResult(data)
                elif command == DO_COMMAND_EXPORT:
                    repgen_system.convertResult(data)
                elif command == DO_COMMAND_SELECT:
                    repgen_system.doSelectAction(data)
                else:
                    log_func.error(u'Not processed start command <%s>' % command)
            else:
                repgen_system.save(data)
        return True
    except:
        log_func.fatal(u'Error starting report generator <%s>' % report_filename)
