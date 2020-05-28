#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx widget abstract component.
"""

from ... import object

from . import spc

__version__ = (0, 0, 0, 1)


class iqWxWidget(object.iqObject):
    """
    Wx widget abstract component.
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

    def getPosition(self):
        """
        Panel position.
        """
        return self.getAttribute('position')

    def getSize(self):
        """
        Panel size.
        """
        return self.getAttribute('size')

    def getStyle(self):
        """
        Panel style.
        """
        return self.getAttribute('style')

    def getForegroundColour(self):
        """
        Panel foreground colour.
        """
        return self.getAttribute('foreground_colour')

    def getBackgroundColour(self):
        """
        Panel background colour.
        """
        return self.getAttribute('background_colour')


COMPONENT = iqWxWidget
