#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Virtual spreadsheet specification module.
"""

from ...editor import property_editor_id
from ...object import object_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqVirtualSpreadsheet'

VIRTUALSPREADSHEET_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    '__package__': u'Office',
    '__icon__': 'fatcow/table_excel',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
    },
    '__help__': {
    },
}

SPC = VIRTUALSPREADSHEET_SPC
