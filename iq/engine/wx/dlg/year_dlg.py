#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора года.
"""

import datetime
import wx
from . import std_dialogs_proto

__version__ = (0, 0, 2, 1)

MIN_YEAR = 1940
MAX_YEAR = MIN_YEAR + 100


class icYearDialog(std_dialogs_proto.yearDialogProto):
    """
    Диалоговое окно выбора года.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.yearDialogProto.__init__(self, *args, **kwargs)

        self._selected_year = None

    def init_year_choice(self):
        """
        Инициализация контрола выбора годов.
        """
        # Заполнить список выбора
        year_choices = [str(i_year) for i_year in range(MIN_YEAR, MAX_YEAR)]
        self.year_choice.AppendItems(year_choices)

        if not self._selected_year:
            # Выбрать текущий системный год
            today = datetime.date.today()
            cur_year_idx = year_choices.index(str(today.year))
        else:
            cur_year_idx = year_choices.index(str(self._selected_year))

        self.year_choice.setSelection(cur_year_idx)

    def getSelectedYear(self):
        return self._selected_year

    def setSelectedYear(self, selected_year):
        if isinstance(selected_year, datetime.datetime) or isinstance(selected_year, datetime.date):
            self._selected_year = selected_year.year
            return
        if not isinstance(selected_year, int):
            self._selected_year = int(selected_year)
            return
        self._selected_year = selected_year

    def getSelectedYearAsDatetime(self):
        if self._selected_year:
            return datetime.datetime(year=self._selected_year, month=1, day=1)
        return None

    def onCancelButtonClick(self, event):
        self._selected_year = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        year_idx = self.year_choice.GetSelection()
        self._selected_year = int(self.year_choice.GetString(year_idx))
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

    dlg = icYearDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
