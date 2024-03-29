#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <radio_choice_maxi_dialog.py>. 
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

__version__ = (0, 0, 0, 1)

# Maximum items
MAX_ITEM_COUNT = 15


class iqRadioChoiceMaxiDialog(gtk_handler.iqGtkHandler):
    """
    Radio maxi choice dialog class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'radio_choice_maxi_dialog.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='radio_choice_maxi_dialog',  
                                          *args, **kwargs)
                                          
    def init(self, title=None, label=None,
                          choices=(), default=None):
        """
        Init form.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 15 items.
        :param default: Default selection list.
        """
        self.initImages()
        self.initControls(title=title, label=label, choices=choices, default=default)

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self, title=None, label=None,
                          choices=(), default=None):
        """
        Init controls method.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 15 items.
        :param default: Default selection list.
        """
        if title:
            self.getGtkTopObject().set_title(title)

        if label:
            self.getGtkObject('prompt_label').set_value(label)

        if choices:
            choices = choices[:MAX_ITEM_COUNT]
            choice_count = len(choices)
            for i in range(MAX_ITEM_COUNT):
                radio_item_name = 'item%d_radiobutton' % (i + 1)
                if i < choice_count:
                    self.getGtkObject(radio_item_name).set_label(choices[i])
                else:
                    self.getGtkObject(radio_item_name).set_visible(False)

                if default is not None and i == default:
                    self.getGtkObject(radio_item_name).set_active()

    def getValue(self):
        """
        Get selected value.
        """
        value = -1
        for i in range(MAX_ITEM_COUNT):
            radio_item_name = 'item%d_radiobutton' % (i + 1)
            if self.getGtkObject(radio_item_name).get_active():
                value = i
        return value

    def onCancelButtonClicked(self, widget):
        """
        <Cancel> button click handler.
        """
        self.getGtkTopObject().close()

    def onOkButtonClicked(self, widget):
        """
        <OK> button click handler.
        """
        self.getGtkTopObject().close()
