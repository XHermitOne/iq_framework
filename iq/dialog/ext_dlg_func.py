#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extended dialogs functions module.
"""

from ..util import global_func
from ..util import log_func

if global_func.isWXEngine():
    from ..engine.wx.dlg import ext_dlg as _ext_dlg
elif global_func.isQTEngine():
    _ext_dlg = None
    log_func.warning(u'Extended dialog functions. Not support QT engine')
elif global_func.isCUIEngine():
    _ext_dlg = None
    log_func.warning(u'Extended dialog functions. Not support CUI engine')

__version__ = (0, 0, 0, 1)


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
    if _ext_dlg:
        return _ext_dlg.getMultiChoiceIdxExtDlg(parent=parent, title=title,
                                                label=label, choices=choices, defaults=defaults)
    return None
