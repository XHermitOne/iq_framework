#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File project item class.
"""

from . import prj_item

__version__ = (0, 0, 0, 1)


class iqProjectFile(prj_item.iqProjectItem):
    """
    File project item class.
    """
    def __init__(self, name=None, parent=None):
        """
        Constructor.
        @param name: Item name.
        @param parent: Parent item object.
        """
        prj_item.iqProjectItem.__init__(self, name=name, parent=parent)
