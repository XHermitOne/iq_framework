#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MenuBar manager.
"""

import wx

from . import base_manager

__version__ = (0, 0, 0, 1)


class iqMenuBarManager(base_manager.iqBaseManager):
    """
    MenuBar manager.
    """
    def enableMenuBarMenuItems(self, menubar=None, menuitem_enable=None):
        """
        Set enable menu items.

        :param menubar: MenuBar object.
        :param menuitem_enable: Dictionary
            {
            menuitem1_id: enable_True_or_False, ...
            }
        :return: True/False.
        """
        assert issubclass(menubar.__class__, wx.MenuBar), u'MenuBar manager type error'

        if menuitem_enable is None:
            return True

        result = True
        for menuitem_id in menuitem_enable.keys():
            menuitem = menubar.FindItemById(menuitem_id)
            if menuitem:
                menuitem.Enable(menuitem_enable.get(menuitem_id, True))
                result = result and True
            else:
                result = False
        return result

