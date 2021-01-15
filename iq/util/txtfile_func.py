#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file functions.
"""

import os
import os.path

from . import log_func

__version__ = (0, 0, 1, 1)


def saveTextFile(txt_filename, txt='', rewrite=True):
    """
    Save text file.

    :param txt_filename: Text file name.
    :param txt: Body text file as unicode.
    :param rewrite: Rewrite file if it exists?
    :return: True/False.
    """
    if not isinstance(txt, str):
        txt = str(txt)

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

    file_obj = None
    try:
        file_obj = open(txt_filename, 'rt')
        txt = file_obj.read()
        file_obj.close()
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Load text file <%s> error' % txt_filename)
        return ''

    return txt


def appendTextFile(txt_filename, txt, cr='\n'):
    """
    Add lines to text file.
    If the file does not exist, then the file is created.

    :param txt_filename: Text filename.
    :param txt: Added text.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if not isinstance(txt, str):
        txt = str(txt)

    txt_filename = os.path.normpath(txt_filename)

    if not os.path.exists(txt_filename):
        cr = ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'at')
        file_obj.write(cr)
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Error append to text file <%s>' % txt_filename)
    return False
