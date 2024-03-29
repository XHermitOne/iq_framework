#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Select component popup menu.
"""

import wx
from wx.lib.agw import flatmenu

from ....util import log_func
from ....util import spc_func
from ....engine.wx import wxbitmap_func
from .... import components

__version__ = (0, 0, 0, 1)


class iqSelectComponentMenuManager(object):
    """
    A class of general control functions for populating
    a component selection menu from all possible.
    """
    def __init__(self):
        """
        Constructor.
        """
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
        log_func.warning(u'Method not define')
        return self


class iqSelectComponentMenu(wx.Menu, iqSelectComponentMenuManager):
    """
    Component selection menu class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.Menu.__init__(self, *args, **kwargs)

        iqSelectComponentMenuManager.__init__(self)

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
            package_menu = wx.Menu()

            component_specifications = self.component_palette[package_name]
            component_specifications = sorted(component_specifications,
                                              key=lambda component_spc: component_spc.get('type', ''))
            for component_spc in component_specifications:
                icon = component_spc.get(spc_func.ICON_ATTR_NAME, None)
                component_type = component_spc.get('type', 'UndefinedType')
                menuitem_id = wx.NewId()
                menuitem = wx.MenuItem(package_menu, menuitem_id, component_type)
                if icon:
                    bmp = wxbitmap_func.createIconBitmap(icon)
                    if bmp is None:
                        bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU)
                    menuitem.SetBitmap(bmp)

                package_menu.Append(menuitem)

                if isinstance(self.content, (list, tuple)) and component_type not in self.content:
                    menuitem.Enable(False)

                if self._parent and menuitem_handler is None:
                    self._parent.Bind(wx.EVT_MENU, self.onSelectComponentMenuItem, id=menuitem_id)
                elif self._parent and menuitem_handler:
                    self._parent.Bind(wx.EVT_MENU, menuitem_handler, id=menuitem_id)
                else:
                    log_func.warning(u'Be sure to specify the parent window when calling the component selection menu')

                self.menuitem2component_spc[menuitem_id] = component_spc

            menu_id = wx.NewId()
            self.Append(menu_id, package_name, package_menu)
        return self

    def onSelectComponentMenuItem(self, event):
        """
        Select component menu item handler.
        """
        menuitem_id = event.GetId()
        self.selected_component = self.menuitem2component_spc.get(menuitem_id, None)
        component_type = self.selected_component.get('type', 'UndefinedType')
        log_func.info(u'Selected component <%s>' % component_type)
        event.Skip()


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


class iqSelectComponentFlatMenu(flatmenu.FlatMenu,
                                iqSelectComponentMenuManager):
    """
    Component selection menu class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        flatmenu.FlatMenu.__init__(self, *args, **kwargs)

        iqSelectComponentMenuManager.__init__(self)

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
            package_menu = flatmenu.FlatMenu()
            # log_func.debug(u'Component palette. Package name <%s>' % package_name)

            component_specifications = self.component_palette[package_name]
            component_specifications = sorted(component_specifications,
                                              key=lambda component_spc: component_spc.get('type', ''))
            for component_spc in component_specifications:
                icon = component_spc.get(spc_func.ICON_ATTR_NAME, None)
                bmp = wxbitmap_func.createIconBitmap(icon)
                component_type = component_spc.get('type', 'UndefinedType')
                menuitem_id = wx.NewId()
                if bmp is None:
                    menuitem = flatmenu.FlatMenuItem(package_menu, menuitem_id, label=component_type)
                else:
                    menuitem = flatmenu.FlatMenuItem(package_menu, menuitem_id, label=component_type, normalBmp=bmp)

                if isinstance(self.content, (list, tuple)) and component_type not in self.content:
                    menuitem.Enable(False)

                package_menu.AppendItem(menuitem)
                # log_func.debug(u'Component palette. Component type <%s>' % component_type)

                if self._parent and menuitem_handler is None:
                    self._parent.Bind(wx.EVT_MENU, self.onSelectComponentMenuItem, id=menuitem_id)
                elif self._parent and menuitem_handler:
                    self._parent.Bind(wx.EVT_MENU, menuitem_handler, id=menuitem_id)
                else:
                    log_func.warning(u'Be sure to specify the parent window when calling the component selection menu')

                self.menuitem2component_spc[menuitem_id] = component_spc

            menu_id = wx.NewId()
            self.AppendMenu(menu_id, package_name, package_menu)
        return self

    def onSelectComponentMenuItem(self, event):
        """
        Select component menu item handler.
        """
        menuitem_id = event.GetId()
        self.selected_component = self.menuitem2component_spc.get(menuitem_id, None)
        component_type = self.selected_component.get('type', 'UndefinedType')
        log_func.info(u'Selected component <%s>' % component_type)
        event.Skip()


def popupComponentFlatMenu(parent=None, button=None, menuitem_handler=None):
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

    select_menu = iqSelectComponentFlatMenu()
    select_menu.init(parent)
    select_menu.create(menuitem_handler=menuitem_handler)

    if button:
        button_size = button.GetSize()
        button_point = button.GetPosition()
        button_point = button.GetParent().ClientToScreen(button_point)

        select_menu.SetOwnerHeight(button_size.y)
        select_menu.Popup(wx.Point(button_point.x, button_point.y), parent)
    else:
        select_menu.Popup(wx.GetMousePosition(), parent)

    return select_menu.selected_component
