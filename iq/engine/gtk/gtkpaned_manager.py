#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkPaned manager.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func
from ...util import spc_func
from ...util import id_func

from . import base_manager

__version__ = (0, 0, 1, 1)


class iqGtkPanedManager(base_manager.iqBaseManager):
    """
    GtkPaned manager.
    """

    def collapseGtkPanedPanel(self, paned, toolbar=None, collapse_tool=None, expand_tool=None,
                              resize_panel=0, redraw=True):
        """
        Collapse the paned panel.

        :param paned: GtkPaned object.
        :param toolbar: GtkToolBar object.
        :param collapse_tool: Collapse tool item.
        :param expand_tool: Expand tool item.
        :param resize_panel: Resizable panel index.
        :param redraw: Redrawing object?
        :return: True/False.
        """
        assert issubclass(paned.__class__, gi.repository.Gtk.Paned), u'GtkPaned manager type error'

        setattr(self, '_last_position_%s' % paned.get_name(), paned.get_position())

        if resize_panel == 0:
            paned.set_position(paned.get_property('min-position'))
        elif resize_panel == 1:
            paned.set_position(paned.get_property('max_position'))
        else:
            log_func.warning(u'Invalid paned panel index')
            return False

        if toolbar and issubclass(toolbar.__class__, gi.repository.Gtk.Toolbar):
            if collapse_tool:
                collapse_tool.set_sensitive(False)
            if expand_tool:
                expand_tool.set_sensitive(True)
        return True

    def expandGtkPanedPanel(self, paned, toolbar=None, collapse_tool=None, expand_tool=None,
                            resize_panel=0, redraw=True):
        """
        Expand the paned panel.

        :param paned: GtkPaned object.
        :param toolbar: GtkToolBar object.
        :param collapse_tool: Collapse tool.
        :param expand_tool: Expand tool.
        :param resize_panel: Resizable panel index.
        :param redraw: Redrawing object?
        :return: True/False.
        """
        assert issubclass(paned.__class__, gi.repository.Gtk.Paned), u'GtkPaned manager type error'

        last_position_name = '_last_position_%s' % paned.get_name()
        if not hasattr(self, last_position_name):
            log_func.warning(u'The previous position of the paned panel is not determined')
            return False

        last_position = getattr(self, last_position_name)

        if resize_panel == 0:
            if last_position != paned.get_position():
                paned.set_position(last_position)
        elif resize_panel == 1:
            if last_position != paned.get_position():
                paned.set_position(last_position)
        else:
            log_func.warning(u'Invalid rollup panel index')
            return False

        if toolbar and issubclass(toolbar.__class__, gi.repository.Gtk.Toolbar):
            if collapse_tool:
                collapse_tool.set_sensitive(True)
            if expand_tool:
                expand_tool.set_sensitive(False)
        return True

