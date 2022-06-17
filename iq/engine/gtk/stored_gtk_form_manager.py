#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manager for storing properties of GTK forms.
"""

import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from .. import stored_ctrl_manager

from ...util import log_func

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
        if save_filename is None:
            save_filename = self.genCustomDataFilename()
        log_func.debug(u'Load from file <%s>' % save_filename)
        var_data = self.loadCustomData(save_filename=save_filename)
        if var_data:
            width = var_data.get('width', -1)
            height = var_data.get('height', -1)
            if width > 0 and height > 0:
                log_func.debug(u'Set window size <%s x %s>' % (width, height))
                self.getGtkTopObject().resize(width, height)

            x = var_data.get('x', -1)
            y = var_data.get('y', -1)
            if x <= 0 and y <= 0:
                log_func.debug(u'Set window center position <%s x %s>' % (x, y))
                self.getGtkTopObject().set_position(gi.repository.Gtk.WindowPosition.CENTER)
            else:
                log_func.debug(u'Set window position <%s x %s>' % (x, y))
                self.getGtkTopObject().move(x, y)

            return True
        return False

    def saveCustomProperties(self, save_filename=None):
        """
        Save custom properties.

        :param save_filename: Stored file name.
        :return: True/False.
        """
        if save_filename is None:
            save_filename = self.genCustomDataFilename()

        size = self.getGtkTopObject().get_size()
        width = size[0]
        height = size[1]
        pos = self.getGtkTopObject().get_position()

        res = dict(width=width, height=height, x=pos[0], y=pos[1])
        log_func.debug(u'Save to file <%s>' % save_filename)
        log_func.debug(u'Save window size and position <%s %s %s>' % (size, pos, str(res)))

        return self.saveCustomData(save_filename=save_filename, save_data=res)
