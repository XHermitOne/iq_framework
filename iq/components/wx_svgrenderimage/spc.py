#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderImage specification module.
"""

from iq.object import object_spc
from ...editor import property_editor_id

__version__ = (0, 0, 0, 1)


def designComponent(spc, *args, **kwargs):
    """
    Design component.

    :param spc: Component specification.
    :return: True/False.
    """
    from . import svg_file

    svg_filename = spc.get('svg_filename', None)
    svg_file_obj = svg_file.iqSVGFile(svg_filename=svg_filename)
    return svg_file_obj.editSVG()


COMPONENT_TYPE = 'iqWxSVGRenderImage'

WXSVGRENDERIMAGE_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    'svg_filename': None,

    '__package__': u'wxPython',
    '__icon__': 'fatcow/picture',
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': (),
    '__design__': designComponent,
    '__edit__': {
        'svg_filename': property_editor_id.FILE_EDITOR,
    },
    '__help__': {
        'svg_filename': u'Image SVG filename',
    },
}

SPC = WXSVGRENDERIMAGE_SPC
