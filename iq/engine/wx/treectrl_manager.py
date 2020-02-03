#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TreeCtrl manager.
"""

# import wx
# import wx.lib.gizmos

from ...util import log_func

from . import base_manager

__version__ = (0, 0, 0, 1)


class iqTreeCtrlManager(base_manager.iqBaseManager):
    """
    TreeCtrl manager.
    """
    def _setTreeData(self, ctrl=None, tree_data=None, columns=(),
                     ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param ctrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return False

        if not tree_data:
            log_func.warning(u'Not define tree data of wx.TreeCtrl control')
            return False

        ctrl.DeleteAllItems()
        self.appendBranch(ctrl=ctrl, node=tree_data, columns=columns, ext_func=ext_func)

        if do_expand_all:
            ctrl.ExpandAll()
        return True

    def setTreeData(self, ctrl=None, tree_data=None, columns=(),
                    ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param ctrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setTreeData(ctrl, tree_data, columns, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of wx.TreeCtrl control.')
        return False

    def _appendBranch(self, ctrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param ctrl: wx.TreeCtrl control.
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
        if ctrl is None:
            log_func.warning(u'wx.TreeCtrl control not defined')
            return False

        if parent_item is None:
            if (isinstance(node, list) or isinstance(node, tuple)) and len(node) > 1:
                log_func.info(u'Create UNKNOWN root item of wx.TreeCtrl control')
                parent_item = ctrl.AddRoot(base_manager.UNKNOWN)
                result = self.appendBranch(ctrl, parent_item=parent_item,
                                           node={base_manager.CHILDREN_ATTR_NAME: node},
                                           columns=columns, ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self.addRootItem(ctrl, node, columns, ext_func)
            elif isinstance(node, dict):
                parent_item = self.addRootItem(ctrl, node, columns, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in wx.TreeCtrl manager' % str(type(node)))
                return False

        for record in node.get(base_manager.CHILDREN_ATTR_NAME, list()):
            label = str(record.get(columns[0], u''))
            item = ctrl.AppendItem(parent_item, label)
            for i, column in enumerate(columns[1:]):
                label = str(record.get(columns[i + 1], u''))
                ctrl.SetItemText(item, label, i + 1)

            if ext_func:
                try:
                    ext_func(ctrl, item, record)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            ctrl.SetItemData(item, record)

            if base_manager.CHILDREN_ATTR_NAME in record and record[base_manager.CHILDREN_ATTR_NAME]:
                for child in record[base_manager.CHILDREN_ATTR_NAME]:
                    self.appendBranch(ctrl, item, child, columns=columns, ext_func=ext_func)

    def appendBranch(self, ctrl=None, parent_item=None, node=None, columns=(), ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param ctrl: wx.TreeCtrl control.
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
            return self._appendBranch(ctrl, parent_item, node, columns, ext_func)
        except:
            log_func.fatal(u'Add branch to node of wx.TreeCtrl control error')
        return False

    def addRootItem(self, ctrl=None, node=None, columns=(), ext_func=None):
        """
        Add root item.

        :return:
        """
        label = str(node.get(columns[0], base_manager.UNKNOWN))
        parent_item = ctrl.AddRoot(label)
        for i, column in enumerate(columns[1:]):
            label = str(node.get(columns[i + 1], base_manager.UNKNOWN))
            ctrl.SetItemText(parent_item, label, i + 1)
        ctrl.SetItemData(parent_item, node)

        if ext_func:
            try:
                ext_func(ctrl, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))
        return parent_item

    def getItemData(self, ctrl=None, item=None):
        """
        Get item data.

        :param ctrl: wx.TreeCtrl control.
        :param item: Tree item.
            If None then get root item.
        :return: Item struct data or None if error.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None

        if item is None:
            item = ctrl.GetRootItem()

        if not item.IsOk():
            log_func.warning(u'Not correct item <%s>' % str(item))
            return None

        return ctrl.GetMainWindow().GetItemData(item)

    def getSelectedItemData(self, ctrl=None):
        """
        Get selected item data.

        :param ctrl: wx.TreeCtrl control.
        :return: Item struct data or None if error.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None

        selected_item = ctrl.GetSelection()
        if selected_item:
            return self.getItemData(ctrl=ctrl, item=selected_item)
        return None

    def setItemData(self, ctrl=None, item=None, data=None):
        """
        Set item data.

        :param ctrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :param data: Item data.
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return False

        if item is None:
            item = ctrl.GetRootItem()

        # return ctrl.GetMainWindow().SetItemData(item, data)
        return ctrl.SetItemData(item, data)

    def setSelectedItemData(self, ctrl=None, data=None):
        """
        Set selected item data.

        :param ctrl: wx.TreeCtrl control.
        :param data: Item data.
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return False

        selected_item = ctrl.GetSelection()
        if selected_item:
            return self.setItemData(ctrl=ctrl, item=selected_item, data=data)
        return None

    def getItemChildren(self, ctrl=None, item=None):
        """
        Get children of item.

        :param ctrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :return: Children list or None if error.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None

        try:
            if item is None:
                item = ctrl.GetRootItem()

            children = list()

            children_count = ctrl.GetChildrenCount(item, False)
            cookie = None
            for i in range(children_count):
                if i == 0:
                    child, cookie = ctrl.GetFirstChild(item)
                else:
                    child, cookie = ctrl.GetNextChild(item, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            log_func.fatal(u'Get item children wx.TreeCtrl <%s> error' % str(ctrl))
        return None

    def getItemChildrenCount(self, ctrl=None, item=None):
        """
        Get item children count.

        :param ctrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :return: Item children count or None if error.
        """
        try:
            if item is None:
                item = ctrl.GetRootItem()
            return ctrl.GetChildrenCount(item)
        except:
            log_func.fatal(u'Get item children count wx.TreeCtrl <%s> error' % str(ctrl))
        return None

    def setItemColourExpression(self, ctrl=None, fg_colour=None, bg_colour=None, expression=None, item=None):
        """
        Set item text colour if expression return True.

        :param ctrl: wx.TreeCtrl control.
        :param fg_colour: Foreground colour, if expression return True.
        :param bg_colour: Background colour, if expression return True.
        :param expression: lambda expression:
            lambda item: ...
            return True/False.
        :param item: Current item.
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None

        if expression is None:
            log_func.warning(u'Not define expression')
            return False

        if fg_colour is None and bg_colour is None:
            log_func.warning(u'Not define foreground/background colour')
            return False

        for child in self.getItemChildren(ctrl=ctrl, item=item):
            colorize = expression(child)
            if fg_colour and colorize:
                self.setItemForegroundColour(ctrl, child, fg_colour)
            if bg_colour and colorize:
                self.setItemBackgroundColour(ctrl, child, bg_colour)

            if ctrl.ItemHasChildren(child):
                self.setItemColourExpression(ctrl, fg_colour=fg_colour,
                                             bg_colour=bg_colour,
                                             expression=expression,
                                             item=child)
        return True

    def setItemForegroundColour(self, ctrl, item, colour):
        """
        Set foreground colour item.

        :param ctrl: wx.TreeCtrl control.
        :param item: Item.
        :param colour: Foreground colour.
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None
        try:
            ctrl.SetItemTextColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set foreground colour item error')
        return False

    def setItemBackgroundColour(self, ctrl, item, colour):
        """
        Set background colour item.

        :param ctrl: wx.TreeCtrl control.
        :param item: Item.
        :param colour: Backgrouind colour.
        :return: True/False.
        """
        if ctrl is None:
            log_func.warning(u'Not define wx.TreeCtrl control')
            return None
        try:
            ctrl.SetItemBackgroundColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set background colour item error')
        return False
