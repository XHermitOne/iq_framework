#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx panel specification module.
"""

import os.path
import wx

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxPanel'

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
    '__icon__': 'fatcow%spanel_blank' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'position': property_editor_id.POINT_EDITOR,
        'size': property_editor_id.SIZE_EDITOR,
        'foreground_colour': property_editor_id.COLOUR_EDITOR,
        'background_colour': property_editor_id.COLOUR_EDITOR,
        # 'style': property_editor_id.,
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
