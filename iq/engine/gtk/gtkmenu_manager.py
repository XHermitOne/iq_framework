#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkMenu manager.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func

from . import base_manager

__version__ = (0, 0, 0, 1)

class iqGtkMenuManager(base_manager.iqBaseManager):
    """
    GtkMenu manager.
    """
    def findGtkMenuMenuItemByName(self, menu=None, menuitem_name=None):
        """
        Find child menuitem by name. Ыearch is performed recursively.

        :param menu: GtkMenu object.
        :param menuitem_name: GtkMenuItem name.
        :return: GtkMenuItem object or None if it not found.
        """
        assert issubclass(menu.__class__, gi.repository.Gtk.Menu), u'GtkMenu manager type error'

        try:
            child_menuitems = menu.get_children()
            for child_menuitem in child_menuitems:
                if issubclass(child_menuitem.__class__, gi.repository.Gtk.MenuItem):
                    if child_menuitem.get_name() == menuitem_name:
                        return child_menuitem
                elif issubclass(child_menuitem.__class__, gi.repository.Gtk.Menu):
                    result = self.findGtkMenuMenuItemByName(menu=child_menuitem, menuitem_name=menuitem_name)
                    if result is not None:
                        return result
                else:
                    log_func.warning(u'Find menuitem not supported for Gtk object <%s>' % child_menuitem.__class__.__name__)
        except:
            log_func.fatal(u'Error find child menuitem by name in menu <%s>' % menu.get_name())
        return None