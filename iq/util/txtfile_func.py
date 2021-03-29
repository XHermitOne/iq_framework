#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file functions.
"""

import os
import os.path

from . import log_func

__version__ = (0, 0, 2, 1)


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


def appendTextFile(txt_filename, txt, cr=None):
    """
    Add lines to text file.
    If the file does not exist, then the file is created.

    :param txt_filename: Text filename.
    :param txt: Added text.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

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


def replaceTextFile(txt_filename, src_text, dst_text, auto_add=True, cr=None):
    """
    Replacing a text in a text file.

    :param txt_filename: Text filename.
    :param src_text: Source text.
    :param dst_text: Destination text.
    :param auto_add: A flag to automatically add a new line.
    :param cr: Carriage return character.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            file_obj.close()
            txt = txt.replace(src_text, dst_text)
            if auto_add and (dst_text not in txt):
                txt += cr
                txt += dst_text
                log_func.info('Text file append <%s> in <%s>' % (dst_text, txt_filename))
            file_obj = None
            file_obj = open(txt_filename, 'wt')
            file_obj.write(txt)
            file_obj.close()
            file_obj = None
            return True
        except:
            if file_obj:
                file_obj.close()
            log_func.fatal('Error replace in text file <%s>' % txt_filename)
    else:
        log_func.warning('Text file <%s> not exists' % txt_filename)
    return False


def isInTextFile(txt_filename, find_text):
    """
    Is there text in a text file?

    :param txt_filename: Text filename.
    :param find_text: Find text.
    :return: True/False.
    """
    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt')
            txt = file_obj.read()
            result = find_text in txt
            file_obj.close()
            file_obj = None
            return result
        except:
            if file_obj:
                file_obj.close()
            log_func.fatal('Error find <%s> in text file <%s>' % (find_text, txt_filename))
    else:
        log_func.warning('Text file <%s> not exists' % txt_filename)
    return False


def readTextFileLines(txt_filename, auto_strip_line=True):
    """
    Read text file as lines.

    :param txt_filename: Text filename.
    :param auto_strip_line: Strip text file lines automatic?
    :return: Text file lines.
    """
    file_obj = None
    lines = list()

    if not os.path.exists(txt_filename):
        # If not exists file then create it
        log_func.warning(u'File <%s> not found' % txt_filename)

        try:
            file_obj = open(txt_filename, 'wt')
            file_obj.close()
            log_func.info(u'Create text file <%s>' % txt_filename)
        except:
            if file_obj:
                file_obj.close()
            log_func.fatal(u'Error create text file <%s>' % txt_filename)
        return lines

    try:
        file_obj = open(txt_filename, 'rt')
        lines = file_obj.readlines()
        if auto_strip_line:
            lines = [filename.strip() for filename in lines]
        file_obj.close()
        file_obj = None
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Error read text file <%s>' % txt_filename)
    return list(lines)


def appendTextFileLine(line, txt_filename=None, add_linesep=True):
    """
    Add new line in text file.

    :param line: Line as string.
    :param txt_filename: Text filename.
    :param add_linesep: Add line separator / carriage return?
    :return: True/False.
    """
    file_obj = None
    try:
        file_obj = open(txt_filename, 'at+')
        file_obj.write(str(line))
        if add_linesep:
            file_obj.write(os.linesep)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Error add line in text file <%s>' % txt_filename)
    return False
