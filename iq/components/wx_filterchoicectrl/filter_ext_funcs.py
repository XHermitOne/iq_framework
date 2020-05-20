#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional filter functions.
"""

import datetime

from ...dialog import std_dlg_func
from ...util import dt_func

__version__ = (0, 0, 0, 1)

DEFAULT_DATE_FMT = '%Y.%m.%d'

DEFAULT_BEGIN_DATE_FMT = '%Y.%m.%d 00:00:00'
DEFAULT_END_DATE_FMT = '%Y.%m.%d 23:59:59'


def getArgsSysDate():
    """
    Get arguments system date.

    :return: Arguments dictionary.
    """
    now_date = datetime.datetime.now()
    str_now_date = now_date.strftime(DEFAULT_BEGIN_DATE_FMT)
    return dict(arg_1=str_now_date)


def getArgsSysMonth():
    """
    Get arguments system month.

    :return: Arguments dictionary.
    """
    now = datetime.datetime.now()
    first_day_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = first_day_month + datetime.timedelta(35)
    first_day_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    last_day_month = first_day_next_month - datetime.timedelta(1)
    str_first_day_month = first_day_month.strftime(DEFAULT_DATE_FMT)
    str_last_day_month = last_day_month.strftime(DEFAULT_DATE_FMT)
    return dict(arg_1=str_first_day_month, arg_2=str_last_day_month)


def getArgsSysYear():
    """
    Get arguments system year.

    :return: Arguments dictionary.
    """
    now = datetime.datetime.now()
    first_day_year = datetime.datetime(now.year, 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    str_first_day_year = first_day_year.strftime(DEFAULT_DATE_FMT)
    str_last_day_year = last_day_year.strftime(DEFAULT_DATE_FMT)
    return dict(arg_1=str_first_day_year, arg_2=str_last_day_year)


def getArgsChoiceDate():
    """
    Get arguments selected date.

    :return: Arguments dictionary.
    """
    choice_date = std_dlg_func.getDateDlg()
    if choice_date:
        str_date = choice_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_date)
    return dict()


def getArgsChoiceMonth():
    """
    Get arguments selected month.

    :return: Arguments dictionary.
    """
    choice_month = std_dlg_func.getMonthDlg()
    if choice_month:
        str_first_date = choice_month.strftime(DEFAULT_DATE_FMT)
        next_month = choice_month+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return dict()


def getArgsChoiceYear():
    """
    Get arguments selected year.

    :return: Arguments dictionary.
    """
    choice_year = std_dlg_func.getYearDlg()
    if choice_year:
        str_first_date = choice_year.strftime(DEFAULT_DATE_FMT)
        next_year = choice_year+datetime.timedelta(370)
        last_date = datetime.datetime(year=next_year.year, month=1, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return dict()


def getArgsChoiceDateRange():
    """
    Get arguments selected date range.

    :return: Arguments dictionary.
    """
    choice_range = std_dlg_func.getDateRangeDlg()
    if choice_range:
        str_first_date = choice_range[0].strftime(DEFAULT_DATE_FMT)
        str_last_date = choice_range[1].strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return dict()


def getArgsChoiceMonthRange():
    """
    Get arguments selected month range.

    :return: Arguments dictionary.
    """
    choice_range = std_dlg_func.getMonthRangeDlg()
    if choice_range:
        str_first_date = choice_range[0].strftime(DEFAULT_DATE_FMT)
        next_month = choice_range[1]+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return dict()


def getArgsSysDateDatetime():
    """
    Get arguments system date as datetime.

    :return: Arguments dictionary.
    """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return dict(arg_1=today, arg_2=tomorrow)


def getArgsYesterdayDatetime():
    """
    Get arguments yesterday as datetime.

    :return: Arguments dictionary.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return dict(arg_1=yesterday, arg_2=today)


def getArgsTwoDaysAgoDatetime():
    """
    Get arguments two days ago as datetime.

    :return: Arguments dictionary.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    two_days_ago = today - datetime.timedelta(days=2)
    return dict(arg_1=two_days_ago, arg_2=yesterday)


def getArgsSysMonthDatetime():
    """
    Get arguments system month as datetime.

    :return: Arguments dictionary.
    """
    now = datetime.datetime.now()
    first_day_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = first_day_month + datetime.timedelta(35)
    first_day_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    last_day_month = first_day_next_month - datetime.timedelta(1)
    return dict(arg_1=first_day_month, arg_2=last_day_month)


def getArgsSysYearDatetime():
    """
    Get arguments system year as datetime.

    :return: Arguments dictionary.
    """
    now = datetime.datetime.now()
    first_day_year = datetime.datetime(now.year, 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    return dict(arg_1=first_day_year, arg_2=last_day_year)


def getArgsOperYearDatetime():
    """
    Get arguments operate year as datetime.

    :return: Arguments dictionary.
    """
    first_day_year = datetime.datetime(dt_func.getOperateYear(), 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    return dict(arg_1=first_day_year, arg_2=last_day_year)


def getArgsChoiceDateDatetime():
    """
    Get arguments selected date as datetime.

    :return: Arguments dictionary.
    """
    choice_date = std_dlg_func.getDateDlg()
    if choice_date:
        next_date = choice_date + datetime.timedelta(days=1)
        return dict(arg_1=choice_date, arg_2=next_date)
    return dict()


def getArgsChoiceMonthDatetime():
    """
    Get arguments selected month as datetime.

    :return: Arguments dictionary.
    """
    choice_month = std_dlg_func.getMonthDlg()
    if choice_month:
        next_month = choice_month+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        return dict(arg_1=choice_month, arg_2=last_date)
    return dict()


def getArgsChoiceYearDatetime():
    """
    Get arguments selected year as datetime.

    :return: Arguments dictionary.
    """
    choice_year = std_dlg_func.getYearDlg()
    if choice_year:
        next_year = choice_year+datetime.timedelta(370)
        last_date = datetime.datetime(year=next_year.year, month=1, day=1)
        return dict(arg_1=choice_year, arg_2=last_date)
    return dict()


def getArgsChoiceDateRangeDatetime():
    """
    Get arguments selected date range as datetime.

    :return: Arguments dictionary.
    """
    choice_range = std_dlg_func.getDateRangeDlg()
    if choice_range:
        return dict(arg_1=choice_range[0], arg_2=choice_range[1])
    return dict()


def getArgsChoiceMonthRangeDatetime():
    """
    Get arguments selected month range as datetime.

    :return: Arguments dictionary.
    """
    choice_range = std_dlg_func.getMonthRangeDlg()
    if choice_range:
        next_month = choice_range[1]+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        return dict(arg_1=choice_range[0], arg_2=last_date)
    return dict()
