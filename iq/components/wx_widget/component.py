#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx widget abstract component.
"""

from ... import object

from . import spc

from ...util import log_func

__version__ = (0, 0, 1, 1)


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

    def findCtrlInParentsByName(self, ctrl_name, parent=None):
        """
        Find control in parents by name.

        :param ctrl_name: Control name.
        :param parent: Current parent control.
        :return: Control or None if control not found.
        """
        if parent is None:
            parent = self

        try:
            if hasattr(parent, ctrl_name):
                return getattr(parent, ctrl_name)
            else:
                parent = parent.GetParent() if hasattr(parent, 'GetParent') else None
                if parent:
                    return self.findCtrlInParentsByName(ctrl_name=ctrl_name, parent=parent)
        except:
            log_func.fatal(u'Error find control <%s>' % ctrl_name)
        return None


COMPONENT = iqWxWidget
