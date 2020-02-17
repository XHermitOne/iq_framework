#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base object class module.
"""

from . import object_context
from ..util import global_func
from ..util import spc_func

__version__ = (0, 0, 0, 1)


class iqObject(object):
    """
    Base object class.
    """
    def __init__(self, parent=None, resource=None, spc=None, context=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param spc: Component specification.
        :param context: Context dictionary.
        :param args:
        :param kwargs:
        """
        self._parent = parent
        self._resource = spc_func.fillResourceBySpc(resource=resource, spc=spc)
        self._context = self.createContext(context)

    def getName(self):
        """
        Object name.
        """
        res = self.getResource()
        if isinstance(res, dict):
            return res.get('name', u'Unknown')
        return u'Unknown'

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

    def getAttribute(self, attribute_name):
        """
        Get attribute from resource.

        :param attribute_name: Attribute name.
        :return: Attribute value.
        """
        value = self._resource.get(attribute_name, None) if self._resource else None
        return value
