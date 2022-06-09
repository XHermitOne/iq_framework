#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Select component popup menu.
"""

import os.path

import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ....util import log_func
from ....util import spc_func
from ....util import id_func
from ....util import lang_func
from ....util import icon_func
# from ....engine.wx import wxbitmap_func
from .... import components

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqSelectComponentMenu(gi.repository.Gtk.Menu):
    """
    Component selection menu class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        gi.repository.Gtk.Menu.__init__(self, *args, **kwargs)

        self.component_palette = components.getComponentSpcPalette()

        self.selected_component = None

        self._parent = None

        self.content = None

        self.menuitem2component_spc = dict()

    def init(self, parent=None, parent_component=None):
        """
        Initialization.

        :param parent: Parent form.
        :param parent_component: Parent component specification.
        """
        self._parent = parent

        if parent_component is None:
            self.content = None
        else:
            self.content = parent_component.get(spc_func.CONTENT_ATTR_NAME, list())

    def create(self, menuitem_handler=None):
        """
        Create component palette menu.

        :param menuitem_handler: Menuitem activate handler.
        :return: wx.FlatMenu object or None if error.
        """
        try:
            return self._create(menuitem_handler=menuitem_handler)
        except:
            log_func.fatal(u'Create component palette menu error')
        return None

    def _create(self, menuitem_handler=None):
        """
        Create component palette menu.

        :param menuitem_handler: Menuitem activate handler.
        :return: wx.FlatMenu object or None if error.
        """
        self.menuitem2component_spc = dict()

        package_names = list(self.component_palette.keys())
        package_names.sort()
        for package_name in package_names:
            package_menu = gi.repository.Gtk.Menu()

            component_specifications = self.component_palette[package_name]
            component_specifications = sorted(component_specifications,
                                              key=lambda component_spc: component_spc.get('type', ''))
            for component_spc in component_specifications:
                icon = component_spc.get(spc_func.ICON_ATTR_NAME, None)
                component_type = component_spc.get('type', 'UndefinedType')
                menuitem_id = id_func.genGUID()
                menuitem = gi.repository.Gtk.ImageMenuItem(label=component_type)
                menuitem.guid = menuitem_id
                if icon:
                    icon_filename = icon_func.getIconFilename(icon)
                    image = gi.repository.Gtk.Image()
                    if os.path.exists(icon_filename):
                        # menuitem.set_use_stock(False)
                        image.set_from_file(icon_filename)
                    else:
                        # menuitem.set_use_stock(True)
                        image.set_from_icon_name('gtk-missing-image', gi.repository.Gtk.IconSize.BUTTON)
                    menuitem.set_image(image)
                    # log_func.debug(u'Component <%s> (Icon: %s) : [%s]' % (component_type, icon_filename, menuitem_id))

                package_menu.append(menuitem)

                if isinstance(self.content, (list, tuple)) and component_type not in self.content:
                    menuitem.set_sensitive(False)

                if self._parent and menuitem_handler is None:
                    # self._parent.Bind(wx.EVT_MENU, self.onSelectComponentMenuItem, id=menuitem_id)
                    menuitem.connect('activate', self.onSelectComponentMenuItemActivate)
                elif self._parent and menuitem_handler:
                    # self._parent.Bind(wx.EVT_MENU, menuitem_handler, id=menuitem_id)
                    menuitem.connect('activate', menuitem_handler)
                else:
                    log_func.warning(u'Be sure to specify the parent window when calling the component selection menu')

                self.menuitem2component_spc[menuitem_id] = component_spc

            submenu_item = gi.repository.Gtk.MenuItem()
            submenu_item.set_label(package_name)
            submenu_item.set_submenu(package_menu)
            # log_func.debug(u'Component package <%s>' % package_name)
            self.append(submenu_item)

        self.show_all()
        return self

    def onSelectComponentMenuItemActivate(self, widget):
        """
        Select component menu item handler.
        """
        menuitem_id = widget.guid
        self.selected_component = self.menuitem2component_spc.get(menuitem_id, None)
        component_type = self.selected_component.get('type', 'UndefinedType')
        log_func.info(u'Selected component <%s>' % component_type)


def popupComponentMenu(parent=None, button=None, menuitem_handler=None):
    """
    Open popup component palette menu.

    :param parent: Parent frame.
    :param button: wx.Button object, which calls up the menu.
    :param menuitem_handler: Menuitem activate handler.
    :return: The specification of the selected component or
        None if the component is not selected.
    """
    if parent is None:
        log_func.warning(u'Not define parent frame for popup menu')
        return None

    select_menu = iqSelectComponentMenu()
    select_menu.init(parent)
    select_menu.create(menuitem_handler=menuitem_handler)

    if button:
        button.PopupMenu(select_menu)
    return select_menu.selected_component
