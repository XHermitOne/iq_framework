#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WX Application functions module.
"""

from ...util import log_func


__version__ = (0, 0, 0, 1)


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
