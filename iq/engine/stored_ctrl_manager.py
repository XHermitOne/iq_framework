#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manager for storing properties of controls.
"""

from ..util import log_func
from ..util import res_func


__version__ = (0, 0, 0, 1)


class iqStoredCtrlManager(object):
    """
    Manager for storing properties of controls.
    """
    def saveCustomData(self, save_filename, save_data=None):
        """
        Save custom data.

        :param save_filename: Stored file name.
        :param save_data: Stored data.
        :return: True/False.
        """
        if save_filename:
            return res_func.saveResourcePickle(save_filename, save_data)
        else:
            log_func.warning(u'File for store custom data not defined')
        return False

    def loadCustomData(self, save_filename):
        """
        Load custom data from file.

        :param save_filename: Stored file name.
        :return: Stored data or None if error.
        """
        if save_filename:
            # Просто записать в файл
            return res_func.loadResourcePickle(save_filename)
        else:
            log_func.warning(u'File for store custom data not defined')
        return None
