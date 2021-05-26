#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension level.
"""

__version__ = (0, 0, 0, 1)


class iqCubeDimensionLevelProto(object):
    """
    OLAP Cube dimension level prototype class.
    """
    def getAdditionalAttributes(self):
        """
        List of field names of additional attributes.
        """
        return list()

    def getLabel(self):
        """
        Dimension level label.
        """
        return u''

    def getLabelAttribute(self):
        """
        Label attribute. Indicates which attribute will be displayed in the user interface.
        """
        return None

    def getMapping(self):
        """
        A physical indication of the field to display the level.
        """
        return u''
