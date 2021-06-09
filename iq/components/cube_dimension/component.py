#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension component.
"""

from ... import object

from . import spc
from . import cube_dimension_proto

from ..cube_dimension_level import cube_dimension_level_proto
from ..cube_dimension_hierarchy import cube_dimension_hierarchy_proto

__version__ = (0, 0, 0, 1)


class iqCubeDimension(object.iqObject, cube_dimension_proto.iqCubeDimensionProto):
    """
    OLAP Cube dimension component.
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

        cube_dimension_proto.iqCubeDimensionProto.__init__(self)

        self.createChildren()

    def getFieldName(self):
        """
        The name of the dimension field in the cube table.
        """
        field_name = self.getAttribute('field_name')
        if not field_name:
            field_name = self.getName()
        return field_name

    def getMapping(self):
        """
        A physical indication of the field to display the measurement.
        """
        return self.getAttribute('mapping')

    def getAdditionalAttributes(self):
        """
        List of field names of additional attributes.
        """
        attributes = self.getAttribute('attributes')
        return [attribute for attribute in attributes if attribute] if attributes else list()

    def getDetailTableName(self):
        """
        The name of the drill table associated with the cube table field.
        """
        detail_tabname = self.getAttribute('detail_tabname')
        return detail_tabname if detail_tabname else self.getName()

    def getDetailFieldName(self):
        """
        The name of the detail table field by which the link is made.
        """
        return self.getAttribute('detail_fldname')

    def getLabel(self):
        """
        Dimension label.
        If not specified, then description is taken.
        If in this case it is not defined, then we take name.
        """
        label = self.getAttribute('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

    def getLevels(self):
        """
        List of dimension level objects.
        """
        return [child for child in self.getChildren() if isinstance(child, cube_dimension_level_proto.iqCubeDimensionLevelProto)]

    def getHierarchies(self):
        """
        List of hierarchies of dimension levels.
        """
        return [child for child in self.getChildren() if isinstance(child, cube_dimension_hierarchy_proto.iqCubeDimensionHierarchyProto)]


COMPONENT = iqCubeDimension
