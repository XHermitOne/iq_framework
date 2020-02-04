#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file iQ framework.
"""

import os.path
import datetime

VERSION = (0, 0, 1, 1)

DEBUG_MODE = False
LOG_MODE = False

RUNTIME_MODE = False

PROJECT_NAME = None

# Program profile folder name
PROFILE_DIRNAME = '.iq'

DEFAULT_ENCODING = 'utf-8'

# Log file name
LOG_FILENAME = os.path.join(os.environ.get('HOME',
                                           os.path.join(os.path.dirname(__file__), 'log', 'log')),
                            PROFILE_DIRNAME,
                            'iq_%s.log' % datetime.date.today().isoformat())

# Path to profile folder
PROFILE_PATH = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)),
                            PROFILE_DIRNAME)

# Kernel object
KERNEL = None

# Engine type. wx, qt or cui
WX_ENGINE_TYPE = 'wx'
QT_ENGINE_TYPE = 'qt'
CUI_ENGINE_TYPE = 'cui'
DEFAULT_ENGINE_TYPE = WX_ENGINE_TYPE
ENGINE_TYPE = DEFAULT_ENGINE_TYPE


def get_cfg_param(name):
    """
    Read the config parameter value.

    :type name: C{string}
    :param name: Parameter name.
    """
    return globals()[name]


def set_cfg_param(name, value):
    """
    Set config parameter value.

    :type name: C{string}
    :param name: Parameter name.
    :param value: Parameter value.
    """
    globals()[name] = value
