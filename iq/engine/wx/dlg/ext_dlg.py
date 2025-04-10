#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extended dialog functions module.
"""

import datetime
import wx

from . import multichoice_ext_dlg

from iq.util import log_func

from ....engine.wx import wxbitmap_func

__version__ = (0, 1, 1, 1)


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = multichoice_ext_dlg.iqMultiChoiceExtDialog(parent)

    dlg_choices = [(True if isinstance(defaults, (list, tuple)) and choices[i] in defaults else False, choices[i]) for i in range(len(choices))] if choices else list()
    dlg.init(title=title, label=label, choices=dlg_choices)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getMultiChoiceIdxExtDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select multi choice item indexes in extended dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
    :param defaults: Default selection list.
    :return: Selected item indexes or None if press <Cancel>.
    """
    selected_items = getMultiChoiceExtDlg(parent=parent, title=title, label=label,
                                          choices=choices, defaults=defaults)
    if selected_items is None:
        # Press CANCEL button
        return None
    try:
        return [choices.index(item) for item in selected_items]
    except:
        log_func.fatal(u'Error get multi choice extended dialog item indexes')
    return None
