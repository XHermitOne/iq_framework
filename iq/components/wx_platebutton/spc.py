#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PlateButton specification module.
"""

import os.path
import wx

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxPlateButton'

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

    '__package__': u'wxPython',
    '__icon__': 'fatcow%sbutton' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'position': property_editor_id.POINT_EDITOR,
        'size': property_editor_id.SIZE_EDITOR,
        'foreground_colour': property_editor_id.COLOUR_EDITOR,
        'background_colour': property_editor_id.COLOUR_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
        # 'style': property_editor_id.,
        'image': property_editor_id.LIBICON_EDITOR,
    },
    '__help__': {
        'position': u'Control position',
        'size': u'Control size',
        'foreground_colour': u'Foreground colour',
        'background_colour': u'Background colour',
        'style': u'Control style',
        'label': u'Label',
        'image': u'Button library icon name',
    },
}

SPC = WXPLATEBUTTON_SPC
