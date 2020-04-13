#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select wxRadioBox item dialog.

Maximum 5 items.
"""

import wx

from . import std_dialogs_proto

__version__ = (0, 0, 0, 1)

# Maximum items
MAX_ITEM_COUNT = 5


class iqRadioChoiceDialog(std_dialogs_proto.radioChoiceDialogProto):
    """
    Select wxRadioBox item dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.radioChoiceDialogProto.__init__(self, *args, **kwargs)

        # Selected item index
        self._item_idx = None

    def getValue(self):
        return self._item_idx

    def init(self, title=None, label=None, choices=(), do_fit_dlg=True):
        """
        Init dialog.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 5 items.
        :param do_fit_dlg: Fit dialog?
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

        if do_fit_dlg:
            self.Fit()

    def onCancelButtonClick(self, event):
        self._item_idx = -1
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._item_idx = self.choice_radioBox.GetSelection()
        self.EndModal(wx.ID_OK)
        event.Skip()
