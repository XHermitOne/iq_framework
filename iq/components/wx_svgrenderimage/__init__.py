#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderImage component.
"""

try:
    from .spc import SPC
    from .spc import COMPONENT_TYPE
    from .component import COMPONENT
except:
    print(u'Import error <iqWxSVGRenderImage>')
    raise

__version__ = (0, 0, 0, 1)
