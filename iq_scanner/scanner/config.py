#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file.
"""

import os.path
import datetime

from iq.util import file_func
from iq.util import global_func

__version__ = (0, 2, 1, 2)

PRJ_NAME = global_func.getProjectName()

# Log file name
LOG_FILENAME = os.path.join(file_func.getProfilePath(),
                            PRJ_NAME if PRJ_NAME else 'iq_scanner',
                            'scan_%s.log' % datetime.date.today().isoformat())


DEFAULT_OPTIONS_FILENAME = os.path.join(file_func.getProfilePath(),
                                        PRJ_NAME if PRJ_NAME else 'iq_scanner',
                                        'options.ini')

DEFAULT_SCAN_FILENAME = os.path.join(file_func.getProfilePath(),
                                     PRJ_NAME if PRJ_NAME else 'iq_scanner',
                                     'scan_output.pdf')

DEFAULT_EXT_SCAN_PRG = 'gscan2pdf&'

# Maximum number of sheets loaded in the scanner tray by default
DEFAULT_SCANNER_MAX_SHEETS = 60


def getConfigParam(name):
    """
    Read the config parameter value.

    :type name: C{string}
    :param name: Parameter name.
    """
    return globals()[name]


def setConfigParam(name, value):
    """
    Set config parameter value.

    :type name: C{string}
    :param name: Parameter name.
    :param value: Parameter value.
    """
    globals()[name] = value
    return value
