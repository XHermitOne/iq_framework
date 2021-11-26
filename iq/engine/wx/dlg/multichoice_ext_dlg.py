#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi choice extended dialog.
"""

import wx
from . import ext_dialogs_proto

__version__ = (0, 0, 0, 1)


class iqMultiChoiceExtDialog(ext_dialogs_proto.MultiChoiceListBoxExtDialogProto):
    """
    Select multi choice extended dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        ext_dialogs_proto.MultiChoiceListBoxExtDialogProto.__init__(self, *args, **kwargs)

        self._selected_items = None

    def init(self, title=None, label=None, choices=None):
        """
        Init dialog.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: List of selection lines as tuple in format ((True/False, 'line text'),...).
        """
        if title:
            self.SetTitle(title)
        if label:
            self.label_staticText.SetLabel(label)

        if isinstance(choices, (list, tuple)):
            for i, item in enumerate(choices):
                self.items_checkList.Append(item[1])
                if item[0]:
                    self.items_checkList.Check(i, item[0])

    def onCancelButtonClick(self, event):
        """
        Cancel click button handler.
        """
        self._selected_items = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        OK click button handler.
        """
        self._selected_items = self.items_checkList.GetCheckedStrings()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSelectWithoutButtonClick(self, event):
        """
        Select without items click button handler.
        """
        checked_items = self.items_checkList.GetCheckedStrings()
        self._selected_items = [item for item in self.items_checkList.GetItems() if item not in checked_items]
        self.EndModal(wx.ID_OK)
        event.Skip()

    def getSelectedItems(self):
        """
        Get selected items.
        """
        return self._selected_items

    def onClearToolClicked(self, event):
        """
        Clear tool click handler.
        """
        for i, item in enumerate(self.items_checkList.GetItems()):
            self.items_checkList.Check(i, False)
        event.Skip()

    def onSetAllToolClicked(self, event):
        """
        Set all tool click handler.
        """
        for i, item in enumerate(self.items_checkList.GetItems()):
            self.items_checkList.Check(i, True)
        event.Skip()

    # Function alias
    getValue = getSelectedItems
