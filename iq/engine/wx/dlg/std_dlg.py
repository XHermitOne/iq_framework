#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standart dialog functions module.
"""

import datetime
import wx
import wx.lib.calendar

from . import calendar_dlg
from . import year_dlg
from . import month_dlg
from . import quarter_dlg
from . import monthrange_dlg
from . import daterange_dlg

# from . import icnsilistdlg
from . import integer_dlg
from . import radiochoice_dlg
from . import intrange_dlg
from . import checkbox_dlg
from . import radiochoicemaxi_dlg
from . import checkboxmaxi_dlg

from iq.util import log_func
from iq.util import dt_func
from . import wxdlg_func
from .. import wxdatetime_func


__version__ = (0, 1, 1, 2)


def getIntegerDlg(parent=None, title=None, label=None, min_value=0, max_value=100, default_value=0):
    """
    Entry integer number in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param label: Prompt text.
    :param min_value: Minimum value.
    :param max_value: Maximum value.
    :param default_value: Default value.
    :return: Entered value or None if press <Cancel>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = integer_dlg.iqIntegerDialog(parent)
    dlg.init(title=title, label=label, min_value=min_value, max_value=max_value, default_value=default_value)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getDateDlg(parent=None, default_date=None):
    """
    Select date dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param default_date: If define then set default date.
    :return: Selected date (as datetime) or None if press <Cancel>.
    """
    selected_date = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = calendar_dlg.iqCalendarDialog(parent)
    if default_date:
        dlg.setSelectedDate(default_date)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_date = dlg.getSelectedDateAsDatetime()
    dlg.Destroy()

    return selected_date


def getYearDlg(parent=None, title=None, default_year=None):
    """
    Select year in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param default_year: Default year.
    :return: Selected year (as datetime) or None if press <Cancel>.
    """
    selected_year = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = year_dlg.iqYearDialog(parent)
    dlg.Centre()

    if title:
        dlg.SetTitle(title)

    if default_year:
        dlg.setSelectedYear(default_year)
    dlg.initYearChoice()

    if dlg.ShowModal() == wx.ID_OK:
        selected_year = dlg.getSelectedYearAsDatetime()
    dlg.Destroy()

    return selected_year


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
    if default_year is None:
        default_year = datetime.date.today().year
    start_choice_year = datetime.date.today().year - month_dlg.DEFAULT_YEAR_RANGE
    if default_month is None:
        default_month = datetime.date.today().month

    selected_month = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = month_dlg.iqMonthDialog(parent)
    if title:
        dlg.SetTitle(title)
    dlg.Centre()

    # Set default
    dlg.year_choice.Select(default_year - start_choice_year)
    dlg.month_choice.Select(default_month - 1)

    if dlg.ShowModal() == wx.ID_OK:
        selected_month = dlg.getSelectedMonthAsDatetime()
    dlg.Destroy()

    return selected_month


def getQuarterDlg(parent=None):
    """
    Select quarter in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :return: Tuple (year, quarter number) or None press <Cancel>.
    """
    selected_quarter = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = quarter_dlg.iqQuarterDialog(parent=parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_quarter = dlg.getSelectedQuarter()
    dlg.Destroy()

    return selected_quarter


MONTH_CHOICES = dt_func.getMonths()


def getMonthNumDlg(parent=None, title=None, text=None):
    """
    Select month number in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :param title: Dialog title.
    :param text: Prompt text.
    :return: Month number or None if press <Cancel>.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    title = u'MONTH' if title is None else title
    text = u'Select month' if text is None else text
    selected_idx = wxdlg_func.getSingleChoiceIdxDlg(parent, title=title, prompt_text=text, choices=MONTH_CHOICES)
    if selected_idx >= 0:
        return selected_idx + 1
    return None


def getMonthRangeDlg(parent=None):
    """
    Select month range in dialog.

    :param parent: Parent window.
        If None then get wx.GetApp().GetTopWindow()
    :return: Month range tuple (as datetime) or None if press <Cancel>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = monthrange_dlg.iqMonthRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedMonthRangeAsDatetime()
    dlg.Destroy()

    return selected_range


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
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = daterange_dlg.iqDateRangeDialog(parent)
    dlg.setConcreteDateCheck(is_concrete_date)
    if default_start_date:
        if isinstance(default_start_date, wx.DateTime):
            wx_date = default_start_date
        else:
            wx_date = wxdatetime_func.date2wxDateTime(default_start_date)
        if wx_date:
            dlg.firstDatePicker.SetValue(wx_date)
    if default_stop_date:
        if isinstance(default_stop_date, wx.DateTime):
            wx_date = default_stop_date
        else:
            wx_date = wxdatetime_func.date2wxDateTime(default_stop_date)
        if wx_date:
            dlg.lastDatePicker.SetValue(wx_date)

    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedDateRangeAsDatetime()
    dlg.Destroy()

    if selected_range:
        try:
            log_func.debug(u'Selected date range: <%s> - <%s>' % selected_range)
        except:
            pass
    return selected_range


# def getNSIListDlg(parent=None,
#                   db_url=None, nsi_sprav_tabname=None,
#                   code_fieldname='cod', name_fieldname='name',
#                   ext_filter=''):
#     """
#     Выбор значения из простого спискового справочника.
#
#     :param parent: Родительское окно. Если не определено, то
#         береться wx.GetApp().GetTopWindow()
#     :param db_url: URL подключения к БД.
#     :param nsi_sprav_tabname: Имя таблицы справочника.
#     :param code_fieldname: Имя поля кода в таблице справочника.
#     :param name_fieldname: Имя поля наименования в таблице справочника.
#     :param ext_filter: Дополнительный фильтр записей.
#     :return: Выбранный код справочника или None если нажата <отмена>.
#     """
#     selected_code = None
#
#     if parent is None:
#         parent = wx.GetApp().GetTopWindow()
#
#     dlg = icnsilistdlg.icNSIListDialog(parent)
#     dlg.Centre()
#     dlg.setDbURL(db_url)
#     dlg.initChoice(nsi_sprav_tabname, code_fieldname, name_fieldname, ext_filter)
#
#     if dlg.ShowModal() == wx.ID_OK:
#         selected_code = dlg.getSelectedCode()
#
#     try:
#         dlg.Destroy()
#     except wx.PyDeadObjectError:
#         print(u'wx.PyDeadObjectError. Ошибка удаления диалогового окна')
#     return selected_code


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
    frame = wx.Frame(None, -1)
    frame.Center()

    result = dict()

    for dlg in dlgs:
        dlg_func = dlg.get('function', None)
        args = dlg.get('args', tuple())
        kwargs = dlg.get('kwargs', dict())
        if dlg_func:
            result_key = dlg['key'] if 'key' in dlg else dlg_func.__name__
            result[result_key] = dlg_func(parent=frame, *args, **kwargs)

    frame.Destroy()
    return result


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = radiochoice_dlg.iqRadioChoiceDialog(parent)
    dlg.init(title=title, label=label, choices=choices)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = intrange_dlg.iqIntRangeDialog(parent)
    dlg.init(title=title, label_begin=label_begin, label_end=label_end,
             min_value=min_value, max_value=max_value)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = checkbox_dlg.iqCheckBoxDialog(parent)
    dlg.init(title=title, label=label, choices=choices, defaults=defaults)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = radiochoicemaxi_dlg.iqRadioChoiceMaxiDialog(parent)
    dlg.init(title=title, label=label, choices=choices, default=default)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


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
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = checkboxmaxi_dlg.iqCheckBoxMaxiDialog(parent)
    dlg.init(title=title, label=label, choices=choices, defaults=defaults)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value
