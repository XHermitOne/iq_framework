#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XLSX file to XLS file convert functions.
"""

from . import log_func
from . import file_func
from . import sys_func
from . import exec_func

__version__ = (0, 0, 0, 1)

XLSX_FILENAME_EXT = '.xlsx'
XLS_FILENAME_EXT = '.xls'
CONVERT_CMD_FMT = 'unoconv --format=xls --output=%s %s'


def xlsx2xls(xlsx_filename, xls_filename=None):
    """
    XLSX file to XLS file convert function.

    :param xlsx_filename: XLSX source filename.
    :param xls_filename: XLS destination filename.
    :return: True/False.
    """
    if xls_filename is None:
        xls_filename = file_func.setFilenameExt(xlsx_filename, XLS_FILENAME_EXT)
    try:
        return _xlsx2xls(xlsx_filename=xlsx_filename, xls_filename=xls_filename)
    except:
        log_func.fatal(u'Error convert XLSX file <%s> to XLS file <%s>' % (xlsx_filename, xls_filename))
    return False


def _xlsx2xls(xlsx_filename, xls_filename):
    """
    XLSX file to XLS file convert function.

    :param xlsx_filename: XLSX source filename.
    :param xls_filename: XLS destination filename.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        cmd = CONVERT_CMD_FMT % (xls_filename, xlsx_filename)
        exec_func.execSystemCommand(cmd)
        return True
    else:
        log_func.warning(u'Not support platform <%s> for convert XLSX file <%s> to XLS file <%s>' % (sys_func.getPlatform(),
                                                                                                     xlsx_filename,
                                                                                                     xls_filename))
    return False
