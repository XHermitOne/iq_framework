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

__version__ = (0, 0, 0, 1)


def getColumnNames(resource=None, *args, **kwargs):
    """
    Get column names.

    :param resource: Object resource.
    :return:
    """
    model_psp = resource.get('model', None)
    if model_psp:
        psp = passport.iqPassport().setAsStr(model_psp)
        model_res = psp.findObjResource()
        if model_res:
            columns = model_res.get(spc_func.CHILDREN_ATTR_NAME, list())
            column_names = [column.get('name', u'unknown') for column in columns]
            return column_names
    return list()


def onModelChange(resource_editor=None, resource=None, *args, **kwargs):
    """
    Change model.
    When replacing a model, the list of column name changes.

    :param resource_editor: Resource editor frame.
    :param resource: Object resource.
    """
    if resource:
        column_names = getColumnNames(resource)
        if resource_editor:
            choices = wx.propgrid.PGChoices(column_names)
            resource_editor.getProperty('cod_column').SetChoices(choices)
            resource_editor.getProperty('active_column').SetChoices(choices)
            resource_editor.getProperty('name_column').SetChoices(choices)


COMPONENT_TYPE = 'iqDataRefObject'


DATAREFOBJECT_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'cod_column': None,
    'active_column': None,
    'name_column': None,

    '__package__': u'Data',
    '__icon__': 'fatcow%sbook_addresses' % os.path.sep,
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'on_change': onModelChange,
        },
        'cod_column': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getColumnNames,
        },
        'active_column': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getColumnNames,
        },
        'name_column': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getColumnNames,
        },
    },
    '__help__': {
        'cod_column': u'Column name for unique code',
        'active_column': u'Column name for active',
        'name_column': u'Column name for name',
    },
}

SPC = DATAREFOBJECT_SPC
