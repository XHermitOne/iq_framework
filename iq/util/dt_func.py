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


__version__ = (0, 0, 0, 1)

RU_MONTHS = (u'Январь', u'Февраль',
             u'Март', u'Апрель', u'Май',
             u'Июнь', u'Июль', u'Август',
             u'Сентябрь', u'Октябрь', u'Ноябрь',
             u'Декабрь')


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


def getOperateYear():
    """
    Get operate year.
    """
    return global_data.getGlobal('OPERATE_YEAR')
