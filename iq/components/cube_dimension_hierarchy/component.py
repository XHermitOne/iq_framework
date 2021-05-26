#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension hierarchy component.
"""

from ... import object

from . import spc
from . import cube_dimension_hierarchy_proto

__version__ = (0, 0, 0, 1)


class iqCubeDimensionHierarchy(object.iqObject,
                               cube_dimension_hierarchy_proto.iqCubeDimensionHierarchyProto):
    """
    OLAP Cube dimension hierarchy component.
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

        cube_dimension_hierarchy_proto.iqCubeDimensionHierarchyProto.__init__(self)

    def getLevelNames(self):
        """
        List of field names of additional attributes.
        """
        level_names = self.getAttribute('levels')
        return level_names if level_names else list()


COMPONENT = iqCubeDimensionHierarchy
