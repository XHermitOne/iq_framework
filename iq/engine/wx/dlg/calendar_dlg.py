#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calendar dialog module.
"""

import wx
from . import std_dialogs_proto

from ....engine.wx import wxdatetime_func

__version__ = (0, 0, 0, 1)


class iqCalendarDialog(std_dialogs_proto.calendarDialogProto):
    """
    Calendar dialog class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.calendarDialogProto.__init__(self, *args, **kwargs)

        self._selected_date = None

    def getSelectedDate(self):
        return self._selected_date

    def getSelectedDateAsDatetime(self):
        return wxdatetime_func.wxDateTime2date(self._selected_date)

    def onCancelButtonClick(self, event):
        self._selected_date = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_date = self.calendarCtrl.GetDate()
        self.EndModal(wx.ID_OK)
        event.Skip()
