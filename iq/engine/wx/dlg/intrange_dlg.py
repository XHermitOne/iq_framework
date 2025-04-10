#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry integer range dialog.
"""

import wx

from . import std_dialogs_proto

from ....engine.wx import wxbitmap_func

__version__ = (0, 1, 1, 1)


class iqIntRangeDialog(std_dialogs_proto.intRangeDialogProto):
    """
    Entry integer range dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.intRangeDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/sort_number_column')))

        self._begin_integer_value = None
        self._end_integer_value = None

    def getValue(self):
        return self._begin_integer_value, self._end_integer_value

    def init(self, title=None, label_begin=None, label_end=None, min_value=1, max_value=1000):
        """
        Init dialog.

        :param title: Dialog title.
        :param label_begin: First prompt text.
        :param label_end: Last prompt text.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        """
        if title:
            self.SetTitle(title)
        if label_begin:
            self.begin_spinCtrl.SetLabel(label_begin)
        if label_end:
            self.end_spinCtrl.SetLabel(label_end)

        self.begin_spinCtrl.SetRange(min(min_value, max_value),
                                     max(min_value, max_value))
        self.end_spinCtrl.SetRange(min(min_value, max_value),
                                   max(min_value, max_value))

    def onBeginSpinCtrl(self, event):
        """
        Change first value handler.
        """
        value = self.begin_spinCtrl.GetValue()
        if value > self.end_spinCtrl.GetValue():
            self.end_spinCtrl.SetValue(value)
        event.Skip()

    def onEndSpinCtrl(self, event):
        """
        Change last value handler.
        """
        value = self.end_spinCtrl.GetValue()
        if value < self.end_spinCtrl.GetValue():
            self.begin_spinCtrl.SetValue(value)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Button <Cancel> click handler.
        """
        self._begin_integer_value = None
        self._end_integer_value = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Button <OK> click handler.
        """
        self._begin_integer_value = self.begin_spinCtrl.GetValue()
        self._end_integer_value = self.end_spinCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()
