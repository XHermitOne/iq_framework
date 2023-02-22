#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file.
"""

import os
import os.path

__version__ = (0, 2, 1, 1)

# The full path to the executable file scanner.py
DEFAULT_SCANNER_EXEC_FILENAME = os.path.join(os.path.dirname(__file__), 'scanner.py')

PROFILE_SCAN_DIRNAME = os.path.join('.iq', 'iq_scanner')
DEFAULT_SCAN_PATH = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)+'/log'),
                                 PROFILE_SCAN_DIRNAME)


def getConfigParam(name):
    """
    Get variable value.

    :type name: C{string}
    :param name: Variable name.
    """
    return globals()[name]


def setConfigParam(name, value):
    """
    Set variable value.

    :type name: C{string}
    :param name: Variable name.
    :param value: Variable value.
    """
    globals()[name] = value
    return value
