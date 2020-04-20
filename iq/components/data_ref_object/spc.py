#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object specification module.
"""

import os.path
import wx.propgrid

from ...editor import property_editor_id

from .. import data_navigator

from ...util import spc_func
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


COMPONENT_TYPE = 'iqDataRefObject'


DATAREFOBJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'cod_len': None,

    '__package__': u'Data',
    '__icon__': 'fatcow/book_addresses',
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validRefObjModelPsp,
        },

        'cod_len': property_editor_id.STRINGLIST_EDITOR,
    },
    '__help__': {
        'cod_len': u'List of level code lengths',
    },
}

SPC = DATAREFOBJECT_SPC