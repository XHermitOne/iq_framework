#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main form manager.
"""

import os.path
import wx
import wx.adv

from ...util import log_func
from ...util import file_func
from ..wx.dlg import wxdlg_func
from ..wx import wxbitmap_func

from . import base_manager

__version__ = (0, 0, 0, 1)

DEFAULT_SPLASH_DELAY = 5


def getMainWindow():
    """
    Main window object.
    """
    app = wx.GetApp()
    if app:
        return app.GetTopWindow()
    return None


class iqMainFormManager(base_manager.iqBaseManager):
    """
    Main form manager.
    """
    def showMainFormSplash(self, main_form, splash_filename, delay=DEFAULT_SPLASH_DELAY):
        """
        Show splash window.

        :param main_form: Main form object.
        :param splash_filename: Splash image filename.
        :param delay: Time delay in seconds.
        :return: True/False.
        """
        assert isinstance(main_form, wx.Frame) or isinstance(main_form, wx.Dialog), u'Main form manager type error'

        splash_filename = file_func.getAbsolutePath(splash_filename)

        if not splash_filename or not os.path.exists(splash_filename):
            log_func.error(u'Splash image filename <%s> not found' % splash_filename)
            return False

        bmp = wxbitmap_func.createBitmap(splash_filename)
        splash = wx.adv.SplashScreen(bitmap=bmp,
                                     splashStyle=wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                     milliseconds=delay * 1000,
                                     parent=None,
                                     pos=wx.DefaultPosition,
                                     size=wx.DefaultSize,
                                     style=wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        splash.Show()
        return True

