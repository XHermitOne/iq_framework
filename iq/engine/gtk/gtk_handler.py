#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Gtk handler.
"""

import os.path
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqGtkHandler(object):
    """
    Base Gtk handler.
    """
    def __init__(self, glade_filename=None, top_object_name=None):
        """
        Constructor.

        :param glade_filename: Glade project filename.
        :param top_object_name: Top Gtk object name.
        """
        add_from_glade_file = True
        if not glade_filename:
            log_func.warning(u'Not define Glade project filename for Gtk handler')
            add_from_glade_file = False
        else:
            glade_filename = os.path.realpath(glade_filename)
            if not os.path.exists(glade_filename):
                log_func.warning(u'Glade project filename <%s> not found for Gtk handler' % glade_filename)
                add_from_glade_file = False

        # Top Gtk object
        self.gtk_top_object = None

        # Builder object
        self.gtk_builder = gi.repository.Gtk.Builder()
        if self.gtk_builder:
            if add_from_glade_file:
                self.gtk_builder.add_from_file(glade_filename)
                if top_object_name:
                    self.gtk_top_object = self.gtk_builder.get_object(top_object_name)
            self.gtk_builder.connect_signals(self)

    def getGtkBuilder(self):
        """
        Get Gtk builder.
        """
        return self.gtk_builder

    def getGtkTopObject(self):
        """
        Get top Gtk object.
        """
        return self.gtk_top_object

    def setGtkTopObject(self, gtk_object):
        """
        Set top Gtk object.

        :param gtk_object: Gtk object.
        """
        self.gtk_top_object = gtk_object

    def getGtkObject(self, gtk_object_name):
        """
        Get Gtk object by name.

        :param gtk_object_name: Gtk object name.
        :return: Gtk object on None if it not found.
        """
        builder = self.getGtkBuilder()
        return builder.get_object(gtk_object_name) if builder else None
