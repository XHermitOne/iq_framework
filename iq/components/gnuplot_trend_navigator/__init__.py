#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gnuplot historical trend navigator panel component package.
"""

try:
    from .spc import SPC
    from .spc import COMPONENT_TYPE
    from .component import COMPONENT
except ImportError:
    print(u'Import error <iqGnuplotTrendNavigator>')

__version__ = (0, 0, 0, 1)
