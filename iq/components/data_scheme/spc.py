#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme specification module.
"""

import os.path
from iq.object import object_spc
from ...editor import property_editor_id

from . import scheme_module_generator

from ... import passport
from .. import data_engine

__version__ = (0, 0, 0, 1)


DB_ENGINE_TYPES = (data_engine.COMPONENT_TYPE, )


def validDBEnginePsp(psp, *args, **kwargs):
    """
    Validate DB engine passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in DB_ENGINE_TYPES


COMPONENT_TYPE = 'iqDataScheme'

DATASCHEME_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,
    'module': None,

    '_children_': [],

    'db_engine': None,

    '__gen_module__': scheme_module_generator.genModule,
    '__package__': u'Data',
    '__icon__': 'fatcow/chart_organisation',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqDataModel', 'iqDataRefObjModel', 'iqDataUniObjModel'),
    '__edit__': {
        'db_engine': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validDBEnginePsp,
        }
    },
    '__help__': {
        'db_engine': u'Database engine',
    },
}

SPC = DATASCHEME_SPC
