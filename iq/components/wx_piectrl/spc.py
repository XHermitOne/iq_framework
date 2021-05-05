#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PieCtrl specification module.
"""

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqWxPieCtrl'

WXPIECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    # 'label': 'button',
    #
    # 'image': None,
    # 'on_button_click': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/chart_pie_title',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        # 'label': property_editor_id.STRING_EDITOR,
        # 'style': {
        #     'editor': property_editor_id.FLAG_EDITOR,
        #     'choices': WXPLATEBUTTON_STYLE,
        # },
        # 'image': property_editor_id.ICON_EDITOR,
        # 'on_button_click': property_editor_id.EVENT_EDITOR,
    },
    '__help__': {
        # 'label': u'Label',
        # 'image': u'Button library icon name',
        # 'on_button_click': u'Button click event handler'
    },
}

SPC = WXPIECTRL_SPC
