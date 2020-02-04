#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора периода по датам.
"""

import wx
from . import std_dialogs_proto

try:
    from ic.std.utils import ic_time
except ImportError:
    from ic.utils import datetimefunc

try:
    from ic.log import log
except ImportError:
    pass

__version__ = (0, 1, 2, 1)


class icDateRangeDialog(std_dialogs_proto.dateRangeDialogProto):
    """
    Диалоговое окно выбора периода по датам.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        std_dialogs_proto.dateRangeDialogProto.__init__(self, *args, **kwargs)

        self._selected_range = None

    def getSelectedDateRange(self):
        return self._selected_range

    def getSelectedDateRangeAsDatetime(self):
        if self._selected_range:
            return datetimefunc.wxdate2pydate(self._selected_range[0]), datetimefunc.wxdate2pydate(self._selected_range[1])
        return None

    def setConcreteDateCheck(self, checked=True):
        """
        Вкл./выкл. режима установки конкретной даты.

        :param checked: Установлена метка или нет. 
        """
        self.concrete_date_checkBox.SetValue(checked)
        self.lastDatePicker.Enable(not checked)
        if checked:
            first_date = self.firstDatePicker.GetValue()
            self.lastDatePicker.SetValue(first_date)

    def onCancelButtonClick(self, event):
        self._selected_range = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self._selected_range = (self.firstDatePicker.GetValue(),
                                self.lastDatePicker.GetValue())
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onFirstDateChanged(self, event):
        """
        Обработчик изменения начальной даты диапазона. 
        """
        first_date = event.GetDate()
        last_date = self.lastDatePicker.GetValue()

        if first_date > last_date:
            self.lastDatePicker.SetValue(first_date)
        elif self.concrete_date_checkBox.IsChecked():
            self.lastDatePicker.SetValue(first_date)

        event.Skip()

    def onLastDateChanged(self, event):
        """
        Обработчик изменения конечной даты диапазона. 
        """
        first_date = self.firstDatePicker.GetValue()
        last_date = event.GetDate()

        try:
            log.debug(u'Корректировка конечной даты <%d.%d.%d>' % (last_date.GetDay(),
                                                                   last_date.GetMonth(),
                                                                   last_date.GetYear()))
        except:
            pass
        if first_date > last_date and len(str(last_date.GetYear())) == 4:
            self.lastDatePicker.SetValue(first_date)

        event.Skip()

    def onConcreteDateCheckBox(self, event):
        """
        Обработчик вкл./выкл. флага конкретной даты.
        """
        checked = event.IsChecked()
        self.lastDatePicker.Enable(not checked)
        if checked:
            first_date = self.firstDatePicker.GetValue()
            self.lastDatePicker.SetValue(first_date)
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

    dlg = icDateRangeDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
