#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Net connection functions.
"""

import sys
import os
import time

from . import log_func

__version__ = (0, 0, 1, 1)


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


def doPing(host):
    """
    Check connect with host by ping3 library.
    Install: pip3 install ping3.

    :param host: Host name/ip address.
    :return: True - connected. False - not connected.
    """
    try:
        import ping3
    except ImportError:
        log_func.error(u'Not installed pip3 library. Install: pip3 install ping3')
        return None

    try:
        result = ping3.ping(host)
        log_func.debug(u'Ping to <%s> ... %s' % (host, result))
        return isinstance(result, float)
    except:
        log_func.fatal(u'Error ping to <%s>' % host)
    return None


def allSeriesPing(host, count, delay=0):
    """
    Check connect with host by series ping3.

    :param host: Host name/ip address.
    :param count: Number of pings.
    :param delay: Delay in milliseconds.
    :return: True - connected. False - not connected.
    """
    try:
        import ping3
    except ImportError:
        log_func.error(u'Not installed pip3 library. Install: pip3 install ping3')
        return None

    try:
        results = list()
        for i in range(count):
            result = ping3.ping(host)
            log_func.debug(u'%d. Ping to <%s> ... %s' % (i+1, host, result))
            results.append(isinstance(result, float))
            if delay:
                time.sleep(float(delay) / 1000.0)
        return all(results)
    except:
        log_func.fatal(u'Error series ping to <%s>' % host)
    return None


def anySeriesPing(host, count, delay=0):
    """
    Check connect with host by series ping3.

    :param host: Host name/ip address.
    :param count: Number of pings.
    :param delay: Delay in milliseconds.
    :return: True - connected. False - not connected.
    """
    try:
        import ping3
    except ImportError:
        log_func.error(u'Not installed pip3 library. Install: pip3 install ping3')
        return None

    try:
        results = list()
        for i in range(count):
            result = ping3.ping(host)
            log_func.debug(u'%d. Ping to <%s> ... %s' % (i+1, host, result))
            results.append(isinstance(result, float))
            if delay:
                time.sleep(float(delay) / 1000.0)
        return any(results)
    except:
        log_func.fatal(u'Error series ping to <%s>' % host)
    return None
