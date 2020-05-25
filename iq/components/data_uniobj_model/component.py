#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object model component.
"""

from ... import object

from . import spc

from .. import data_model

__version__ = (0, 0, 0, 1)


class iqDataUniObjModel(data_model.COMPONENT):
    """
    Unique data object model component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        data_model.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context, *args, **kwargs)


COMPONENT = iqDataUniObjModel
