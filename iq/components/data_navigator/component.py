#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator component.
"""

from ... import object

from . import spc
from . import model_navigator

__version__ = (0, 0, 0, 1)


class iqDataNavigator(object.iqObject, model_navigator.iqModelNavigatorManager):
    """
    Data model navigator component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        model_navigator.iqModelNavigatorManager.__init__(self, *args, **kwargs)


COMPONENT = iqDataNavigator
