#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frame and Dialog manager.
"""

import os
import os.path
import wx

from ...util import file_func
from ...util import global_func
from ...util import res_func
from ...util import log_func

from . import panel_manager
from .. import stored_manager

from . import wxcolour_func

__version__ = (0, 1, 1, 1)


class iqFormManager(panel_manager.iqPanelManager,
                    stored_manager.iqStoredManager):
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
            data = self._getPanelCtrlData()
        return res_func.saveResourcePickle(res_filename, data)

    def loadFormData(self, name=None):
        """
        Load position and size of frame/dialog object.

        :param name: Object name.
            If None then get class name.
        :return: Saved data dictionary.
        """
        if name is None:
            res_filename = self.genCustomDataFilename()
        else:
            res_filename = os.path.join(file_func.getProjectProfilePath(),
                                        name + res_func.PICKLE_RESOURCE_FILE_EXT)
        data = res_func.loadResourcePickle(res_filename)
        self._setPanelCtrlData(data)
        return data

    def isDarkSysTheme(self):
        """
        Checking if the OS system theme is dark.

        :return: True/False.
        """
        return wxcolour_func.isDarkSysTheme()

    def loadPosAndSize(self):
        """
        Load form position and size.
        :return: True/False.
        """
        try:
            login_data = self.loadCustomData()
            if login_data:
                size = login_data.get('size', None)
                if size:
                    self.SetSize(wx.Size(*size))
                position = login_data.get('pos', None)
                if position:
                    self.SetPosition(wx.Point(*position))
                return True
        except:
            log_func.fatal(u'Error load and set form position and size')
        return False

    def savePosAndSize(self, ext_save_data=None):
        """
        Save for position and size.

        :param ext_save_data: Additional data for save as dictionary.
        :return: True/False.
        """
        try:
            data = dict(size=tuple(self.GetSize()),
                        pos=tuple(self.GetPosition()))
            if ext_save_data:
                if isinstance(ext_save_data, dict):
                    data.update(ext_save_data)
                else:
                    log_func.warning(u'Type error additional data for save <%s>' % type(ext_save_data).__class__.__name__)
            return self.saveCustomData(save_data=data)
        except:
            log_func.fatal(u'Error save form position and size')
        return False


class iqDialogManager(iqFormManager):
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
