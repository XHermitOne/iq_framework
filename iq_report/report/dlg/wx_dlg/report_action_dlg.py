#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog box for selecting an action on a report.
"""

import wx

from iq_report.report.dlg.wx_dlg import report_dlg_proto

from iq.util import str_func
from iq.util import log_func
from iq.util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_UNICODE = 'utf-8'

PRINT_ACTION_ID = 'print'
PREVIEW_ACTION_ID = 'preview'
EXPORT_ACTION_ID = 'export'


class iqReportActionDialog(report_dlg_proto.iqReportActionDialogProto):
    """
    Dialog box for selecting an action on a report.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        report_dlg_proto.iqReportActionDialogProto.__init__(self, *args, **kwargs)

        # Selected action
        self._selected_action = None

    def setReportNameTitle(self, report_name):
        """
        Set the name of the report in the title of the dialog box.

        :param report_name: Report name.
        :return: True/False.
        """
        if not isinstance(report_name, str):
            report_name = str_func.toUnicode(report_name, DEFAULT_UNICODE)
        title = _(u'Report:') + ' ' + report_name
        self.SetLabel(title)
        return True

    def getSelectedAction(self):
        """
        Get selected action.

        :return: Selected action identifier.
        """
        return self._selected_action

    def isSelectedPrintAction(self):
        """
        Select PRINT action?

        :return: True/False.
        """
        return self._selected_action == PRINT_ACTION_ID

    def isSelectedPreviewAction(self):
        """
        Selec PREVIEW action?

        :return: True/False.
        """
        return self._selected_action == PREVIEW_ACTION_ID

    def isSelectedExportAction(self):
        """
        Selec EXPORT action?

        :return: True/False.
        """
        return self._selected_action == EXPORT_ACTION_ID

    def onPrintButtonClick(self, event):
        """
        Button click handler <Print>.
        """
        self._selected_action = PRINT_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onPreviewButtonClick(self, event):
        """
        Button click handler <Preview>.
        """
        self._selected_action = PREVIEW_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onExportButtonClick(self, event):
        """
        Button click handler <Export>.
        """
        self._selected_action = EXPORT_ACTION_ID
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Button click handler <Cancel>.
        """
        self._selected_action = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def getReportActionDlg(parent=None, title=''):
    """
    Open the dialog box for selecting an action on the report.

    :param parent: Parent window.
    :param title: Dialog title.
    """
    result = None
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = None
    try:
        dlg = iqReportActionDialog(None)
        dlg.setReportNameTitle(title)
        dlg.ShowModal()
        result = dlg.getSelectedAction()
        dlg.Destroy()
    except:
        log_func.fatal(u'Error report action dialog')
        if dlg:
            dlg.Destroy()
    return result
