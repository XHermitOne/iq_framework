#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора элемента wxRadioBox.

Максимальное количество элементов выбора 5.
При большем количестве элементов необходимо использовать 
другую диалоговую форму выбора.
"""

import wx

try:
    from . import std_dialogs_proto
except ValueError:
    import std_dialogs_proto

__version__ = (0, 0, 1, 1)

# Максимальное количество элементов выбора
MAX_ITEM_COUNT = 5


class icRadioChoiceDialog(std_dialogs_proto.radioChoiceDialogProto):
    """
    Диалоговое окно выбора элемента wxRadioBox.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.radioChoiceDialogProto.__init__(self, *args, **kwargs)

        # Выбранный элемент
        self._item_idx = None

    def getValue(self):
        return self._item_idx

    def init(self, title=None, label=None, choices=(), do_fit_dlg=True):
        """
        Инициализация диалогового окна.

        :param title: Заголовок окна.
        :param label: Текст приглашения ввода.
        :param choices: Список выбора.
            Максимальное количество элементов выбора 5.
            При большем количестве элементов необходимо использовать 
            другую диалоговую форму выбора.
        :param do_fit_dlg: Переразмерить диалоговое окно для удаления
            не заполненной области отсутствующих элементов?
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

        # Т.к не все элементы отображаются переразмерить окно для того чтобы
        # не было пустого места
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

    dlg = icRadioChoiceDialog(frame)
    dlg.init(u'Заголовок окна', u'Выбор:',
             (u'Элемент 1', u'Элемент 2', u'Элемент 3'))

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
