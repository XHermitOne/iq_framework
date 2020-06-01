#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TreeListCtrl manager.
"""

import wx
import wx.lib.gizmos

from ...util import log_func
from ...util import spc_func

from . import base_manager

__version__ = (0, 0, 0, 1)


class iqTreeListCtrlManager(base_manager.iqBaseManager):
    """
    TreeListCtrl manager.
    """
    def _setTreeListCtrlData(self, treelistctrl=None, tree_data=None, columns=(),
                             ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if not tree_data:
            log_func.error(u'Not define tree data of wx.TreeListCtrl control')
            return False

        treelistctrl.GetMainWindow().DeleteAllItems()
        self.appendTreeListCtrlBranch(treelistctrl=treelistctrl, node=tree_data, columns=columns, ext_func=ext_func)

        if do_expand_all:
            treelistctrl.GetMainWindow().ExpandAll()
        return True

    def setTreeListCtrlData(self, treelistctrl=None, tree_data=None, columns=(),
                            ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setTreeListCtrlData(treelistctrl, tree_data, columns, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of wx.TreeListCtrl control.')
        return False

    def _appendTreeListCtrlBranch(self, treelistctrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeListCtrl control.

        :param treelistctrl: wx.TreeListCtrl control.
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
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if parent_item is None:
            if (isinstance(node, list) or isinstance(node, tuple)) and len(node) > 1:
                log_func.info(u'Create UNKNOWN root item of wx.TreeListCtrl control')
                parent_item = treelistctrl.GetMainWindow().AddRoot(base_manager.UNKNOWN)
                result = self.appendTreeListCtrlBranch(treelistctrl, parent_item=parent_item,
                                                       node={spc_func.CHILDREN_ATTR_NAME: node},
                                                       columns=columns, ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self.addTreeListCtrlRootItem(treelistctrl, node, columns, ext_func)
            elif isinstance(node, dict):
                parent_item = self.addTreeListCtrlRootItem(treelistctrl, node, columns, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in wx.TreeListCtrl manager' % str(type(node)))
                return False

        for record in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            label = str(record.get(columns[0], u''))
            item = treelistctrl.GetMainWindow().AppendItem(parent_item, label)
            for i, column in enumerate(columns[1:]):
                label = str(record.get(columns[i + 1], u''))
                treelistctrl.GetMainWindow().SetItemText(item, label, i + 1)

            if ext_func:
                try:
                    ext_func(treelistctrl, item, record)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            treelistctrl.GetMainWindow().SetItemData(item, record)

            if spc_func.CHILDREN_ATTR_NAME in record and record[spc_func.CHILDREN_ATTR_NAME]:
                for child in record[spc_func.CHILDREN_ATTR_NAME]:
                    self.appendTreeListCtrlBranch(treelistctrl, item, child, columns=columns, ext_func=ext_func)

    def appendTreeListCtrlBranch(self, treelistctrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeListCtrl control.

        :param treelistctrl: wx.TreeListCtrl control.
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
            return self._appendTreeListCtrlBranch(treelistctrl, parent_item, node, columns, ext_func)
        except:
            log_func.fatal(u'Add branch to node of wx.TreeListCtrl control error')
        return False

    def addTreeListCtrlRootItem(self, treelistctrl=None, node=None, columns=(), ext_func=None):
        """
        Add root item.

        :return:
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        label = str(node.get(columns[0], base_manager.UNKNOWN))
        parent_item = treelistctrl.GetMainWindow().AddRoot(label)
        for i, column in enumerate(columns[1:]):
            label = str(node.get(columns[i + 1], base_manager.UNKNOWN))
            treelistctrl.GetMainWindow().SetItemText(parent_item, label, i + 1)
        treelistctrl.GetMainWindow().SetItemData(parent_item, node)

        if ext_func:
            try:
                ext_func(treelistctrl, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))
        return parent_item

    def getTreeListCtrlItemData(self, treelistctrl=None, item=None):
        """
        Get item data.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Tree item.
            If None then get root item.
        :return: Item struct data or None if error.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if item is None:
            item = treelistctrl.GetMainWindow().GetRootItem()

        if not item.IsOk():
            log_func.warning(u'Not correct item <%s>' % str(item))
            return None

        return treelistctrl.GetMainWindow().GetItemData(item)

    def getTreeListCtrlSelectedItemData(self, treelistctrl=None):
        """
        Get selected item data.

        :param treelistctrl: wx.TreeListCtrl control.
        :return: Item struct data or None if error.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        selected_item = treelistctrl.GetMainWindow().GetSelection()
        if selected_item:
            return self.getTreeListCtrlItemData(treelistctrl=treelistctrl, item=selected_item)
        return None

    def setTreeListCtrlItemData(self, treelistctrl=None, item=None, data=None):
        """
        Set item data.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item. If None then get root item.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if item is None:
            item = treelistctrl.GetMainWindow().GetRootItem()

        # return treelistctrl.GetMainWindow().SetItemData(item, data)
        return treelistctrl.GetMainWindow().SetItemData(item, data)

    def setTreeListCtrlSelectedItemData(self, treelistctrl=None, data=None):
        """
        Set selected item data.

        :param treelistctrl: wx.TreeListCtrl control.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        selected_item = treelistctrl.GetMainWindow().GetSelection()
        if selected_item:
            return self.setTreeListCtrlItemData(treelistctrl=treelistctrl, item=selected_item, data=data)
        return None

    def getTreeListCtrlItemChildren(self, treelistctrl=None, item=None):
        """
        Get children of item.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item. If None then get root item.
        :return: Children list or None if error.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        try:
            if item is None:
                item = treelistctrl.GetMainWindow().GetRootItem()

            children = list()

            children_count = treelistctrl.GetMainWindow().GetChildrenCount(item, False)
            cookie = None
            for i in range(children_count):
                if i == 0:
                    child, cookie = treelistctrl.GetMainWindow().GetFirstChild(item)
                else:
                    child, cookie = treelistctrl.GetMainWindow().GetNextChild(item, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            log_func.fatal(u'Get item children wx.TreeListCtrl <%s> error' % str(treelistctrl))
        return None

    def getTreeListCtrlItemChildrenCount(self, treelistctrl=None, item=None):
        """
        Get item children count.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item. If None then get root item.
        :return: Item children count or None if error.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        try:
            if item is None:
                item = treelistctrl.GetMainWindow().GetRootItem()
            return treelistctrl.GetMainWindow().GetChildrenCount(item)
        except:
            log_func.fatal(u'Get item children count wx.TreeListCtrl <%s> error' % str(treelistctrl))
        return None

    def setTreeListCtrlItemColourExpression(self, treelistctrl=None, fg_colour=None, bg_colour=None, expression=None, item=None):
        """
        Set item text colour if expression return True.

        :param treelistctrl: wx.TreeListCtrl control.
        :param fg_colour: Foreground colour, if expression return True.
        :param bg_colour: Background colour, if expression return True.
        :param expression: lambda expression:
            lambda item: ...
            return True/False.
        :param item: Current item.
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if expression is None:
            log_func.warning(u'Not define expression')
            return False

        if fg_colour is None and bg_colour is None:
            log_func.warning(u'Not define foreground/background colour')
            return False

        for child in self.getTreeListCtrlItemChildren(treelistctrl=treelistctrl, item=item):
            colorize = expression(child)
            if fg_colour and colorize:
                self.setTreeListCtrlItemForegroundColour(treelistctrl, child, fg_colour)
            if bg_colour and colorize:
                self.setTreeListCtrlItemBackgroundColour(treelistctrl, child, bg_colour)

            if treelistctrl.GetMainWindow().ItemHasChildren(child):
                self.setTreeListCtrlItemColourExpression(treelistctrl, fg_colour=fg_colour,
                                                         bg_colour=bg_colour,
                                                         expression=expression,
                                                         item=child)
        return True

    def setTreeListCtrlItemForegroundColour(self, treelistctrl, item, colour):
        """
        Set foreground colour item.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item.
        :param colour: Foreground colour.
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        try:
            treelistctrl.GetMainWindow().SetItemTextColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set foreground colour item error')
        return False

    def setTreeListCtrlItemBackgroundColour(self, treelistctrl, item, colour):
        """
        Set background colour item.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item.
        :param colour: Backgrouind colour.
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        try:
            treelistctrl.GetMainWindow().SetItemBackgroundColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set background colour item error')
        return False
