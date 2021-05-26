#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP Cube dimension level component.
"""

from ... import object

from . import spc
from . import cube_dimension_level_proto

from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqCubeDimensionLevel(object.iqObject,
                           cube_dimension_level_proto.iqCubeDimensionLevelProto):
    """
    OLAP Cube dimension level component.
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

        cube_dimension_level_proto.iqCubeDimensionLevelProto.__init__(self)

    def getAdditionalAttributes(self):
        """
        List of field names of additional attributes.
        """
        attributes = self.getAttribute('attributes')
        return [attribute for attribute in attributes if attribute] if attributes else list()

    def getKey(self):
        """
        Key. Indicates which attribute will be used for filtering.
        """
        return self.getAttribute('key')

    def getLabelAttribute(self):
        """
        Label attribute. Indicates which attribute will be displayed in the user interface.
        """
        return self.getAttribute('label_attribute')

    def getLabel(self):
        """
        Dimension level label.
        If not specified, then description is taken.
        If in this case it is not defined, then we take name.
        """
        label = self.getAttribute('label')
        if not label:
            label = self.getDescription()
        if not label:
            label = self.getName()
        return label

    def getMapping(self):
        """
        A physical indication of the field to display the level.
        """
        return self.getAttribute('mapping')

    def getNormal(self):
        """
        Level data normalization function.
        """
        if self.isAttributeValue('get_normal'):
            context = self.getContext()
            function_body = self.getAttribute('get_normal')
            return exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)
        return None


COMPONENT = iqCubeDimensionLevel
