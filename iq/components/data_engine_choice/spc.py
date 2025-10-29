#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine choice specification module.
"""

from iq.object import object_spc

from ...editor import property_editor_id

# from ...util import global_func
# from ... import global_data

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataEngineChoice'

DATAENGINECHOICE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'filename': None,
    # 'engine': global_func.getEngineType(),

    '__package__': u'Data',
    '__icon__': 'fatcow/database_access',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.data_engine_choice.html',
    '__content__': (),
    '__test__': None,
    '__edit__': {
        'filename': property_editor_id.FILE_EDITOR,
        # 'engine': {
        #     'editor': property_editor_id.CHOICE_EDITOR,
        #     'choices': global_data.ENGINE_TYPES,
        # },
    },
    '__help__': {
        'filename': u'DB engine data file name',
        # 'engine': u'Engine type',
    },
}

SPC = DATAENGINECHOICE_SPC
