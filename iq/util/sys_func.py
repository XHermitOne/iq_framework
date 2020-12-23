#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System functions module.
"""

import sys
import socket
import platform
import os

try:
    # For Python 2
    import commands as get_procesess_module
except ImportError:
    # For Python 3
    import subprocess as get_procesess_module

from . import log_func

__version__ = (0, 0, 0, 1)

# System line separator
UNIX_LINESEP = '\n'
WIN_LINESEP = '\r\n'
LINE_SEPARATORS = (WIN_LINESEP, UNIX_LINESEP)

# Current system line separator
LINESEP = os.linesep


def getComputerName():
    """
    Get computer name.

    :return: Computer name or None if error.
    """
    comp_name = socket.gethostname()
    if isWindowsPlatform():
        from . import str_func
        comp_name = str_func.rus2lat(comp_name)
    return comp_name


def getPlatform():
    """
    Get platform name.
    """
    return platform.uname()[0].lower()


def isWindowsPlatform():
    return getPlatform() == 'windows'


def isLinuxPlatform():
    return getPlatform() == 'linux'


def getActiveProcessCount(find_process):
    """
    The number of active processes running.

    :param find_process: The search string of the process.
    :return: The number of processes found.
    """
    processes_txt = get_procesess_module.getoutput('ps -eo pid,cmd')
    processes = processes_txt.strip().split('\n')
    find_processes = [process for process in processes if find_process in process]
    # log_func.debug(u'Find processes %s' % str(find_processes))
    return len(find_processes)


def isActiveProcess(find_process):
    """
    Check for the existence of an active executable process.

    :param find_process: The search string of the process.
    :return: True - process exists / False - process not found.
    """
    return getActiveProcessCount(find_process) >= 1


def exitForce():
    """
    Forced closing of the program.
    """
    sys.exit(0)


def beep(count=1):
    """
    Play system sound.

    :param count: The number of repetitions.
    """
    for i in range(count):
        print('\a')
