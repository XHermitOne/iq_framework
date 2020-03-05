#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TreeCtrl manager.
"""

import wx
# import wx.lib.gizmos

from ...util import log_func
from ...util import spc_func

from . import base_manager

__version__ = (0, 0, 0, 1)


class iqTreeCtrlManager(base_manager.iqBaseManager):
    """
    TreeCtrl manager.
    """
    def _setTreeCtrlData(self, treectrl=None, tree_data=None, columns=(),
                         ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        if not tree_data:
            log_func.warning(u'Not define tree data of wx.TreeCtrl control')
            return False

        treectrl.DeleteAllItems()
        self.appendTreeCtrlBranch(treectrl=treectrl, node=tree_data, columns=columns, ext_func=ext_func)

        if do_expand_all:
            treectrl.ExpandAll()
        return True

    def setTreeCtrlData(self, treectrl=None, tree_data=None, columns=(),
                        ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setTreeCtrlData(treectrl, tree_data, columns, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of wx.TreeCtrl control.')
        return False

    def _appendTreeCtrlBranch(self, treectrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param treectrl: wx.TreeCtrl control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param columns: Columns as tuple:
            ('column key 1', ...)
        :param ext_func: Extended function.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        if parent_item is None:
            if (isinstance(node, list) or isinstance(node, tuple)) and len(node) > 1:
                log_func.info(u'Create UNKNOWN root item of wx.TreeCtrl control')
                parent_item = treectrl.AddRoot(base_manager.UNKNOWN)
                result = self.appendTreeCtrlBranch(treectrl, parent_item=parent_item,
                                                   node={spc_func.CHILDREN_ATTR_NAME: node},
                                                   columns=columns, ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self.addTreeCtrlRootItem(treectrl, node, columns, ext_func)
            elif isinstance(node, dict):
                parent_item = self.addTreeCtrlRootItem(treectrl, node, columns, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in wx.TreeCtrl manager' % str(type(node)))
                return False

        for record in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            label = str(record.get(columns[0], u''))
            item = treectrl.AppendItem(parent_item, label)
            for i, column in enumerate(columns[1:]):
                label = str(record.get(columns[i + 1], u''))
                treectrl.SetItemText(item, label, i + 1)

            if ext_func:
                try:
                    ext_func(treectrl, item, record)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            treectrl.SetItemData(item, record)

            if spc_func.CHILDREN_ATTR_NAME in record and record[spc_func.CHILDREN_ATTR_NAME]:
                for child in record[spc_func.CHILDREN_ATTR_NAME]:
                    self.appendTreeCtrlBranch(treectrl, item, child, columns=columns, ext_func=ext_func)

    def appendTreeCtrlBranch(self, treectrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param treectrl: wx.TreeCtrl control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param columns: Columns as tuple:
            ('column key 1', ...)
        :param ext_func: Extended function.
        :return: True/False.
        """
        try:
            return self._appendTreeCtrlBranch(treectrl, parent_item, node, columns, ext_func)
        except:
            log_func.fatal(u'Add branch to node of wx.TreeCtrl control error')
        return False

    def addTreeCtrlRootItem(self, treectrl=None, node=None, columns=(), ext_func=None):
        """
        Add root item.

        :return:
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        label = str(node.get(columns[0], base_manager.UNKNOWN))
        parent_item = treectrl.AddRoot(label)
        for i, column in enumerate(columns[1:]):
            label = str(node.get(columns[i + 1], base_manager.UNKNOWN))
            treectrl.SetItemText(parent_item, label, i + 1)
        treectrl.SetItemData(parent_item, node)

        if ext_func:
            try:
                ext_func(treectrl, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))
        return parent_item

    def getTreeCtrlItemData(self, treectrl=None, item=None):
        """
        Get item data.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If None then get root item.
        :return: Item struct data or None if error.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetRootItem()

        if not item.IsOk():
            log_func.warning(u'Not correct item <%s>' % str(item))
            return None

        return treectrl.GetMainWindow().GetItemData(item)

    def getTreeCtrlSelectedItemData(self, treectrl=None):
        """
        Get selected item data.

        :param treectrl: wx.TreeCtrl control.
        :return: Item struct data or None if error.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        selected_item = treectrl.GetSelection()
        if selected_item:
            return self.getTreeCtrlItemData(treectrl=treectrl, item=selected_item)
        return None

    def setTreeCtrlItemData(self, treectrl=None, item=None, data=None):
        """
        Set item data.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetRootItem()

        # return treelistctrl.GetMainWindow().SetItemData(item, data)
        return treectrl.SetItemData(item, data)

    def setTreeCtrlSelectedItemData(self, treectrl=None, data=None):
        """
        Set selected item data.

        :param treectrl: wx.TreeCtrl control.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        selected_item = treectrl.GetSelection()
        if selected_item:
            return self.setTreeCtrlItemData(treectrl=treectrl, item=selected_item, data=data)
        return None

    def getTreeCtrlItemChildren(self, treectrl=None, item=None):
        """
        Get children of item.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :return: Children list or None if error.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            if item is None:
                item = treectrl.GetRootItem()

            children = list()

            children_count = treectrl.GetChildrenCount(item, False)
            cookie = None
            for i in range(children_count):
                if i == 0:
                    child, cookie = treectrl.GetFirstChild(item)
                else:
                    child, cookie = treectrl.GetNextChild(item, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            log_func.fatal(u'Get item children wx.TreeCtrl <%s> error' % str(treectrl))
        return None

    def getTreeCtrlItemChildrenCount(self, treectrl=None, item=None):
        """
        Get item children count.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :return: Item children count or None if error.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            if item is None:
                item = treectrl.GetRootItem()
            return treectrl.GetChildrenCount(item)
        except:
            log_func.fatal(u'Get item children count wx.TreeCtrl <%s> error' % str(treectrl))
        return None

    def setTreeCtrlItemColourExpression(self, treectrl=None, fg_colour=None, bg_colour=None, expression=None, item=None):
        """
        Set item text colour if expression return True.

        :param treectrl: wx.TreeCtrl control.
        :param fg_colour: Foreground colour, if expression return True.
        :param bg_colour: Background colour, if expression return True.
        :param expression: lambda expression:
            lambda item: ...
            return True/False.
        :param item: Current item.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        if expression is None:
            log_func.warning(u'Not define expression')
            return False

        if fg_colour is None and bg_colour is None:
            log_func.warning(u'Not define foreground/background colour')
            return False

        for child in self.getTreeCtrlItemChildren(treectrl=treectrl, item=item):
            colorize = expression(child)
            if fg_colour and colorize:
                self.setTreeCtrlItemForegroundColour(treectrl, child, fg_colour)
            if bg_colour and colorize:
                self.setTreeCtrlItemBackgroundColour(treectrl, child, bg_colour)

            if treectrl.ItemHasChildren(child):
                self.setTreeCtrlItemColourExpression(treectrl, fg_colour=fg_colour,
                                                     bg_colour=bg_colour,
                                                     expression=expression,
                                                     item=child)
        return True

    def setTreeCtrlItemForegroundColour(self, treectrl, item, colour):
        """
        Set foreground colour item.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item.
        :param colour: Foreground colour.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            treectrl.SetItemTextColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set foreground colour item error')
        return False

    def setTreeCtrlItemBackgroundColour(self, treectrl, item, colour):
        """
        Set background colour item.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item.
        :param colour: Backgrouind colour.
        :return: True/False.
        """
        assert issubclass(treectrl, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            treectrl.SetItemBackgroundColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set background colour item error')
        return False
