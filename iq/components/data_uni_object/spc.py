#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object specification module.
"""

import os.path
import wx.propgrid

from ...editor import property_editor_id

from .. import data_navigator

from ...util import spc_func
from ... import passport

__version__ = (0, 0, 0, 1)


COMPONENT_TYPE = 'iqDataUniObject'


DATAUNIOBJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    '__package__': u'Data',
    '__icon__': 'fatcow/brick',
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
        },
    },
    '__help__': {
    },
}

SPC = DATAUNIOBJECT_SPC
