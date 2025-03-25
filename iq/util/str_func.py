#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Strings and text manipulate functions.
"""

import string
import encodings.aliases
import html


from . import log_func

from .. import global_data

__version__ = (0, 1, 1, 2)


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

    log_func.warning(u'Error recode text <%s>' % str(txt))
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
           u'з': 'z', u'и': 'i', u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p',
           u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch',
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


def isWordsInText(text, words, case_sensitivity=True):
    """
    Are there words in the text?
    The search is conducted before the first finding of one of the indicated words.

    :param text: Text.
    :param words: Words.
    :param case_sensitivity: Check case sensitive?
    :return: True (there are such words in the text)/False (no words found).
    """
    if not isinstance(text, str):
        text = str(text)

    find = False
    for word in words:
        if case_sensitivity:
            # Case sensitive check
            find = word in text
        else:
            # Case insensitive check
            find = word.lower() in text.lower()
        if find:
            break
    return find


def startswithWords(text, words, case_sensitivity=True):
    """
    Search for words at the beginning of the text.
    The search is carried out until the first finding of one of the specified words.

    :param text: Text.
    :param words: Words.
    :param case_sensitivity: Check case sensitive?
    :return: True (there are such words at the beginning of the text)/False (words not found).
    """
    if not isinstance(text, str):
        text = str(text)

    find = False
    for word in words:
        if case_sensitivity:
            # Case sensitive check
            find = text.startswith(word)
        else:
            # Case insensitive check
            find = text.lower().startswith(word.lower())
        if find:
            break
    return find


def endswithWords(text, words, case_sensitivity=True):
    """
    Search for words at the end of the text.
    The search is carried out until the first finding of one of the specified words. \

    :param text: Text.
    :param words: Words.
    :param case_sensitivity: Check case sensitive?
    :return: True (there are such words at the end of the text )/False (words not found).
    """
    if not isinstance(text, str):
        text = str(text)

    find = False
    for word in words:
        if case_sensitivity:
            # Case sensitive check
            find = text.endswith(word)
        else:
            # Case insensitive check
            find = text.lower().endswith(word.lower())
        if find:
            break
    return find


def isMultiLineText(text=u''):
    """
    Checking that the text is many lines.

    :param text: Text.
    :return: True - multi line text, False - one line, None - error.
    """
    if not isinstance(text, str):
        # If the type does not match the text, then the error is
        return None

    return u'\n' in text.strip()


def isDigitsInText(text):
    """
    Checking the presence of numbers in the text.

    :param text: Text.
    :return: True - there are numbers in the text  / False - no numbers .
    """
    for symbol in text:
        if symbol.isdigit():
            return True
    return False


def isSerialSymbol(text, symbol=' '):
    """
    Checking what the text is
    a sequence of one specific character.

    :param text: Text.
    :param symbol: Symbol.
    :return: True/False.
    """
    if not text or not isinstance(text, str):
        # If it is an empty string, then it is not a sequence at all
        return False

    return all([symb == symbol for symb in text])


def isSerial(text):
    """
    Checking what the text is a sequence of one character.

    :param text: Text.
    :return: True/False.
    """
    return isSerialSymbol(text, text[0]) if text and isinstance(text, str) else False


def isSerialZero(text):
    """
    Checking what the text is a sequence of one character '0'.

    :param text: Text.
    :return: True/False.
    """
    return isSerialSymbol(text, '0')


def getStrDigit(text):
    """
    Get all numbers from a string of text as a string.

    :param text: Text. For example '12ASD321'.
    :return: Text with numbers . For example '12321'
    """
    return u''.join([symb for symb in text if symb.isdigit()])


def getStrDigitAsInt(text):
    """
    Get all digits from a string of text as an integer.

    :param text: Text. For example '12ASD321'.
    :return: Integer. For example 12321. If there are no digits, then 0 is returned.
    """
    num_txt = getStrDigit(text)
    return int(num_txt) if num_txt else 0


def replaceInText(text, replacements):
    """
    Make a number of replacements in the text.

    :param text: Text.
    :param replacements: Replacements.
        Can be specified as a dictionary or a list of tuples.
        Dictionary:
            {
            'source replace': 'destination replace', ...
            }
        List of tuples (used when the order of replacements is important ):
            [
            ('source replace', 'destination replace'), ...
            ]
    :return: The text with all the replacements made, or the original text in case of an error.
    """
    result_text = text
    try:
        if isinstance(replacements, dict):
            for src_txt, dst_txt in replacements.items():
                result_text = result_text.replace(src_txt, dst_txt)
        elif isinstance(replacements, list) or isinstance(replacements, tuple):
            for src_txt, dst_txt in replacements:
                result_text = result_text.replace(src_txt, dst_txt)
        else:
            # Incorrect type
            return text
        return result_text
    except:
        log_func.fatal(u'Error replace in text')
        return text


def deleteInText(text, delete_txt_list):
    """
    Remove lines from text.

    :param text: Text.
    :param delete_txt_list: List of lines to remove from text.
    :return: The text with all the replacements made, or the original text in case of an error.
    """
    replacements = [(str(delete_txt), u'') for delete_txt in delete_txt_list]
    return replaceInText(text, replacements=replacements)


def deleteSymbolInText(text, symbol=u' '):
    """
    Remove character from text.

    :param text: Text.
    :param symbol: The character to remove.
    :return: Text with a deleted character, or the original text in case of an error.
    """
    return deleteInText(text, (symbol, ))


def isFloatStr(text):
    """
    Determine if a string is a floating point number.

    :param text: Text.
    :return: True/False
    """
    try:
        float(text)
        return True
    except ValueError:
        return False


def isIntStr(text):
    """
    Determine if a string is an integer.

    :param text: Text.
    :return: True/False
    """
    return text.isdigit()


def isNoneStr(text):
    """
    Determine if string is None.

    :param text: Text.
    :return: True/False
    """
    return text.strip() == 'None'


def parseWiseTypeStr(text):
    """
    Type conversion from string to real type.

    :param text: Text.
    :return: Real type value.
        For example:
            text = 'None' - None
            text = '099' - 99
            text = '3.14' - 3.14
            text = 'XYZ' - 'XYZ'
    """
    if isNoneStr(text):
        return None
    elif isIntStr(text):
        return int(text)
    elif isFloatStr(text):
        return float(text)
    # String
    return text


def limitTextLen(text, length, filler=u' '):
    """
    Limit the text to length.
        If the text is larger, then the last characters are cut off.
        If the text is smaller, then characters are added to the end of the text
        filling up to the specified length.

    :param text: Source text.
    :param length: The length of the resulting text.
    :param filler: The filler symbol.
    :return: Edited text of a certain length.
    """
    if not isinstance(text, str):
        text = str(text)

    if len(filler) > 1:
        filler = filler[0]
    elif len(filler) == 0:
        filler = u' '

    if len(text) > length:
        return text[:length]
    else:
        text += filler * (length - len(text))
    return text


def replaceUnprintableSymbol(text, replacement=string.whitespace[0]):
    """
    Replace all unprintable symbols in text.

    :param text: Text.
    :param replacement: Replacement symbol.
    :return: Modified text.
    """
    for i, symbol in enumerate(text):
        if symbol not in string.printable:
            text = text[:i] + replacement + text[i + 1:]
    return text


def text2html(text, quote=True):
    """
    Convert text to HTML like.

    :param text: Text.
    :param quote: Quote convert.
    :return: HTML text.
    """
    return html.escape(text, quote=quote)


def html2text(html_text):
    """
    Convert HTML like to text.

    :param html_text: HTML Text.
    :return: Text.
    """
    return html.unescape(html_text)
