#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query specification module.
"""

# import os.path
# import sqlalchemy.dialects
# import wx.propgrid

from iq.object import object_spc
from ...editor import property_editor_id
# from ...util import str_func
# from ...util import log_func
from ...util import lang_func
# from ...dialog import dlg_func
# from ...kernel import kernel

from ... import passport
from .. import data_engine

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

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
            'valid': validDBEnginePsp,
        },
        'sql_txt': property_editor_id.SCRIPT_EDITOR,
    },
    '__help__': {
        'db_engine': u'Database engine',
        'sql_txt': u'SQL query text template',
    },
}

SPC = DATAQUERY_SPC
