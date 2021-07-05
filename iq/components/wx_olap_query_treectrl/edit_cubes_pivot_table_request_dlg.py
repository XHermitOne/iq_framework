#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Edit OLAP server pivot table request dialog.
"""

import wx

from . import edit_cubes_olap_srv_request_dlg_proto

from ...util import log_func


__version__ = (0, 0, 0, 1)


class iqEditCubesPivotTabRequestDialog(edit_cubes_olap_srv_request_dlg_proto.iqEditCubesPivotTabRequestDlgProto):
    """
    Edit OLAP server pivot table request dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        edit_cubes_olap_srv_request_dlg_proto.iqEditCubesPivotTabRequestDlgProto.__init__(self, *args, **kwargs)

        # OLAP server
        self._OLAP_server = None

        # Request struct data
        self._request = None

    def setOLAPServer(self, olap_server):
        """
        Set OLAP server.

        :param olap_server: OLAP server object.
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            self.request_panel.setOLAPServer(self._OLAP_server, refresh=True)

    def getRequest(self):
        """
        Get request struct data.
        """
        return self._request

    def setRequest(self, request=None):
        """
        Set request struct data.

        :param request: Request struct data as dictionary.
        """
        self._request = request

        if self._request:
            self.request_panel.setRequest(self._request)

    def onCancelButtonClick(self, event):
        """
        CANCEL button handler.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        OK button handler.
        """
        self._request = self.request_panel.getRequest()
        # We save the url separately for further use in the browser
        self._request['url'] = self.request_panel.getRequestURL(self._request)
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRefreshButtonClick(self, event):
        """
        URL refresh button handler.
        """
        url = self.request_panel.getRequestURL()
        self.request_panel.request_textCtrl.SetValue(url)
        event.Skip()


def editCubesPivotTableRequestDlg(parent=None, olap_srv=None, olap_srv_request=None):
    """
    Open edit OLAP server pivot table request dialog.

    :param parent: Parent window. If not defined then get main window.
    :param olap_srv: OLAP server object.
    :param olap_srv_request: OLAP server request struct.
    :return: Edited OLAP server request struct or None, if <Cancel> pressed.
    """
    if olap_srv is None:
        log_func.warning(u'OLAP server object not defined for edit pivot table request')
        return None

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        dlg = iqEditCubesPivotTabRequestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)
        log_func.debug(u'Edit request %s' % str(olap_srv_request))
        dlg.setRequest(olap_srv_request)

        result = None
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getRequest()
        dlg.Destroy()
        return result
    except:
        log_func.fatal(u'Error edit OLAP server pivot table request')
    return None
