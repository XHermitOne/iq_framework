#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Select wxCheckBox items dialog.
Maximum 7 items.
"""

import wx

from . import std_dialogs_proto

__version__ = (0, 0, 0, 1)

MAX_ITEM_COUNT = 7


class iqCheckBoxDialog(std_dialogs_proto.checkBoxDialogProto):
    """
    Select wxCheckBox items dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        std_dialogs_proto.checkBoxDialogProto.__init__(self, *args, **kwargs)

        # Checked items
        self._check_items = None
        self._check_item_count = 0

        # CheckBox controlls
        self.check_box_ctrl = (self.item_checkBox1,
                               self.item_checkBox2,
                               self.item_checkBox3,
                               self.item_checkBox4,
                               self.item_checkBox5,
                               self.item_checkBox6,
                               self.item_checkBox7)

    def getValue(self):
        """
        Get checked items.

        :return: Checked items tuple or None if canceled.
            For example: (False, True, True, False).
        """
        return self._check_items

    def init(self, title=None, label=None, choices=(), do_fit_dlg=True,
             defaults=()):
        """
        Init dialog.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
        :param do_fit_dlg: Fit dialog?
        :param defaults: Default checked items.
        """
        if title:
            self.SetTitle(title)
        if label:
            self.label_staticText.SetLabel(label)
        if choices:
            choices = choices[:MAX_ITEM_COUNT]
            self._check_item_count = len(choices)
            for i in range(MAX_ITEM_COUNT):
                check_box_ctrl = self.check_box_ctrl[i]
                if i < self._check_item_count:
                    check_box_ctrl.SetLabel(choices[i])

                    if defaults and i < len(defaults):
                        check = bool(defaults[i])
                        check_box_ctrl.SetValue(check)
                else:
                    check_box_ctrl.Show(False)

        if do_fit_dlg:
            self.Fit()

    def getCheckedList(self):
        """
        Get checked list.

        :return: Checked items tuple.
            For example: (False, True, True, False).
        """
        result = list()
        for i in range(MAX_ITEM_COUNT):
            check_box_ctrl = self.check_box_ctrl[i]
            if i < self._check_item_count:
                result.append(check_box_ctrl.IsChecked())
            else:
                break
        return tuple(result)

    def onCancelButtonClick(self, event):
        self._check_items = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._check_items = self.getCheckedList()
        self.EndModal(wx.ID_OK)
        event.Skip()
