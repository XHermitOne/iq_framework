#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube aggregate component.
"""

from ... import object

from . import spc
from . import cube_aggregate_proto

__version__ = (0, 0, 0, 1)


class iqCubeAggregate(object.iqObject, cube_aggregate_proto.iqCubeAggregateProto):
    """
    OLAP Cube aggregate component.
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

        cube_aggregate_proto.iqCubeAggregateProto.__init__(self)

    def getFunctionName(self):
        """
        Get aggregate function name.
        """
        return self.getAttribute('function')

    def getMeasureName(self):
        """
        Measure/Fact that is being aggregated.
        """
        return self.getAttribute('measure')

    def getExpressionCode(self):
        """
        Get aggregate expression body.
        """
        return self.getAttribute('expression')

    def getLabel(self):
        """
        Aggregate label.
        If not specified, then description is taken.
        If in this case it is not defined, then we take name.
        """
        label = self.getAttribute('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label


COMPONENT = iqCubeAggregate
