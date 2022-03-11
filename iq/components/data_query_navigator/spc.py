#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query dataset navigator specification module.
"""

import os.path
from iq.object import object_spc
from ... import passport

from ...editor import property_editor_id

from . import query_navigator

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqDataQueryNavigator'

QUERY_TYPES = ('iqDataQuery',)


def validQueryPsp(psp, *args, **kwargs):
    """
    Validate query passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in QUERY_TYPES


DATAQUERYNAVIGATOR_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'query': None,

    'where_name': query_navigator.DEFAULT_WHERE_VARIABLE_NAME,
    'order_by_name': query_navigator.DEFAULT_ORDER_BY_VARIABLE_NAME,
    'limit_name': query_navigator.DEFAULT_LIMIT_VARIABLE_NAME,

    '__package__': u'Data',
    '__icon__': 'fatcow/table_lightning',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),

    '__edit__': {
        'query': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validQueryPsp,
        },
        'where_name': property_editor_id.STRING_EDITOR,
        'order_by_name': property_editor_id.STRING_EDITOR,
        'limit_name': property_editor_id.STRING_EDITOR,
    },
    '__help__': {
        'query': u'Query manager object',
        'where_name': u'Records filter name in Query expression WHERE section',
        'order_by_name': u'Sorting name in Query expression ORDER BY section',
        'limit_name': u'Limiting name in Query expression LIMIT section',
    },

}

SPC = DATAQUERYNAVIGATOR_SPC
