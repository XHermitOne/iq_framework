#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model component.
"""

from ... import object

from . import spc
from . import model

__version__ = (0, 0, 0, 1)


class iqDataModel(model.iqModelManager, object.iqObject):
    """
    Data model component.
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
        model.iqModelManager.__init__(self)

        self.createChildren()


COMPONENT = iqDataModel
