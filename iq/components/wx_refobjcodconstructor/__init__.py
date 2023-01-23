#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjCodConstructor component.
"""

from .spc import SPC
from .spc import COMPONENT_TYPE

try:
    from .component import COMPONENT
except:
    print(u'Import error <%s>' % COMPONENT_TYPE)

__version__ = (0, 0, 0, 1)
