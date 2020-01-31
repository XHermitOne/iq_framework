#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Context object class module.
"""

from ..util import global_func


class context_dict(dict):
    """
    Empty class dictionary.
    """


class iqContext(context_dict):
    """
    Context object class.
    """
    def __init__(self, runtime_object=None, kernel=None, **kwargs):
        """
        Constructor.

        :param runtime_object: Object.
        :param kernel: Kernel object.
        """
        context_dict.__init__(self, **kwargs)

        self._object = runtime_object
        self._kernel = kernel if kernel else global_func.getKernel()

    def getObject(self):
        """
        Get object of context.
        """
        return self._object

    def getKernel(self):
        """
        Get kernel object.
        """
        return self._kernel

    def init(self):
        """
        Init context.
        """
        pass
