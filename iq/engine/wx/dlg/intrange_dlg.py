#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно ввода диапазона целых номеров.
"""

import wx

try:
    from . import std_dialogs_proto
except ValueError:
    import std_dialogs_proto

__version__ = (0, 0, 0, 1)


class icIntRangeDialog(std_dialogs_proto.intRangeDialogProto):
    """
    Диалоговое окно ввода диапазона целых номеров.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.intRangeDialogProto.__init__(self, *args, **kwargs)

        self._begin_integer_value = None
        self._end_integer_value = None

    def getValue(self):
        return self._begin_integer_value, self._end_integer_value

    def init(self, title=None, label_begin=None, label_end=None, min_value=1, max_value=1000):
        """
        Инициализация диалогового окна.

        :param title: Заголовок окна.
        :param label_begin: Текст приглашения ввода первого номера диапазона.
        :param label_end: Текст приглашения ввода последнего номера диапазона.
        :param min_value: Минимально-допустимое значение.
        :param max_value: Максимально-допустимое значение.
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
        Обработчик изменения значения первого номера диапазона.
        """
        value = self.begin_spinCtrl.GetValue()
        if value > self.end_spinCtrl.GetValue():
            self.end_spinCtrl.SetValue(value)
        event.Skip()

    def onEndSpinCtrl(self, event):
        """
        Обработчик изменения значения последнего номера диапазона.
        """
        value = self.end_spinCtrl.GetValue()
        if value < self.end_spinCtrl.GetValue():
            self.begin_spinCtrl.SetValue(value)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик кнопки <Отмена>.
        """
        self._begin_integer_value = None
        self._end_integer_value = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Обработчик кнопки <OK>.
        """
        self._begin_integer_value = self.begin_spinCtrl.GetValue()
        self._end_integer_value = self.end_spinCtrl.GetValue()
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

    dlg = icIntRangeDialog(frame)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
