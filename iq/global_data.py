#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global variables and objects iqFramework.
"""

import sys
import locale
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

# Default shell encoding
DEFAULT_SHELL_ENCODING = sys.stdout.encoding if sys.platform.startswith('win') else locale.getpreferredencoding()

# Log file name
HOME_PATH = os.environ['HOME'] if 'HOME' in os.environ else (os.environ.get('HOMEDRIVE',
                                                                            '') + os.environ.get('HOMEPATH', ''))
LOG_PATH = HOME_PATH if HOME_PATH else os.path.join(os.path.dirname(__file__), 'log')
LOG_FILENAME = os.path.join(LOG_PATH,
                            PROFILE_DIRNAME,
                            'iq_%s.log' % datetime.date.today().isoformat())

# Path to profile folder
PROFILE_PATH = os.path.join(os.environ.get('HOME', os.path.dirname(__file__)),
                            PROFILE_DIRNAME)

# Kernel object
KERNEL = None

# Current project object
PROJECT = None
# Current user object
USER = None

# Engine type. wx, qt or cui
WX_ENGINE_TYPE = 'WX'
QT_ENGINE_TYPE = 'QT'
CUI_ENGINE_TYPE = 'CUI'

# Set default engine type
try:
    import wx
    DEFAULT_ENGINE_TYPE = WX_ENGINE_TYPE
except ImportError:
    DEFAULT_ENGINE_TYPE = CUI_ENGINE_TYPE

ENGINE_TYPE = DEFAULT_ENGINE_TYPE
ENGINE_TYPES = (WX_ENGINE_TYPE, QT_ENGINE_TYPE, CUI_ENGINE_TYPE)

# Application object
APPLICATION = None

# Main window object
MAIN_WINDOW = None

FRAMEWORK_LOGO_TXT = u'''
 _     _____                                 _   
|_|___|   __|___ ___ _____ ___ _ _ _ ___ ___| |_ 
| | . |   __|  _| .'|     | -_| | | | . |  _| '_|
|_|_  |__|  |_| |__,|_|_|_|___|_____|___|_| |_,_|
    |_|     
'''


OPERATE_YEAR = datetime.datetime.now().year


def getGlobal(name):
    """
    Read the global parameter value.

    :type name: C{string}
    :param name: Parameter name.
    """
    return globals()[name]


def setGlobal(name, value):
    """
    Set global parameter value.

    :type name: C{string}
    :param name: Parameter name.
    :param value: Parameter value.
    """
    globals()[name] = value
