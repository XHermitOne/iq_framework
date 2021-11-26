#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Abstract timeline class. Historical trend.
The class organizes the interface that all trends must inherit.
"""

import datetime
import wx

from ...util import log_func
from ...util import dt_func

from ...engine.wx import wxdatetime_func

__version__ = (0, 0, 0, 1)

# Formats used to display the timeline
DEFAULT_TIME_FMT = '%H:%M:%S'
DEFAULT_DATE_FMT = '%d.%m.%Y'
DEFAULT_DATETIME_FMT = '%d.%m.%Y-%H:%M:%S'
DEFAULT_DT_FORMATS = (DEFAULT_TIME_FMT,
                      DEFAULT_DATETIME_FMT,
                      DEFAULT_DATE_FMT)

# Default scale format
DEFAULT_X_FORMAT = 'time'
DEFAULT_Y_FORMAT = 'numeric'

DEFAULT_X_FORMATS = ('time', 'date', 'datetime')
DEFAULT_Y_FORMATS = ('numeric', )


class iqTrendProto(object):
    """
    Abstract timeline class. Historical trend.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        today = datetime.date.today()

        self.start_datetime = datetime.datetime.combine(today,
                                                        datetime.datetime.min.time())
        self.stop_datetime = datetime.datetime.combine(today+datetime.timedelta(days=1),
                                                       datetime.datetime.min.time())

    def _convertDate(self, dt):
        """
        Correct date type conversion to datetime.datetime.

        :param dt: Date.
        :return: Date-time.
        """
        new_dt = None
        if isinstance(dt, datetime.date):
            # If the date is specified by datetime.date then translate to datetime.datetime
            new_dt = datetime.datetime.combine(dt,
                                               datetime.datetime.min.time())
        elif isinstance(dt, wx.DateTime):
            new_dt = wxdatetime_func.wxDateTime2datetime(dt)
        elif dt is None:
            new_dt = datetime.datetime.now()
        elif isinstance(dt, datetime.datetime):
            new_dt = dt
        else:
            assert isinstance(dt, (datetime.datetime, datetime.date))
        return new_dt

    def _dt2str(self, dt_value=None, time_format=DEFAULT_X_FORMAT):
        """
        Convert datetime to string according to format.

        :param dt_value: The value is datetime.datetime or datetime.timedelta.
        :param time_format: Presentation format.
        :return: A formatted string of datetime values.
        """
        if time_format == 'time':
            time_format = DEFAULT_TIME_FMT
        elif time_format == 'date':
            time_format = DEFAULT_DATE_FMT
        elif time_format == 'datetime':
            time_format = DEFAULT_DATETIME_FMT

        if isinstance(dt_value, datetime.datetime) or isinstance(dt_value, datetime.date):
            return dt_value.strftime(time_format)
        elif isinstance(dt_value, datetime.timedelta):
            return dt_func.strfdelta(dt_value, fmt=dt_func.DEFAULT_TIME_TIMEDELTA_FMT)
        else:
            log_func.warning(u'Unsupported time value type <%s>' % dt_value.__class__.__name__)
        return ''

    def _str2dt(self, time_value=None, time_format=DEFAULT_X_FORMAT, bToTimeDelta=False):
        """
        Converting a string representation of timeline values to a datetime view.

        :param time_value: String representation of date-time.
        :param time_format: Presentation format.
        :param bToTimeDelta: Convert to datetime.timedelta?
        :return: datetime.datetime/datetime.timedelta, corresponding to the string representation.
        """
        if time_format == 'time':
            time_format = DEFAULT_TIME_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        elif time_format == 'date':
            time_format = DEFAULT_DATE_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day)
        elif time_format == 'datetime':
            time_format = DEFAULT_DATETIME_FMT
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day,
                                          hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        else:
            dt = datetime.datetime.strptime(time_value, time_format)
            if bToTimeDelta:
                return datetime.timedelta(days=dt.day,
                                          hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        return dt

    def _get_dt_format(self, time_format=DEFAULT_X_FORMAT):
        """
        Make the format of temporary values uniform.

        :param time_format: Presentation format.
        :return: Format.
        """
        dt_format = time_format
        if time_format == 'time':
            dt_format = DEFAULT_TIME_FMT
        elif time_format == 'date':
            dt_format = DEFAULT_DATE_FMT
        elif time_format == 'datetime':
            dt_format = DEFAULT_DATETIME_FMT
        return dt_format

    def setStartDT(self, new_dt):
        """
        The start date-time of the trend.

        :param new_dt: New value.
        """
        self.start_datetime = self._convertDate(new_dt)

    def getStartDT(self):
        """
        The start date-time of the trend.
        """
        return self.start_datetime

    def setStopDT(self, new_dt):
        """
        The final date and time of the trend.

        :param new_dt: New value.
        """
        self.stop_datetime = self._convertDate(new_dt)

    def getStopDT(self):
        """
        The final date and time of the trend.
        """
        return self.stop_datetime

    def setDefaults(self):
        """
        Set default options.
        """
        pass

    def drawEmpty(self):
        """
        Drawing an empty trend.
        """
        log_func.warning(u'Undefined method for drawing an empty trend')

    def getPenData(self, pen_index=0):
        """
        Data relevant to pen.

        :param pen_index: Pen index. By default, the first pen is taken.
        :return: List (Time, Value)
        """
        pens = self.getPens()

        if pens and pen_index < len(pens):
            return pens[pen_index].getLineData()

        return list()

    def draw(self, redraw=True):
        """
        The main method of plotting a trend.

        :param redraw: Forced drawing.
        """
        log_func.warning(u'Undefined trend drawing method')

    def getPens(self):
        """
        List of trend feathers.
        """
        log_func.warning(u'Not defined feather production method')
        return list()

    def setHistory(self, history):
        """
        Change the data source for all trend feathers.

        :param history: The object of historical data is the data source.
        :return: True/False.
        """
        pens = self.getPens()

        result = True
        for pen in pens:
            result = result and pen.setHistory(history)
        return result

    def zoomX(self, step=1, redraw=True):
        """
        Increase the X axis graduation value according to the setting scale.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        log_func.warning(u'Trend scaling method not defined')
        return False

    def zoomY(self, step=1, redraw=True):
        """
        Increase the Y-axis division price according to the setting scale.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        log_func.warning(u'Trend scaling method not defined')
        return False

    def moveSceneX(self, step=1, redraw=True):
        """
        Moving the scene along the X axis by the specified amount of the division price.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        log_func.warning(u'Undefined trend movement method')
        return False

    def moveSceneY(self, step=1, redraw=True):
        """
        Moving the scene along the Y axis by the specified amount of the division price.

        :param step: Step on the scale
            >0 - increase
            <0 - decrease
        :param redraw: Redraw the trend frame?
        :return: True/False.
        """
        log_func.warning(u'Undefined trend movement method')
        return False
