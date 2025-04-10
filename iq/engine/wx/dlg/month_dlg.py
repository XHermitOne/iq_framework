#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select month dialog.
"""

import datetime
import wx

from . import std_dialogs_proto

from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)

TODAY = datetime.date.today()

DEFAULT_YEAR_RANGE = 10

# Years
YEAR_LIST = [TODAY.year + i for i in range(-DEFAULT_YEAR_RANGE, DEFAULT_YEAR_RANGE)]


class iqMonthDialog(std_dialogs_proto.monthDialogProto):
    """
    Select month dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.monthDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/calendar_view_month')))

        # Select current month
        self.month_choice.Select(TODAY.month - 1)

        # Year list
        self.year_choice.Clear()
        self.year_choice.AppendItems([str(n_year) for n_year in YEAR_LIST])

        # Select current year
        self.year_choice.Select(YEAR_LIST.index(TODAY.year))

        self._selected_month = None

    def getSelectedMonth(self):
        return self._selected_month

    def getSelectedMonthAsDatetime(self):
        if self._selected_month:
            return datetime.datetime(year=self._selected_month[0], month=self._selected_month[1], day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_month = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_month = (YEAR_LIST[self.year_choice.GetSelection()],
                                self.month_choice.GetSelection() + 1)
        self.EndModal(wx.ID_OK)
        event.Skip()
