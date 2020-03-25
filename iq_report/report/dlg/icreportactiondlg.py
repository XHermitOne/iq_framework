#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора действия над отчетом.
"""

import wx
from . import report_dlg_proto
from ic.std.utils import textfunc

__version__ = (0, 1, 1, 1)

DEFAULT_UNICODE = 'utf-8'

PRINT_ACTION_ID = 'print'
PREVIEW_ACTION_ID = 'preview'
EXPORT_ACTION_ID = 'export'


class icReportActionDialog(report_dlg_proto.icReportActionDialogProto):
    """
    Диалоговое окно выбора действия над отчетом.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        report_dlg_proto.icReportActionDialogProto.__init__(self, *args, **kwargs)

        # Выбранное действие
        self._selected_action = None

    def setReportNameTitle(self, report_name):
        """
        Установить наименование отчета в заголовке диалогового окна.

        :param report_name: Имя отчета
        :return: True/False.
        """
        if not isinstance(report_name, str):
            report_name = textfunc.toUnicode(report_name, DEFAULT_UNICODE)
        title = u'Отчет: %s' % report_name
        self.SetLabel(title)
        return True

    def getSelectedAction(self):
        """
        Выбранное действие.

        :return: Строка-идентификатор выбранного действия.
        """
        return self._selected_action

    def isSelectedPrintAction(self):
        """
        Выбрано действие ПЕЧАТЬ?

        :return: True/False.
        """
        return self._selected_action == PRINT_ACTION_ID

    def isSelectedPreviewAction(self):
        """
        Выбрано действие ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР?

        :return: True/False.
        """
        return self._selected_action == PREVIEW_ACTION_ID

    def isSelectedExportAction(self):
        """
        Выбрано действие ЭКСПОРТ В ОФИС ПО?

        :return: True/False.
        """
        return self._selected_action == EXPORT_ACTION_ID

    def onPrintButtonClick(self, event):
        """
        Обработчик нажатия на кнопку <Печать>.
        """
        self._selected_action = PRINT_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onPreviewButtonClick(self, event):
        """
        Обработчик нажатия на кнопку <Предварительный просмотр>.
        """
        self._selected_action = PREVIEW_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onExportButtonClick(self, event):
        """
        Обработчик нажатия на кнопку <Экспорт в Office>.
        """
        self._selected_action = EXPORT_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Обработчик нажатия на кнопку <Отмена>.
        """
        self._selected_action = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def getReportActionDlg(parent=None, title=''):
    """
    Запустить диалоговое окно выбора действия над отчетом.

    :param parent: Родительское wxWindow окно.
    :param title: Заголовок диалогового окна. Обычно это имя отчета.
    """
    result = None
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = None
    try:
        dlg = icReportActionDialog(None)
        dlg.setReportNameTitle(title)
        dlg.ShowModal()
        result = dlg.getSelectedAction()
        dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
            raise
    return result


def test():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()

    dlg = icReportActionDialog(None)

    dlg.ShowModal()

    print((u'ACTION <%s>' % dlg.getSelectedAction()))

    dlg.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    test()
