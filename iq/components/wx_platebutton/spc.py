#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton specification module.
"""

import wx.lib.platebtn

from ..wx_widget import SPC as wx_widget_spc
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

    '_children_': [],

    'label': 'button',

    'image': None,
    'on_button_click': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/button',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'label': property_editor_id.STRING_EDITOR,
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXPLATEBUTTON_STYLE,
        },
        'image': property_editor_id.ICON_EDITOR,
        'on_button_click': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'label': u'Label',
        'image': u'Button library icon name',
        'on_button_click': u'Button click event handler'
    },
}

SPC = WXPLATEBUTTON_SPC
