#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Entry integer number dialog.
"""

import wx

from . import std_dialogs_proto

from ....engine.wx import  wxbitmap_func

__version__ = (0, 1, 2, 1)

DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 500


class iqIntegerDialog(std_dialogs_proto.integerDialogProto):
    """
    Entry integer number dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.integerDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/numeric_stepper')))

        self._integer_value = None

    def getValue(self):
        return self._integer_value

    def init(self, title=None, label=None,
             min_value=DEFAULT_MIN_VALUE, max_value=DEFAULT_MAX_VALUE,
             default_value=DEFAULT_MIN_VALUE):
        """
        Init dialog.

        :param title: Dialog title.
        :param label: Prompt text.
        :param min_value: Minimum value.
        :param max_value: Maximum value.
        :param default_value: Default value.
        """
        if title:
            self.SetTitle(title)
        if label:
            self.label_staticText.SetLabel(label)

        self.value_spinCtrl.SetRange(min(min_value, max_value),
                                     max(min_value, max_value))
        self.value_spinCtrl.SetValue(default_value)

    def onCancelButtonClick(self, event):
        self._integer_value = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._integer_value = self.value_spinCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()
