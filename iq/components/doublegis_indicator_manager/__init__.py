#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2GIS map indicator manager component.
"""

try:
    from .spc import SPC
    from .spc import COMPONENT_TYPE
    from .component import COMPONENT
except ImportError:
    print(u'Import error <iqDoubleGISMapIndicatorManager>')

__version__ = (0, 0, 0, 1)
