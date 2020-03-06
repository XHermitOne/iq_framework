#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx panel component.
"""

import wx

from ... import object

from . import spc

__version__ = (0, 0, 0, 1)


class iqWxPanel(object.iqObject, wx.Panel):
    """
    Wx panel component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)

        wx.Panel.__init__(self, parent=parent, id=wx.NewId(),
                          pos=self.getPosition(),
                          size=self.getSize(),
                          style=self.getStyle(),
                          name=self.getName())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        self.createChildren()

    def getPosition(self):
        """
        Panel position.
        """
        return self.getAttribute('position')

    def getSize(self):
        """
        Panel size.
        """
        return self.getAttribute('size')

    def getStyle(self):
        """
        Panel style.
        """
        return self.getAttribute('style')

    def getForegroundColour(self):
        """
        Panel foreground colour.
        """
        return self.getAttribute('foreground_colour')

    def getBackgroundColour(self):
        """
        Panel background colour.
        """
        return self.getAttribute('background_colour')


COMPONENT = iqWxPanel