#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP cubes query tree control specification module.
"""

import wx

from ...editor import property_editor_id
from ..wx_widget import SPC as wx_widget_spc
from ... import passport

from ..wx_filtertreectrl import spc as wx_filtertreectrl_spc

from ..import cubes_olap_server

__version__ = (0, 0, 0, 1)

OLAP_SERVER_TYPES = (cubes_olap_server.COMPONENT_TYPE,
                     )


def validOLAPServerPsp(psp, *args, **kwargs):
    """
    Validate OLAP server passport.

    :param psp: Passport.
    :param args:
    :param kwargs:
    :return: True/False.
    """
    psp_obj = passport.iqPassport().setAsAny(psp)
    return psp_obj.getType() in OLAP_SERVER_TYPES


WXOLAPQUERYTREECTRL_STYLE = wx_filtertreectrl_spc.WXFILTERTREECTRL_STYLE

COMPONENT_TYPE = 'iqWxOLAPQueryTreeCtrl'

WXOLAPQUERYTREECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'style': wx.TR_DEFAULT_STYLE,

    'save_filename': None,
    'on_change': None,
    'olap_server': None,

    '__package__': u'OLAP',
    '__icon__': 'fatcow/table_heatmap_cell',
    '__parent__': wx_widget_spc,
    '__doc__': 'iq.components.wx_olap_query_treectrl.html',
    '__content__': (),
    '__edit__': {
        'save_filename': property_editor_id.FILE_EDITOR,
        'on_change': property_editor_id.EVENT_EDITOR,
        'olap_server': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': validOLAPServerPsp,
        },

        'style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXOLAPQUERYTREECTRL_STYLE,
        },
    },
    '__help__': {
        'save_filename': u'Filter storage filename',
        'on_change': u'Filter change event handler',
        'style': u'Control style',
        'olap_server': u'OLAP server',
    },
}

SPC = WXOLAPQUERYTREECTRL_SPC
