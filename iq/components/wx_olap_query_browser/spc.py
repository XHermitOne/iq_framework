#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP server query browser specification module.
"""

from .. import wx_panel

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxOLAPQueryBrowser'

WXOLAPQUERYBROWSER_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    '__package__': u'OLAP',
    '__icon__': 'fatcow/table_analysis',
    '__parent__': wx_panel.SPC if hasattr(wx_panel, 'SPC') else dict(),
    '__doc__': None,
    '__content__': (),
    '__edit__': {
    },
    '__help__': {
    },
}

SPC = WXOLAPQUERYBROWSER_SPC
