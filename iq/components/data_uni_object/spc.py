#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object specification module.
"""

from ...editor import property_editor_id

from .. import data_navigator

from ... import passport

from .. import data_uniobj_model

__version__ = (0, 0, 0, 1)


UNI_OBJ_MODEL_TYPES = (data_uniobj_model.COMPONENT_TYPE, )


def validUniObjModelPsp(psp, *args, **kwargs):
    """
    Validate unique object model passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in UNI_OBJ_MODEL_TYPES


COMPONENT_TYPE = 'iqDataUniObject'


DATAUNIOBJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    '__package__': u'Data',
    '__icon__': 'fatcow/brick',
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validUniObjModelPsp,
        },
    },
    '__help__': {
    },
}

SPC = DATAUNIOBJECT_SPC
