#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjLevelChoiceCtrl specification module.
"""

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

from ..data_ref_object import spc as data_ref_object_spc

from ...util import global_func

__version__ = (0, 0, 0, 1)


def getSortColumns(resource=None, *args, **kwargs):
    """
    Get sort column names.

    :param resource: Object resource.
    :return: Column name list of reference object model.
    """
    ref_obj_psp = resource.get('ref_obj', None)
    if ref_obj_psp:
        kernel = global_func.getKernel()
        ref_obj = kernel.createByPsp(psp=ref_obj_psp)
        model = ref_obj.getModelObj()
        columns = model.getColumns()
        return [column.getName() for column in columns]
    return list()


COMPONENT_TYPE = 'iqWxRefObjLevelChoiceCtrl'

WXREFOBJLEVELCHOICECTRL_STYLE = {
}

WXREFOBJLEVELCHOICECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'ref_obj': None,

    'label': None,
    'auto_select': True,
    'sort_col': 'id',
    'on_select_code': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/combo_boxes',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'ref_obj': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': data_ref_object_spc.validRefObjPsp,
        },

        'label': property_editor_id.STRING_EDITOR,
        'auto_select': property_editor_id.CHECKBOX_EDITOR,
        'sort_col': {
            'editor': property_editor_id.CHOICE_EDITOR,
            'choices': getSortColumns,
        },
        'on_select_code': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        'ref_obj': u'Reference object passport',

        'label': u'Selection area title',
        'auto_select': u'Auto-complete',
        'sort_col': u'Sort column name',
        'on_select_code': u'Select code handler',
    },
}

SPC = WXREFOBJLEVELCHOICECTRL_SPC
