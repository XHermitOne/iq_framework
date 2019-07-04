#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kernel - general dispatcher of all program objects.
"""

__version__ = (0, 0, 0, 1)


class iqKernel(object):
    """
    Kernel - general dispatcher of all program objects.
    """
    def __init__(self):
        """
        Constructor.
        """
        # Program object cache
        self._object_cache = dict()
