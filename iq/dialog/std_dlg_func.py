#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standart dialogs functions module.
"""

from ..util import global_func
from ..util import log_func

__version__ = (0, 1, 1, 2)

DIALOG_FUNCTION_MODULE = None


def _importDialogFunctions():
    """
    Check and import dialog function module.

    :return: Dialog function module object or None if error.
    """
    _std_dlg = None
    if globals()['DIALOG_FUNCTION_MODULE'] is None:
        if global_func.isWXEngine():
            log_func.info(u'Standard dialog functions. Use WX engine')
            from ..engine.wx.dlg import std_dlg as _std_dlg
        elif global_func.isQTEngine():
            log_func.warning(u'Standard dialog functions. Not support QT engine')
        elif global_func.isGTKEngine():
            log_func.info(u'Standard dialog functions. Use GTK engine')
            from ..engine.gtk.dlg import std_dlg as _std_dlg
        elif global_func.isCUIEngine():
            log_func.info(u'Standard dialog functions. Not support QT engine')
        globals()['DIALOG_FUNCTION_MODULE'] = _std_dlg
    return globals()['DIALOG_FUNCTION_MODULE']


def getIntegerDlg(parent=None, title=None, label=None, min_value=0, max_value=100, default_value=0):
    """
    Entry integer number in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param min_value: Minimum value.
    :param max_value: Maximum value.
    :param  default_value: Default value.
    :return: Entered value or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getIntegerDlg(parent=parent, title=title,
                                      label=label, min_value=min_value,
                                      max_value=max_value,
                                      default_value=default_value)
    return None


def getDateDlg(parent=None, default_date=None):
    """
    Select date dalog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param default_date: If define then set default date.
    :return: Selected date (as datetime) or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getDateDlg(parent=parent, default_date=default_date)
    return None


def getYearDlg(parent=None, title=None, default_year=None):
    """
    Select year in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param default_year: Default year.
    :return: Selected year (as datetime) or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getYearDlg(parent=parent, title=title,
                                   default_year=default_year)
    return None


def getMonthDlg(parent=None, title=None, default_year=None, default_month=None):
    """
    Select month in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param default_year: Default year. If None then get current year.
    :param default_month: Default month (1-12). If None then get current month.
    :return: Selected first month day (as datetime) or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getMonthDlg(parent=parent, title=title, default_year=default_year, default_month=default_month)
    return None


def getQuarterDlg(parent=None):
    """
    Select quarter in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :return: Tuple (year, quarter number) or None press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getQuarterDlg(parent=parent)
    return None


def getMonthNumDlg(parent=None, title=None, text=None):
    """
    Select month number in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param text: Prompt text.
    :return: Month number or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getMonthNumDlg(parent=parent, title=title,
                                       text=text)
    return None


def getMonthRangeDlg(parent=None):
    """
    Select month range in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :return: Month range tuple (as datetime) or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getMonthRangeDlg(parent=parent)
    return None


def getDateRangeDlg(parent=None, is_concrete_date=False,
                    default_start_date=None, default_stop_date=None):
    """
    Select date range in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param is_concrete_date: Select concrete date?
    :param default_start_date: Default begin range date.
    :param default_stop_date: Default end range date.
    :return: Date range tuple (as datetime) or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getDateRangeDlg(parent=parent,
                                        is_concrete_date=is_concrete_date,
                                        default_start_date=default_start_date,
                                        default_stop_date=default_stop_date)
    return None


def getStdDlgQueue(*dlgs):
    """
    Open dialogs queue.

    :param dlgs: Dialog box description dictionaries list.
        Format:
        {'key': Result name,
         'function': Dialog function,
         'args': Dialog function arguments,
         'kwargs': Dialog function named arguments}.
    :return: Result dictionary.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getStdDlgQueue(*dlgs)
    return None


def getRadioChoiceDlg(parent=None, title=None, label=None, choices=()):
    """
    Select wxRadioBox item.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 5 items.
    :return: Selected item index or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getRadioChoiceDlg(parent=parent, title=title,
                                          label=label, choices=choices)
    return None


def getIntRangeDlg(parent=None, title=None, label_begin=None, label_end=None, min_value=0, max_value=100):
    """
    Entry integer range in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label_begin: First prompt text.
    :param label_end: Second prompt text.
    :param min_value: Minimal value.
    :param max_value: Maximal value.
    :return: Entered value or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getIntRangeDlg(parent=parent, title=title,
                                       label_begin=label_begin,
                                       label_end=label_end,
                                       min_value=min_value,
                                       max_value=max_value)
    return None


def getCheckBoxDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select wxCheckBox items in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 7 items.
    :param defaults: Default selection list.
    :return: Selected values or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getCheckBoxDlg(parent=parent, title=title,
                                       label=label,
                                       choices=choices, defaults=defaults)
    return None


def getRadioChoiceMaxiDlg(parent=None, title=None, label=None,
                          choices=(), default=None):
    """
    Select wxRadioBox item in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 15 items.
    :param default: Default selection list.
    :return: Selected item index or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getRadioChoiceMaxiDlg(parent=parent, title=title,
                                              label=label, choices=choices,
                                              default=default)
    return None


def getCheckBoxMaxiDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select wxCheckBox items in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 15 items.
    :param defaults: Default selection list.
    :return: Selected items index or None if press <Cancel>.
    """
    _std_dlg = _importDialogFunctions()
    if _std_dlg:
        return _std_dlg.getCheckBoxMaxiDlg(parent=parent, title=title,
                                           label=label, choices=choices,
                                           defaults=defaults)
    return None
