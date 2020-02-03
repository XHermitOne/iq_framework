#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frame and Dialog manager.
"""

import os
import os.path

from ...util import file_func
from ...util import global_func
from ...util import res_func

from . import panel_manager
from .. import stored_ctrl_manager


__version__ = (0, 0, 0, 1)


class iqFormManager(stored_ctrl_manager.iqStoredCtrlManager):
    """
    Frame and dialog manager.
    """
    def saveFormData(self):
        """
        Save position and size of frame/dialog object.

        :return: True/False.
        """
        res_filename = os.path.join(file_func.getProfilePath(),
                                    global_func.getProjectName(),
                                    self.__class__.__name__)
        data = self._getCtrlData()
        return res_func.saveResourcePickle(res_filename, data)

    def loadFormData(self):
        """
        Load position and size of frame/dialog object.

        :return: True/False.
        """
        res_filename = os.path.join(file_func.getProfilePath(),
                                    global_func.getProjectName(),
                                    self.__class__.__name__)
        data = res_func.loadResourcePickle(res_filename)
        return self._setCtrlData(data)
