#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data wide history specification module.
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
            resource_editor.getProperty('dt_column').SetChoices(choices)


COMPONENT_TYPE = 'iqDataWideHistory'


DATAWIDEHISTORY_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'filter': None,
    'dt_column': None,

    '__package__': u'Data',
    '__icon__': 'fatcow%sclock_history_frame' % os.path.sep,
    '__parent__': data_navigator.SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'model': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'on_change': onModelChange,
        },
        'dt_column': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getColumnNames,
        },
    },
    '__help__': {
        'dt_column': u'Column name for time',
    },
}

SPC = DATAWIDEHISTORY_SPC
