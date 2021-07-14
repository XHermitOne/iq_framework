#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XLSX file to ODS file convert functions.
"""

from . import log_func
from . import file_func
from . import sys_func
from . import exec_func

__version__ = (0, 0, 0, 1)

XLSX_FILENAME_EXT = '.xlsx'
ODS_FILENAME_EXT = '.ods'
CONVERT_CMD_FMT = 'unoconv --format=ods --output=%s %s'


def xlsx2ods(xlsx_filename, ods_filename=None):
    """
    XLSX file to ODS file convert function.

    :param xlsx_filename: XLSX source filename.
    :param ods_filename: ODS destination filename.
    :return: True/False.
    """
    if ods_filename is None:
        ods_filename = file_func.setFilenameExt(xlsx_filename, ODS_FILENAME_EXT)
    try:
        return _xlsx2ods(xlsx_filename=xlsx_filename, ods_filename=ods_filename)
    except:
        log_func.fatal(u'Error convert XLSX file <%s> to ODS file <%s>' % (xlsx_filename, ods_filename))
    return False


def _xlsx2ods(xlsx_filename, ods_filename):
    """
    XLSX file to ODS file convert function.

    :param xlsx_filename: XLSX source filename.
    :param ods_filename: ODS destination filename.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        cmd = CONVERT_CMD_FMT % (ods_filename, xlsx_filename)
        exec_func.execSystemCommand(cmd)
        return True
    else:
        log_func.warning(u'Not support platform <%s> for convert XLSX file <%s> to ODS file <%s>' % (sys_func.getPlatform(),
                                                                                                     xlsx_filename,
                                                                                                     ods_filename))
    return False
