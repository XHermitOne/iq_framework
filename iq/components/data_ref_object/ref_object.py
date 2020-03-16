#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object manager.
"""

# import sqlalchemy

from ..data_navigator import model_navigator

# from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqRefObjectManager(model_navigator.iqModelNavigatorManager):
    """
    Reference data object manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        model_navigator.iqModelNavigatorManager.__init__(self, model=model)
