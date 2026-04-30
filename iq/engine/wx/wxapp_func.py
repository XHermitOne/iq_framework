#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WX Application functions module.
"""

import platform
from ...util import log_func


__version__ = (0, 1, 2, 1)


def setSystemLocaleApplicationLinux(app=None):
    """
    Set system locale in Application. Only for Linux.
    :param app: Application object.
    :return: True/False.
    """
    if platform.system() != 'Linux':
        log_func.warning(u'Not set locale in WX Application. Platform not support')
        return False

    try:
        import wx

        if app is None:
            app = wx.GetApp()

        # Set system locale
        app.locale = wx.Locale()
        system_locale_language = wx.Locale.GetSystemLanguage()
        app.locale.Init(system_locale_language)
        system_locale_language_name = wx.Locale.GetLanguageName(system_locale_language)
        log_func.info(u'Set system locale in WX application. Language <%s>' % system_locale_language_name)

        return True
    except:
        log_func.fatal(u'Error set system locale in WX application')
    return False

def closeForceWxApplication():
    """
    Force closing an application.

    :return: True/False.
    """
    try:
        import wx

        app = wx.GetApp()
        app.ExitMainLoop()
        app.Destroy()
        return True
    except:
        log_func.fatal(u'Error closing an WX application')
    return False
