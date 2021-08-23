#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF to SVG convert functions.
"""

import os.path
from . import log_func
from . import exec_func
from . import file_func
from . import sys_func

__version__ = (0, 0, 0, 1)

DEFAULT_PDF2SVG_CONVERT_EXEC = 'pdf2svg'
SVG_FILENAME_EXT = '.svg'


def pdf2svg(pdf_filename, svg_filename=None, page=1):
    """
    Convert PDF file to SVG.

    :param pdf_filename: PDF filename.
    :param svg_filename: Destination SVG filename.
    :param page: Number of PDF pages for converting.
    :return: True/False.
    """
    if not os.path.exists(pdf_filename):
        log_func.warning(u'PDF file <%s> not found for convert to SVG' % pdf_filename)
        return False

    if svg_filename is None:
        svg_filename = file_func.setFilenameExt(file_func.getPrjProfileTempFilename(), SVG_FILENAME_EXT)

    try:
        if sys_func.isLinuxPlatform():
            cmd = '%s %s %s %s' % (DEFAULT_PDF2SVG_CONVERT_EXEC,
                                   pdf_filename,
                                   svg_filename,
                                   page)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Convert PDF <%s> to SVG <%s> not supported on Windows platform' % (pdf_filename,
                                                                                                  svg_filename))
    except:
        log_func.fatal(u'Error convert PDF file <%s> to SVG file <%s>' % (pdf_filename, svg_filename))
    return False
