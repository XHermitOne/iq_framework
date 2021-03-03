#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderPanel specification module.
"""

from ...editor import property_editor_id

from .. import wx_panel

__version__ = (0, 0, 0, 1)


def designComponent(spc, *args, **kwargs):
    """
    Design component.

    :param spc: Component specification.
    :return: True/False.
    """
    from ..wx_svgrenderimage import svg_file

    svg_filename = spc.get('svg_background', None)
    svg_file_obj = svg_file.iqSVGFile(svg_filename=svg_filename)
    return svg_file_obj.editSVG()


COMPONENT_TYPE = 'iqWxSVGRenderPanel'

WXSVGRENDERPANEL_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,

    '_children_': [],

    'svg_background': None,
    # 'svg_width': 0.0,
    # 'svg_height': 0.0,
    'center': False,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/application_view_gallery',
    '__parent__': wx_panel.SPC if hasattr(wx_panel, 'SPC') else dict(),
    '__doc__': None,
    '__content__': ('iqWxSVGRenderImage', ),
    '__design__': designComponent,

    '__edit__': {
        'svg_background': property_editor_id.FILE_EDITOR,
        # 'svg_width': property_editor_id.FLOAT_EDITOR,
        # 'svg_height': property_editor_id.FLOAT_EDITOR,
        'center': property_editor_id.CHECKBOX_EDITOR,
    },
    '__help__': {
        'svg_background': u'SVG render panel background svg file',
        # 'svg_width': u'SVG width in source units',
        # 'svg_height': u'SVG height in source units',
        'center': u'Center background image?',
    },
}

SPC = WXSVGRENDERPANEL_SPC
