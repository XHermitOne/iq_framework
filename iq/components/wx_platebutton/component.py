#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton component.
"""

import wx
import wx.lib.platebtn

from ..wx_widget import component

from . import spc

from ...util import log_func
from ...util import exec_func

from ...engine.wx import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqWxPlateButton(wx.lib.platebtn.PlateButton,
                      component.iqWxWidget):
    """
    Wx PlateButton component.
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
            # log_func.debug(u'wx PlateButton set background colour %s' % str(background_colour))
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        self.Bind(wx.EVT_BUTTON, self.onButtonClick)

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
