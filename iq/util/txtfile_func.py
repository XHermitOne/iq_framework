#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text file functions.
"""

import os
import os.path

from . import log_func
from . import global_func
from . import str_func
from . import file_func
from . import exec_func
from . import sys_func

__version__ = (0, 0, 5, 4)

DEFAULT_ENCODING = global_func.getDefaultEncoding()
DEFAULT_REPLACEMENTS = {u'"': u'\''}

DEFAULT_CSV_DELITEMER = u','
ALTER_CSV_DELIMETER = u';'

OPEN_LINUX_EDITOR_FMT = 'gedit \"%s\" &'
OPEN_WINDOWS_EDITOR_FMT = 'notepad.exe \"%s\"'

DEFAULT_TXT_FILE_ENCODING = 'utf-8'

BYTE_ORDER_MARK = '\ufeff'


def saveTextFile(txt_filename, txt='', rewrite=True, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Save text file.

    :param txt_filename: Text file name.
    :param txt: Body text file as unicode.
    :param rewrite: Rewrite file if it exists?
    :param encoding: Text file code page.
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

        # Check path
        txt_dirname = os.path.dirname(txt_filename)
        if not os.path.exists(txt_dirname):
            file_func.createDir(txt_dirname)

        file_obj = open(txt_filename, 'wt', encoding=encoding)
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal('Save text file <%s> error' % txt_filename)
    return False


def loadTextFile(txt_filename, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Load from text file.

    :param txt_filename: Text file name.
    :param encoding: Text file code page.
    :return: File text or empty text if error.
    """
    if not os.path.exists(txt_filename):
        log_func.warning(u'File <%s> not found' % txt_filename)
        return ''

    file_obj = None
    try:
        file_obj = open(txt_filename, 'rt', encoding=encoding)
        txt = file_obj.read()
        file_obj.close()
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Load text file <%s> error' % txt_filename)
        return ''

    return txt


