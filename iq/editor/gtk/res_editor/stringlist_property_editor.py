#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <property_box.py>. 
Generated by the iqFramework module the Glade prototype.
"""

import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func

from iq.engine.gtk import gtk_handler
# from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

from . import property_editor_proto

from . import edit_stringlist_dialog

__version__ = (0, 0, 0, 1)

STRING_DELIMETER = ', '


class iqStringListPropertyEditor(gtk_handler.iqGtkHandler,
                                 property_editor_proto.iqPropertyEditorProto):
    """
    String list property editor class.
    """
    def __init__(self, label='', value=None, choices=None, default=None, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'stringlist_property_editor.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='property_box',  
                                          *args, **kwargs)

        property_editor_proto.iqPropertyEditorProto.__init__(self, label=label, value=value,
                                                             choices=choices, default=default)

        if label:
            self.getGtkObject('property_label').set_text(label)
        if value:
            self.setValue(value)

    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass

    def onPropertyIconPress(self, widget, icon, event):
        """
        Property edit icon mouse click handler.
        """
        if icon.value_name == 'GTK_ENTRY_ICON_SECONDARY':
            result = edit_stringlist_dialog.editStringlistDialog(string_list=self.value)
            self.value = result
            self.setValue(self.value)

    def setValue(self, value):
        """
        Set property editor value.
        """
        if isinstance(value, (list, tuple)):
            value = STRING_DELIMETER.join([str(value_item) for value_item in value])
        else:
            value = u''

        self.getGtkObject('property_entry').set_text(value)

    def setHelpString(self, help_string):
        """
        Set help string.

        :param help_string: Help string.
        """
        label = self.getGtkObject('property_label')
        label.set_property('tooltip-text', help_string)
