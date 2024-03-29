#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Date-time functions module.
"""

import time
import calendar
import datetime
import locale
import string

from . import log_func

from .. import global_data


__version__ = (0, 1, 9, 1)

RU_MONTHS = (u'Январь', u'Февраль',
             u'Март', u'Апрель', u'Май',
             u'Июнь', u'Июль', u'Август',
             u'Сентябрь', u'Октябрь', u'Ноябрь',
             u'Декабрь')

RU_QUARTERS = (u'Первый квартал (январь-март)',
               u'Второй квартал (апрель-июнь)',
               u'Третий квартал (июль-сентябрь)',
               u'Четвертый квартал (октябрь-декабрь)')

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
    if isinstance(cur_locale, str) and cur_locale != 'ru_RU':
        return tuple(calendar.month_name[1:])
    elif isinstance(cur_locale, tuple) and cur_locale[0] != 'ru_RU':
        return tuple(calendar.month_name[1:])
    return RU_MONTHS


def getMonthName(month):
    """
    Get month name by month number.

    :param month: Month number.
    :return: Month name.
    """
    if month < 1:
        month = 1
    elif month > 12:
        month = 12
    month_names = getMonths()
    return month_names[month - 1]


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


def time2datetime(unix_time):
    """
    Convert UNIX time to datetime.datetime.

    :param unix_time: UNIX time as float. For example: 1680146855.7007616
    :return: Time as datetime.datetime.
    """
    return datetime.datetime.fromtimestamp(unix_time)


def datetime2time(dt):
    """
    Convert datetime.datetime to UNIX time.

    :param dt: Time as datetime.datetime.
    :return: UNIX time as float.
    """
    unix_time = time.mktime(dt.timetuple())
    return unix_time


def getNowYear():
    """
    Get current system year.
    """
    return datetime.datetime.now().year


def getNowMonth():
    """
    Get current system month.
    """
    return datetime.datetime.now().month


def getNowDay():
    """
    Get current system day.
    """
    return datetime.datetime.now().day


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


def getStartQuarterDT(quarter=None, year=None):
    """
    Get start quarter datetime.

    :param quarter: Quarter number (1..4).
    :param year: Year.
    :return: Start quarter as datetime.
    """
    if quarter is None:
        quarter = int(datetime.date.today().month / 3) + 1
    if year is None:
        year = datetime.date.today().year

    if quarter == 1:
        return datetime.datetime(year=year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif quarter == 2:
        return datetime.datetime(year=year, month=4, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif quarter == 3:
        return datetime.datetime(year=year, month=7, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif quarter == 4:
        return datetime.datetime(year=year, month=10, day=1, hour=0, minute=0, second=0, microsecond=0)
    return None


def getStopQuarterDT(quarter=None, year=None):
    """
    Get stop quarter datetime.

    :param quarter: Quarter number (1..4).
    :param year: Year.
    :return: Stop quarter as datetime.
    """
    if quarter is None:
        quarter = int(datetime.date.today().month / 3) + 1
    if year is None:
        year = datetime.date.today().year

    if quarter == 1:
        return datetime.datetime(year=year, month=3, day=31, hour=23, minute=59, second=59, microsecond=999999)
    elif quarter == 2:
        return datetime.datetime(year=year, month=6, day=30, hour=23, minute=59, second=59, microsecond=999999)
    elif quarter == 3:
        return datetime.datetime(year=year, month=9, day=30, hour=23, minute=59, second=59, microsecond=999999)
    elif quarter == 4:
        return datetime.datetime(year=year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    return None


def getStartMonthDT(now=None):
    """
    Get start month datetime.

    :param now: Now datetime.
    :return: Start month as datetime.
    """
    if now is None:
        now = datetime.datetime.now()
    elif isinstance(now, datetime.date):
        now = date2datetime(now)
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def getStopMonthDT(now=None):
    """
    Get stop month datetime.

    :param now: Now datetime.
    :return: Stop month as datetime.
    """
    if now is None:
        now = datetime.datetime.now()
    elif isinstance(now, datetime.date):
        now = date2datetime(now)
    day_month_range = calendar.monthrange(year=now.year, month=now.month)
    return now.replace(day=day_month_range[1], hour=23, minute=59, second=59, microsecond=999999)


def getStartDayDT(dt=None):
    """
    Get start day as datetime.

    :param dt: Day. If None then get today.
    :return: Day 00:00:00 as Datetime.
    """
    if dt is None:
        dt = datetime.date.today()
    elif isinstance(dt, datetime.date):
        dt = date2datetime(dt)

    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def getStopDayDT(dt=None):
    """
    Get stop day as datetime.

    :param dt: Day. If None then get today.
    :return: Day 23:59:59 as Datetime.
    """
    if dt is None:
        dt = datetime.date.today()
    elif isinstance(dt, datetime.date):
        dt = date2datetime(dt)

    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def getLastMonthDay(month=1, year=None):
    """
    Get last day of month.

    :param month: Month number (1-12).
    :param year: Year.
    :return: Last day number (1-31).
    """
    if year is None:
        year = getNowYear()
    if month == 0:
        n_month = 1
    return calendar.monthrange(year=year, month=month)[1]


def getPeriodDays(start_day=None, stop_day=None):
    """
    Get days of period.

    :param start_day: The start date of the period.
        If not defined, then the beginning of the current month is taken.
    :param stop_day: The end date of the period.
        If not defined, then the ending of the current month is taken.
    :return: Date list.
    """
    if start_day is None:
        start_day = getStartMonthDT()
    if stop_day is None:
        stop_day = getStopMonthDT()

    result = list()
    day = start_day
    while day <= stop_day:
        result.append(day)
        day += datetime.timedelta(days=1)
    return result


def getMonthDays(month=None, year=None):
    """
    Get days of month.

    :param month: Month number (1-12).
    :param year: Year.
    :return: Day list as [datetime.datetime, ...].
    """
    now = datetime.datetime.now()

    if year is None:
        year = now.year
    if month is None:
        month = now.month

    first_day = now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    start_day = getStartMonthDT(first_day)
    stop_day = getStopMonthDT(first_day)
    return getPeriodDays(start_day=start_day, stop_day=stop_day)


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


def getTomorrow():
    """
    Tomorrow as date.
    """
    return datetime.date.today() + datetime.timedelta(days=1)


def getTomorrowDT():
    """
    Tomorrow as datetime.
    """
    return date2datetime(getTomorrow())


def getTomorrowFmt(fmt=DEFAULT_DATE_FMT):
    """
    Tomorrow as string.

    :param fmt: Tomorrow string format.
    :return: Tomorrow as string.
    """
    return getTomorrowDT().strftime(fmt)


def getDaysAgo(days=1):
    """
    Get several days ago.
    """
    return datetime.date.today() - datetime.timedelta(days=days)


def getDaysAgoDT(days=1):
    """
    Get several days ago as datetime.
    """
    return date2datetime(getDaysAgo(days=days))


def getDayBeforeYesterday():
    """
    Get day before yesterday as date.
    """
    return getDaysAgo(days=2)


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


def getNextMonth(month_day=None):
    """
    Get first day next month as date.

    :param month_day: Current day of month.
         If None then get today.
    :return: First day of next month.
    """
    return datetime2date(getNextMonthDT(month_day))


def getNextMonthDT(month_day=None):
    """
    Get first day next month as datetime.

    :param month_day: Current day of month.
         If None then get today.
    :return: First day of next month.
    """
    if month_day is None:
        month_day = getToday()
    stop_month_day = getStopMonthDT(month_day)
    return stop_month_day + datetime.timedelta(days=1)


def getPrevMonth(month_day=None):
    """
    Get first day of prev month as date.

    :param month_day: Current day of month.
         If None then get today.
    :return: First day of prev month.
    """
    return datetime2date(getPrevMonthDT(month_day))


def getPrevMonthDT(month_day=None):
    """
    Get first day of prev month as datetime.

    :param month_day: Current day of month.
         If None then get today.
    :return: First day of prev month.
    """
    if month_day is None:
        month_day = getToday()
    start_month_day = getStartMonthDT(month_day)
    stop_prev_month_day = start_month_day - datetime.timedelta(days=1)
    return getStartMonthDT(stop_prev_month_day)


def getYearAgoDT(day=None):
    """
    Get date year ago.

    :param day: Current day.
         If None then get today.
    :return: Day year ago.
    """
    if day is None:
        day = getToday()

    cur_year = day.year
    return day.replace(year=cur_year - 1)


def getMinDateTime():
    """
    Get minimum datetime.
    """
    return datetime.datetime.min


def getMinDate():
    """
    Get minimum date.
    """
    return datetime.date.min()


def getTimeDelta(*args, **kwargs):
    """
    Get timedelta.
    """
    return datetime.timedelta(*args, **kwargs)


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


def parseStrDatetime(dt_str, fmt=(DEFAULT_DATETIME_FMT, )):
    """
    Get datetime from string by several formats.

    :param dt_str: Datetime as string.
    :param fmt: Datetime string formats as tuple.
    :return: DateTime.
    """
    for cur_fmt in fmt:
        try:
            return datetime.datetime.strptime(dt_str, cur_fmt)
        except ValueError:
            pass
    log_func.warning(u'Not parse string <%s> as datetime by formats %s' % (dt_str, fmt))
    return getMinDateTime()


def parseStrDate(dt_str, fmt=(DEFAULT_DATE_FMT, )):
    """
    Get date from string by several format.

    :param dt_str: Date as string.
    :param fmt: Date string formats as tuple.
    :return: Date.
    """
    dt = parseStrDatetime(dt_str=dt_str, fmt=fmt)
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


def hours2timedelta(hours):
    """
    Convert hours to timedelta format.

    :param hours: Hours. For example 4.5.
    :return: TimeDelta. For example 04:30:00.
    """
    minutes_seconds = hours % 1
    hours = int(hours)
    days = 0
    if hours > 24:
        days = int(int(hours) / 24.0)
        hours = hours % 24

    minutes = minutes_seconds * 60.0
    seconds = (minutes % 1) * 60.0
    minutes = int(minutes)
    seconds = int(seconds)

    return datetime.timedelta(days=days,
                              hours=hours,
                              minutes=minutes,
                              seconds=seconds)


class TimeDeltaTemplate(string.Template):
    """
    Time delta template class.
    """
    delimiter = '%'


DEFAULT_TIMEDELTA_FMT = '%D days %H:%M:%S'
DEFAULT_TIME_TIMEDELTA_FMT = '%H:%M:%S'
DEFAULT_TIMEDELTA_FMT_RU = u'%D дней %H:%M:%S'
DEFAULT_WITHOUT_DAYS_TIMEDELTA_FMT = '%L:%M:%S'


def strfdelta(timedelta, fmt=None):
    """
    Timedelta to string.

    :param timedelta: Timedelta.
    :param fmt: Format string.
        Format:
        D - days;
        L - total hours;
        H - hours;
        M - minutes;
        S - seconds.
    :return: Timedelta string.
    """
    assert isinstance(timedelta, datetime.timedelta), u'Type error timedelta'

    if fmt is None:
        fmt = DEFAULT_TIME_TIMEDELTA_FMT
        if timedelta.days:
            import locale
            from . import lang_func
            language = locale.getlocale()[0]
            if language == lang_func.RUSSIAN_LOCALE:
                fmt = DEFAULT_TIMEDELTA_FMT_RU
            else:
                fmt = DEFAULT_TIMEDELTA_FMT

    fmt_dict = {'D': timedelta.days}
    hours, rem = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    sum_hours = timedelta.days * 24 + hours
    fmt_dict['H'] = '{:02d}'.format(hours)
    fmt_dict['M'] = '{:02d}'.format(minutes)
    fmt_dict['S'] = '{:02d}'.format(seconds)
    fmt_dict['L'] = '{:d}'.format(sum_hours)
    t = TimeDeltaTemplate(fmt)
    return t.substitute(**fmt_dict)


def strDateTime2Tuple(dt_str='01.01.0001', fmt=DEFAULT_DATETIME_FMT):
    """
    Convert datetime as string to tuple.

    :param dt_str: Datetime as string.
    :param fmt: Datetime string format.
    :return: Datetime as tuple.
    """
    try:
        return time.strptime(dt_str, fmt)
    except:
        log_func.fatal(u'Error convert string datetime to tuple')
    return None


def strDateTime2Date(date_str, fmt=DEFAULT_DATETIME_FMT):
    """
    Convert the string representation of a date in the specified format to date format.

    :return: Date or None if error.
    """
    try:
        date_time_tuple = strDateTime2Tuple(date_str, fmt)
        year = date_time_tuple[0]
        month = date_time_tuple[1]
        day = date_time_tuple[2]
        return datetime.date(year, month, day)
    except:
        log_func.fatal(u'Error convert string datetime to date')
    return None


def strDateTime2DateTime(dt_str, fmt=DEFAULT_DATETIME_FMT):
    """
    Convert the string representation of a date in the specified format to date format.

    :return: DateTime or None if error.
    """
    try:
        date_time_tuple = strDateTime2Tuple(dt_str, fmt)
        year = date_time_tuple[0]
        month = date_time_tuple[1]
        day = date_time_tuple[2]
        hour = date_time_tuple[3]
        minute = date_time_tuple[4]
        second = date_time_tuple[5]
        return datetime.datetime(year, month, day, hour, minute, second)
    except:
        log_func.fatal(u'Error convert string datetime to datetime')
    return None


def sleep(seconds=1):
    """
    Sleep.
    """
    return time.sleep(seconds)


def calcAge(dt_birth, now=None):
    """
    Calculate age.

    :param dt_birth: Birth datetime or date.
    :param now: Now datetime. If not defined then get system datetime.
    :return: Age timedelta.
    """
    if isinstance(dt_birth, datetime.date):
        dt_birth = date2datetime(dt_birth)
    if now is None:
        now = datetime.datetime.now()

    return now - dt_birth


def calcYearAge(dt_birth, today=None):
    """
    Calculate age in years.

    :param dt_birth: Birth datetime or date.
    :param today: Today. If not defined then get system date.
    :return: Age years.
    """
    if isinstance(dt_birth, datetime.date):
        dt_birth = date2datetime(dt_birth)
    if today is None:
        today = datetime.date.today()

    years = today.year - dt_birth.year

    def get_leap_birthday(year):
        country = locale.getlocale()[0].split('_')[1]
        if country in ('US', 'RU'):
            return datetime.date(year, 2, 28)
        elif country in ('GB', 'HK'):
            return datetime.date(year, 3, 1)
        else:
            raise Exception('It is unknown whether your country treats leap year '
                            + 'birthdays as being on the 28th of February or '
                            + 'the 1st of March. Please consult your country\'s '
                            + 'legal code for in order to ascertain an answer.')
    try:
        birthday = datetime.date(today.year, dt_birth.month, dt_birth.day)
    except ValueError as e:
        if dt_birth.month == 2 and dt_birth.day == 29:
            birthday = get_leap_birthday(today.year)
        else:
            raise e

    if today < birthday:
        years -= 1
    return years


def calcBirthDate(age_year, today=None):
    """
    Calculate birth date by age.

    :param age_year: Age year.
    :param today: Today. If not defined then get system date.
    :return: Birth date.
    """
    if today is None:
        today = datetime.date.today()

    birth_date = today.replace(year=today.year - age_year)
    return birth_date


def calcDateAndTime(dt_date, dt_time):
    """
    Calculate datetime as date and time.

    :param dt_date: Date as datetime.
    :param dt_time: Time as datetime.
    :return: Datetime.
    """
    if isinstance(dt_date, datetime.date):
        dt_date = date2datetime(dt_date)
    assert isinstance(dt_date, datetime.datetime), u'Type error datetime'
    assert isinstance(dt_time, datetime.datetime), u'Type error datetime'

    result = dt_date.replace(hour=dt_time.hour, minute=dt_time.minute,
                             second=dt_time.second, microsecond=dt_time.microsecond)
    return result