#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Date-time functions module.
"""

import calendar
import datetime
import locale

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
