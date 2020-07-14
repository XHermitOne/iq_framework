#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trend pen component.
"""

try:
    import wx
except ImportError:
    print(u'Import error wx')

from ... import object

from . import spc

from ...util import log_func

__version__ = (0, 0, 0, 1)

DEFAULT_RGB_STR_COLOUR = '#0000FF'


class iqTrendPen(object.iqObject):
    """
    Trend pen component.
    """
    # Register of registered historical data objects
    history_registry = dict()

    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        # Passport of the current historical data object
        self.current_history_psp = None

    def getLegend(self):
        """
        Legend label.
        """
        legend = self.getAttribute('legend')
        return u'' if legend is None else legend

    def getColour(self):
        """
        Pen colour.
        """
        colour = self.getAttribute('colour')
        return wx.Colour(*colour) if colour else wx.Colour(0, 0, 255)

    def getColourStr(self):
        """
        Цвет пера в строковом виде RGB. Например #FF0000.
        """
        wx_colour = self.getColour()
        if wx_colour:
            return wx_colour.GetAsString(wx.C2S_HTML_SYNTAX)
        return DEFAULT_RGB_STR_COLOUR

    def getHistoryPsp(self):
        """
        Passport of the object of historical data - data source.
        """
        if self.current_history_psp is None:
            return self.getAttribute('history')
        return self.current_history_psp

    def getHistory(self):
        """
        The object of historical data is the data source.

        :return: Object or None in case of error.
        """
        psp = self.getHistoryPsp()
        if psp and psp in self.history_registry:
            return self.history_registry[psp]
        history_obj = self.getKernel().getObject(psp)
        self.history_registry[psp] = history_obj
        return history_obj

    def setHistory(self, history):
        """
        Set the historical data object as the data source.

        :param history: The object of historical data is the data source.
        :return: True/False.
        """
        if history is None:
            log_func.error(u'Undefined historical data object')
            return False

        try:
            psp = history.GetPassport()
            if not isinstance(psp, tuple):
                psp = tuple(psp)
            self.current_history_psp = psp
            if psp not in self.history_registry:
                self.history_registry[psp] = history
            return True
        except:
            log_func.fatal(u'Error setting historical data object for trend pen')
        return False

    def getTagName(self):
        """
        Tag name.
        """
        return self.getAttribute('tag_name')

    def getLineData(self):
        """
        Get line data.

        :return: List of coordinates of points.
        """
        history_obj = self.getHistory()
        data = list
        if history_obj:
            tag_name = self.getTagName()
            trend = self.getParent()
            start_dt = trend.getStartDT()
            stop_dt = trend.getStopDT()
            data = history_obj.getValues(col_name=tag_name,
                                         start_dt=start_dt,
                                         stop_dt=stop_dt)
        return data


COMPONENT = iqTrendPen
