#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP server query browser specification module.
"""

from .. import wx_panel

from ...editor import property_editor_id

from ..wx_olap_query_treectrl import spc as wx_olap_query_treectrl_spc

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxOLAPQueryBrowser'

WXOLAPQUERYBROWSER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'olap_server': None,

    '__package__': u'OLAP',
    '__icon__': 'fatcow/table_analysis',
    '__parent__': wx_panel.SPC if hasattr(wx_panel, 'SPC') else dict(),
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'olap_server': {
            'editor': property_editor_id.PASSPORT_EDITOR,
            'valid': wx_olap_query_treectrl_spc.validOLAPServerPsp,
        },
    },
    '__help__': {
        'olap_server': u'OLAP server',
    },
}

SPC = WXOLAPQUERYBROWSER_SPC
