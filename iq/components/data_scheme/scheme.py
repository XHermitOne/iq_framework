#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme manager.
"""

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqSchemeManager(object):
    """
    Data scheme manager.
    """
    def getDBEngine(self):
        """
        Get database engine.

        :return:
        """
        return None

    def genModule(self, module_filename=None):
        """
        Generate scheme module.

        :param module_filename: Module filename.
            If None then open file dialog.
        :return: New module filename or None if error.
        """
        try:
            pass
        except:
            log_func.fatal(u'Generate scheme module error')
        return None
