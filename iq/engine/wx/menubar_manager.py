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
    def enableMenuBarMenuItems(self, menubar=None, **item_enable):
        """
        Set enable menu items.

        :param menubar: MenuBar object.
        :param item_enable: Dictionary
            {
            item1_id: enable_True_or_False, ...
            }
        :return: True/False.
        """
        assert issubclass(menubar, wx.MenuBar), u'MenuBar manager type error'

        result = True
        for item_id in item_enable.keys():
            item = menubar.FindItem(item_id)
            if item and item.IsOk():
                item.Enable(item_enable.get(item_id, True))
                result = result and True
            else:
                result = False
        return result

