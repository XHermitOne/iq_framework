#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Info popup window function.
"""

import wx

from ....util import log_func

__version__ = (0, 1, 1, 1)

DEFAULT_INFO_WINDOW_BACKGROUND_COLOUR_NAME = 'CADET BLUE'


class iqPopupInfoWindow(wx.PopupWindow):
    """
    Popup info window.
    """
    def __init__(self, parent, style=wx.SIMPLE_BORDER, info_text=u''):
        wx.PopupWindow.__init__(self, parent, style)

        # popup_win = wx.PopupWindow(parent, wx.SIMPLE_BORDER)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(DEFAULT_INFO_WINDOW_BACKGROUND_COLOUR_NAME)

        static_txt = wx.StaticText(self.panel, -1, info_text, pos=(10, 10))

        size = static_txt.GetBestSize()
        self.SetSize((size.width + 20, size.height + 20))
        self.panel.SetSize((size.width + 20, size.height + 20))

        # self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeft)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeft)
        static_txt.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeft)
        wx.CallAfter(self.Refresh)

    def close(self):
        """
        Close window.
        """
        self.Show(False)
        wx.CallAfter(self.Destroy)

    def onMouseLeft(self, event):
        """
        Popup right click handler.
        """
        self.close()


def showInfoWindow(parent=None, ctrl=None, x=-1, y=-1, info_text=u'',
                   backgroundColour=None):
    """
    Show popup info window.

    :param parent: Parent window.
    :param ctrl: The control to which the popup is riveted.
    :param x: The X coordinate of the popup output.
         If not specified, then the left border of the control is taken.
    :param y:The y-coordinate of the popup output.
         If not specified, then the lower limit of the control is taken.
    :param info_text: Info message text.
    :param backgroundColour: Window background color.
    :return: The function returns the created popup
         or None on error.
    """
    try:
        if ctrl:
            x_offset, y_offset = ctrl.ClientToScreen((0, 0))
            if x <= 0:
                x = x_offset
            if y <= 0:
                y = y_offset

        if x <= 0:
            x = 0
        if y <= 0:
            y = 0

        if parent is None:
            parent = wx.GetApp().GetTopWindow()

        popup_win = iqPopupInfoWindow(parent, wx.SIMPLE_BORDER,
                                      info_text=info_text)

        if backgroundColour:
            popup_win.panel.SetBackgroundColour(backgroundColour)

        height = ctrl.GetSize().height if ctrl else 0
        popup_win.Position(wx.Point(x, y), (0, height))
        popup_win.Show(True)
        return popup_win
    except:
        log_func.fatal(u'Error shew popup info window')
    return None
