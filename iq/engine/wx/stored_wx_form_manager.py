#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manager for storing properties of wxPython forms.
"""

import wx

from .. import stored_ctrl_manager

__version__ = (0, 0, 0, 1)


class iqStoredWxFormsManager(stored_ctrl_manager.iqStoredCtrlManager):
    """
    Manager for storing properties of wxPython forms.
    """
    def loadCustomProperties(self, save_filename=None):
        """
        Загрузить пользовательские данные.

        :param save_filename: Stored file name.
        :return: True/False.
        """
        var_data = self.loadCustomData(save_filename=save_filename)
        if var_data:
            width = var_data.get('width', -1)
            height = var_data.get('height', -1)
            if width > 0 and height > 0:
                self.SetSize(wx.Size(width, height))

            x = var_data.get('x', -1)
            y = var_data.get('y', -1)
            if x <= 0 and y <= 0:
                if hasattr(self, 'Centre'):
                    self.Centre()
            else:
                self.SetPosition(wx.Point(x, y))

            return True
        return False

    def saveCustomProperties(self, save_filename=None):
        """
        Сохранить пользовательские данные.

        :param save_filename: Stored file name.
        :return: True/False.
        """
        size = self.GetSize()
        width = size.GetWidth()
        height = size.GetHeight()
        pos = self.GetPosition()

        res = dict(width=width, height=height,
                   x=pos.x, y=pos.y)

        return self.saveCustomData(save_filename=save_filename, save_data=res)