def appendTextFile(txt_filename, txt, cr=None, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Add lines to text file.
    If the file does not exist, then the file is created.

    :param txt_filename: Text filename.
    :param txt: Added text.
    :param cr: Carriage return character.
    :param encoding: Text file code page.
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
        # Check path
        txt_dirname = os.path.dirname(txt_filename)
        if not os.path.exists(txt_dirname):
            file_func.createDir(txt_dirname)

        file_obj = open(txt_filename, 'at', encoding=encoding)
        file_obj.write(cr)
        file_obj.write(txt)
        file_obj.close()
        return True
    except:
        if file_obj:
            file_obj.close()
        log_func.fatal(u'Error append to text file <%s>' % txt_filename)
    return False


def replaceTextFile(txt_filename, src_text, dst_text, auto_add=True, cr=None, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Replacing a text in a text file.

    :param txt_filename: Text filename.
    :param src_text: Source text.
    :param dst_text: Destination text.
    :param auto_add: A flag to automatically add a new line.
    :param cr: Carriage return character.
    :param encoding: Text file code page.
    :return: True/False.
    """
    if cr is None:
        cr = os.linesep

    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt', encoding=encoding)
            txt = file_obj.read()
            file_obj.close()
            txt = txt.replace(src_text, dst_text)
            if auto_add and (dst_text not in txt):
                txt += cr
                txt += dst_text
                log_func.info('Text file append <%s> in <%s>' % (dst_text, txt_filename))
            file_obj = None
            file_obj = open(txt_filename, 'wt', encoding=encoding)
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


def isInTextFile(txt_filename, find_text, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Is there text in a text file?

    :param txt_filename: Text filename.
    :param find_text: Find text.
    :param encoding: Text file code page.
    :return: True/False.
    """
    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt', encoding=encoding)
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


def searchLinesInTextFile(txt_filename, search_text, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Search lines in text file by text.
    Is there text in a text file?

    :param txt_filename: Text filename.
    :param search_text: Search text.
    :param encoding: Text file code page.
    :return: Lines list or None if error.
    """
    txt_filename = os.path.normpath(txt_filename)

    if os.path.exists(txt_filename):
        file_obj = None
        try:
            file_obj = open(txt_filename, 'rt', encoding=encoding)
            lines = file_obj.readlines()
            file_obj.close()
            result = [line for line in lines if search_text in line]
            file_obj = None
            return result
        except:
            if file_obj:
                file_obj.close()
            log_func.fatal('Error search lines <%s> in text file <%s>' % (search_text, txt_filename))
    else:
        log_func.warning('Text file <%s> not exists' % txt_filename)
    return None


def readTextFileLines(txt_filename, auto_strip_line=True, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Read text file as lines.

    :param txt_filename: Text filename.
    :param auto_strip_line: Strip text file lines automatic?
    :param encoding: Text file code page.
    :return: Text file lines.
    """
    file_obj = None
    lines = list()

    if not os.path.exists(txt_filename):
        # If not exists file then create it
        log_func.warning(u'File <%s> not found' % txt_filename)

        try:
            file_obj = open(txt_filename, 'wt', encoding=encoding)
            file_obj.close()
            log_func.info(u'Create text file <%s>' % txt_filename)
        except:
            if file_obj:
                file_obj.close()
            log_func.fatal(u'Error create text file <%s>' % txt_filename)
        return lines

    try:
        file_obj = open(txt_filename, 'rt', encoding=encoding)
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


def appendTextFileLine(line, txt_filename=None, add_linesep=True, encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Add new line in text file.

    :param line: Line as string.
    :param txt_filename: Text filename.
    :param add_linesep: Add line separator / carriage return?
    :param encoding: Text file code page.
    :return: True/False.
    """
    file_obj = None
    try:
        # Check path
        txt_dirname = os.path.dirname(txt_filename)
        if not os.path.exists(txt_dirname):
            file_func.createDir(txt_dirname)

        file_obj = open(txt_filename, 'at+', encoding=encoding)
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


def saveCSVFile(csv_filename, records=(),
                delim=DEFAULT_CSV_DELITEMER, encoding=DEFAULT_TXT_FILE_ENCODING,
                replacements=None):
    """
    Save CSV file.

    :param csv_filename: CSV filename.
    :param records: Record list.
        Each record is a list of field values.
    :param delim: Separator character.
    :param encoding: Result file encoding.
    :param replacements: Dictionary of automatic field value substitutions.
    :return: True/False.
    """
    global DEFAULT_REPLACEMENTS
    if replacements is None:
        replacements = DEFAULT_REPLACEMENTS
        if delim not in replacements:
            replacements[delim] = ALTER_CSV_DELIMETER if delim == DEFAULT_CSV_DELITEMER else (DEFAULT_CSV_DELITEMER if delim == ALTER_CSV_DELIMETER else DEFAULT_CSV_DELITEMER)
    prepare_records = [[str_func.replaceInText(str_func.toUnicode(field, encoding), replacements) for field in record] for record in records]
    txt = u'\n'.join([delim.join(record) for record in prepare_records])
    return saveTextFile(csv_filename, txt)


def loadCSVFile(csv_filename, delim=u',', encoding=DEFAULT_TXT_FILE_ENCODING):
    """
    Load CSV file as record list.

    :param csv_filename: CSV filename.
    :param delim: Separator character.
    :param encoding: Text file code page.
    :return: Record list.
        Each record is a list of field values.
        Or None if error.
    """
    if not os.path.exists(csv_filename):
        log_func.warning(u'File <%s> not found' % csv_filename)
        return None

    txt = loadTextFile(csv_filename, encoding=encoding)
    if txt:
        txt = txt.strip()
        # Delete Byte Order Mark
        if txt.startswith(BYTE_ORDER_MARK):
            txt = txt.lstrip(BYTE_ORDER_MARK)

        try:
            records = list()
            txt_lines = txt.split(u'\n')
            for txt_line in txt_lines:
                if txt_line:
                    record = [str_func.parseWiseTypeStr(field) for field in txt_line.split(delim)]
                    records.append(record)
            return records
        except:
            log_func.fatal(u'Error convert CSV file <%s> to record list' % csv_filename)
    return None


def openEditorTxtFileLinux(txt_filename):
    """
    Open text file in editor. Linux OS.

    :param txt_filename: Text file name.
    :return: True/False.
    """
    try:
        if not os.path.exists(txt_filename):
            log_func.warning(u'Open in editor text file <%s> not found' % txt_filename)
            return False

        cmd = OPEN_LINUX_EDITOR_FMT % txt_filename
        return exec_func.execSystemCommand(cmd)
    except:
        log_func.fatal(u'Error open text file <%s> in editor' % txt_filename)
    return False


def openEditorTxtFileWindows(txt_filename):
    """
    Open text file in editor. Windows OS.

    :param txt_filename: Text file name.
    :return: True/False.
    """
    try:
        if not os.path.exists(txt_filename):
            log_func.warning(u'Open in editor text file <%s> not found' % txt_filename)
            return False

        cmd = OPEN_WINDOWS_EDITOR_FMT % txt_filename
        return exec_func.execSystemCommand(cmd)
    except:
        log_func.fatal(u'Error open text file <%s> in editor' % txt_filename)
    return False


def openEditorTxtFile(txt_filename):
    """
    Open text file in editor.

    :param txt_filename: Text file name.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        return openEditorTxtFileLinux(txt_filename)
    elif sys_func.isWindowsPlatform():
        return openEditorTxtFileWindows(txt_filename)
    else:
        log_func.warning(u'Open text file in editor. Not supported platform')
    return False
