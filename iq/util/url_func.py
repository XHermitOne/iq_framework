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

__version__ = (0, 0, 0, 1)


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
