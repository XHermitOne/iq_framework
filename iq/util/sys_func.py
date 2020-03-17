#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System functions module.
"""

import socket

__version__ = (0, 0, 0, 1)


def getComputerName():
    """
    Get computer name.

    :return: Computer name or None if error.
    """
    comp_name = socket.gethostname()
    return comp_name
