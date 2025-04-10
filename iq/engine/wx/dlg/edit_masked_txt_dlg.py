#!/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog box for editing formatted / masked text.
"""

import gettext
import wx
from . import edit_masked_txt_dlg_proto

from ....util import log_func
from . import wxdlg_func

from ....engine.wx import wxbitmap_func

__version__ = (0, 1, 1, 1)

_ = gettext.gettext


class iqEditMaskedTextDlg(edit_masked_txt_dlg_proto.iqEditMaskedTextDlgProto):
    """
    Dialog box for editing formatted / masked text.
    """

    def onCancelButtonClick(self, event):
        """
        The handler for the <Cancel> button.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        The handler for the <OK> button.
        """
        value = self.masked_textCtrl.GetValue()
        # Checking values for correct filling
        if self.masked_textCtrl.IsValid(value):
            self.edit_text = value
        else:
            msg = u'Invalid input value <%s>' % value
            log_func.warning(msg)
            wxdlg_func.openWarningBox(_(u'ERROR'), msg)
            self.edit_text = None
        self.EndModal(wx.ID_OK)
        event.Skip()

    def init(self, title=u'', label=u'',
             default_txt=u'', mask=u'', reg_exp=r''):
        """
        Dialog initialization.

        :param title: Dialog title.
        :param label: Prompt text label.
        :param default_txt: Default text.
        :param mask: Text mask.
        :param reg_exp: Regular expression.
        """
        # Check input parameters
        if default_txt is None:
            default_txt = u''

        self.edit_text = u''

        self.SetTitle(title)
        self.label_staticText.SetLabelText(label)
        log_func.debug(u'Set default value <%s> for editing' % default_txt)
        self.masked_textCtrl.SetMaskParameters(mask=mask,
                                               validRegex=reg_exp)
        # Setting the value m. only after setting the mask parameters
        # SetValue provides additional value control
        self.masked_textCtrl.SetValue(default_txt)

    def getEditText(self):
        """
        Edited value.
        """
        return self.edit_text


def editMaskedTextDlg(parent=None, title=u'', label=u'',
                      default_txt=u'', mask=u'', reg_exp=r'',
                      *args, **kwargs):
    """
    Open dialog function.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param default_txt: Default text.
    :param mask: Mask.
    :param reg_exp: Regular expression.
    :return: Edited value or None, if the <Cancel> button is pressed.
    """
    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    result = None
    dlg = None
    try:
        dlg = iqEditMaskedTextDlg(parent=parent, *args, **kwargs)
        dlg.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/textfield_format')))

        dlg.init(title=title, label=label,
                 default_txt=default_txt, mask=mask, reg_exp=reg_exp)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.getEditText()
        dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error edit masked text dialog')
    return result
