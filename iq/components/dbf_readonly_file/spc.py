#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DBF readonly file component specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDBFReadOnlyFile'


DBFREADONLYFILE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'dbf_filename': None,

    '__package__': u'Data',
    '__icon__': 'fatcow/database_table',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'dbf_filename': property_editor_id.FILE_EDITOR,
    },
    '__help__': {
        'dbf_filename': u'DBF filename',
    },
}

SPC = DBFREADONLYFILE_SPC
