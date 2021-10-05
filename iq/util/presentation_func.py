#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Show presentation functions.
"""

import os.path
from . import log_func
from . import exec_func
from . import sys_func

__version__ = (0, 0, 0, 1)

SHOW_PRESENTATION_LINUX_EXEC_FMT = 'libreoffice --impress --show %s &'

SOFFICE_WINDOWS_EXEC = 'C:\\Program Files\\LibreOffice\\program\\soffice.exe'
ALTER_SOFFICE_WINDOWS_EXEC = 'C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe'
SHOW_PRESENTATION_WINDOWS_EXEC_FMT = '"%s" --impress --show %s &'


def showPresentationLibreOffice(presentation_filename=None):
    """
    Show presentation in LibreOffice.

    :param presentation_filename: Presentation filename.
    :return: True/False.
    """
    if presentation_filename is None:
        log_func.warning(u'Not define presentation file for show')
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = SHOW_PRESENTATION_LINUX_EXEC_FMT % presentation_filename
        elif sys_func.isWindowsPlatform():
            if os.path.exists(SOFFICE_WINDOWS_EXEC):
                cmd = SHOW_PRESENTATION_WINDOWS_EXEC_FMT % (SOFFICE_WINDOWS_EXEC, presentation_filename)
            elif os.path.exists(ALTER_SOFFICE_WINDOWS_EXEC):
                cmd = SHOW_PRESENTATION_WINDOWS_EXEC_FMT % (ALTER_SOFFICE_WINDOWS_EXEC, presentation_filename)
            else:
                log_func.warning(u'Not found soffice.exe file')
                return False
        else:
            log_func.warning(u'Unsupported platform for show presentation <%s>' % presentation_filename)
            return False
        return exec_func.execSystemCommand(cmd)
    except:
        log_func.fatal(u'Error show presentation <%s>' % presentation_filename)
    return False


def showPresentation(presentation_filename=None):
    """
    Show presentation.

    :param presentation_filename: Presentation filename.
    :return: True/False.
    """
    return showPresentationLibreOffice(presentation_filename=presentation_filename)
