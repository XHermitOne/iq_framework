#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjTreeComboCtrl component.
"""

import wx

from ... import object

from . import spc

from ...util import log_func

from . import refobjtreecomboctrl

__version__ = (0, 0, 0, 1)


class iqWxRefObjTreeComboCtrl(refobjtreecomboctrl.iqRefObjTreeComboCtrlProto,
                              object.iqObject):
    """
    Wx RefObjTreeComboCtrl component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        refobjtreecomboctrl.iqRefObjTreeComboCtrlProto.__init__(self, parent=parent,
                                                                id=wx.NewId(),
                                                                pos=self.getPosition(),
                                                                size=self.getSize(),
                                                                style=self.getStyle())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

    def getPosition(self):
        """
        Control position.
        """
        return self.getAttribute('position')

    def getSize(self):
        """
        Control size.
        """
        return self.getAttribute('size')

    def getStyle(self):
        """
        Control style.
        """
        return self.getAttribute('style')

    def getForegroundColour(self):
        """
        Get foreground colour.
        """
        return self.getAttribute('foreground_colour')

    def getBackgroundColour(self):
        """
        Get background colour.
        """
        return self.getAttribute('background_colour')


COMPONENT = iqWxRefObjTreeComboCtrl
