#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web browser control functions module.
"""

import webbrowser

from . import log_func
from . import exec_func

__version__ = (0, 1, 1, 1)


def openHtmlBrowser(html_filename=None):
    """
    Open default HTML browser.

    :param html_filename: HTML filename.
    :return: True/False
    """
    if html_filename:
        cmd_fmt = 'open %s'
        cmd = cmd_fmt % html_filename
        return exec_func.execSystemCommand(cmd)
    else:
        log_func.warning(u'Not define HTML file for view')
    return False


def getDefaultWebBrowserName():
    """
    Get default WEB browser name.
    """
    try:
        browser = webbrowser.get()
        return browser.name
    except:
        log_func.fatal(u'Error get default web browser name')
    return 'firefox'


def getDefaultWebBrowserBaseName():
    """
    Get default WEB browser basename.
    """
    try:
        browser = webbrowser.get()
        return browser.basename
    except:
        log_func.fatal(u'Error get default web browser basename')
    return 'firefox'


def openWebBrowserURL(url):
    """
    Open URL in default web browser.

    :param url: URL. For example http://localhost:8080
    :return: True/False.
    """
    try:
        return webbrowser.open(url)
    except:
        log_func.fatal(u'Error open URL <%s> in default web browser' % url)
    return False
