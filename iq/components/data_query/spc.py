#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id
from ...util import lang_func

from ..data_engine import spc as data_engine_spc

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


def testComponent(spc, *args, **kwargs):
    """
    Test component.

    :param spc: Component specification.
    :return: True/False.
    """
    from . import component
    obj = component.iqDataQuery(parent=None, resource=spc, context=dict())
    return obj.test()


COMPONENT_TYPE = 'iqDataQuery'

DATAQUERY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'db_engine': None,
    'sql_txt': None,

    '__package__': u'Data',
    '__icon__': 'fatcow/database_lightning',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__test__': testComponent,
    '__edit__': {
        'db_engine': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_engine_spc.validDBEnginePsp,
        },
        'sql_txt': property_editor_id.SCRIPT_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database engine',
        'sql_txt': u'SQL query text template',
    },
}

SPC = DATAQUERY_SPC
