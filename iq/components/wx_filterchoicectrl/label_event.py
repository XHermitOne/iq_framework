#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controls used in filter constructor.
"""

import wx

__version__ = (0, 0, 0, 1)

# Event on changing the label of the visual component
EVT_LABEL_CHANGE_TYPE = wx.NewEventType()
EVT_LABEL_CHANGE = wx.PyEventBinder(EVT_LABEL_CHANGE_TYPE)


class iqLabelChangeEvent(wx.PyEvent):
    """
    Event on changing the label of the visual component
    """
    def __init__(self, event_type, id):
        wx.PyEvent.__init__(self, id, event_type)

        self.id = id
        self.data = None

        # Event trigger object
        self._object = None

    def setData(self, val):
        self.data = val

    def getData(self):
        return self.data

    def setObject(self, obj):
        self._object = obj

    def getObject(self):
        return self._object
