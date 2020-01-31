#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base object class module.
"""

from . import object_context
from ..util import global_func

__version__ = (0, 0, 0, 1)


class iqObjectProto(object):
    """
    Base object class.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        :param args:
        :param kwargs:
        """
        self._parent = parent
        self._resource = resource
        self._context = self.createContext(context)

    def getParent(self):
        """
        Get parent object.
        """
        return self._parent

    def getResource(self):
        """
        Get object resource dictionary.
        """
        return self._resource

    def getContext(self):
        """
        Get context object.
        """
        return self._context

    def createContext(self, context=None):
        """
        Create object context.

        :param context: Context dictionary.
        :return: Context.
        """
        self._context = None
        if context is None:
            self._context = object_context.iqContext(runtime_object=self)
        elif isinstance(context, dict):
            self._context = object_context.iqContext(runtime_object=self)
            self._context.update(context)
        elif isinstance(context, object_context.iqContext):
            self._context = context
        return self._context

    def getKernel(self):
        """
        Get kernel object.
        """
        return self._context.getKernel() if self._context else global_func.getKernel()
