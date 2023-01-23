#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extended dialogs functions module.
"""

from ..util import global_func
from ..util import log_func

__version__ = (0, 0, 1, 1)

DIALOG_FUNCTION_MODULE = None


def _importDialogFunctions():
    """
    Check and import dialog function module.

    :return: Dialog function module object or None if error.
    """
    _ext_dlg = None
    if globals()['DIALOG_FUNCTION_MODULE'] is None:
        if global_func.isWXEngine():
            log_func.info(u'Extended dialog functions. Use WX engine')
            from ..engine.wx.dlg import ext_dlg as _ext_dlg
        elif global_func.isQTEngine():
            log_func.warning(u'Extended dialog functions. Not support QT engine')
        elif global_func.isGTKEngine():
            log_func.info(u'Extended dialog functions. Not support GTK engine')
        elif global_func.isCUIEngine():
            log_func.info(u'Extended dialog functions. Not support CUI engine')
        globals()['DIALOG_FUNCTION_MODULE'] = _ext_dlg
    return globals()['DIALOG_FUNCTION_MODULE']


def getMultiChoiceExtDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select multi choice items in extended dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
    :param defaults: Default selection list.
    :return: Selected values or None if press <Cancel>.
    """
    _ext_dlg = _importDialogFunctions()
    if _ext_dlg:
        return _ext_dlg.getMultiChoiceExtDlg(parent=parent, title=title,
                                             label=label, choices=choices, defaults=defaults)
    return None


def getMultiChoiceIdxExtDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select multi choice item indexes in extended dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
    :param defaults: Default selection list.
    :return: Selected values or None if press <Cancel>.
    """
    _ext_dlg = _importDialogFunctions()
    if _ext_dlg:
        return _ext_dlg.getMultiChoiceIdxExtDlg(parent=parent, title=title,
                                                label=label, choices=choices, defaults=defaults)
    return None
