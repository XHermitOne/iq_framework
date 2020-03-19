#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System functions module.
"""

import socket
import platform

__version__ = (0, 0, 0, 1)


def getComputerName():
    """
    Get computer name.

    :return: Computer name or None if error.
    """
    comp_name = socket.gethostname()
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
