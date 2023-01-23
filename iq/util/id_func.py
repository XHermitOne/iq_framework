#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Object identification functions.
"""

import uuid

__version__ = (0, 0, 1, 2)

NONE_GUID = '00000000-0000-0000-0000-000000000000'


def genNewId(limit_len=5):
    """
    Generate new id.

    :param limit_len: Identifier string length restriction.
    :return: New id as string.
    """
    return str(uuid.uuid4().fields[-1])[:limit_len]


def genGUID():
    """
    Generate new GUID.

    :return: New GUID as string.
    """
    return str(uuid.uuid4())


def isGUID(guid_string):
    """
    Is GUID?

    :param guid_string: Text.
    :return: True - guid / False - not guid.
    """
    if not isinstance(guid_string, str):
        return False

    if guid_string == NONE_GUID:
        return True

    try:
        val = uuid.UUID(guid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False
    return val.hex == guid_string.replace('-', '')
