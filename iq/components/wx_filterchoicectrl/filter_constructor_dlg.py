#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter constructor dialog_func.
"""

import gettext
import wx

from ...engine.wx import wxbitmap_func
from ...util import log_func

from . import filter_constructor
from . import filter_builder_env

__version__ = (0, 0, 0, 1)

_ = gettext.gettext


def getFilterConstructorDlg(parent=None, default_filter_data=None, env=None):
    """
    The function of calling the dialog box of the filter designer.

    :param parent: Parent window.
    :param default_filter_data: Default filter data.
    :param env: Filter constructor environment.
    """
    if env is None:
        log_func.error(u'Not define filter constructor environment')

        env = filter_builder_env.FILTER_ENVIRONMENT

    dlg = None
    win_clear = False
    try:
        if parent is None:
            id_ = wx.NewId()
            parent = wx.Frame(None, id_, '')
            win_clear = True

        dlg = iqFilterConstructorDialog(parent, default_filter_data, env)
        if dlg.ShowModal() in (wx.ID_OK,):
            result = dlg.getFilterData()
            dlg.Destroy()
            # Destroy parent window
            if win_clear:
                parent.Destroy()
            return result
    except:
        log_func.fatal(u'Error filter constructor dialog')

    finally:
        if dlg:
            dlg.Destroy()

        # Destroy parent window
        if win_clear:
           parent.Destroy()
    return None


class iqFilterConstructorDialog(wx.Dialog):
    """
    Filter constructor dialog_func.
    """
    def __init__(self, parent, default_filter_data=None, env=None):
        """
        Constructor.
        """
        try:
            _title = _(u'Filter constructor')

            wx.Dialog.__init__(self, parent, -1, title=_title,
                               style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                               pos=wx.DefaultPosition, size=wx.Size(900, 400))

            icon = None
            icon_img = wxbitmap_func.createIconBitmap('fatcow/filter_advanced')
            if icon_img:
                icon = wx.Icon(icon_img)
            if icon:
                self.SetIcon(icon)

            self._boxsizer = wx.BoxSizer(wx.VERTICAL)

            self._button_boxsizer = wx.BoxSizer(wx.HORIZONTAL)

            button_id = wx.NewId()
            self._ok_button = wx.Button(self, button_id, _(u'OK'), size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.onOK, id=button_id)
            button_id = wx.NewId()
            self._cancel_button = wx.Button(self, button_id, _(u'Cancel'), size=wx.Size(-1, -1))
            self.Bind(wx.EVT_BUTTON, self.onCancel, id=button_id)

            self._button_boxsizer.Add(self._ok_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)
            self._button_boxsizer.Add(self._cancel_button, 0, wx.ALIGN_CENTRE | wx.ALL, 10)

            self._filter_constructor_ctrl = filter_constructor.iqFilterConstructorTreeList(self)

            if env:
                # УSet filter constructor environment
                self._filter_constructor_ctrl.setEnvironment(env)

            if default_filter_data:
                self._filter_constructor_ctrl.setFilterData(default_filter_data)
            else:
                self._filter_constructor_ctrl.setDefault()

            self._boxsizer.Add(self._filter_constructor_ctrl, 1, wx.EXPAND | wx.GROW, 0)
            self._boxsizer.Add(self._button_boxsizer, 0, wx.ALIGN_RIGHT, 10)

            self.SetSizer(self._boxsizer)
            self.SetAutoLayout(True)
        except:
            log_func.fatal(u'Error create filter constructor dialog')

    def onOK(self, event):
        """
        Button <OK> click handler.
        """
        self.EndModal(wx.ID_OK)

    def onCancel(self, event):
        """
        Button <Cancel> click handler.
        """
        self.EndModal(wx.ID_CANCEL)

    def getFilterData(self):
        """
        Get filter data.
        """
        if self._filter_constructor_ctrl:
            return self._filter_constructor_ctrl.getFilterData()
        return None
