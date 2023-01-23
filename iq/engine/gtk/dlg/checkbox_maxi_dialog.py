#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <checkbox_maxi_dialog.py>. 
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

MAX_ITEM_COUNT = 15


class iqCheckboxMaxiDialog(gtk_handler.iqGtkHandler):
    """
    CheckBox maxi items dialog class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'checkbox_maxi_dialog.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='checkbox_maxi_dialog',  
                                          *args, **kwargs)

        self._check_item_count = MAX_ITEM_COUNT

    def init(self, title=None, label=None, choices=(), defaults=()):
        """
        Init form.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 15 items.
        :param defaults: Default selection list.
        """
        self.initImages()
        self.initControls(title=title, label=label, choices=choices, defaults=defaults)

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self, title=None, label=None, choices=(), defaults=()):
        """
        Init controls method.

        :param title: Dialog title.
        :param label: Prompt text.
        :param choices: Choice list.
            Maximum 15 items.
        :param defaults: Default selection list.
        """
        if title:
            self.getGtkTopObject().set_title(title)

        if label:
            self.getGtkObject('prompt_label').set_value(label)

        if choices:
            choices = choices[:MAX_ITEM_COUNT]
            self._check_item_count = len(choices)
            for i in range(MAX_ITEM_COUNT):
                checkbox_item_name = 'item%d_checkbutton' % (i + 1)
                if i < self._check_item_count:
                    self.getGtkObject(checkbox_item_name).set_label(choices[i])
                    if defaults and i < len(defaults):
                        checked = defaults[i]
                        self.getGtkObject(checkbox_item_name).set_active(checked)
                else:
                    self.getGtkObject(checkbox_item_name).set_visible(False)

                if defaults and i < len(defaults):
                    self.getGtkObject(checkbox_item_name).set_active(defaults[i])

    def getValue(self):
        """
        Get checked items.

        :return: Checked items tuple or None if canceled.
            For example: (False, True, True, False).
        """
        return self.getCheckedList()

    def getCheckedList(self):
        """
        Get checked list.

        :return: Checked items tuple.
            For example: (False, True, True, False).
        """
        result = list()
        for i in range(MAX_ITEM_COUNT):
            checkbox_item_name = 'item%d_checkbutton' % (i + 1)
            if i < self._check_item_count:
                checked = self.getGtkObject(checkbox_item_name).get_active()
                result.append(checked)
            else:
                break
        return tuple(result)

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
