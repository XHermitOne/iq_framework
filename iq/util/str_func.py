#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Strings and text manipulate functions.
"""

import encodings.aliases

from . import log_func

__version__ = (0, 0, 0, 1)


def getEncodings():
    """
    Supported code page list.
    """
    try:
        encode_list = [str(code).lower() for code in encodings.aliases.aliases.values()]
        result = list()
        for code in encode_list:
            if code not in result:
                result.append(code)
        result.sort()
        return tuple(result)
    except:
        return 'utf_8',


def replaceUpper2Lower(txt):
    """
    Replacing uppercase letters in a string with underscores
    except the first character.

    :param txt: Text string as AbcdEfghIklmn.
    :return: Modified text as abcd_efgh_iklmn.
    """
    if not isinstance(txt, str):
        txt = str(txt)

    txt = ''.join([symb.lower() if i and symb.isupper() and txt[i-1].isupper() else symb for i, symb in enumerate(list(txt))])
    return ''.join([('_'+symb.lower() if symb.isupper() and i else symb.lower()) for i, symb in enumerate(list(txt))])


INDENT = '    '


def data2txt(data, level=0):
    """
    Translation of a dictionary-list structure into formatted text.

    :param data: Vocabulary list structure.
    :param level: Nesting level.
    :return: Formatted text.
    """
    txt = ''
    try:
        if isinstance(data, list):
            txt = txt + '\n' + level * INDENT + '[\n'
            for obj in data:
                txt += level * INDENT
                txt += data2txt(obj, level + 1)
                txt += ',\n'
            if len(data) != 0:
                txt = txt[:-2]
            txt = txt + '\n' + level * INDENT + ']'
        elif isinstance(data, dict):
            txt = txt + '\n' + level * INDENT + '{\n'
            keys = data.keys()
            values = data.values()
            for key in keys:
                txt = txt + level * INDENT + '\'' + key + '\':'
                txt += data2txt(data[key], level + 1)
                txt += ',\n'
            if len(keys) != 0:
                txt = txt[:-2]
            txt = txt + '\n' + level * INDENT + '}'
        elif isinstance(data, str):
            # Check for quotes
            txt = txt + '\'' + data.replace('\'',
                                            '\\\'').replace('\'',
                                                            '\\\'').replace('\r',
                                                                            '\\r').replace('\n',
                                                                                           '\\n').replace('\t',
                                                                                                          '\\t') + '\''
        else:
            txt = txt + str(data)

        # Remove first carriage return
        if txt[0] == '\n' and (not level):
            txt = txt[1:]
    except:
        log_func.fatal(u'Error transform data to text. Level <%d>' % level)
    return txt
