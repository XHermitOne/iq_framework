#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select month range dialog.
"""

import datetime
import wx

from . import std_dialogs_proto

__version__ = (0, 0, 0, 1)


class iqMonthRangeDialog(std_dialogs_proto.monthRangeDialogProto):
    """
    Select month range dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.monthRangeDialogProto.__init__(self, *args, **kwargs)

        self._selected_range = None

    def getSelectedMonthRange(self):
        return self._selected_range

    def getSelectedMonthRangeAsDatetime(self):
        if self._selected_range:
            return (datetime.datetime(year=self._selected_range[0][0], month=self._selected_range[0][1], day=1),
                    datetime.datetime(year=self._selected_range[1][0], month=self._selected_range[1][1], day=1))
        return None

    def onCancelButtonClick(self, event):
        self._selected_range = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        first_selected_month = (self.yearFirstChoiceControl.get_selected_year(),
                                self.monthFirstChoiceControl.get_selected_month_num())
        last_selected_month = (self.yearLastChoiceControl.get_selected_year(),
                               self.monthLastChoiceControl.get_selected_month_num())
        self._selected_range = (first_selected_month, last_selected_month)
        self.EndModal(wx.ID_OK)
        event.Skip()
