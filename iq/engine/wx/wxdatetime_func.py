#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wxDateTime convert functions.
"""

import datetime
import wx

__version__ = (0, 0, 0, 1)


def date2wxdatetime(date):
    """
    Convert <datetime.date> to <wx.DateTime>.

    :param date: Date as <datetime>.
    :return: Date as <wx.DateTime> or None if error.
    """
    if date is None:
        return None

    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTime.FromDMY(*dmy)


def wxdatetime2date(date):
    """
    Convert <wx.DateTime> to <datetime.date>.

    :param date: Date as <wx.DateTime>.
    :return: Date as <datetime> or None is error.
    """
    if date is None:
        return None

    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = list(map(int, date.FormatISODate().split('-')))
        return datetime.date(*ymd)
    return None


def datetime2wxdatetime(dt):
    """
    Convert <datetime.datetime> to <wx.DateTime>.

    :param dt: Time as <datetime.datetime>.
    :return: Time as <wx.DateTime> or None if error.
    """
    if dt is None:
        return None

    assert isinstance(dt, (datetime.datetime, datetime.date))
    tt = dt.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    hms = (tt[2], tt[1]-1, tt[0])
    result = wx.DateTime.FromDMY(*dmy)
    result.SetHour(hms[0])
    result.SetMinute(hms[1])
    result.SetSecond(hms[2])
    return result


def wxdatetime2datetime(dt):
    """
    Convert <wx.DateTime> to <datetime>.

    :param dt: Time as <wx.DateTime>.
    :return: Time as <datetime> or None if error.
    """
    if dt is None:
        return None

    assert isinstance(dt, wx.DateTime)
    if dt.IsValid():
        ymd = [int(t) for t in dt.FormatISODate().split('-')]
        hms = [int(t) for t in dt.FormatISOTime().split(':')]
        dt_args = ymd+hms
        return datetime.datetime(*dt_args)
    else:
        return None
