#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно ввода целого числа.
"""

import wx

try:
    from . import std_dialogs_proto
except ValueError:
    import std_dialogs_proto

__version__ = (0, 0, 2, 1)

DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 500


class icIntegerDialog(std_dialogs_proto.integerDialogProto):
    """
    Диалоговое окно ввода целого числа.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.integerDialogProto.__init__(self, *args, **kwargs)

        self._integer_value = None

    def getValue(self):
        return self._integer_value

    def init(self, title=None, label=None,
             min_value=DEFAULT_MIN_VALUE, max_value=DEFAULT_MAX_VALUE):
        """
        Инициализация диалогового окна.

        :param title: Заголовок окна.
        :param label: Текст приглашения ввода.
        :param min_value: Минимально-допустимое значение.
        :param max_value: Максимально-допустимое значение.
        """
        if title:
            self.SetTitle(title)
        if label:
            self.label_staticText.SetLabel(label)

        self.value_spinCtrl.SetRange(min(min_value, max_value),
                                     max(min_value, max_value))

    def onCancelButtonClick(self, event):
        self._integer_value = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._integer_value = self.value_spinCtrl.GetValue()
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

    dlg = icIntegerDialog(frame)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
