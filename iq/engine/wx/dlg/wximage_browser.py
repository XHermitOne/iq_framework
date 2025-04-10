#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WxPython image browser dialog function.
"""

import os.path
import wx
import wx.lib.imagebrowser

from ....util import icon_func
from ....util import log_func

from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)


def getImageBrowserDlg(parent=None, img_dirname=None):
    """
    Get image browser dialog.

    :param parent: Parent form.
    :param img_dirname: Image directory path.
    :return: Selected image filename or None if cancel pressed.
    """
    if img_dirname is None:
        img_dirname = icon_func.getIconPath()

    img_filename = None
    dlg = None
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        # set the initial directory for the demo bitmaps
        initial_dir = os.path.abspath(img_dirname)

        # open the image browser dialog
        dlg = wx.lib.imagebrowser.ImageDialog(parent, initial_dir)
        dlg.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/pictures')))
        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            img_filename = dlg.GetFile()

        dlg.Destroy()
        return img_filename
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error image browser dialog')
    return None
