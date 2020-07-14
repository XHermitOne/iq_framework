#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx panel specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxPanel'

WXPANEL_STYLE = {
    'CAPTION': wx.CAPTION,
    'MINIMIZE_BOX': wx.MINIMIZE_BOX,
    'MAXIMIZE_BOX': wx.MAXIMIZE_BOX,
    # 'THICK_FRAME': wx.THICK_FRAME,
    'SIMPLE_BORDER': wx.SIMPLE_BORDER,
    'DOUBLE_BORDER': wx.DOUBLE_BORDER,
    'SUNKEN_BORDER': wx.SUNKEN_BORDER,
    'RAISED_BORDER': wx.RAISED_BORDER,
    'STATIC_BORDER': wx.STATIC_BORDER,
    'TRANSPARENT_WINDOW': wx.TRANSPARENT_WINDOW,
    'TAB_TRAVERSAL': wx.TAB_TRAVERSAL,
    'WANTS_CHARS': wx.WANTS_CHARS,
    'NO_FULL_REPAINT_ON_RESIZE': wx.NO_FULL_REPAINT_ON_RESIZE,
    'VSCROLL': wx.VSCROLL,
    'HSCROLL': wx.HSCROLL,
    'CLIP_CHILDREN': wx.CLIP_CHILDREN,
}

WXPANEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'position': (-1, -1),
    'size': (100, 100),
    'foreground_colour': None,
    'background_colour': None,
    'style': wx.TAB_TRAVERSAL,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/panel_blank',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXPANEL_STYLE,
        },
    },
    '__help__': {
        'position': u'Panel position',
        'size': u'Panel size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Panel style',
    },
}

SPC = WXPANEL_SPC
