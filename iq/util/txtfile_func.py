#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file functions.
"""

import os
import os.path

from . import log_func

__version__ = (0, 0, 0, 1)


def saveTextFile(txt_filename, txt='', rewrite=True):
    """
    Save text file.

    :param txt_filename: Text file name.
    :param txt: Body text file as unicode.
    :param rewrite: Rewrite file if it exists?
    :return: True/False.
    """
    file_obj = None
    try:
        if rewrite and os.path.exists(txt_filename):
            os.remove(txt_filename)
            log_func.info(u'Remove file <%s>' % txt_filename)
        if not rewrite and os.path.exists(txt_filename):
            log_func.warning(u'File <%s> not saved' % txt_filename)
            return False

        file_obj = open(txt_filename, 'wt')
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal('Save text file <%s> error' % txt_filename)
    return False


def loadTextFile(txt_filename):
    """
    Load from text file.

    :param txt_filename: Text file name.
    :return: File text or empty text if error.
    """
    if not os.path.exists(txt_filename):
        log_func.warning(u'File <%s> not found' % txt_filename)
        return ''

    f = None
    try:
        f = open(txt_filename, 'rt')
        txt = f.read()
        f.close()
    except:
        if f:
            f.close()
        log_func.fatal(u'Load text file <%s> error' % txt_filename)
        return ''

    return txt
