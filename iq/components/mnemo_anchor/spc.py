#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme anchor specification module.
"""

import os.path

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqMnemoAnchor'

ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT = 1  # From left to right
ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT = 2  # From right to left
ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM = 4  # From top to down
ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP = 8  # From down to top

DIRECTION_CHOICES = {
    'ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT': ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT,
    'ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT': ANCHOR_DIRECTION_FROM_RIGHT_TO_LEFT,
    'ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM': ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
    'ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP': ANCHOR_DIRECTION_FROM_BOTTOM_TO_TOP,
}


MNEMOANCHOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'attachment': None,
    'direction': ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
    'min_size': (-1, -1),
    'max_size': (-1, -1),
    'svg_pos': (0.0, 0.0),
    'svg_size': (-1, -1),

    '__package__': u'SCADA',
    '__icon__': 'fatcow/anchor',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'svg_pos': property_editor_id.POINT_EDITOR,
        'svg_size': property_editor_id.SIZE_EDITOR,
        'direction': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': DIRECTION_CHOICES,
        },
        'min_size': property_editor_id.SIZE_EDITOR,
        'max_size': property_editor_id.SIZE_EDITOR,
        'attachment': property_editor_id.PASSPORT_EDITOR,
    },
    '__help__': {
        'svg_pos': u'Anchor reference position in SVG units',
        'svg_size': u'Anchor cell size in SVG units',
        'direction': u'Indication of the direction of the anchor displacement relative to the anchor point',
        'min_size': u'Specify a minimum pixel size limit',
        'max_size': u'Specifying a maximum size limit in pixels',
        'attachment': u'Passport control mnemonic attached to the anchor',
    },
}

SPC = MNEMOANCHOR_SPC
