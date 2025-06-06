#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check list box dialog.
"""

import wx

from . import std_dialogs_proto

from ....engine.wx import wxbitmap_func

__version__ = (0, 1, 1, 1)


class iqCheckListBoxDialog(std_dialogs_proto.checkListBoxDialogProto):
    """
    Check list box dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.checkListBoxDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/check_box_list')))

    def onCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()
