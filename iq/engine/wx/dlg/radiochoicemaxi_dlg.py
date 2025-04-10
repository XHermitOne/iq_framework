#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select wxRadioBox item dialog.
Elements are arranged vertically.
Maximum 15 items.
"""

import wx

from . import std_dialogs_proto

from .. import wxbitmap_func

__version__ = (0, 1, 1, 1)

# Maximum items number
MAX_ITEM_COUNT = 15


class iqRadioChoiceMaxiDialog(std_dialogs_proto.radioChoiceMaxiDialogProto):
    """
    Select wxRadioBox item dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.radioChoiceMaxiDialogProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/radiobutton_group')))

        # Selected item index
        self._item_idx = None

    def getValue(self):
        return self._item_idx

    def init(self, title=None, label=None, choices=(), do_fit_dlg=True,
             default=None):
        """
        Init dialog.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 15 items.
        :param do_fit_dlg: Fit dialog?
        :param default: Default item index.
        """
        if title:
            self.SetTitle(title)
        if label:
            self.choice_radioBox.SetLabel(label)
        if choices:
            choices = choices[:MAX_ITEM_COUNT]
            choice_count = len(choices)
            count = self.choice_radioBox.GetCount()
            for i in range(count):
                if i < choice_count:
                    self.choice_radioBox.SetItemLabel(i, choices[i])
                else:
                    self.choice_radioBox.ShowItem(i, False)
            if default is not None:
                self.choice_radioBox.setSelection(default)

        if do_fit_dlg:
            self.doFit()

    def doFit(self):
        """
        Fit dialog.
        """
        self.choice_radioBox.Layout()
        self.Fit()

    def onCancelButtonClick(self, event):
        self._item_idx = -1
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._item_idx = self.choice_radioBox.GetSelection()
        self.EndModal(wx.ID_OK)
        event.Skip()
