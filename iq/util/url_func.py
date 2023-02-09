#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Url connection functions.
"""

import traceback

try:
    import urllib.request
except ImportError:
    pass

try:
    import urllib.parse
except ImportError:
    pass

try:
    import webbrowser
except ImportError:
    print(u'Error import webbrowser')

from . import log_func
from . import exec_func

__version__ = (0, 0, 2, 1)

DEFAULT_WEBBROWSER_CMD_FMT = '%s %s &'


def validURL(url):
    """
    URL availability check.

    :param url: URL. For example http://localhost:8080
    :return: True/False.
    """
    try:
        response = urllib.request.urlopen(url)
        return response.getcode() == 200
    except:
        # error_txt = traceback.format_exc()
        pass
    return False


def getNotValidURLErrTxt(url):
    """
    Get error message if not available URL.

    :param url: URL. For example http://localhost:8080
    :return: Error message or empty string if not error.
    """
    error_txt = u''
    try:
        response = urllib.request.urlopen(url)
        response_code = response.getcode()
        if response_code == 200:
            pass
        else:
            error_txt = u'Availability check URL <%s>. Result code <%d>' % (url, response_code)
    except:
        error_txt = u'Error availability check URL <%s>\n%s' % (url, traceback.format_exc())
    return error_txt


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
    web_vrowser_basename = getDefaultWebBrowserBaseName()
    cmd = DEFAULT_WEBBROWSER_CMD_FMT % (web_vrowser_basename, url)
    return exec_func.execSystemCommand(cmd)


def splitURL(url):
    """
    Split URL to list.

    :param url: URL. For example http://localhost:8080/path/to/resource.
    :return: URL list. For example ['http', 'localhost:8080', 'path', 'to', 'resource'].
    """
    parse_result = urllib.parse.urlparse(url)
    return [parse_result.scheme, parse_result.netloc] + parse_result.path.split('/')


def joinURL(url_as_list):
    """
    Join list to URL.

    :param url_as_list: URL list. For example ['http', 'localhost:8080', 'path', 'to', 'resource'].
    :return: URL as string. For example http://localhost:8080/path/to/resource.
    """
    assert isinstance(url_as_list, (list, tuple)) or (len(url_as_list) < 2), u'Incorrect type url_as_list <%s>' % url_as_list.__class__.__name__

    parse_result = urllib.parse.ParseResult(scheme=str(url_as_list[0]),
                                            netloc=str(url_as_list[1]),
                                            path='/'.join([str(item) for item in url_as_list[2:]]),
                                            params='', query='', fragment='')
    return parse_result.geturl()
