#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqCubeDimensionProto(object):
    """
    OLAP Cube dimension prototype class.
    """
    def getFieldName(self):
        """
        The name of the dimension field in the cube table.
        """
        return u''

    def getAdditionalAttributes(self):
        """
        List of field names of additional attributes.
        """
        return list()

    def getDetailTableName(self):
        """
        The name of the drill table associated with the cube table field.
        """
        return None

    def getDetailFieldName(self):
        """
        The name of the detail table field by which the link is made.
        """
        return None

    def getLabel(self):
        """
        Dimension label.
        """
        return u''

    def getLevels(self):
        """
        List of dimension level objects.
        """
        return list()

    def getHierarchies(self):
        """
        List of hierarchies of dimension levels.
        """
        return list()

    def findHierarchy(self, hierarchy_name):
        """
        Find a hierarchy object by name.

        :param hierarchy_name: The name of the hierarchy object.
        :return: Hierarchy object, or None if not found.
        """
        finds = [obj for obj in self.getHierarchies() if obj.getName() == hierarchy_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Hierarchy object with name <%s> not found in dimension <%s>' % (hierarchy_name, self.getName()))
        return None

    def findLevel(self, level_name):
        """
        Search for a measurement level object by its name.

        :param level_name: Level name.
        :return: Dimension level object, or None if no object with that name was found.
        """
        finds = [obj for obj in self.getLevels() if obj.getName() == level_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Level object with name <%s> not found in dimension <%s>' % (level_name, self.getName()))
        return None

    def getMapping(self):
        """
        A physical indication of the field to display the measurement.
        """
        return u''
