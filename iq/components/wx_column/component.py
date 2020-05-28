#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx column component.
"""

from ... import object

from . import spc

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqWxColumn(object.iqObject):
    """
    Wx column component.
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

    def getLabel(self):
        """
        Column label.
        """
        return self.getAttribute('label')

    def getWidth(self):
        """
        Column width.
        """
        return self.getAttribute('width')

    def getBackgroundColour(self):
        """
        Column background colour.
        """
        return self.getAttribute('background_colour')

    def getForegroundColour(self):
        """
        Column text colour.
        """
        return self.getAttribute('foreground_colour')

    def getFont(self):
        """
        Column label font.
        """
        return self.getAttribute('font')

    def getAlignment(self):
        """
        Column text alignment.
        """
        return self.getAttribute('align')

    def isSort(self):
        """
        Sort column?.
        """
        return self.getAttribute('sort')

    def getDataName(self):
        """
        Get data column name.
        """
        data_name = self.getAttribute('data_name')
        return data_name if data_name else self.getName()


COMPONENT = iqWxColumn
