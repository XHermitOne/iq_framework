#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model manager.
"""

from . import data_object

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqModelManager(data_object.iqDataObject):
    """
    Data model manager.
    """
    def getScheme(self):
        """
        Get scheme object.

        :return:
        """
        log_func.warning(u'Not define method <getScheme> in <%s>' % self.__class__.__name__)
        return None

    def getModel(self):
        """
        Get model.
        """
        log_func.warning(u'Not define method <getModel> in <%s>' % self.__class__.__name__)
        return None
