#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Strings and text manipulate functions.
"""

import encodings.aliases

from . import log_func

from .. import global_data

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


def replaceLower2Upper(txt):
    """
    Replacing lowercase letters in a string with underscores
    except the first character.

    :param txt: Text string as abcd_efgh_iklmn.
    :return: Modified text as  AbcdEfghIklmn.
    """
    if not isinstance(txt, str):
        txt = str(txt)

    return ''.join([(symb.upper() if not i or (i and symb.islower() and txt[i-1] == '_') else symb.lower()) for i, symb in enumerate(list(txt)) if symb != '_'])


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


RUS2LAT = {u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'yo', u'ж': 'j',
           u'з': 'z', u'и': 'idx', u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p',
           u'р': 'r', u'с': 'text', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
           u'ш': 'sh', u'щ': 'sch', u'ь': '', u'ы': 'y', u'ъ': '', u'э': 'e', u'ю': 'yu', u'я': 'ya',
           u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E', u'Ё': 'YO', u'Ж': 'J',
           u'З': 'Z', u'И': 'I', u'Й': 'Y', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N', u'О': 'O', u'П': 'P',
           u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H', u'Ц': 'C', u'Ч': 'CH',
           u'Ш': 'SH', u'Щ': 'SCH', u'Ь': '', u'Ы': 'Y', u'Ъ': '', u'Э': 'E', u'Ю': 'YU', u'Я': 'YA'}


def rus2lat(text, translate_dict=RUS2LAT):
    """
    Translation of Russian letters into Latin according to the dictionary of substitutions.
    """
    if isinstance(text, bytes):
        # To unicode
        text = text.decode(global_data.DEFAULT_ENCODING)

    txt_list = list(text)
    txt_list = [translate_dict.setdefault(ch, ch) for ch in txt_list]
    return ''.join(txt_list)


def isLATText(text):
    """
    The text is written in Latin?
    """
    if isinstance(text, str):
        rus_chr = [c for c in text if ord(c) > 128]
        return not bool(rus_chr)
    # This is not a string
    return False


def isRUSText(text):
    """
    String with Russian letters?
    """
    if isinstance(text, str):
        rus_chr = [c for c in text if ord(c) > 128]
        return bool(rus_chr)
    # This is not a string
    return False


def isWordsInText(text, *words):
    """
    Are there words in the text?
    The search is conducted before the first finding of one of the indicated words.

    :param text: Text.
    :param words: Words.
    :return: True (there are such words in the text)/False (no words found).
    """
    if not isinstance(text, str):
        text = toUnicode(text)
    find = any([word in text for word in words])
    return find
