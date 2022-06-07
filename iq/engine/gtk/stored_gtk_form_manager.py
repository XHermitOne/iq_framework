#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manager for storing properties of GTK forms.
"""

import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from .. import stored_ctrl_manager

__version__ = (0, 0, 1, 1)


class iqStoredGtkFormsManager(stored_ctrl_manager.iqStoredCtrlManager):
    """
    Manager for storing properties of GTK forms.
    """
    def loadCustomProperties(self, save_filename=None):
        """
        Load custom properties.

        :param save_filename: Stored file name.
        :return: True/False.
        """
        var_data = self.loadCustomData(save_filename=save_filename)
        if var_data:
            width = var_data.get('width', -1)
            height = var_data.get('height', -1)
            if width > 0 and height > 0:
                self.getGtkTopObject().resize(width, height)

            x = var_data.get('x', -1)
            y = var_data.get('y', -1)
            if x <= 0 and y <= 0:
                self.getGtkTopObject().set_position(gi.repository.Gtk.WindowPosition.CENTER)
            else:
                self.getGtkTopObject().move(x, y)

            return True
        return False

    def saveCustomProperties(self, save_filename=None):
        """
        Save custom properties.

        :param save_filename: Stored file name.
        :return: True/False.
        """
        size = self.getGtkTopObject().get_size()
        width = size[0]
        height = size[1]
        pos = self.getGtkTopObject().get_position()

        res = dict(width=width, height=height, x=pos[0], y=pos[1])

        return self.saveCustomData(save_filename=save_filename, save_data=res)
