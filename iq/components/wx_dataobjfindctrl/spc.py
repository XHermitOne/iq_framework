#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data object find control specification module.
"""

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

from ... import passport
from .. import data_ref_object
from .. import data_uni_object

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxDataObjFindCtrl'

DATA_OBJECT_TYPES = (data_ref_object.COMPONENT_TYPE, data_uni_object.COMPONENT_TYPE)

def validDataObjectPsp(psp, *args, **kwargs):
    """
    Validate data object passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in DATA_OBJECT_TYPES


WXDATAOBJFINDCTRL_STYLE = {
}


WXDATAOBJFINDCTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'data_obj': None,
    'columns': [],
    'label': 'Find:',
    'image': None,
    'on_find': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/table_tab_search',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'data_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validDataObjectPsp,
        },
        'columns': property_editor_id.STRINGLIST_EDITOR,
        'label': property_editor_id.STRING_EDITOR,
        'image': property_editor_id.ICON_EDITOR,
        'on_find': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'data_obj': u'Find data object',
        'columns': u'Find column names',
        'label': u'Label',
        'image': u'Find button library icon name',
        'on_find': u'Find button click event handler'
    },
}

SPC = WXDATAOBJFINDCTRL_SPC
