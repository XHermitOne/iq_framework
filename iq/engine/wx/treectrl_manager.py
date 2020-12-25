#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TreeCtrl manager.
"""

import hashlib
import wx
import wx.lib.gizmos

from ...util import log_func
from ...util import spc_func

from .dlg import wxdlg_func
from . import base_manager
from . import wxbitmap_func

__version__ = (0, 0, 0, 1)

DEFAULT_ITEM_IMAGE_WIDTH = wxbitmap_func.DEFAULT_ICON_WIDTH
DEFAULT_ITEM_IMAGE_HEIGHT = wxbitmap_func.DEFAULT_ICON_HEIGHT
DEFAULT_ITEM_IMAGE_SIZE = (DEFAULT_ITEM_IMAGE_WIDTH, DEFAULT_ITEM_IMAGE_HEIGHT)

TREE_CTRL_IMAGE_LIST_CACHE_NAME = '__image_list_cache'


class iqTreeCtrlManager(base_manager.iqBaseManager):
    """
    TreeCtrl manager.
    """
    def _setTreeCtrlData(self, treectrl=None, tree_data=None, label='name',
                         ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if not tree_data:
            log_func.warning(u'Not define tree data of wx.TreeCtrl control')
            return False

        treectrl.DeleteAllItems()
        self.appendTreeCtrlBranch(treectrl=treectrl, node=tree_data, label=label, ext_func=ext_func)

        if do_expand_all:
            treectrl.ExpandAll()
        return True

    def setTreeCtrlData(self, treectrl=None, tree_data=None, label='name',
                        ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setTreeCtrlData(treectrl, tree_data, label, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of wx.TreeCtrl control')
        return False

    def _appendTreeCtrlBranch(self, treectrl=None, parent_item=None, node=None, label='name', ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param treectrl: wx.TreeCtrl control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param label: Key as label. For example 'name'.
        :param ext_func: Extended function.
        :return: True/False.
        """
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if parent_item is None:
            if isinstance(node, (list, tuple)) and len(node) > 1:
                log_func.debug(u'Create UNKNOWN root item of wx.TreeCtrl control')
                parent_item = treectrl.AddRoot(base_manager.UNKNOWN)
                result = self.appendTreeCtrlBranch(treectrl, parent_item=parent_item,
                                                   node={spc_func.CHILDREN_ATTR_NAME: node},
                                                   label=label, ext_func=ext_func)
                return result
            elif isinstance(node, (list, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self.addTreeCtrlRootItem(treectrl, node, label, ext_func)
            elif isinstance(node, dict):
                parent_item = self.addTreeCtrlRootItem(treectrl, node, label, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in wx.TreeCtrl manager' % str(type(node)))
                return False

        for record in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            item_label = str(record.get(label, u''))
            # log_func.debug(u'Append tree item data <%s>' % item_label)
            item = treectrl.AppendItem(parent_item, item_label)

            if ext_func:
                try:
                    ext_func(treectrl, item, record)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            treectrl.SetItemData(item, record)

            if spc_func.CHILDREN_ATTR_NAME in record and record[spc_func.CHILDREN_ATTR_NAME]:
                for child in record[spc_func.CHILDREN_ATTR_NAME]:
                    self.appendTreeCtrlBranch(treectrl, item, child, label=label, ext_func=ext_func)

    def appendTreeCtrlBranch(self, treectrl=None, parent_item=None, node=None, label='name', ext_func=None):
        """
        Add branch data to node of wx.TreeCtrl control.

        :param treectrl: wx.TreeCtrl control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param label: Key as label.
        :param ext_func: Extended function.
        :return: True/False.
        """
        try:
            return self._appendTreeCtrlBranch(treectrl, parent_item, node, label, ext_func)
        except:
            log_func.fatal(u'Add branch to node of wx.TreeCtrl control error')
        return False

    def addTreeCtrlRootItem(self, treectrl=None, node=None, label='name', ext_func=None):
        """
        Add root item.

        :return:
        """
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        root_label = str(node.get(label, base_manager.UNKNOWN))
        parent_item = treectrl.AddRoot(root_label)

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetRootItem()

        if not item.IsOk():
            log_func.warning(u'Not correct item <%s>' % str(item))
            return None

        return treectrl.GetItemData(item)

    def getTreeCtrlSelectedItemData(self, treectrl=None):
        """
        Get selected item data.

        :param treectrl: wx.TreeCtrl control.
        :return: Item struct data or None if error.
        """
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

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
        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            treectrl.SetItemBackgroundColour(item, colour)
            return True
        except:
            log_func.fatal(u'Set background colour item error')
        return False

    def getTreeCtrlItemLevelIdx(self, treectrl=None, item=None):
        """
        Determine the level of the tree item.
        For example, the root item has level 0.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item.
            If None, then the root element is taken.
        :return: Level index or None if error.
        """
        label_path = self.getTreeCtrlItemPathLabel(treectrl=treectrl, item=item)
        return len(label_path) if label_path is not None else None

    def getTreeCtrlItemPathLabel(self, treectrl=None, item=None, cur_path=None):
        """
        The path to the item. Path is a list of element names.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item.
            If None, then the root element is taken.
        :param cur_path: Current filled path.
        :return: Path list to item or None if error.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        try:
            if item is None:
                # The root element has an empty path
                return []

            parent = treectrl.GetItemParent(item)
            # If there is a parent item, then call recursively
            if parent and parent.IsOk():
                if cur_path is None:
                    cur_path = []
                cur_path.insert(-1, treectrl.GetItemText(item))
                return self.getTreeCtrlItemPathLabel(treectrl=treectrl, item=parent, cur_path=cur_path)

            if cur_path is None:
                # This is the root item.
                cur_path = []
            return cur_path
        except:
            log_func.fatal(u'Error get level path in <%s>' % str(treectrl))
        return None

    def setTreeCtrlItemText(self, treectrl=None, item=None, label=u''):
        """
        Set item text.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :param label: Item text/label.
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            if item is None:
                item = treectrl.GetRootItem()
            if item.IsOk():
                treectrl.SetItemText(item, label)
                return True
            else:
                log_func.warning(u'wx.TreeCtrl item failed')
        except:
            log_func.fatal(u'Set item text/label error')
        return False

    def getTreeCtrlItemText(self, treectrl=None, item=None):
        """
        Get item text.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item. If None then get root item.
        :return: Item text/label or None if error.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            if item is None:
                item = treectrl.GetRootItem()
            return treectrl.GetItemText(item)
        except:
            log_func.fatal(u'Get item text/label error')
        return None

    def setTreeCtrlRootTitle(self, treectrl=None, title=u''):
        """
        Set root item text/label.

        :param treectrl: wx.TreeCtrl control.
        :param title: Root item text/label.
        :return: True/False.
        """
        return self.setTreeCtrlItemText(treectrl=treectrl, label=title)

    def getTreeCtrlRootTitle(self, treectrl=None):
        """
        Get root item text/label.

        :param treectrl: wx.TreeCtrl control.
        :return: Root item text/label or None if error.
        """
        return self.getTreeCtrlItemText(treectrl=treectrl)

    def isTreeCtrlRootItem(self, treectrl=None, item=None):
        """
        Check if the tree element is root.

        :param treectrl: wx.TreeCtrl control.
        :param item: Item.
        :return: True - root item / False - no.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        return treectrl.GetRootItem() == item

    def getTreeCtrlItemPathData(self, treectrl=None, item=None, cur_path=None):
        """
        The path to the element. Path is a list of these items.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If None, then the root element is taken.
        :param cur_path: The current filled path.
        :return: A list of the data path to the element, or None on error.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if cur_path is None:
            cur_path = list()

        try:
            # item_data = self.getItemData_tree(ctrl=tree_ctrl, item=item)
            item_data = self.getTreeCtrlItemData(treectrl=treectrl, item=item)
            cur_path.insert(-1, item_data)

            if item is not None and item.IsOk():
                parent = treectrl.GetItemParent(item)
                if not parent.IsOk():
                    # [NOTE] GetItemParent return not None.
                    # Need to check for IsOk
                    return cur_path
                elif self.isTreeCtrlRootItem(treectrl=treectrl, item=parent):
                    parent = None
                # If there is a parent element, then call recursively
                return self.getTreeCtrlItemPathData(treectrl=treectrl, item=parent, cur_path=cur_path)
            return cur_path
        except:
            log_func.fatal(u'Error determining the path of an object element <%s>' % str(treectrl))
        return None

    def isTreeCtrlFirstItem(self, treectrl=None, item=None):
        """
        Checking if the item is the first at the current level?

        :param treectrl: wx.TreeCtrl object.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :return: True - first item / False - no.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            # This is the root element. He is always the first
            return True

        parent_item = treectrl.GetItemParent(item)
        if parent_item and parent_item.IsOk():
            first_child, cookie = treectrl.GetFirstChild(parent_item)
            return first_child == item
        elif self.isTreeCtrlRootItem(treectrl=treectrl, item=item):
            # This is the root element. He is always the first
            return True
        else:
            log_func.warning(u'Incorrect tree item')
        return False

    def isTreeCtrlLastItem(self, treectrl=None, item=None):
        """
        Checking if the item is the last one at the current level?

        :param treectrl: wx.TreeCtrl.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :return: True - last item / False - no.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            # This is the root element. He is always the last
            return True

        parent_item = treectrl.GetItemParent(item)
        if parent_item and parent_item.IsOk():
            last_child = treectrl.GetLastChild(parent_item)
            return last_child == item
        elif self.isTreeCtrlRootItem(treectrl=treectrl, item=item):
            # This is the root element. He is always the last
            return True
        else:
            log_func.warning(u'Incorrect tree item')
        return False

    def moveUpTreeCtrlItem(self, treectrl=None, item=None, auto_select=True):
        """
        Move the tree element higher in the current list.

        :param treectrl: wx.TreeCtrl.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :param auto_select: Automatically select the item to be moved?
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            # The root element cannot be moved
            return False

        # parent_item = self.getParentTreeItem(ctrl=ctrl, item=item)
        parent_item = self.getTreeCtrlParentItem(treectrl=treectrl, item=item)
        if parent_item:
            prev_item = treectrl.GetPrevSibling(treectrl.GetPrevSibling(item))
            if prev_item and not prev_item.IsOk():
                prev_item = None
            new_item = treectrl.InsertItem(parent_item, prev_item,
                                           text=treectrl.GetItemText(item),
                                           image=treectrl.GetItemImage(item),
                                           data=self.getTreeCtrlItemData(treectrl=treectrl, item=item))
            treectrl.Delete(item)
            if auto_select:
                # self.selectTreeItem(ctrl=ctrl, item=new_item)
                self.selectTreeCtrlItem(treectrl=treectrl, item=new_item)
            return True
        return False

    def moveDownTreeCtrlItem(self, treectrl=None, item=None, auto_select=True):
        """
        Move the tree element lower in the current list.

        :param treectrl: wx.TreeCtrl.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :param auto_select: Automatically select the item to be moved?
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            # The root element cannot be moved
            return False

        # parent_item = self.getParentTreeItem(ctrl=ctrl, item=item)
        parent_item = self.getTreeCtrlParentItem(treectrl=treectrl, item=item)
        if parent_item:
            next_item = treectrl.GetNextSibling(item)
            if next_item and not next_item.IsOk():
                next_item = None
            new_item = treectrl.InsertItem(parent_item, next_item,
                                           text=treectrl.GetItemText(item),
                                           image=treectrl.GetItemImage(item),
                                           data=self.getTreeCtrlItemData(treectrl=treectrl, item=item))
            treectrl.Delete(item)
            if auto_select:
                self.selectTreeCtrlItem(treectrl=treectrl, item=new_item)
            return True
        return False

    def getTreeCtrlParentItem(self, treectrl=None, item=None):
        """
        Get the parent of the tree item.

        :param treectrl: wx.TreeCtrl.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :return: The parent item, or None if not present.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        parent_item = treectrl.GetItemParent(item)
        return parent_item if parent_item and parent_item.IsOk() else None

    def selectTreeCtrlItem(self, treectrl=None, item=None, select=True):
        """
        Select tree item.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :param select: True - select item. False - unselect item.
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetRootItem()

        treectrl.SelectItem(item, select=select)
        return True

    def selectTreeCtrlRootItem(self, treectrl, select=True):
        """
        Selecting the root element of the tree.

        :param treectrl: wx.TreeCtrl control.
        :param select: True - select item. False - unselect item.
        :return: True/False.
        """
        return self.selectTreeCtrlItem(treectrl=treectrl, select=select)

    def appendTreeCtrlChildItem(self, treectrl=None, parent_item=None,
                                label=u'', image=None, data=None, select=True):
        """
        Add a child of the tree.

        :param treectrl: wx.TreeCtrl control.
        :param parent_item: Parent tree item.
            If not specified, it is considered to be the root element.
        :param label: New item label.
        :param image: New item image.
        :param data: Data automatically attached to the new item.
        :param select: Automatically select a new item?
        :return: New tree item or None on error.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if parent_item is None:
            parent_item = treectrl.GetRootItem()

        # img_idx = self.getImageIndex_tree_ctrl(ctrl=ctrl, image=image, auto_add=True)
        img_idx = self.getTreeCtrlImageIndex(treectrl=treectrl, image=image, auto_add=True)

        try:
            new_item = treectrl.AppendItem(parent_item, text=label, image=img_idx, data=data)
            if select:
                treectrl.SelectItem(new_item)
            return new_item
        except:
            log_func.fatal(u'Error adding child element')
        return None

    def getTreeCtrlImageIndex(self, treectrl=None, image=None, auto_add=True):
        """
        Searching for an image in the image list wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param image: Image object.
        :param auto_add: Automatically add to list if missing?
        :return: Object image or -1 if image not found.
        """
        if image is None:
            return -1

        if isinstance(image, wx.Bitmap):
            img = image.ConvertToImage()
            img_id = hashlib.md5(img.GetData()).hexdigest()
        elif isinstance(image, wx.Image):
            img_id = hashlib.md5(image.GetData()).hexdigest()
        else:
            log_func.warning(u'Unsupported image type <%s>' % image.__class__.__name__)
            return -1

        # First check in the cache
        img_cache = self.getTreeCtrlImageListCache(treectrl=treectrl)

        img_idx = -1
        if img_id in img_cache:
            img_idx = img_cache[img_id]
        else:
            if auto_add:
                image_list = self.getTreeCtrlImageList(treectrl=treectrl)
                img_idx = image_list.Add(image)
                # Save to cache
                img_cache[img_id] = img_idx
        return img_idx

    def getTreeCtrlImageList(self, treectrl=None, image_width=DEFAULT_ITEM_IMAGE_WIDTH,
                             image_height=DEFAULT_ITEM_IMAGE_HEIGHT):
        """
        Get a list of pictures of elements of the tree control wx.TreeCtrl.

        :param treectrl: wx.TreeCtrl control.
        :param image_width: Image width.
        :param image_height: Image height.
        :return: wx.ImageList object.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        image_list = treectrl.GetImageList()
        if not image_list:
            image_list = wx.ImageList(image_width, image_height)
            # [NOTE] Add empty Bitmap
            empty_dx = image_list.Add(wxbitmap_func.createEmptyBitmap(image_width, image_height))
            treectrl.SetImageList(image_list)
        return image_list

    def getTreeCtrlImageListCache(self, treectrl=None):
        """
        Image list cache.

        :param treectrl: wx.TreeCtrl control.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if not hasattr(treectrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME):
            setattr(treectrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME, dict())
        return getattr(treectrl, TREE_CTRL_IMAGE_LIST_CACHE_NAME)

    def setTreeCtrlItemImage(self, treectrl=None, item=None, image=None):
        """
        Set tree item image.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :param image: wx.Bitmap object.
            If not specified, the image is deleted.
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetRootItem()

        if image is None:
            treectrl.SetItemImage(item, None)
        else:
            img_idx = self.getTreeCtrlImageIndex(treectrl=treectrl, image=image, auto_add=True)
            treectrl.SetItemImage(item, img_idx)
        return True

    def deleteTreeCtrlItem(self, treectrl=None,item=None, ask=False, select=True):
        """
        Delete tree item.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If not specified, it is considered to be the currently selected item.
        :param ask: Ask for confirmation of deletion?
        :param select: Automatically select a new item?
        :return: True/False.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return False

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        if item is None:
            item = treectrl.GetSelection()

        if not item:
            log_func.warning(u'The current tree element is not defined for deletion')
            return False

        do_del = True
        if ask:
            label = treectrl.GetItemText(item)
            do_del = wxdlg_func.openAskBox(u'DELETE', u'Delete <%s>?' % label)

        if do_del:
            treectrl.Delete(item)
            return True
        return False

    def _getTreeCtrlData(self, treectrl=None, item=None):
        """
        Get tree item all data.

        :param treectrl: wx.TreeCtrl control.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :return: Tree data or None if error.
        """
        if item is None:
            item = treectrl.GetRootItem()

        item_data = self.getTreeCtrlItemData(treectrl=treectrl, item=item)
        if item_data is None:
            item_data = dict()

        children = self.getTreeCtrlItemChildren(treectrl=treectrl, item=item)
        if children:
            item_data[spc_func.CHILDREN_ATTR_NAME] = list()
        for child in children:
            child_data = self._getTreeCtrlData(treectrl=treectrl, item=child)
            item_data[spc_func.CHILDREN_ATTR_NAME].append(child_data)
        return item_data

    def getTreeCtrlData(self, treectrl=None, *args, **kwargs):
        """
        Get tree item all data.

        :param treectrl: wx.TreeCtrl control.
        :return: Tree data or None if error.
            Children data in '_children_' key as list.
        """
        if treectrl is None:
            log_func.warning(u'Not define wx.TreeCtrl object')
            return None

        assert issubclass(treectrl.__class__, wx.TreeCtrl), u'TreeCtrl manager type error'

        try:
            return self._getTreeCtrlData(treectrl=treectrl)
        except:
            log_func.fatal(u'Error get tree data <%s>' % str(treectrl))
        return None
