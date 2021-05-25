#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx PieCtrl specification module.
"""

import wx

from ..wx_widget import SPC as wx_widget_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)

WXWINDOW_STYLE = {
    # 'CAPTION': wx.CAPTION,
    # 'MINIMIZE_BOX': wx.MINIMIZE_BOX,
    # 'MAXIMIZE_BOX': wx.MAXIMIZE_BOX,
    # 'THICK_FRAME': wx.THICK_FRAME,
    'SIMPLE_BORDER': wx.SIMPLE_BORDER,
    'DOUBLE_BORDER': wx.DOUBLE_BORDER,
    'SUNKEN_BORDER': wx.SUNKEN_BORDER,
    'RAISED_BORDER': wx.RAISED_BORDER,
    'STATIC_BORDER': wx.STATIC_BORDER,
    'TRANSPARENT_WINDOW': wx.TRANSPARENT_WINDOW,
    'TAB_TRAVERSAL': wx.TAB_TRAVERSAL,
    'WANTS_CHARS': wx.WANTS_CHARS,
    'NO_FULL_REPAINT_ON_RESIZE': wx.NO_FULL_REPAINT_ON_RESIZE,
    'VSCROLL': wx.VSCROLL,
    'HSCROLL': wx.HSCROLL,
    'CLIP_CHILDREN': wx.CLIP_CHILDREN,
}


COMPONENT_TYPE = 'iqWxPieCtrl'

WXPIECTRL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'angle': 45.0,
    'rotation_angle': 0.0,
    'show_edges': False,
    # 'ctrl_height': 30,

    'show_legend': True,
    'legend_transparent': True,
    'legend_horizontal_border': -1,
    'legend_vertical_border': -1,
    'legend_window_style': wx.STATIC_BORDER,
    'legend_label_font': None,
    'legend_label_colour': None,
    'legend_background_colour': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/chart_pie_title',
    '__parent__': wx_widget_spc,
    '__doc__': None,
    '__content__': (),
    '__edit__': {
        'angle': property_editor_id.FLOAT_EDITOR,
        'rotation_angle': property_editor_id.FLOAT_EDITOR,
        'show_edges': property_editor_id.CHECKBOX_EDITOR,

        'show_legend': property_editor_id.CHECKBOX_EDITOR,
        'legend_transparent': property_editor_id.CHECKBOX_EDITOR,
        'legend_horizontal_border': property_editor_id.INTEGER_EDITOR,
        'legend_vertical_border': property_editor_id.INTEGER_EDITOR,
        'legend_window_style': {
            'editor': property_editor_id.FLAG_EDITOR,
            'choices': WXWINDOW_STYLE,
        },
        'legend_label_font': property_editor_id.FONT_EDITOR,
        'legend_label_colour': property_editor_id.COLOUR_EDITOR,
        'legend_background_colour': property_editor_id.COLOUR_EDITOR,

    },
    '__help__': {
        'angle': u'Orientation angle, in degree',
        'rotation_angle': u'The angle at which the first sector starts, in degree',
        'show_edges': u'Whether the control edges are visible or not',

        'show_legend': u'Show legend?',
        'legend_transparent': u'Toggles the legend transparency (visibility)',
        'legend_horizontal_border': u'The legend’s horizontal border, in pixels',
        'legend_vertical_border': u'The legend’s vertical border, in pixels',
        'legend_window_style': u'The legend’s window style',
        'legend_label_font': u'The legend label font',
        'legend_label_colour': u'The legend label colour',
        'legend_background_colour': u'The legend background colour',

    },
}

SPC = WXPIECTRL_SPC
