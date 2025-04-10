#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calendar dialog module.
"""

import datetime
import wx
from . import std_dialogs_proto

from .. import wxdatetime_func
from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)


class iqCalendarDialog(std_dialogs_proto.calendarDialogProto):
    """
    Calendar dialog class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.calendarDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/calendar')))

        self._selected_date = None

    def setSelectedDate(self, selected_date=None):
        """
        Set selected date.

        :param selected_date:  Selected date.
            If not defined then get today.
        :return:
        """
        if selected_date is None:
            selected_date = datetime.date.today()

        if isinstance(selected_date, datetime.date):
            selected_date = wxdatetime_func.date2wxDateTime(selected_date)
        elif isinstance(selected_date, datetime.datetime):
            selected_date = wxdatetime_func.datetime2wxDateTime(selected_date)

        self._selected_date = selected_date
        self.calendarCtrl.SetDate(self._selected_date)

    def getSelectedDate(self):
        return self._selected_date

    def getSelectedDateAsDatetime(self):
        return wxdatetime_func.wxDateTime2datetime(self._selected_date)

    def getSelectedDateAsDate(self):
        return wxdatetime_func.wxDateTime2date(self._selected_date)

    def onCancelButtonClick(self, event):
        self._selected_date = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_date = self.calendarCtrl.GetDate()
        self.EndModal(wx.ID_OK)
        event.Skip()
