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

MNEMOANCHOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'svg_pos': (0.0, 0.0),
    'svg_size': (-1, -1),
    'style': ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
    'min_size': (-1, -1),
    'max_size': (-1, -1),
    'attachment': None,

    '__package__': u'SCADA',
    '__icon__': 'fatcow%sanchor' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'svg_pos': property_editor_id.POINT_EDITOR,
        'svg_size': property_editor_id.SIZE_EDITOR,
        'style': ANCHOR_DIRECTION_FROM_LEFT_TO_RIGHT | ANCHOR_DIRECTION_FROM_TOP_TO_BOTTOM,
        'min_size': property_editor_id.SIZE_EDITOR,
        'max_size': property_editor_id.SIZE_EDITOR,
        'attachment': property_editor_id.PASSPORT_EDITOR,
    },
    '__help__': {
        'svg_pos': u'Опорная позиция якоря в единицах измерения SVG',
        'svg_size': u'Размер ячейки якоря в единицах измерения SVG',
        'style': u'Указание направления смещения якоря относительно опорной точки',
        'min_size': u'Указание ограничения размера по минимуму в пикселях',
        'max_size': u'Указание ограничения размера по максимуму в пикселях',
        'attachment': u'Паспорт контрола мнемосхемы, прикрепленного к якорю',
    },
}

SPC = MNEMOANCHOR_SPC
