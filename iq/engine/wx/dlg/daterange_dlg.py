#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select date range dialog.
"""

import wx
from . import std_dialogs_proto

from iq.util import log_func
from ....engine.wx import wxdatetime_func

__version__ = (0, 0, 0, 1)


class iqDateRangeDialog(std_dialogs_proto.dateRangeDialogProto):
    """
    Select date range dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.dateRangeDialogProto.__init__(self, *args, **kwargs)

        self._selected_range = None

    def getSelectedDateRange(self):
        return self._selected_range

    def getSelectedDateRangeAsDatetime(self):
        if self._selected_range:
            return wxdatetime_func.wxDateTime2date(self._selected_range[0]), \
                   wxdatetime_func.wxDateTime2date(self._selected_range[1])
        return None

    def setConcreteDateCheck(self, checked=True):
        """
        On/Off concrete date mode.

        :param checked: On/Off.
        """
        self.concrete_date_checkBox.SetValue(checked)
        self.lastDatePicker.Enable(not checked)
        if checked:
            first_date = self.firstDatePicker.GetValue()
            self.lastDatePicker.SetValue(first_date)

    def onCancelButtonClick(self, event):
        self._selected_range = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_range = (self.firstDatePicker.GetValue(),
                                self.lastDatePicker.GetValue())
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onFirstDateChanged(self, event):
        """
        Change first date handler.
        """
        first_date = event.GetDate()
        last_date = self.lastDatePicker.GetValue()

        if first_date > last_date:
            self.lastDatePicker.SetValue(first_date)
        elif self.concrete_date_checkBox.IsChecked():
            self.lastDatePicker.SetValue(first_date)

        event.Skip()

    def onLastDateChanged(self, event):
        """
        Change last date handler.
        """
        first_date = self.firstDatePicker.GetValue()
        last_date = event.GetDate()

        try:
            log_func.debug(u'Correct last date <%d.%d.%d>' % (last_date.GetDay(),
                                                              last_date.GetMonth(),
                                                              last_date.GetYear()))
        except:
            pass
        if first_date > last_date and len(str(last_date.GetYear())) == 4:
            self.lastDatePicker.SetValue(first_date)

        event.Skip()

    def onConcreteDateCheckBox(self, event):
        """
        On/Off concrete date handler.
        """
        checked = event.IsChecked()
        self.lastDatePicker.Enable(not checked)
        if checked:
            first_date = self.firstDatePicker.GetValue()
            self.lastDatePicker.SetValue(first_date)
        event.Skip()
