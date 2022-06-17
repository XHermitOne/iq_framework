#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkBox manager.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func
# from ...util import spc_func
# from ...util import id_func

from . import base_manager

__version__ = (0, 0, 0, 1)


class iqGtkBoxManager(base_manager.iqBaseManager):
    """
    GtkBox manager.
    """

    def clearGtkBox(self, box=None):
        """
        Clear GtkBox.

        :param box: GtkBox object.
        :return: True/False.
        """
        assert issubclass(box.__class__, gi.repository.Gtk.Box), u'GtkBox manager type error'

        try:
            for child in box.get_children():
                box.remove(child)
                child.destroy()
            return True
        except:
            log_func.fatal(u'Error clear box <%s>' % box.get_name())
        return False
