#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data wide history manager.
"""

from ..data_navigator import model_navigator

__version__ = (0, 0, 0, 1)


class iqWideHistoryManager(model_navigator.iqModelNavigatorManager):
    """
    Data wide history manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        model_navigator.iqModelNavigatorManager.__init__(self, model=model)
