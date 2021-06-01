#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube component.
"""

from ... import object

from . import spc
from . import cube_proto

from ..cube_aggregate import cube_aggregate_proto
from ..cube_measure import cube_measure_proto

__version__ = (0, 0, 0, 1)


class iqCube(object.iqObject, cube_proto.iqCubeProto):
    """
    OLAP Cube component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        cube_proto.iqCubeProto.__init__(self)

        self.createChildren()

    def getTableName(self):
        """
        Get cube table name.
        """
        table_name = self.getAttribute('table_name')
        if not table_name:
            table_name = self.getName()
        return table_name

    def getDimensions(self):
        """
        Get dimension object list.
        """
        return [child for child in self.getChildren() if isinstance(child, cube_dimension_proto.iqCubeDimensionProto)]

    def getMeasures(self):
        """
        Get measure/fact object list.
        """
        return [child for child in self.getChildren() if isinstance(child, cube_measure_proto.iqCubeMeasureProto)]

    def getAggregates(self):
        """
        Get aggregate function object list.
        """
        return [child for child in self.getChildren() if isinstance(child, cube_aggregate_proto.iqCubeAggregateProto)]

    def getLabel(self):
        """
        The label, if not specified, then the description is taken.
        If in this case it is not defined, then we take name.
        """
        label = self.getAttribute('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label


COMPONENT = iqCube