#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wxColour convert function.
"""

import wx

from ...util import log_func

__version__ = (0, 0, 0, 1)

WX_ADAPT_COLOURS = dict()
DEFAULT_COLOUR = 'default'


def wxColour2StrHex(colour):
    """
    wxColour as #RRGGBB string.

    :param colour: wx.Colour object.
    :return: #RRGGBB string.
    """
    if isinstance(colour, wx.Colour):
        return colour.GetAsString(wx.C2S_HTML_SYNTAX)
    elif isinstance(colour, str) and colour not in ('default',):
        return colour

    log_func.warning(u'It is not possible to convert colour <%s> to format #RRGGBB. Black colour used' % str(colour))
    return '#000000'


wxColour2StrRGB = wxColour2StrHex


def StrHex2wxColour(rgb_colour):
    """
    Convert #RRGGBB string to wxColour object.

    :param rgb_colour: #RRGGBB string.
    :return: wx.Colour object.
    """
    str_rgb = rgb_colour.replace('#', '')
    red = eval('0x' + str_rgb[:2])
    green = eval('0x' + str_rgb[2:4])
    blue = eval('0x' + str_rgb[4:])
    colour = wx.Colour(red, green, blue)
    return colour


StrRGB2wxColour = StrHex2wxColour


def RGB2wxColour(rgb):
    """
    Convert colour as (Red, Green, Blue) to wxColour object.

    :param rgb: Colour tuple (Red, Green, Blue).
    :return: wx.Colour object or None if error.
    """
    if (not isinstance(rgb, tuple) or not isinstance(rgb, list)) and len(rgb) != 3:
        log_func.warning(u'It is not possible to convert <%s> to wx.Colour object' % str(rgb))
        return None

    return wx.Colour(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def wxColour2RGB(colour):
    """
    Convert wxColour object to (Red, Green, Blue) tuple.

    :param colour: wx.Colour object.
    :return: Colour tuple (Red, Green, Blue) or None if error.
    """
    assert isinstance(colour, wx.Colour), u'wx.Colour object type error'

    return colour.Red(), colour.Green(), colour.Blue()


def isDarkSysTheme():
    """
    Checking if the OS system theme is dark.

    :return: True/False.
    """
    win_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
    sum_rgb = win_colour.Red() + win_colour.Green() + win_colour.Blue()
    # Sum:       128+128+128
    # ----------------V
    return sum_rgb < 384


def adaptSysThemeColour(dark_theme_colour=None, light_theme_colour=None):
    """
    Adapt color to system theme (dark or light).
    The whole point is that mathematically calculates the color contracting with
    current system theme, but retaining color.
    It is enough to indicate one of the colors:

    :param dark_theme_colour: wx.Colour object, matching / contracting with a dark theme.
    :param light_theme_colour: wx.Colour object, matching / contracting with a light theme.
    :return: Adapted color.
    """
    global WX_ADAPT_COLOURS

    is_dark_sys_theme = isDarkSysTheme()
    if not is_dark_sys_theme and light_theme_colour:
        return light_theme_colour
    elif not is_dark_sys_theme and not light_theme_colour and dark_theme_colour:
        red = max(dark_theme_colour.Red() - 128, 32) if dark_theme_colour.Red() else 0
        green = max(dark_theme_colour.Green() - 128, 32) if dark_theme_colour.Green() else 0
        blue = max(dark_theme_colour.Blue() - 128, 32) if dark_theme_colour.Blue() else 0
        rgb = (red, green, blue)
        if rgb in WX_ADAPT_COLOURS:
            colour = WX_ADAPT_COLOURS[rgb]
        else:
            colour = wx.Colour(red, green, blue)
            WX_ADAPT_COLOURS[rgb] = colour
        return colour
    elif is_dark_sys_theme and dark_theme_colour:
        return dark_theme_colour
    elif is_dark_sys_theme and light_theme_colour and not dark_theme_colour:
        red = min(light_theme_colour.Red() + 128, 255) if light_theme_colour.Red() else 0
        green = min(light_theme_colour.Green() + 128, 255) if light_theme_colour.Green() else 0
        blue = min(light_theme_colour.Blue() + 128, 255) if light_theme_colour.Blue() else 0
        rgb = (red, green, blue)
        if rgb in WX_ADAPT_COLOURS:
            colour = WX_ADAPT_COLOURS[rgb]
        else:
            colour = wx.Colour(red, green, blue)
            WX_ADAPT_COLOURS[rgb] = colour
        return colour
    else:
        log_func.warning(u'It is not possible to adapt the color to the hue of the system theme')

    return wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)


def getTintColour(colour, calc_rate=None):
    """
    Get shaded color from specified.

    :param colour: Basic wx.Colour object.
    :param calc_rate: Shade calculation factor. If not specified then 7/8 is taken.
    :return: Shaded color.
    """
    if calc_rate is None:
        calc_rate = 7.0 / 8.0
    return wx.Colour(tuple([int(c * calc_rate) for c in tuple(colour)[:-1]]))


def isDefaultColour(colour):
    """
    Check if the specified color is the default color

    :param colour: wx.Colour object.
    :return: True/False.
    """
    return isinstance(colour, str) and colour == DEFAULT_COLOUR


def getDefaultEvenRowsBGColour():
    """
    The background color of even lines is the default.
    """
    colour = tuple(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))[:-1]
    return wx.Colour(*colour)


def getDefaultOddRowsBGColour():
    """
    The background color is not even lines by default.
    """
    return getTintColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))
