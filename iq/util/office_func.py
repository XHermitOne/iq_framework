#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control office filenames functions.
"""

import os.path
from . import log_func
from . import exec_func
from . import sys_func

__version__ = (0, 0, 1, 2)

OPEN_SPREADSHEET_LINUX_EXEC_FMT = 'libreoffice --calc %s &'

SOFFICE_WINDOWS_EXEC = 'C:\\Program Files\\LibreOffice\\program\\soffice.exe'
ALTER_SOFFICE_WINDOWS_EXEC = 'C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe'
OPEN_SPREADSHEET_WINDOWS_EXEC_FMT = '"%s" --calc %s &'

OPEN_DOCUMENT_LINUX_EXEC_FMT = 'libreoffice --writer %s &'
OPEN_DOCUMENT_WINDOWS_EXEC_FMT = '"%s" --writer %s &'

SPREADSHEET_FILENAME_EXT = ('.xls', '.xlsx', '.ods')
DOCUMENT_FILENAME_EXT = ('.doc', '.docx', '.odt')


def openSpreadsheetLibreOffice(spreadsheet_filename=None):
    """
    Open spreadsheet file in LibreOffice.

    :param spreadsheet_filename: Spreadsheet filename.
    :return: True/False.
    """
    if spreadsheet_filename is None:
        log_func.warning(u'Not define spreadsheet file for open')
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = OPEN_SPREADSHEET_LINUX_EXEC_FMT % spreadsheet_filename
        elif sys_func.isWindowsPlatform():
            if os.path.exists(SOFFICE_WINDOWS_EXEC):
                cmd = OPEN_SPREADSHEET_WINDOWS_EXEC_FMT % (SOFFICE_WINDOWS_EXEC, spreadsheet_filename)
            elif os.path.exists(ALTER_SOFFICE_WINDOWS_EXEC):
                cmd = OPEN_SPREADSHEET_WINDOWS_EXEC_FMT % (ALTER_SOFFICE_WINDOWS_EXEC, spreadsheet_filename)
            else:
                log_func.warning(u'Not found soffice.exe file')
                return False
        else:
            log_func.warning(u'Unsupported platform for open spreadsheet <%s>' % spreadsheet_filename)
            return False
        return exec_func.execSystemCommand(cmd)
    except:
        log_func.fatal(u'Error open spreadsheet <%s>' % spreadsheet_filename)
    return False


def openSpreadsheet(spreadsheet_filename=None):
    """
    Open spreadsheet.

    :param spreadsheet_filename: Spreadsheet filename.
    :return: True/False.
    """
    return openSpreadsheetLibreOffice(spreadsheet_filename=spreadsheet_filename)


def openDocumentLibreOffice(document_filename=None):
    """
    Open document file in LibreOffice.

    :param document_filename: Document filename.
    :return: True/False.
    """
    if document_filename is None:
        log_func.warning(u'Not define document file for open')
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = OPEN_DOCUMENT_LINUX_EXEC_FMT % document_filename
        elif sys_func.isWindowsPlatform():
            if os.path.exists(SOFFICE_WINDOWS_EXEC):
                cmd = OPEN_DOCUMENT_WINDOWS_EXEC_FMT % (SOFFICE_WINDOWS_EXEC, document_filename)
            elif os.path.exists(ALTER_SOFFICE_WINDOWS_EXEC):
                cmd = OPEN_DOCUMENT_WINDOWS_EXEC_FMT % (ALTER_SOFFICE_WINDOWS_EXEC, document_filename)
            else:
                log_func.warning(u'Not found soffice.exe file')
                return False
        else:
            log_func.warning(u'Unsupported platform for open document <%s>' % document_filename)
            return False
        return exec_func.execSystemCommand(cmd)
    except:
        log_func.fatal(u'Error open document <%s>' % document_filename)
    return False


def openDocument(document_filename=None):
    """
    Open document.

    :param document_filename: Document filename.
    :return: True/False.
    """
    return openDocumentLibreOffice(document_filename=document_filename)


def openInLibreOffice(filename):
    """
    Open filename in LibreOffice.

    :param filename: Full filename path
    :return: True/False.
    """
    filename_ext = os.path.splitext(filename)[1]
    if filename_ext:
        filename_ext = filename_ext.lower()
        if filename_ext in SPREADSHEET_FILENAME_EXT:
            return openSpreadsheet(spreadsheet_filename=filename)
        elif filename_ext in DOCUMENT_FILENAME_EXT:
            return openDocument(document_filename=filename)
        else:
            log_func.warning(u'Not supported file type <%s>' % filename_ext)
    else:
        log_func.warning(u'Not defined ext of filename <%s>' % filename)
    return False
