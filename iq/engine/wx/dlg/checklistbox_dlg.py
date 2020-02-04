#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора элементов из списка.
"""

import wx
from . import std_dialogs_proto


__version__ = (0, 1, 1, 1)


class icCheckListBoxDialog(std_dialogs_proto.checkListBoxDialogProto):
    """
    Диалоговое окно выбора элементов из списка.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.checkListBoxDialogProto.__init__(self, *args, **kwargs)

    def onCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()


def test():
    """
    Тестирование.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)

    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    dlg = icCheckListBoxDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
