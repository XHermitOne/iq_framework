#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migrate python files.
"""

import sys
import os
import os.path

import mtranslate

from ..util import log_func

__version__ = (0, 0, 0, 1)


STARTSWITH_SIGNATURE = '..)'
ENDSWITH_SIGNATURE = '(..'
CONTAIN_SIGNATURE = '(..)'

COMMENT_COMMAND_SIGNATURE = '#'

PREV_TRANSLATE_REPLACES = (
                    )

POST_TRANSLATE_REPLACES = (
                    )

MIGRATE_REPLACES = (dict(compare=STARTSWITH_SIGNATURE, src='log.', dst='log_func.'),
                    )

DO_TRANSLATE = True

DEFAULT_SRC_LANG = 'ru'
DEFAULT_DST_LANG = 'en'


def isNotEnglishText(text):
    """
    Is this not an English text?
    """
    if isinstance(text, str):
        not_english = any([ord(c) > 128 for c in text])
        return not_english
    # Not string
    return False


def _replaceMigrateLine(line, replacement_src, replacement_dst):
    """
    Replace the module line.

    :param line: Module line string.
    :param replacement_src: Original replacement.
    :param replacement_dst: Resulting replacement.
    :return: Modified module string.
    """
    if replacement_dst == COMMENT_COMMAND_SIGNATURE:
        log_func.info(u'Line <%s> commented out' % line)
        return COMMENT_COMMAND_SIGNATURE + line
    log_func.info(u'Replace <%s> to <%s> in line <%s>' % (replacement_src, replacement_dst, line))
    return line.replace(replacement_src, replacement_dst)


def _replacesMigrateLine(line, replaces):
    """
    Make line replacements.

    :param line: Module line string.
    :param replaces: Replacement list.
    :return: Modified module line.
    """
    for replacement in replaces:
        signature = replacement.get('compare', None)
        if signature == STARTSWITH_SIGNATURE and line.startswith(replacement['src']):
            line = _replaceMigrateLine(line, replacement['src'], replacement['dst'])
        elif signature == ENDSWITH_SIGNATURE and line.endswith(replacement['src']):
            line = _replaceMigrateLine(line, replacement['src'], replacement['dst'])
        elif signature == CONTAIN_SIGNATURE and replacement['src'] in line:
            line = _replaceMigrateLine(line, replacement['src'], replacement['dst'])
    return line


def migrateTxtFile(txt_filename, do_translate=True,
                   migrate_replaces=MIGRATE_REPLACES,
                   prev_translate_replaces=PREV_TRANSLATE_REPLACES,
                   post_translate_replaces=POST_TRANSLATE_REPLACES):
    """
    Make python module migration replacements.

    :param txt_filename: Text file path.
    :param do_translate: Automatically translate into English?
    :return: True/False.
    """
    if not os.path.exists(txt_filename):
        log_func.warning(u'File <%s> not found' % txt_filename)
        return False

    # Read lines
    lines = list()
    file_obj = None
    try:
        file_obj = open(txt_filename, 'rt')
        lines = file_obj.readlines()
        file_obj.close()
    except:
        log_func.fatal(u'Error read text file <%s> for migration' % txt_filename)
        if file_obj:
            file_obj.close()
        return False

    # Replaces
    for i, line in enumerate(lines):
        new_line = line
        if do_translate and isNotEnglishText(new_line):
            if prev_translate_replaces:
                new_line = _replacesMigrateLine(new_line, prev_translate_replaces)
            new_line = mtranslate.translate(new_line, DEFAULT_DST_LANG, DEFAULT_SRC_LANG)
            if post_translate_replaces:
                new_line = _replacesMigrateLine(new_line, post_translate_replaces)

        new_line = _replacesMigrateLine(new_line, migrate_replaces)
        lines[i] = new_line

    # Write lines
    file_obj = None
    try:
        file_obj = open(txt_filename, 'wt')
        file_obj.writelines(lines)
        file_obj.close()
        return True
    except:
        log_func.fatal(u'Error write text file <%s> for migration' % txt_filename)
        if file_obj:
            file_obj.close()
    return False


def migratePy(py_filename, *args, **kwargs):
    """
    Make python module migration replacements.

    :param py_filename: Python file path.
    :return: True/False.
    """
    if not os.path.exists(py_filename) or not os.path.isfile(py_filename):
        log_func.warning(u'Python file <%s> not found' % py_filename)
        return False

    result = migrateTxtFile(py_filename, migrate_replaces=MIGRATE_REPLACES, *args, **kwargs)
    if result:
        log_func.info(u'Migration Python module <%s> ... OK' % py_filename)
    else:
        log_func.warning(u'Migration Python module <%s> ... FAIL' % py_filename)
    return result


if __name__ == '__main__':
    migratePy(*sys.argv[1:])
