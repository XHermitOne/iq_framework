#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transformation data specification module.
"""

from ...object import object_spc
from ...editor import property_editor_id
from ... import passport

from .. import data_query
from .. import data_model

__version__ = (0, 0, 0, 1)

TABLE_DATASOURCE_TYPES = (data_query.COMPONENT_TYPE,
                          data_model.COMPONENT_TYPE)


def validTableDataSourcePsp(psp, *args, **kwargs):
    """
    Validate table datasource passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in TABLE_DATASOURCE_TYPES


def testComponent(spc, *args, **kwargs):
    """
    Test component.

    :param spc: Component specification.
    :return: True/False.
    """
    from . import component
    obj = component.iqTransformDataSource(parent=None, resource=spc, context=dict())
    return obj.test()


COMPONENT_TYPE = 'iqTransformDataSource'

TRANSFORMDATASOURCE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'tab_datasource': None,
    'transform': 'return DATAFRAME',

    '__package__': u'Data',
    '__icon__': 'fatcow/table_lightning',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': 'iq.components.transform_datasource.html',
    '__content__': (),
    '__test__': testComponent,
    '__edit__': {
        'tab_datasource': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validTableDataSourcePsp,
        },
        'transform': property_editor_id.METHOD_EDITOR,
    },
    '__help__': {
        'tab_datasource': u'Table datasource object',
        'transform': u'Transform DataFrame method',
    },
}

SPC = TRANSFORMDATASOURCE_SPC
