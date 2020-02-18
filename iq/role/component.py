#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Role component.
"""

from .. import object

from . import spc

__version__ = (0, 0, 0, 1)


class iqRole(object.iqObject):
    """
    Role component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)


COMPONENT = iqRole
