#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Microsoft Windows OS functions.
"""

from . import log_func

try:
    import winreg
except ImportError:
    log_func.error(u'Import error winreg. Not Microsoft Window OS', is_force_print=True)

__version__ = (0, 0, 1, 1)

EXECUTABLE_APPLICATION_PATHS_CACHE = None


def getExeAppPaths(cached=True):
    """
    Get executable applications.

    :param cached: Cached?
    :return: {application_name: exe_application_path} dictionary.
    """
    if cached:
        global EXECUTABLE_APPLICATION_PATHS_CACHE
        if EXECUTABLE_APPLICATION_PATHS_CACHE:
            return EXECUTABLE_APPLICATION_PATHS_CACHE

    app_paths = dict()
    try:
        a_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)

        a_key = winreg.OpenKey(a_reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths')
        for i in range(1024):
            try:
                key_name = winreg.EnumKey(a_key, i)
                a_subkey = winreg.OpenKey(a_key, key_name)
                value = winreg.QueryValueEx(a_subkey, None)
                app_paths[key_name.lower()] = value[0]
            except WindowsError:
                continue

        if cached:
            global EXECUTABLE_APPLICATION_PATHS_CACHE
            EXECUTABLE_APPLICATION_PATHS_CACHE = app_paths

        return app_paths
    except:
        log_func.fatal(u'Error get executable application paths')
    return dict()
