#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pandas DataFrame object view functions.
"""

import os.path

from iq.util import webbrowser_func
from . import log_func
from . import url_func
from . import txtgen_func
from . import file_func

# try:
#     import dtale
# except ImportError:
#     log_func.error(u'ImportError: <dtale> library not available')
#     log_func.error(u'Install: pip3 install dtale')


__version__ = (0, 0, 0, 1)

HTML_FILENAME_EXT = '.html'


def openDataFrameWebBrowser(dataframe):
    """
    Open pandas DataFrame as HTML in Web Browser.

    :param dataframe: Pandas DataFrame object.
    :return: True/False.
    """
    try:
        html_filename = file_func.setFilenameExt(file_func.getTempFilename(), HTML_FILENAME_EXT)
        if writeDataFrameToHTML(dataframe=dataframe, html_filename=html_filename):
            url = 'file://%s' % html_filename
            if isinstance(url, str):
                log_func.info(u'Show DataFrame object in Web Browser. URL <%s>' % url)
                return webbrowser_func.openWebBrowserURL(url)
            else:
                log_func.warning(u'Not define URL for view DataFrame')
    except:
        log_func.fatal(u'Error show DataFrame object in Web Browser')
    return False


def writeDataFrameToHTML(dataframe, html_filename=None):
    """
    Write pandas DataFrame object to HTML file.

    :param dataframe: pandas.DataFrame object.
    :param html_filename: HTML filename. If not define then generate template filename.
    :return: True/False.
    """
    if html_filename is None:
        html_filename = file_func.setFilenameExt(file_func.getTempFilename(), HTML_FILENAME_EXT)

    try:
        dataframe.to_html(html_filename)
        return os.path.exists(html_filename)
    except:
        log_func.fatal(u'Error write DataFrame to HTML file <%s>' % html_filename)
    return False

