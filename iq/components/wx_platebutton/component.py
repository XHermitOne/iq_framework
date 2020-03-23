#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton component.
"""

import wx
import wx.lib.platebtn

from ... import object

from . import spc

from ...util import log_func
from ...util import exec_func

from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqWxPlateButton(wx.lib.platebtn.PlateButton, object.iqObject):
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
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

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

        self.Bind(wx.EVT_BUTTON, self.onButtonClick)

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

    def onButtonClick(self, event):
        """
        Button click handler.
        """
        on_button_click = self.getAttribute('on_button_click')
        if on_button_click:
            context = self.getContext()
            if context:
                context.set(event=event)
            exec_func.execTxtFunction(on_button_click, context=context)
        else:
            log_func.warning(u'Not define button click handler function for <%s : %s>' % (self.getName(),
                                                                                          self.getType()))
        event.Skip()


COMPONENT = iqWxPlateButton
