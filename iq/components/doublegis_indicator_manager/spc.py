#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2GIS map indicator manager specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id
# from .. import wx_panel

# from . import trend_proto
# from . import gnuplot_trend_proto

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDoubleGISMapIndicatorManager'

DOUBLEGISMAPINDICATORMANAGER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    '__package__': u'GIS',
    '__icon__': 'fugue/map-pin',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
    },
    '__help__': {
    },
}

SPC = DOUBLEGISMAPINDICATORMANAGER_SPC
