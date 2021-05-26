#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension hierarchy.
"""

__version__ = (0, 0, 0, 1)


class iqCubeDimensionHierarchyProto(object):
    """
    OLAP Cube dimension hierarchy prototype class.
    """
    def getLevelNames(self):
        """
        List of dimension level names for this hierarchy.
        """
        return list()

    def getLevels(self):
        """
        A list of the dimension levels of this hierarchy.
        """
        return list()
