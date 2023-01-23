#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF file functions.
"""

import os.path

from . import log_func
from . import sys_func
from . import exec_func

__version__ = (0, 0, 0, 1)


PDF_FILENAME_EXT = '.pdf'

DEFAULT_PDF_VIEWER = 'evince'
DEFAULT_PDF_PRINT_SYSTEM = 'lpr'


def viewPDF(pdf_filename):
    """
    View PDF file in viewer.

    :param pdf_filename: PDF filename.
    :return: True/False.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning(u'PDF file <%s> not found' % pdf_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = '%s %s &' % (DEFAULT_PDF_VIEWER, pdf_filename)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Not support view PDF file <%s> on Windows platform' % pdf_filename)
    except:
        log_func.fatal(u'Error view PDF file <%s>' % pdf_filename)
    return False


def printPDF(pdf_filename, printer_name=None):
    """
    Print PDF file.

    :param pdf_filename: PDF filename.
    :param printer_name: Printer name.
    :return: True/False.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning(u'PDF file <%s> not found' % pdf_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            if printer_name:
                cmd = '%s -o fit-to-page -P "%s" %s' % (DEFAULT_PDF_PRINT_SYSTEM, printer_name, pdf_filename)
            else:
                cmd = '%s -o fit-to-page %s' % (DEFAULT_PDF_PRINT_SYSTEM, pdf_filename)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Not support print PDF file <%s> on Windows platform' % pdf_filename)
    except:
        log_func.fatal(u'Error print PDF file <%s>. Printer <%s>' % (pdf_filename, printer_name))
    return False

