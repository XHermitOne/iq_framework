#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Strings and text manipulate functions.
"""

import encodings.aliases

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

