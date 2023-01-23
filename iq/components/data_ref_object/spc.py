#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object specification module.
"""

from ...editor import property_editor_id

from .. import data_navigator

from ... import passport

from .. import data_refobj_model

__version__ = (0, 0, 0, 1)


REF_OBJ_MODEL_TYPES = (data_refobj_model.COMPONENT_TYPE, )


def validRefObjModelPsp(psp, *args, **kwargs):
    """
    Validate reference object model passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in REF_OBJ_MODEL_TYPES


def testComponent(spc, *args, **kwargs):
    """
    Test function.

    :param spc: Component specification.
    :return: True/False.
    """
    from . import component
    obj = component.iqDataRefObject(parent=None, resource=spc, context=dict())
    return obj.test()


COMPONENT_TYPE = 'iqDataRefObject'

REF_OBJ_TYPES = (COMPONENT_TYPE, )


def validRefObjPsp(psp, *args, **kwargs):
    """
    Validate reference object passport.

    :param psp: Passport.
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in REF_OBJ_TYPES


DATAREFOBJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'cod_len': (2, ),
    'level_labels': None,
    'cache': True,

    '__package__': u'Data',
    '__icon__': 'fatcow/book_addresses',
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__test__': testComponent,
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validRefObjModelPsp,
        },

        'cod_len': property_editor_id.STRINGLIST_EDITOR,
        'level_labels': property_editor_id.STRINGLIST_EDITOR,
        'cache': property_editor_id.CHECKBOX_EDITOR,
    },
    '__help__': {
        'cod_len': u'List of level code lengths',
        'level_labels': u'Level label list',
        'cache': 'Cache ref object data',
    },
}

SPC = DATAREFOBJECT_SPC
