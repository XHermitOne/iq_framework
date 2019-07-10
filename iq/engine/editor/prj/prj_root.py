#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Root project item class.
"""

from . import prj_item

__version__ = (0, 0, 0, 1)


class iqProjectRoot(prj_item.iqProjectItem):
    """
    Root project item class.
    """
    def __init__(self, name=None, parent=None):
        """
        Constructor.
        @param name: Item name.
        @param parent: Parent item object.
        """
        prj_item.iqProjectItem.__init__(self, name=name, parent=parent)

    