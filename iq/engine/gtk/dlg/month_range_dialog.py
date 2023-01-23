#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <month_range_dialog.py>. 
Generated by the iqFramework module the Glade prototype.
"""

import datetime
import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func
from iq.util import dt_func

from iq.engine.gtk import gtk_handler
# from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

__version__ = (0, 0, 0, 1)


class iqMonthRangeDialog(gtk_handler.iqGtkHandler):
    """
    Unknown class.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'month_range_dialog.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='month_range_dialog',  
                                          *args, **kwargs)
                                          
    def init(self, title=None, default_from_year=None, default_from_month=None,
             default_to_year=None, default_to_month=None):
        """
        Init form.

        :param title: Dialog title.
        :param default_from_year: Default from year.
        :param default_from_month: Default from month.
        :param default_to_year: Default to year.
        :param default_to_month: Default to month.
        """
        self.initImages()
        self.initControls(title=title,
                          default_from_year=default_from_year,
                          default_from_month=default_from_month,
                          default_to_year=default_to_year,
                          default_to_month=default_to_month)

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self, title=None, default_from_year=None, default_from_month=None,
                     default_to_year=None, default_to_month=None):
        """
        Init controls method.

        :param title: Dialog title.
        :param default_from_year: Default from year.
        :param default_from_month: Default from month.
        :param default_to_year: Default to year.
        :param default_to_month: Default to month.
        """
        if title:
            self.getGtkTopObject().set_title(title)

        cur_year = datetime.date.today().year
        cur_month = datetime.date.today().month

        self.getGtkObject('from_year_spinbutton').set_range(datetime.date.min.year,
                                                            datetime.date.max.year)
        if default_from_year:
            self.getGtkObject('from_year_spinbutton').set_value(default_from_year)
        else:
            self.getGtkObject('from_year_spinbutton').set_value(cur_year)

        for month_name in dt_func.RU_MONTHS:
            model = self.getGtkObject('from_month_combobox').get_model()
            model.append([month_name])

        if default_from_month:
            self.getGtkObject('from_month_combobox').set_active(default_from_month - 1)
        else:
            self.getGtkObject('from_month_combobox').set_active(cur_month - 1)

        self.getGtkObject('to_year_spinbutton').set_range(datetime.date.min.year,
                                                          datetime.date.max.year)
        if default_to_year:
            self.getGtkObject('to_year_spinbutton').set_value(default_to_year)
        else:
            self.getGtkObject('to_year_spinbutton').set_value(cur_year)

        for month_name in dt_func.RU_MONTHS:
            model = self.getGtkObject('to_month_combobox').get_model()
            model.append([month_name])

        if default_to_month:
            self.getGtkObject('to_month_combobox').set_active(default_to_month - 1)
        else:
            self.getGtkObject('to_month_combobox').set_active(cur_month - 1)

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