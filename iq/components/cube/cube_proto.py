#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqCubeProto(object):
    """
    OLAP Cube prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # Alternative name of the cube table in the database,
        # if not specified, then the name of the cube is used
        self._table_name = None

    def getDimensions(self):
        """
        Dimension objects list.
        """
        return list()

    def getMeasures(self):
        """
        Measure objects list .
        """
        return list()

    def getAggregates(self):
        """
        List of objects of aggregation functions.
        """
        return list()

    def findDimension(self, dimension_name):
        """
        Search for a dimension object by its name.

        :return: Dimension object or None, if an object with the same name is not found.
        """
        finds = [obj for obj in self.getDimensions() if obj.getName() == dimension_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Dimension with name <%s> not found in cube <%s>' % (dimension_name, self.getName()))
        return None

    def findMeasure(self, measure_name):
        """
        Search for a measure/fact object by its name.

        :return: Measure object or None, if an object with the same name is not found.
        """
        finds = [obj for obj in self.getMeasures() if obj.getName() == measure_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Measure with name <%s> not found in cube <%s>' % (measure_name, self.getName()))
        return None

    def findAggregate(self, aggregate_name):
        """
        Search for an aggregation function object by its name.

        :return: Aggregation function object or None, if an object with the same name is not found.
        """
        finds = [obj for obj in self.getAggregates() if obj.getName() == aggregate_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Aggregation function with name <%s> not found in cube <%s>' % (aggregate_name, self.getName()))
        return None

    def getLabel(self):
        """
        Label. If not defined then get description.
        """
        return None

    def getChildren(self):
        """
        List of children.
        """
        return list()

    def findChild(self, child_name):
        """
        Search for a child object by name.

        :param child_name: The name of the child.
        :return: Child object or None, if an object with the same name is not found.
        """
        finds = [obj for obj in self.getChildren() if obj.getName() == child_name]
        if finds:
            return finds[0]
        else:
            log_func.warning(u'Object <%s> not found in cube <%s>' % (child_name, self.getName()))
        return None
