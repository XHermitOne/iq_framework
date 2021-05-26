#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube measure/fact.
"""

__version__ = (0, 1, 1, 1)


class iqCubeMeasureProto(object):
    """
    OLAP Cube measure/fact prototype class.
    """
    def getFieldName(self):
        """
        An alternate name for a fact field in a cube table,
        If not specified, the object name is used.
        """
        return None

    def getLabel(self):
        """
        The label, if not specified, then the description is taken.
        """
        return None
