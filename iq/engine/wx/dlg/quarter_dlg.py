#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора квартала.
"""

import datetime
import wx
from . import std_dialogs_proto

__version__ = (0, 1, 1, 1)

TODAY = datetime.date.today()

# Диапазон списка годов
DEFAULT_YEAR_RANGE = 10

# Список годов
YEAR_LIST = [TODAY.year + i for i in range(-DEFAULT_YEAR_RANGE, DEFAULT_YEAR_RANGE)]


class icQuarterDialog(std_dialogs_proto.quarterDialogProto):
    """
    Диалоговое окно выбора квартала.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.quarterDialogProto.__init__(self, *args, **kwargs)

        # Выбрать текущий месяц
        cur_quarter = self.get_cur_quarter(today=TODAY)
        self.quarter_choice.Select(cur_quarter - 1)

        # Заполнить список годов
        self.year_choice.Clear()
        self.year_choice.AppendItems([str(n_year) for n_year in YEAR_LIST])

        # Выбрать текущий год
        self.year_choice.Select(YEAR_LIST.index(TODAY.year))

        self._selected_quarter = None

    def get_cur_quarter(self, today=None):
        """
        Определить квартал относительно текущего дня.

        :param today: Текущий/сегодняшний день.
            Если не определен, то берется datetime.date.today()
        :return: Номер квартала.
        """
        if today is None:
            today = datetime.date.today()
        cur_month = today.month
        return (cur_month - 1)//3 + 1

    def getSelectedQuarter(self):
        return self._selected_quarter

    def onCancelButtonClick(self, event):
        self._selected_quarter = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_quarter = (YEAR_LIST[self.year_choice.GetSelection()],
                                  self.quarter_choice.GetSelection() + 1)
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

    dlg = icQuarterDialog(frame)

    result = dlg.ShowModal()
    if result == wx.ID_OK:
        print(u'Selected quarter <%s>' % dlg.getSelectedQuarter())

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
