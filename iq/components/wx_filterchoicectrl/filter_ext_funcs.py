#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дополнительные функции обработки фильтра.
"""

import datetime

from ic.dlg import std_dlg

__version__ = (0, 1, 1, 2)

DEFAULT_DATE_FMT = '%Y.%m.%d'

DEFAULT_BEGIN_DATE_FMT = '%Y.%m.%d 00:00:00'
DEFAULT_END_DATE_FMT = '%Y.%m.%d 23:59:59'


def get_args_sys_date():
    """
    Получение аргументов текущей даты.
    :return: Словарь заполненных аргументов.
    """
    now_date = datetime.datetime.now()
    # next_date = now_date + datetime.timedelta(days=1)
    str_now_date = now_date.strftime(DEFAULT_BEGIN_DATE_FMT)
    # str_next_date = next_date.strftime(DEFAULT_BEGIN_DATE_FMT)
    return dict(arg_1=str_now_date)


def get_args_sys_month():
    """
    Получение аргументов текущего месяца.
    :return: Словарь заполненных аргументов.
    """
    now = datetime.datetime.now()
    first_day_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = first_day_month + datetime.timedelta(35)
    first_day_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    last_day_month = first_day_next_month - datetime.timedelta(1)
    str_first_day_month = first_day_month.strftime(DEFAULT_DATE_FMT)
    str_last_day_month = last_day_month.strftime(DEFAULT_DATE_FMT)
    return dict(arg_1=str_first_day_month, arg_2=str_last_day_month)


def get_args_sys_year():
    """
    Получение аргументов текущего года.
    :return: Словарь заполненных аргументов.
    """
    now = datetime.datetime.now()
    first_day_year = datetime.datetime(now.year, 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    str_first_day_year = first_day_year.strftime(DEFAULT_DATE_FMT)
    str_last_day_year = last_day_year.strftime(DEFAULT_DATE_FMT)
    return dict(arg_1=str_first_day_year, arg_2=str_last_day_year)


def get_args_choice_date():
    """
    Получение аргументов даты с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_date = std_dlg.getDateDlg()
    if choice_date:
        str_date = choice_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_date)
    return {}


def get_args_choice_month():
    """
    Получение аргументов месяца с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_month = std_dlg.getMonthDlg()
    if choice_month:
        str_first_date = choice_month.strftime(DEFAULT_DATE_FMT)
        next_month = choice_month+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return {}


def get_args_choice_year():
    """
    Получение аргументов года с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_year = std_dlg.getYearDlg()
    if choice_year:
        str_first_date = choice_year.strftime(DEFAULT_DATE_FMT)
        next_year = choice_year+datetime.timedelta(370)
        last_date = datetime.datetime(year=next_year.year, month=1, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return {}


def get_args_choice_date_range():
    """
    Получение аргументов c выбором диапазона дат.
    :return: Словарь заполненных аргументов.
    """
    choice_range = std_dlg.getDateRangeDlg()
    if choice_range:
        str_first_date = choice_range[0].strftime(DEFAULT_DATE_FMT)
        str_last_date = choice_range[1].strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return {}


def get_args_choice_month_range():
    """
    Получение аргументов c выбором диапазона месяцев.
    :return: Словарь заполненных аргументов.
    """
    choice_range = std_dlg.getMonthRangeDlg()
    if choice_range:
        str_first_date = choice_range[0].strftime(DEFAULT_DATE_FMT)
        next_month = choice_range[1]+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        str_last_date = last_date.strftime(DEFAULT_DATE_FMT)
        return dict(arg_1=str_first_date, arg_2=str_last_date)
    return {}


def get_args_sys_date_datetime():
    """
    Получение аргументов текущей даты.
    :return: Словарь заполненных аргументов.
    """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return dict(arg_1=today, arg_2=tomorrow)


def get_args_yesterday_datetime():
    """
    Получение аргументов вчерашней даты.
    :return: Словарь заполненных аргументов.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return dict(arg_1=yesterday, arg_2=today)


def get_args_two_days_ago_datetime():
    """
    Получение аргументов позавчерашней даты.
    :return: Словарь заполненных аргументов.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    two_days_ago = today - datetime.timedelta(days=2)
    return dict(arg_1=two_days_ago, arg_2=yesterday)


def get_args_sys_month_datetime():
    """
    Получение аргументов текущего месяца.
    :return: Словарь заполненных аргументов.
    """
    now = datetime.datetime.now()
    first_day_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = first_day_month + datetime.timedelta(35)
    first_day_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    last_day_month = first_day_next_month - datetime.timedelta(1)
    return dict(arg_1=first_day_month, arg_2=last_day_month)


def get_args_sys_year_datetime():
    """
    Получение аргументов текущего системного года.
    :return: Словарь заполненных аргументов.
    """
    now = datetime.datetime.now()
    first_day_year = datetime.datetime(now.year, 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    return dict(arg_1=first_day_year, arg_2=last_day_year)


def get_args_oper_year_datetime():
    """
    Получение аргументов текущего операционного года.
    :return: Словарь заполненных аргументов.
    """
    from ic.engine import glob_functions
    first_day_year = datetime.datetime(glob_functions.getOperateYear(), 1, 1)
    date_on_next_year = first_day_year + datetime.timedelta(370)
    first_day_next_year = datetime.datetime(date_on_next_year.year, 1, 1)
    last_day_year = first_day_next_year - datetime.timedelta(1)
    return dict(arg_1=first_day_year, arg_2=last_day_year)


def get_args_choice_date_datetime():
    """
    Получение аргументов даты с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_date = std_dlg.getDateDlg()
    if choice_date:
        next_date = choice_date + datetime.timedelta(days=1)
        return dict(arg_1=choice_date, arg_2=next_date)
    return {}


def get_args_choice_month_datetime():
    """
    Получение аргументов месяца с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_month = std_dlg.getMonthDlg()
    if choice_month:
        next_month = choice_month+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        return dict(arg_1=choice_month, arg_2=last_date)
    return {}


def get_args_choice_year_datetime():
    """
    Получение аргументов года с выбором.
    :return: Словарь заполненных аргументов.
    """
    choice_year = std_dlg.getYearDlg()
    if choice_year:
        next_year = choice_year+datetime.timedelta(370)
        last_date = datetime.datetime(year=next_year.year, month=1, day=1)
        return dict(arg_1=choice_year, arg_2=last_date)
    return {}


def get_args_choice_date_range_datetime():
    """
    Получение аргументов c выбором диапазона дат.
    :return: Словарь заполненных аргументов.
    """
    choice_range = std_dlg.getDateRangeDlg()
    if choice_range:
        return dict(arg_1=choice_range[0], arg_2=choice_range[1])
    return {}


def get_args_choice_month_range_datetime():
    """
    Получение аргументов c выбором диапазона месяцев.
    :return: Словарь заполненных аргументов.
    """
    choice_range = std_dlg.getMonthRangeDlg()
    if choice_range:
        next_month = choice_range[1]+datetime.timedelta(35)
        last_date = datetime.datetime(year=next_month.year, month=next_month.month, day=1)
        return dict(arg_1=choice_range[0], arg_2=last_date)
    return {}
