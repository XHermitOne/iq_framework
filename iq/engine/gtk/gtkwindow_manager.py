#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkWindow manager.
"""

import os.path
import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func
# from ...util import spc_func

from . import base_manager

__version__ = (0, 0, 1, 1)


class iqGtkWindowManager(base_manager.iqBaseManager):
    """
    GtkWindow manager.
    """
    def setGtkWindowIcon(self, window=None, icon_filename=None, icon_size=(16, 16)):
        """
        Set dialog icon.

        :param window: GtkWindow object.
        :param icon_filename: Icon filename.
        :param icon_size: Icon size (width, height).
        :return: True/False.
        """
        if window is None and issubclass(self.__class__, gi.repository.Gtk.Window):
            window = self

        assert issubclass(window.__class__, gi.repository.Gtk.Window), u'GtkWindow manager type error'

        try:
            if os.path.exists(icon_filename):
                icon_width, icon_height = icon_size
                pixbuf16 = gi.repository.GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_filename,
                                                                                 icon_width, icon_height, False)
                window.set_icon(pixbuf16)
            else:
                log_func.warning(u'Window icon file <%s> not found' % icon_filename)

            return True
        except:
            log_func.fatal(u'Error set icon for window <%s>' % window.get_name())
        return False
