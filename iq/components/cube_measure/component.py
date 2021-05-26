#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube measure/fact component.
"""

from ... import object

from . import spc
from . import cube_measure_proto

__version__ = (0, 0, 0, 1)


class iqCubeMeasure(object.iqObject, cube_measure_proto.iqCubeMeasureProto):
    """
    OLAP Cube measure/fact component.
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

        cube_measure_proto.iqCubeMeasureProto.__init__(self)

    def getFieldName(self):
        """
        The name of the fact field in the cube table.
        """
        field_name = self.getAttribute('field_name')
        if not field_name:
            field_name = self.getName()
        return field_name

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


COMPONENT = iqCubeMeasure
