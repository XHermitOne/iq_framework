#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standard dialog functions.
"""

import datetime

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ....util import log_func
from ....util import dt_func
from ....engine.gtk.dlg import gtk_dlg_func

from . import integer_dialog
from . import calendar_dialog
from . import year_dialog
from . import month_dialog
from . import quarter_dialog
from . import month_range_dialog
from . import date_range_dialog
from . import radio_choice_dialog
from . import int_range_dialog
from . import checkbox_dialog
from . import radio_choice_maxi_dialog
from . import checkbox_maxi_dialog

__version__ = (0, 0, 1, 2)


def getIntegerDlg(parent=None, title=None, label=None, min_value=0, max_value=100):
    """
    Entry integer number in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param min_value: Minimum value.
    :param max_value: Maximum value.
    :return: Entered value or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = integer_dialog.iqIntegerDialog()
        dlg.init(title=title, label=label, min_value=min_value, max_value=max_value)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getGtkObject('integer_spinbutton').get_value()
    except:
        log_func.fatal(u'Error integer dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return value


def getDateDlg(parent=None, default_date=None):
    """
    Select date dialog.

    :param parent: Parent window.
    :param default_date: If define then set default date.
    :return: Selected date (as datetime) or None if press <Cancel>.
    """
    selected_date = None

    dlg = None

    try:
        dlg = calendar_dialog.iqCalendarDialog()
        dlg.init(default_date=default_date)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            selected_year, selected_month, selected_day = dlg.getGtkObject('calendar').get_date()
            selected_date = datetime.date.today().replace(year=selected_year,
                                                          month=selected_month + 1,
                                                          day=selected_day)
    except:
        log_func.fatal(u'Error date dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_date


def getYearDlg(parent=None, title=None, default_year=None):
    """
    Select year in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param default_year: Default year.
    :return: Selected year (as datetime) or None if press <Cancel>.
    """
    selected_year = None
    dlg = None

    try:
        dlg = year_dialog.iqYearDialog()
        dlg.init(title=title, default_year=default_year)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            year = dlg.getGtkObject('year_spinbutton').get_value()
            selected_year = datetime.date.today().replace(year=year, month=1, day=1)
    except:
        log_func.fatal(u'Error year dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_year


def getMonthDlg(parent=None, title=None, default_year=None, default_month=None):
    """
    Select month in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param default_year: Default year.
    :param default_month: Default month.
    :return: Selected first month day (as datetime) or None if press <Cancel>.
    """
    selected_month = None
    dlg = None

    try:
        dlg = month_dialog.iqMonthDialog()
        dlg.init(title=title, default_year=default_year, default_month=default_month)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            year = dlg.getGtkObject('year_spinbutton').get_value()
            month = dlg.getGtkObject('month_combobox').get_active()
            selected_month = datetime.date.today().replace(year=int(year),
                                                           month=month + 1,
                                                           day=1)
    except:
        log_func.fatal(u'Error month dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_month


def getQuarterDlg(parent=None, title=None, default_quarter=None, default_year=None):
    """
    Select quarter in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param default_year: Default year.
    :param default_quarter: Default quarter.
    :return: Tuple (year, quarter number) or None press <Cancel>.
    """
    selected_quarter = None
    dlg = None

    try:
        dlg = quarter_dialog.iqQuarterDialog()
        dlg.init(title=title, default_year=default_year, default_quarter=default_quarter)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            year = dlg.getGtkObject('year_spinbutton').get_value()
            quarter = dlg.getGtkObject('quarter_combobox').get_active() + 1
            selected_quarter = (year, quarter)
    except:
        log_func.fatal(u'Error quarter dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_quarter


MONTH_CHOICES = dt_func.getMonths()


def getMonthNumDlg(parent=None, title=None, text=None):
    """
    Select month number in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param text: Prompt text.
    :return: Month number or None if press <Cancel>.
    """
    title = u'MONTH' if title is None else title
    text = u'Select month' if text is None else text
    selected_idx = gtk_dlg_func.getSingleChoiceIdxDlg(parent, title=title, prompt_text=text, choices=MONTH_CHOICES)
    if selected_idx >= 0:
        return selected_idx + 1
    return None


def getMonthRangeDlg(parent=None, title=None, default_from_year=None, default_from_month=None,
                     default_to_year=None, default_to_month=None):
    """
    Select month range in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param default_from_year: Default from year.
    :param default_from_month: Default from month.
    :param default_to_year: Default to year.
    :param default_to_month: Default to month.
    :return: Month range tuple (as datetime) or None if press <Cancel>.
    """
    selected_range = None
    dlg = None

    try:
        dlg = month_range_dialog.iqMonthRangeDialog()
        dlg.init(title=title,
                 default_from_year=default_from_year,
                 default_from_month=default_from_month,
                 default_to_year=default_to_year,
                 default_to_month=default_to_month)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            from_year = dlg.getGtkObject('from_year_spinbutton').get_value()
            from_month = dlg.getGtkObject('from_month_combobox').get_active()
            selected_from_month = datetime.date.today().replace(year=from_year, month=from_month, day=1)
            to_year = dlg.getGtkObject('to_year_spinbutton').get_value()
            to_month = dlg.getGtkObject('to_month_combobox').get_active()
            selected_to_month = datetime.date.today().replace(year=to_year, month=to_month, day=1)
            selected_range = (selected_from_month, selected_to_month)
    except:
        log_func.fatal(u'Error month range dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_range


def getDateRangeDlg(parent=None, title=None, is_concrete_date=False,
                    default_start_date=None, default_stop_date=None):
    """
    Select date range in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param is_concrete_date: Select concrete date?
    :param default_start_date: Default begin range date.
    :param default_stop_date: Default end range date.
    :return: Date range tuple (as datetime) or None if press <Cancel>.
    """
    selected_range = None
    dlg = None

    try:
        dlg = date_range_dialog.iqDateRangeDialog()
        dlg.init(title=title,
                 is_concrete_date=is_concrete_date,
                 default_start_date=default_start_date,
                 default_stop_date=default_stop_date)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            from_date_txt = dlg.getGtkObject('from_date_entry').get_text()
            selected_from_date = datetime.datetime.strptime(from_date_txt, date_range_dialog.DEFAULT_ENTRY_DATE_FMT)
            to_date_txt = dlg.getGtkObject('to_date_entry').get_text()
            selected_to_date = datetime.datetime.strptime(to_date_txt, date_range_dialog.DEFAULT_ENTRY_DATE_FMT)
            selected_range = (selected_from_date, selected_to_date)
    except:
        log_func.fatal(u'Error date range dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return selected_range


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
    result = dict()

    for dlg in dlgs:
        dlg_func = dlg.get('function', None)
        args = dlg.get('args', tuple())
        kwargs = dlg.get('kwargs', dict())
        if dlg_func:
            result_key = dlg['key'] if 'key' in dlg else dlg_func.__name__
            result[result_key] = dlg_func(parent=None, *args, **kwargs)

    return result


def getRadioChoiceDlg(parent=None, title=None, label=None, choices=()):
    """
    Select radio item.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 5 items.
    :return: Selected item index or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = radio_choice_dialog.iqRadioChoiceDialog()
        dlg.init(title=title, label=label, choices=choices)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getValue()
    except:
        log_func.fatal(u'Error radio choice dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return value


def getIntRangeDlg(parent=None, title=None, label_begin=None, label_end=None, min_value=0, max_value=100):
    """
    Entry integer range in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label_begin: First prompt text.
    :param label_end: Second prompt text.
    :param min_value: Minimal value.
    :param max_value: Maximal value.
    :return: Entered value or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = int_range_dialog.iqIntRangeDialog()
        dlg.init(title=title, label_begin=label_begin, label_end=label_end,
                 min_value=min_value, max_value=max_value)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getValue()
    except:
        log_func.fatal(u'Error integer range dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()
    return value


def getCheckBoxDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select CheckBox items in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 7 items.
    :param defaults: Default selection list.
    :return: Selected values or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = checkbox_dialog.iqCheckboxDialog()
        dlg.init(title=title, label=label, choices=choices, defaults=defaults)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getValue()
    except:
        log_func.fatal(u'Error check box dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return value


def getRadioChoiceMaxiDlg(parent=None, title=None, label=None,
                          choices=(), default=None):
    """
    Select wxRadioBox item in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 15 items.
    :param default: Default selection list.
    :return: Selected item index or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = radio_choice_maxi_dialog.iqRadioChoiceMaxiDialog()
        dlg.init(title=title, label=label, choices=choices, default=default)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getValue()
    except:
        log_func.fatal(u'Error radio choice maxi dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return value


def getCheckBoxMaxiDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Select CheckBox maxi items in dialog.

    :param parent: Parent window.
    :param title: Dialog title.
    :param label: Prompt text.
    :param choices: Choice list.
        Maximum 15 items.
    :param defaults: Default selection list.
    :return: Selected items index or None if press <Cancel>.
    """
    value = None
    dlg = None

    try:
        dlg = checkbox_maxi_dialog.iqCheckboxMaxiDialog()
        dlg.init(title=title, label=label, choices=choices, defaults=defaults)
        response = dlg.getGtkTopObject().run()
        if response == gi.repository.Gtk.ResponseType.OK:
            value = dlg.getValue()
    except:
        log_func.fatal(u'Error check box maxi dialog')

    if dlg and dlg.getGtkTopObject() is not None:
        dlg.getGtkTopObject().destroy()

    return value
