#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file.
"""

import os.path
import datetime

from iq.util import file_func
from iq.util import global_func

# Log file name
LOG_FILENAME = os.path.join(file_func.getProfilePath(),
                            global_func.getProjectName(),
                            'scan_%s.log' % datetime.date.today().isoformat())


DEFAULT_OPTIONS_FILENAME = os.path.join(file_func.getProfilePath(),
                                        global_func.getProjectName(),
                                        'options.ini')

DEFAULT_SCAN_FILENAME = os.path.join(file_func.getProfilePath(),
                                     global_func.getProjectName(),
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
