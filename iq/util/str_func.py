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
