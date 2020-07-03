#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Net connection functions.
"""

import sys
import os


__version__ = (0, 0, 0, 1)


def validPingHost(host_name):
    """
    Check connect with host by ping.

    :param host_name: Host name/ip address.
    :return: True - connected. False - not connected.
    """
    if sys.platform.startswith('win'):
        response = os.system('ping -n 1 %s' % host_name)
    elif sys.platform.startswith('linux'):
        response = os.system('ping -c 1 %s' % host_name)
    else:
        return False
    return response == 0
