#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UniReader controller specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

from . import uni_reader_controller

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqUniReaderController'

UNIREADERCONTROLLER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'host': u'',
    'port': uni_reader_controller.DEFAULT_PORT,
    'server': uni_reader_controller.RSLINX_SERVER,
    'node': uni_reader_controller.OPC_SERVER_NODE,
    'tags': None,

    '__package__': u'SCADA',
    '__icon__': 'fatcow/server_go',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'host': property_editor_id.STRING_EDITOR,
        'port': property_editor_id.INTEGER_EDITOR,
        'server': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': uni_reader_controller.SERVERS,
        },
        'node': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': uni_reader_controller.NODES,
        },
        'tags': property_editor_id.SCRIPT_EDITOR,
    },
    '__help__': {
        'host': u'Server host',
        'port': u'Server port',
        'server': u'Server name',
        'node': u'Node name',
        'tags': u'Tags dictionary',
    },
}

SPC = UNIREADERCONTROLLER_SPC
