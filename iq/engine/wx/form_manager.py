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

from . import wxcolour_func

__version__ = (0, 0, 0, 1)


class iqFormManager(stored_ctrl_manager.iqStoredCtrlManager):
    """
    Frame and dialog manager.
    """
    def saveFormData(self, name=None, data=None):
        """
        Save position and size of frame/dialog object.

        :param name: Object name.
            If None then get class name.
        :param data: Saving data.
            If None then get data from controls.
        :return: True/False.
        """
        if name is None:
            name = self.__class__.__name__

        res_filename = os.path.join(file_func.getProfilePath(),
                                    global_func.getProjectName(),
                                    name)
        if data is None:
            data = self._getCtrlData()
        return res_func.saveResourcePickle(res_filename, data)

    def loadFormData(self, name=None):
        """
        Load position and size of frame/dialog object.

        :param name: Object name.
            If None then get class name.
        :return: Saved data dictionary.
        """
        if name is None:
            name = self.__class__.__name__

        res_filename = os.path.join(file_func.getProfilePath(),
                                    global_func.getProjectName(),
                                    name)
        data = res_func.loadResourcePickle(res_filename)
        return self._setCtrlData(data)

    def isDarkSysTheme(self):
        """
        Checking if the OS system theme is dark.

        :return: True/False.
        """
        return wxcolour_func.isDarkSysTheme()


class iqDialogManager(panel_manager.iqPanelManager,
                      iqFormManager):
    """
    Dialog form manager class.
    """
    setDialogCtrlValue = panel_manager.iqPanelManager.setPanelCtrlValue
    getDialogCtrlValues = panel_manager.iqPanelManager.getPanelCtrlValues
    setDialogCtrlValues = panel_manager.iqPanelManager.setPanelCtrlValues
    clearDialogCtrlValue = panel_manager.iqPanelManager.clearPanelCtrlValue

    getDialogCtrlData = panel_manager.iqPanelManager.getPanelCtrlData
    setDialogCtrlData = panel_manager.iqPanelManager.setPanelCtrlData
    clearDialogData = panel_manager.iqPanelManager.clearPanelData

    setDialogAccord = panel_manager.iqPanelManager.setPanelAccord
    addDialogAccord = panel_manager.iqPanelManager.addPanelAccord
    getDialogAccord = panel_manager.iqPanelManager.getPanelAccord
    getDialogAccordCtrlData = panel_manager.iqPanelManager.getPanelAccordCtrlData
    setDialogAccordCtrlData = panel_manager.iqPanelManager.setPanelAccordCtrlData
    findDialogAccord = panel_manager.iqPanelManager.findPanelAccord
