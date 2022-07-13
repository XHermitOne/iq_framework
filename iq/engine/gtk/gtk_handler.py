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
from ...util import lang_func

from ...editor.gtk.code_generator import gui_generator

__version__ = (0, 0, 1, 1)

_ = lang_func.getTranslation().gettext


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
        # Set translation domain
        self.gtk_builder.set_translation_domain(lang_func.TEXT_DOMAIN)
        if self.gtk_builder:
            if add_from_glade_file:
                self.gtk_builder.add_from_file(glade_filename)
                if top_object_name:
                    self.gtk_top_object = self.gtk_builder.get_object(top_object_name)
            self.gtk_builder.connect_signals(self)

        # CSS file
        self.gtk_css_provider = None
        self.gtk_style_context = None
        css_filename = gui_generator.getGladeProjectCSSFilename(glade_filename)
        if css_filename:
            if os.path.exists(css_filename):
                log_func.info(u'GtkHandler. Load CSS file <%s>' % css_filename)
                self.gtk_css_provider = gi.repository.Gtk.CssProvider()
                self.gtk_css_provider.load_from_path(css_filename)
                self.gtk_style_context = gi.repository.Gtk.StyleContext()
                self.gtk_style_context.add_provider_for_screen(gi.repository.Gdk.Screen.get_default(),
                                                               self.gtk_css_provider,
                                                               gi.repository.Gtk.STYLE_PROVIDER_PRIORITY_USER)
            else:
                log_func.warning(u'GtkHandler. CSS file <%s> not found' % css_filename)

    def getGtkBuilder(self):
        """
        Get Gtk builder.
        """
        return self.gtk_builder

    def getGtkCSSProvider(self):
        """
        Get CSS provider.
        """
        return self.gtk_css_provider

    def getGtkStyleContext(self):
        """
        Get Gtk style context.
        """
        return self.gtk_style_context

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
