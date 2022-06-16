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

__version__ = (0, 0, 0, 1)


class iqScriptPropertyEditor(gtk_handler.iqGtkHandler,
                             property_editor_proto.iqPropertyEditorProto):
    """
    Script property editor class.
    """
    def __init__(self, label='', value=None, choices=None, default=None, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'script_property_editor.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='property_box',  
                                          *args, **kwargs)

        property_editor_proto.iqPropertyEditorProto.__init__(self, label=label, value=value,
                                                             choices=choices, default=default)

        if label:
            self.getGtkObject('property_label').set_text(label)
        if value:
            self.getGtkObject('property_entry').set_text(value)

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

    def onPropertyIconPress(self, widget):
        """
        """
        pass


def openPropertyBox():
    """
    Open property_box.

    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iqPropertyBox()
        obj.init()
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <property_box>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    
