#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model column specification module.
"""

import copy
import os.path
import sqlalchemy.types

from iq.object import object_spc
from ...editor import property_editor_id

from ... import passport

from ...util import log_func

__version__ = (0, 0, 0, 1)

SQLALCHEMY_FIELD_TYPES = copy.deepcopy(sqlalchemy.types.__all__)
SQLALCHEMY_FIELD_TYPES.sort()


def validObjLinkPsp(psp, *args, **kwargs):
    """
    Validate object link passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    if not psp or psp == str(None):
        # No link
        log_func.debug(u'Validate object link passport <%s>' % str(psp))
        return True

    from .. import data_ref_object
    from .. import data_uni_object

    data_object_types = (data_ref_object.COMPONENT_TYPE,
                         data_uni_object.COMPONENT_TYPE)

    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in data_object_types


COMPONENT_TYPE = 'iqDataColumn'

DATACOLUMN_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'field_type': 'Text',
    'field_attr': None,
    'link': None,

    'autoincrement': False,
    'default': None,
    'key': None,
    'index': False,
    'info': None,
    'nullable': True,
    'onupdate': None,
    'primary_key': False,
    'server_default': '',
    'server_onupdate': None,
    'quote': False,
    'unique': False,
    'system': False,

    '__package__': u'Data',
    '__icon__': 'fatcow/table_select_column',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'field_type': {
            'editor': property_editor_id.SINGLE_CHOICE_EDITOR,
            'choices': SQLALCHEMY_FIELD_TYPES,
        },
        'field_attr': property_editor_id.SCRIPT_EDITOR,
        'link': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validObjLinkPsp,
        },

        'autoincrement': property_editor_id.CHECKBOX_EDITOR,
        'default': property_editor_id.SCRIPT_EDITOR,
        'key': property_editor_id.STRING_EDITOR,
        'index': property_editor_id.CHECKBOX_EDITOR,
        'info': property_editor_id.SCRIPT_EDITOR,
        'nullable': property_editor_id.CHECKBOX_EDITOR,
        'onupdate': property_editor_id.SCRIPT_EDITOR,
        'primary_key': property_editor_id.CHECKBOX_EDITOR,
        'server_default': property_editor_id.TEXT_EDITOR,
        'server_onupdate': property_editor_id.SCRIPT_EDITOR,
        'quote': property_editor_id.CHECKBOX_EDITOR,
        'unique': property_editor_id.CHECKBOX_EDITOR,
        'system': property_editor_id.CHECKBOX_EDITOR,
    },
    '__help__': {
        'field_type': u'The column\'s type',
        'field_attr': u'Additional field type attributes',
        'link': u'Data object link',

        'autoincrement': u'Autoincrement flag',
        'default': u'Scalar or Python callable representing the default value for this column',
        'key': u'An optional string identifier which will identify this Column object on the Table',
        'index': u'This is a shortcut for using a Index construct on the table',
        'info': u'Optional data dictionary which SchemaItem.info attribute of this object',
        'nullable': u'If set to the default of True, indicates the column will be rendered as allowing NULL, else it\'s rendered as NOT NULL',
        'onupdate': u'A scalar or Python callable representing a de-fault value to be applied to the column',
        'primary_key': u'If True, marks this column as a primary key column',
        'server_default': u'A string representing the DDL DEFAULT value for the column',
        'server_onupdate': u'A FetchedValue instance representing a database-side default generation function',
        'quote': u'Force quoting of this column’s name on or off',
        'unique': u'When True, indicates that this column contains a unique constraint,',
        'system': u'When True, indicates this is a \"system\" column, that is a column which is automatically made available by the database, and should not be included in the columns list',
    },
}

SPC = DATACOLUMN_SPC
