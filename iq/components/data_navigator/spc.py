#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator specification module.
"""

import os.path
from iq.object import object_spc
from ... import passport

from ...editor import property_editor_id

__version__ = (0, 0, 2, 1)

COMPONENT_TYPE = 'iqDataNavigator'

MODEL_TYPES = ('iqDataModel', 'iqDataRefObjModel', 'iqDataUniObjModel')


def validModelPsp(psp, *args, **kwargs):
    """
    Validate model passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in MODEL_TYPES


DATANAVIGATOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'model': None,
    'readonly': False,

    '__package__': u'Data',
    '__icon__': 'fatcow/compass',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),

    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validModelPsp,
        },
        'readonly': {
            'editor': property_editor_id.CHECKBOX_EDITOR,
        },
    },
    '__help__': {
        'model': u'Model manager object',
        'readonly': u'Model readonly option',
    },

}

SPC = DATANAVIGATOR_SPC
