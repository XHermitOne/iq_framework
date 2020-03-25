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


RU_ENCODINGS = {'UTF-8': 'utf-8',
                'CP1251': 'windows-1251',
                'KOI8-R': 'koi8-r',
                'IBM866': 'ibm866',
                'ISO-8859-5': 'iso-8859-5',
                'MAC': 'mac',
                }


def getCodepage(text=None):
    """
    Definition of text encoding.

    Function call example:
    print(RU_ENCODINGS[getCodepage(file('test.txt').read())])
    There is an alternative encoding definition (using chardet):
    a = 'sdfds'
    import chardet
    print(chardet.detect(a))
    {'confidence': 1.0, 'encoding': 'ascii'}
    a = 'any text'
    print(chardet.detect(a))
    {'confidence': 0.99, 'encoding': 'utf-8'}
    """
    uppercase = 1
    lowercase = 3
    utfupper = 5
    utflower = 7
    codepages = {}
    for enc in RU_ENCODINGS.keys():
        codepages[enc] = 0
    if text is not None and len(text) > 0:
        last_simb = 0
        for simb in text:
            simb_ord = ord(simb)

            # non-russian characters
            if simb_ord < 128 or simb_ord > 256:
                continue

            # UTF-8
            if last_simb == 208 and (143 < simb_ord < 176 or simb_ord == 129):
                codepages['UTF-8'] += (utfupper * 2)
            if (last_simb == 208 and (simb_ord == 145 or 175 < simb_ord < 192)) \
               or (last_simb == 209 and (127 < simb_ord < 144)):
                codepages['UTF-8'] += (utflower * 2)

            # CP1251
            if 223 < simb_ord < 256 or simb_ord == 184:
                codepages['CP1251'] += lowercase
            if 191 < simb_ord < 224 or simb_ord == 168:
                codepages['CP1251'] += uppercase

            # KOI8-R
            if 191 < simb_ord < 224 or simb_ord == 163:
                codepages['KOI8-R'] += lowercase
            if 222 < simb_ord < 256 or simb_ord == 179:
                codepages['KOI8-R'] += uppercase

            # IBM866
            if 159 < simb_ord < 176 or 223 < simb_ord < 241:
                codepages['IBM866'] += lowercase
            if 127 < simb_ord < 160 or simb_ord == 241:
                codepages['IBM866'] += uppercase

            # ISO-8859-5
            if 207 < simb_ord < 240 or simb_ord == 161:
                codepages['ISO-8859-5'] += lowercase
            if 175 < simb_ord < 208 or simb_ord == 241:
                codepages['ISO-8859-5'] += uppercase

            # MAC
            if 221 < simb_ord < 255:
                codepages['MAC'] += lowercase
            if 127 < simb_ord < 160:
                codepages['MAC'] += uppercase

            last_simb = simb_ord

        idx = ''
        max_cp = 0
        for item in codepages:
            if codepages[item] > max_cp:
                max_cp = codepages[item]
                idx = item
        return idx


def recodeText(txt, src_codepage='cp1251', dst_codepage='utf-8'):
    """
    Transcode text from one encoding to another.

    :param txt: Source text.
    :param src_codepage: Source code page.
    :param dst_codepage: Destination code page.
    :return: Recoded text in a new encoding.
    """
    unicode_txt = toUnicode(txt, src_codepage)
    if isinstance(unicode_txt, str):
        return unicode_txt.encode(dst_codepage)

    log_func.error(u'Error recode text <%s>' % str(txt))
    return None


def toUnicode(value, code_page='utf-8'):
    """
    Convert any value to unicode.

    :param value: Value.
    :param code_page: Code page.
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return value.decode(code_page)
    return str(value)
