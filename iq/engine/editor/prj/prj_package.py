#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Package project item class.
"""

from . import prj_item

__version__ = (0, 0, 0, 1)


class iqProjectPackage(prj_item.iqProjectItem):
    """
    Package project item class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        prj_item.iqProjectItem.__init__(self, *args, **kwargs)


