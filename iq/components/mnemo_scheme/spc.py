#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme specification module.
"""

from ...editor import property_editor_id

from .. import wx_panel

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqMnemoScheme'

MNEMOSCHEME_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'svg_background': None,
    'svg_width': 0.0,
    'svg_height': 0.0,

    '__package__': u'SCADA',
    '__icon__': 'fatcow/smartart_organization_chart_stand',
    '__parent__': wx_panel.SPC if hasattr(wx_panel, 'SPC') else dict(),
    '__doc__': None,
    '__content__': ('iqMnemoAnchor', 'iqWxPlateButton'),
    '__edit__': {
        'svg_background': property_editor_id.FILE_EDITOR,
        'svg_width': property_editor_id.FLOAT_EDITOR,
        'svg_height': property_editor_id.FLOAT_EDITOR,
    },
    '__help__': {
        'svg_background': u'Mnemoscheme background svg file',
        'svg_width': u'SVG width in source units',
        'svg_height': u'SVG height in source units',
    },
}

SPC = MNEMOSCHEME_SPC
