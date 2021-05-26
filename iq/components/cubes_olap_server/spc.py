#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cubes OLAP Framework Server specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id
from ... import passport

from . import cubes_olap_server_proto

from .. import data_engine

__version__ = (0, 0, 0, 1)

DB_SOURCE_TYPES = (data_engine.COMPONENT_TYPE,
                   )


def validDBPsp(psp, *args, **kwargs):
    """
    Validate database passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in DB_SOURCE_TYPES


COMPONENT_TYPE = 'iqCubesOLAPServer'

CUBESOLAPSERVER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'db': None,
    'ini_filename': cubes_olap_server_proto.DEFAULT_INI_FILENAME,
    'model_filename': cubes_olap_server_proto.DEFAULT_MODEL_FILENAME,
    'exec': cubes_olap_server_proto.ALTER_SLICER_EXEC,
    'srv_path': cubes_olap_server_proto.DEFAULT_OLAP_SERVER_DIRNAME,

    'log_filename': None,
    'log_level': cubes_olap_server_proto.LOG_LEVELS[0],
    'host': 'localhost',
    'port': 5000,
    'reload': True,
    'prettyprint': True,
    'allow_cors_origin': '*',

    '__package__': u'OLAP',
    '__icon__': 'fatcow/server_components',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqCube', ),
    '__edit__': {
        'db': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validDBPsp,
        },
        'ini_filename': property_editor_id.STRING_EDITOR,
        'model_filename': property_editor_id.STRING_EDITOR,
        'exec': property_editor_id.STRING_EDITOR,
        'srv_path': property_editor_id.DIR_EDITOR,

        'log_filename': property_editor_id.FILE_EDITOR,
        'log_level': property_editor_id.STRINGLIST_EDITOR,
        'host': property_editor_id.STRING_EDITOR,
        'port': property_editor_id.INTEGER_EDITOR,
        'reload': property_editor_id.CHECKBOX_EDITOR,
        'prettyprint': property_editor_id.CHECKBOX_EDITOR,
        'allow_cors_origin': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'db': u'Database object passport for OLAP cubes storage',
        'ini_filename': u'OLAP Server configuration file',
        'model_filename': u'JSON OLAP Server cubes description file',
        'exec': u'OLAP Server launch file',
        'srv_path': u'The folder where the OLAP server settings files are located',

        'log_filename': u'Path to log file ',
        'log_level': u'Logging level',
        'host': u'Server host',
        'port': u'Server port',
        'reload': u'',
        'prettyprint': u'Demonstration purposes ',
        'allow_cors_origin': u'Resource sharing header. Other related headers are also added if this option is present',
    },
}

SPC = CUBESOLAPSERVER_SPC
