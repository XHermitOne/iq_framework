#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора элементов wxCheckBox.

Максимальное количество элементов выбора 7.
При большем количестве элементов необходимо использовать 
другую диалоговую форму выбора.
"""

import wx

try:
    from . import std_dialogs_proto
except ValueError:
    import std_dialogs_proto

__version__ = (0, 1, 1, 1)

# Максимальное количество элементов выбора
MAX_ITEM_COUNT = 7


class icCheckBoxDialog(std_dialogs_proto.checkBoxDialogProto):
    """
    Диалоговое окно выбора элементов wxCheckBox.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.checkBoxDialogProto.__init__(self, *args, **kwargs)

        # Выбранные элементы
        self._check_items = None
        self._check_item_count = 0

        # Список контролов CheckBox
        self.check_box_ctrl = (self.item_checkBox1,
                               self.item_checkBox2,
                               self.item_checkBox3,
                               self.item_checkBox4,
                               self.item_checkBox5,
                               self.item_checkBox6,
                               self.item_checkBox7)

    def getValue(self):
        """
        Выбранные элементы.

        :return: Кортеж выбранных элементов либо None при отмене выбора.
            Например (False, True, True, False).
        """
        return self._check_items

    def init(self, title=None, label=None, choices=(), do_fit_dlg=True,
             defaults=()):
        """
        Инициализация диалогового окна.

        :param title: Заголовок окна.
        :param label: Текст приглашения ввода.
        :param choices: Список выбора.
            Максимальное количество элементов выбора 7.
            При большем количестве элементов необходимо использовать 
            другую диалоговую форму выбора.
        :param do_fit_dlg: Переразмерить диалоговое окно для удаления
            не заполненной области отсутствующих элементов?
        :param defaults: Список отметок по умолчанию.
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
                    # Установить значение по умолчанию
                    if defaults and i < len(defaults):
                        check = bool(defaults[i])
                        check_box_ctrl.SetValue(check)
                else:
                    check_box_ctrl.Show(False)

        # Т.к не все элементы отображаются переразмерить окно для того чтобы
        # не было пустого места
        if do_fit_dlg:
            self.Fit()

    def getCheckedList(self):
        """
        Список выбранных отметок.

        :return: Кортеж выбранных элементов.
            Например (False, True, True, False).
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

    dlg = icCheckBoxDialog(frame)
    dlg.init(u'Заголовок окна', u'Выбор:',
             (u'Элемент 1', u'Элемент 2', u'Элемент 3 '))

    dlg.ShowModal()
    selected = dlg.getValue()
    print(selected)

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
