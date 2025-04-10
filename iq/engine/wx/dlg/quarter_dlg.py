#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select quarter dialog.
"""

import datetime
import wx

from . import std_dialogs_proto

from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)

TODAY = datetime.date.today()

DEFAULT_YEAR_RANGE = 10

# Year list
YEAR_LIST = [TODAY.year + i for i in range(-DEFAULT_YEAR_RANGE, DEFAULT_YEAR_RANGE)]


class iqQuarterDialog(std_dialogs_proto.quarterDialogProto):
    """
    Select quarter dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.quarterDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/calendar_group')))

        # Select current quarter
        cur_quarter = self.getCurQuarter(today=TODAY)
        self.quarter_choice.Select(cur_quarter - 1)

        # Init year list
        self.year_choice.Clear()
        self.year_choice.AppendItems([str(n_year) for n_year in YEAR_LIST])

        # Select current year
        self.year_choice.Select(YEAR_LIST.index(TODAY.year))

        self._selected_quarter = None

    def getCurQuarter(self, today=None):
        """
        Determine the quarter relative to the current day.

        :param today: Today.
            If None then get datetime.date.today()
        :return: Quarter number.
        """
        if today is None:
            today = datetime.date.today()
        cur_month = today.month
        return (cur_month - 1)//3 + 1

    def getSelectedQuarter(self):
        return self._selected_quarter

    def onCancelButtonClick(self, event):
        self._selected_quarter = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_quarter = (YEAR_LIST[self.year_choice.GetSelection()],
                                  self.quarter_choice.GetSelection() + 1)
        self.EndModal(wx.ID_OK)
        event.Skip()
