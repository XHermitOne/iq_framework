#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton component.
"""

import wx
import wx.lib.platebtn

from ... import object

from . import spc

from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqWxPlateButton(object.iqObject, wx.lib.platebtn.PlateButton):
    """
    Wx PlateButton component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)

        wx.lib.platebtn.PlateButton.__init__(self, parent, wx.NewId(),
                                             label=self.getLabel(),
                                             bmp=self.getImage(),
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

    def getLabel(self):
        """
        Button label.
        """
        return self.getAttribute('label')

    def getImageName(self):
        """
        Button image filename.
        """
        return self.getAttribute('image')

    def getImage(self):
        """
        Get Bitmap object of button image.
        """
        img_name = self.getImageName()
        return wxbitmap_func.createIconBitmap(img_name)

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


COMPONENT = iqWxPlateButton
