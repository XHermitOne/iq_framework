#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx panel component.
"""

import wx

from . import spc

from ...util import log_func
from ..wx_widget import component

__version__ = (0, 0, 0, 1)


class iqWxPanel(wx.Panel, component.iqWxWidget):
    """
    Wx panel component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        component.iqWxWidget.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

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

    def drawDCBitmap(self, dc=None, bmp=None, pos_x=0, pos_y=0):
        """
        Draw wx.Bitmap on panel device context.

        :param dc: Device context object.
            If None then get panel DC.
        :param bmp: wx.Bitmap object.
        :param pos_x: Left coordinate wx.Bitmap on DC.
            Default 0.
        :param pos_y: Top coorninate wx.Bitmap on DC.
            Default 0.
        :return: True/False.
        """
        if bmp:
            if not dc:
                dc = wx.ClientDC(self)

                rect = self.GetUpdateRegion().GetBox()
                dc.SetClippingRect(rect)

            dc.Clear()
            dc.DrawBitmap(bmp, pos_x, pos_y)
            return True
        else:
            log_func.error(u'Not define wx.Bitmap object for drawing on <%s> panel' % self.getName())
        return False

    def getControl(self, ctrl_name):
        """
        Get panel control by name.

        :param ctrl_name: Control name.
        :return: Control object or None if not found.
        """
        find_control = self.findChild(name=ctrl_name)
        return find_control if issubclass(find_control.__class__, wx.Window) else None


COMPONENT = iqWxPanel
