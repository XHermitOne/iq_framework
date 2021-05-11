#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Date-time functions module.
"""

import calendar
import datetime
import locale

from . import log_func

from .. import global_data


__version__ = (0, 0, 1, 1)

RU_MONTHS = (u'Январь', u'Февраль',
             u'Март', u'Апрель', u'Май',
             u'Июнь', u'Июль', u'Август',
             u'Сентябрь', u'Октябрь', u'Ноябрь',
             u'Декабрь')

DEFAULT_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_FMT = '%Y-%m-%d'
DEFAULT_TIME_FMT = '%H:%M:%S'
DEFAULT_TIME_ZERO = '00:00:00'
DEFAULT_DATE_ZERO = '0000-00-00'

DT_FORMATS = (DEFAULT_DATETIME_FMT, DEFAULT_DATE_FMT, DEFAULT_TIME_FMT)


def getMonths():
    """
    Get month name list.

    :return:
    """
    cur_locale = locale.getlocale()
    if cur_locale != 'ru_RU':
        return tuple(calendar.month_name[1:])
    return RU_MONTHS


def date2datetime(d):
    """
    Convert datetime.date to datetime.datetime.

    :param d: Date as datetime.date
    :return: Date as datetime.datetime.
    """
    if isinstance(d, datetime.datetime):
        return d
    elif isinstance(d, datetime.date):
        return datetime.datetime.combine(d, datetime.datetime.min.time())
    log_func.warning(u'Unsupported type <%s> for convert datetime.date -> datetime.datetime' % type(d))
    return None


def datetime2date(dt):
    """
    Convert datetime.datetime to datetime.date.

    :param dt: Date as datetime.datetime.
    :return: Date as datetime.date.
    """
    if isinstance(dt, datetime.datetime):
        return dt.date()
    elif isinstance(dt, datetime.date):
        return dt
    log_func.warning(u'Unsupported type <%s> for convert datetime.datetime -> datetime.date' % type(dt))
    return None


def getNowYear():
    """
    Get current system year.
    """
    return datetime.datetime.now().year


def getStartYearDT(year=None):
    """
    Get start year datetime as 01.01.year 00:00:00.

    :param year: Year. If None ten get current system year.
    :return: 01.01.year 00:00:00 as datetime.
    """
    if year is None:
        year = getNowYear()
    return datetime.datetime(year=year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def getStopYearDT(year=None):
    """
    Get stop year datetime as 31.12.year 23:59:59.

    :param year: Year. If None ten get current system year.
    :return: 31.12.year 23:59:59 as datetime.
    """
    if year is None:
        year = getNowYear()
    return datetime.datetime(year=year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)


def getStartMonthDT(now=None):
    """
    Get start month datetime.

    :param now: Now datetime.
    :return: Start month as datetime.
    """
    if now is None:
        now = datetime.datetime.now()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def getStopMonthDT(now=None):
    """
    Get stop month datetime.

    :param now: Now datetime.
    :return: Stop month as datetime.
    """
    if now is None:
        now = datetime.datetime.now()
    day_month_range = calendar.monthrange(year=now.year, month=now.month)
    return now.replace(day=day_month_range[1], hour=23, minute=59, second=59, microsecond=999999)


def getOperateYear():
    """
    Get operate year.
    """
    return global_data.getGlobal('OPERATE_YEAR')


def getNow():
    """
    Now datetime.
    """
    return datetime.datetime.now()


def getToday():
    """
    Today as date.
    """
    return datetime.date.today()


def getTodayDT():
    """
    Today as datetime.
    """
    return date2datetime(datetime.date.today())


def getTodayFmt(fmt=DEFAULT_DATE_FMT):
    """
    Today as string.

    :param fmt: Today string format.
    :return: Today as string.
    """
    return getTodayDT().strftime(fmt)


def getYesterday():
    """
    Yesterday as date.
    """
    return datetime.date.today() - datetime.timedelta(days=1)


def getYesterdayDT():
    """
    Yesterday as datetime.
    """
    return date2datetime(getYesterday())


def getYesterdayFmt(fmt=DEFAULT_DATE_FMT):
    """
    Yesterday as string.

    :param fmt: Yesterday string format.
    :return: Yesterday as string.
    """
    return getYesterdayDT().strftime(fmt)


def getDayBeforeYesterday():
    """
    Get day before yesterday as date.
    """
    return datetime.date.today() - datetime.timedelta(days=2)


def getDayBeforeYesterdayDT():
    """
    Get day before yesterday as datetime.
    """
    return date2datetime(getDayBeforeYesterday())


def getNextDay(day=None):
    """
    Get next day as date.

    :param day: Current day.
         If None then get today.
    :return: Next day after current.
    """
    if day is None:
        day = getToday()

    return day + datetime.timedelta(days=1)


def getNextDayDT(day=None):
    """
    Get next day as datetime.

    :param day: Current day.
         If None then get today.
    :return: Next day after current.
    """
    return date2datetime(getNextDay(day))


def getPrevDay(day=None):
    """
    Get prev day as date.

    :param day: Current day.
         If None then get today.
    :return: Prev day before current.
    """
    if day is None:
        day = getToday()

    return day - datetime.timedelta(days=1)


def getPrevDayDT(day=None):
    """
    Get prev day as datetime.

    :param day: Current day.
         If None then get today.
    :return: Prev day before current.
    """
    return date2datetime(getPrevDay(day))


def str2datetime(dt_str, fmt=DEFAULT_DATETIME_FMT):
    """
    Get datetime from string by format.

    :param dt_str: Datetime as string.
    :param fmt: Datetime string format.
    :return: DateTime.
    """
    return datetime.datetime.strptime(dt_str, fmt)


def str2date(dt_str, fmt=DEFAULT_DATE_FMT):
    """
    Get date from string by format.

    :param dt_str: Date as string.
    :param fmt: Date string format.
    :return: Date.
    """
    dt = str2datetime(dt_str=dt_str, fmt=fmt)
    return datetime2date(dt)


def datetime2str(dt, fmt=DEFAULT_DATETIME_FMT):
    """
    Get datetime as string.

    :param dt: Datetime.
    :param fmt: Datetime string format.
    :return: Datetime as string.
    """
    return dt.strftime(fmt)


def date2str(dt, fmt=DEFAULT_DATE_FMT):
    """
    Get date as string.

    :param dt: Date.
    :param fmt: Date string format.
    :return: Date as string.
    """
    dt = date2datetime(dt)
    return dt.strftime(fmt)


def isStartDayTime(dt, cmp_microsecond=False):
    """
    Start time of the day?

    :param dt: datetime.datetime.
    :param cmp_microsecond: Compare microseconds?
    :return: True-yes. For example 2018-01-01 00:00:00 / False - no.
    """
    if not cmp_microsecond:
        return dt.hour == 0 and dt.minute == 0 and dt.second == 0
    return dt.hour == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0


def parseDTStr(dt_str, dt_formats=DT_FORMATS):
    """
    Parse datetime/date/time string.

    :param dt_str: Datetime string.
    :param dt_formats: Datetime/date/time formats.
    :return: Datetime or MIN datetime if error.
    """
    dt = None
    for dt_fmt in dt_formats:
        try:
            if dt_fmt == DEFAULT_DATETIME_FMT:
                dt = str2datetime(dt_str=dt_str, fmt=dt_fmt)
            elif dt_fmt == DEFAULT_DATE_FMT:
                dt = str2date(dt_str=dt_str, fmt=dt_fmt)
            else:
                dt = datetime.datetime.strptime(dt_str, dt_fmt)
        except:
            dt = None
        if dt is not None:
            break
    return dt
