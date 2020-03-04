#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme specification module.
"""

import copy
import os.path

from iq.object import object_spc
from ...editor import property_editor_id

# from .. import data_column

__version__ = (0, 0, 0, 1)

COMPONENT_TYPE = 'iqMnemoScheme'

MNEMOSCHEME_SPC = {
    'name': 'default',
    'type': COMPONENT_TYPE,
    'description': '',
    'activate': True,
    'uuid': None,

    '_children_': [],

    # 'engines': list(),
    # 'scan_class': None,
    # 'auto_run': False,
    'svg_background': None,
    'svg_width': 0.0,
    'svg_height': 0.0,

    '__package__': u'SCADA',
    '__icon__': 'fatcow%ssmartart_organization_chart_stand' % os.path.sep,
    '__parent__': object_spc.OBJECT_SPC,
    '__doc__': None,
    '__content__': ('iqMnemoAnchor', ),
    '__edit__': {
        'svg_background': property_editor_id.FILE_EDITOR,
        'svg_width': property_editor_id.FLOAT_EDITOR,
        'svg_height': property_editor_id.FLOAT_EDITOR,
    },
    '__help__': {
        # 'engines': u'Список движков SCADA системы',
        # 'scan_class': u'Класс сканирования',
        # 'auto_run': u'Признак автозапуска и автоостанова всех движков при создании/закрытии окна',
        'svg_background': u'SVG файл фона мнемосхемы',
        'svg_width': u'Ширина SVG в исходных единицах измерения',
        'svg_height': u'Высота SVG в исходных единицах измерения',
    },
}

SPC = MNEMOSCHEME_SPC
