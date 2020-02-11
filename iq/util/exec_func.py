#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execute functions module.
"""

import os

from . import log_func

__version__ = (0, 0, 0, 1)


def execSystemCommand(cmd=''):
    """
    Execute system command.

    :param cmd: Command string.
    :return: True/False.
    """
    if cmd:
        try:
            log_func.info(u'Run system command <%s>' % cmd)
            os.system(cmd)
            return True
        except:
            log_func.fatal(u'Execute system command <%s>' % cmd)
    else:
        log_func.warning(u'Not define system command')
    return False


def openHtmlBrowser(html_filename=None):
    """
    Open default HTML browser.

    :param html_filename: HTML filename.
    :return: True/False
    """
    if html_filename:
        cmd_fmt = 'open %s'
        cmd = cmd_fmt % html_filename
        return execSystemCommand(cmd)
    else:
        log_func.warning(u'Not define HTML file for view')
    return False
