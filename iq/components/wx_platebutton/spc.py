#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton specification module.
"""

import os.path
import wx
import wx.lib.platebtn

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxPlateButton'

WXPLATEBUTTON_STYLE = {
    'PB_STYLE_DEFAULT': wx.lib.platebtn.PB_STYLE_DEFAULT,
    'PB_STYLE_DROPARROW': wx.lib.platebtn.PB_STYLE_DROPARROW,
    'PB_STYLE_GRADIENT': wx.lib.platebtn.PB_STYLE_GRADIENT,
    'PB_STYLE_NOBG': wx.lib.platebtn.PB_STYLE_NOBG,
    'PB_STYLE_SQUARE': wx.lib.platebtn.PB_STYLE_SQUARE,
    'PB_STYLE_TOGGLE': wx.lib.platebtn.PB_STYLE_TOGGLE,
}


WXPLATEBUTTON_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'label': 'button',
    'style': 0,
    'position': (-1, -1),
    'size': (-1, -1),
    'font': {},
    'foreground_colour': None,
    'background_colour': None,
    'image': None,
    'on_button_click': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/button',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'position': property_editor_id.POINT_EDITOR,
        'size': property_editor_id.SIZE_EDITOR,
        'foreground_colour': property_editor_id.COLOUR_EDITOR,
        'background_colour': property_editor_id.COLOUR_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXPLATEBUTTON_STYLE,
        },
        'image': property_editor_id.ICON_EDITOR,
        'on_button_click': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'position': u'Control position',
        'size': u'Control size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Control style',
        'label': u'Label',
        'image': u'Button library icon name',
        'on_button_click': u'Button click event handler'
    },
}

SPC = WXPLATEBUTTON_SPC
