#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data wide history component.
"""

from ...components import data_navigator

from . import spc
from . import wide_history

__version__ = (0, 0, 0, 1)


class iqDataWideHistory(data_navigator.COMPONENT, wide_history.iqWideHistoryManager):
    """
    Data wide history component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        data_navigator.COMPONENT.__init__(self, parent=parent, resource=resource, context=context)
        wide_history.iqWideHistoryManager.__init__(self, *args, **kwargs)


COMPONENT = iqDataWideHistory
