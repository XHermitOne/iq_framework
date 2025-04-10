#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select year dialog.
"""

import datetime
import wx

from . import std_dialogs_proto

from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)

MIN_YEAR = 1940
MAX_YEAR = MIN_YEAR + 100


class iqYearDialog(std_dialogs_proto.yearDialogProto):
    """
    Select year dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.yearDialogProto.__init__(self, *args, **kwargs)
        wx.Icon(wxbitmap_func.createIconBitmap('fatcow/calendar_view_day'))

        self._selected_year = None

    def initYearChoice(self):
        """
        Init select year control.
        """
        year_choices = [str(i_year) for i_year in range(MIN_YEAR, MAX_YEAR)]
        self.year_choice.AppendItems(year_choices)

        if not self._selected_year:
            today = datetime.date.today()
            cur_year_idx = year_choices.index(str(today.year))
        else:
            cur_year_idx = year_choices.index(str(self._selected_year))

        self.year_choice.setSelection(cur_year_idx)

    def getSelectedYear(self):
        return self._selected_year

    def setSelectedYear(self, selected_year):
        if isinstance(selected_year, datetime.datetime) or isinstance(selected_year, datetime.date):
            self._selected_year = selected_year.year
            return
        if not isinstance(selected_year, int):
            self._selected_year = int(selected_year)
            return
        self._selected_year = selected_year

    def getSelectedYearAsDatetime(self):
        if self._selected_year:
            return datetime.datetime(year=self._selected_year, month=1, day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_year = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        year_idx = self.year_choice.GetSelection()
        self._selected_year = int(self.year_choice.GetString(year_idx))
        self.EndModal(wx.ID_OK)
        event.Skip()
