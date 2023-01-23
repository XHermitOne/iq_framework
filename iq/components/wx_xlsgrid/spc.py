#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx XLSGrid specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxXLSGrid'

WXXLSGRID_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'position': (-1, -1),
    'size': (-1, -1),
    'xls_filename': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/table_excel',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'xls_filename': property_editor_id.FILE_EDITOR,
    },
    '__help__': {
        'position': u'Control position',
        'size': u'Control size',
        'xls_filename': u'Default opened XLS filename',
    },
}

SPC = WXXLSGRID_SPC
