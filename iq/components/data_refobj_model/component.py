#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Refrence data object model component.
"""

from ... import object

from . import spc

from .. import data_model

__version__ = (0, 0, 0, 1)


class iqDataRefObjModel(data_model.COMPONENT):
    """
    Reference data object model component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        data_model.COMPONENT.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context, *args, **kwargs)


COMPONENT = iqDataRefObjModel
