#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TreeListCtrl manager.
"""

import os.path
import hashlib
import wx
import wx.lib.gizmos
import wx.dataview

from ...util import log_func
from ...util import spc_func
from ...util import icon_func

from ...engine.wx import wxbitmap_func

from . import base_manager

__version__ = (0, 0, 1, 1)

DEFAULT_ITEM_IMAGE_WIDTH = wxbitmap_func.DEFAULT_ICON_WIDTH
DEFAULT_ITEM_IMAGE_HEIGHT = wxbitmap_func.DEFAULT_ICON_HEIGHT
DEFAULT_ITEM_IMAGE_SIZE = (DEFAULT_ITEM_IMAGE_WIDTH, DEFAULT_ITEM_IMAGE_HEIGHT)

TREE_LIST_CTRL_IMAGE_LIST_CACHE_NAME = '__image_list_cache'


class iqTreeListCtrlManager(base_manager.iqBaseManager):
    """
    TreeListCtrl manager.
    """
    def _setTreeListCtrlData(self, treelistctrl=None, tree_data=None,
                             columns=(), image=None,
                             ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param image: Image as attribute name.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if not tree_data:
            log_func.warning(u'Not define tree data of wx.TreeListCtrl control')
            return False

        treelistctrl.GetMainWindow().DeleteAllItems()
        self.appendTreeListCtrlBranch(treelistctrl=treelistctrl, node=tree_data, columns=columns, image=image, ext_func=ext_func)

        if do_expand_all:
            treelistctrl.GetMainWindow().ExpandAll()
        return True

    def setTreeListCtrlData(self, treelistctrl=None, tree_data=None,
                            columns=(), image=None,
                            ext_func=None, do_expand_all=False):
        """
        Set tree data of control wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
        :param tree_data: Tree data:
        :param columns: Columns as tuple.
        :param image: Image as attribute name.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setTreeListCtrlData(treelistctrl, tree_data, columns, image, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of wx.TreeListCtrl control.')
        return False

    def _appendTreeListCtrlBranch(self, treelistctrl=None, parent_item=None, node=None,
                                  columns=(), image=None, ext_func=None):
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
        :param image: Image as attribute name: 'image key'.
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
                                                       columns=columns, image=image, ext_func=ext_func)
                return result
            elif (isinstance(node, list) or isinstance(node, tuple)) and len(node) == 1:
                node = node[0]
                parent_item = self.addTreeListCtrlRootItem(treelistctrl, node, columns, image, ext_func)
            elif isinstance(node, dict):
                parent_item = self.addTreeListCtrlRootItem(treelistctrl, node, columns, image, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in wx.TreeListCtrl manager' % str(type(node)))
                return False

        for record in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            label = str(record.get(columns[0], u''))
            # Normal or checkable item
            item_type = 1 if treelistctrl.GetWindowStyle() & wx.dataview.TL_CHECKBOX else 0
            item = treelistctrl.GetMainWindow().AppendItem(parent_item, label, ct_type=item_type)
            for i, column in enumerate(columns[1:]):
                label = str(record.get(columns[i + 1], u''))
                treelistctrl.GetMainWindow().SetItemText(item, label, i + 1)

            if ext_func:
                try:
                    ext_func(treelistctrl, item, record)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            treelistctrl.GetMainWindow().SetItemData(item, record)

            if image is not None:
                self.setTreeListCtrlItemImage(treelistctrl=treelistctrl, item=item, image=image)

            if spc_func.CHILDREN_ATTR_NAME in record and record[spc_func.CHILDREN_ATTR_NAME]:
                for child in record[spc_func.CHILDREN_ATTR_NAME]:
                    self.appendTreeListCtrlBranch(treelistctrl, item, child, columns=columns, image=image, ext_func=ext_func)

    def appendTreeListCtrlBranch(self, treelistctrl=None, parent_item=None, node=None,
                                 columns=(), image=None, ext_func=None):
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
        :param image: Image as attribute name: 'image key'.
        :param ext_func: Extended function.
        :return: True/False.
        """
        try:
            return self._appendTreeListCtrlBranch(treelistctrl, parent_item, node, columns, image, ext_func)
        except:
            log_func.fatal(u'Add branch to node of wx.TreeListCtrl control error')
        return False

    def addTreeListCtrlRootItem(self, treelistctrl=None, node=None,
                                columns=(), image=None, ext_func=None):
        """
        Add root item.

        :param image: Image as attribute name: 'image key'.
        :return:
        """
        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        label = str(node.get(columns[0], base_manager.UNKNOWN))
        # Normal or checkable item
        item_type = 1 if treelistctrl.GetWindowStyle() & wx.dataview.TL_CHECKBOX else 0
        parent_item = treelistctrl.GetMainWindow().AddRoot(label, ct_type=item_type)

        for i, column in enumerate(columns[1:]):
            label = str(node.get(columns[i + 1], base_manager.UNKNOWN))
            treelistctrl.GetMainWindow().SetItemText(parent_item, label, i + 1)

        if ext_func:
            try:
                ext_func(treelistctrl, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))

        treelistctrl.GetMainWindow().SetItemData(parent_item, node)

        if image is not None:
            self.setTreeListCtrlItemImage(treelistctrl=treelistctrl, item=parent_item, image=image)

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

    def getTreeListCtrlItemLevelIdx(self, treelistctrl=None, item=None):
        """
        Determine the level of the tree item.
        For example, the root item has level 0.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item.
            If None, then the root element is taken.
        :return: Level index or None if error.
        """
        label_path = self.getTreeListCtrlItemPathLabel(treelistctrl=treelistctrl, item=item)
        return len(label_path) if label_path is not None else None

    def getTreeListCtrlItemPathLabel(self, treelistctrl=None, item=None, cur_path=None):
        """
        The path to the item. Path is a list of element names.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Item.
            If None, then the root element is taken.
        :param cur_path: Current filled path.
        :return: Path list to item or None if error.
        """
        if treelistctrl is None:
            log_func.warning(u'Not define wx.TreeListCtrl object')
            return None

        try:
            if item is None:
                # The root element has an empty path
                return []

            parent = treelistctrl.GetItemParent(item)
            # If there is a parent item, then call recursively
            if parent and parent.IsOk():
                if cur_path is None:
                    cur_path = []
                cur_path.insert(-1, treelistctrl.GetItemText(item))
                return self.getTreeListCtrlItemPathLabel(treelistctrl=treelistctrl, item=parent, cur_path=cur_path)

            if cur_path is None:
                # This is the root item.
                cur_path = []
            return cur_path
        except:
            log_func.fatal(u'Error get level path in <%s>' % str(treelistctrl))
        return None

    def getTreeListCtrlImageIndex(self, treelistctrl=None, image=None, auto_add=True):
        """
        Searching for an image in the image list wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
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
            log_func.warning(u'Unsupported image type <%s : %s>' % (image.__class__.__name__, str(image)))
            return -1

        # First check in the cache
        img_cache = self.getTreeListCtrlImageListCache(treelistctrl=treelistctrl)

        img_idx = -1
        if img_id in img_cache:
            img_idx = img_cache[img_id]
        else:
            if auto_add:
                image_list = self.getTreeListCtrlImageList(treelistctrl=treelistctrl)
                img_idx = image_list.Add(image)
                # Save to cache
                img_cache[img_id] = img_idx
        return img_idx

    def getTreeListCtrlImageList(self, treelistctrl=None, image_width=DEFAULT_ITEM_IMAGE_WIDTH,
                                 image_height=DEFAULT_ITEM_IMAGE_HEIGHT):
        """
        Get a list of pictures of elements of the tree control wx.TreeListCtrl.

        :param treelistctrl: wx.TreeListCtrl control.
        :param image_width: Image width.
        :param image_height: Image height.
        :return: wx.ImageList object.
        """
        if treelistctrl is None:
            log_func.warning(u'Not define wx.TreeListCtrl object')
            return None

        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        image_list = treelistctrl.GetImageList()
        if not image_list:
            image_list = wx.ImageList(image_width, image_height)
            # [NOTE] Add empty Bitmap
            empty_dx = image_list.Add(wxbitmap_func.createEmptyBitmap(image_width, image_height))
            treelistctrl.SetImageList(image_list)
        return image_list

    def getTreeListCtrlImageListCache(self, treelistctrl=None):
        """
        Image list cache.

        :param treelistctrl: wx.TreeListCtrl control.
        """
        if treelistctrl is None:
            log_func.warning(u'Not define wx.TreeListCtrl object')
            return None

        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if not hasattr(treelistctrl, TREE_LIST_CTRL_IMAGE_LIST_CACHE_NAME):
            setattr(treelistctrl, TREE_LIST_CTRL_IMAGE_LIST_CACHE_NAME, dict())
        return getattr(treelistctrl, TREE_LIST_CTRL_IMAGE_LIST_CACHE_NAME)

    def setTreeListCtrlItemImage(self, treelistctrl=None, item=None, image=None):
        """
        Set tree item image.

        :param treelistctrl: wx.TreeListCtrl control.
        :param item: Tree item.
            If not specified, it is considered to be the root element.
        :param image: wx.Bitmap object/Icon name/Image filename/Item data key
            If not specified, the image is deleted.
        :return: True/False.
        """
        if treelistctrl is None:
            log_func.warning(u'Not define wx.TreeListCtrl object')
            return None

        assert issubclass(treelistctrl.__class__, wx.lib.gizmos.TreeListCtrl), u'TreeListCtrl manager type error'

        if item is None:
            item = treelistctrl.GetRootItem()

        if image is None:
            treelistctrl.SetItemImage(item, None)
        else:
            if image and isinstance(image, str):
                # If item image as icon name or image filename
                item_data = self.getTreeListCtrlItemData(treelistctrl=treelistctrl, item=item)
                img = item_data[image] if item_data and image in item_data else image
                # log_func.debug(u'Image <%s>. Item data %s' % (str(img), str(item_data)))
                if isinstance(img, str) and os.path.exists(img):
                    # Image as filename
                    # log_func.debug(u'Set item image as filename <%s>' % img)
                    image = wxbitmap_func.createBitmap(img)
                elif isinstance(img, str) and icon_func.existsIconFile(img):
                    # Image as icon name
                    # log_func.debug(u'Set item image as icon <%s>' % img)
                    image = wxbitmap_func.createIconBitmap(img)
                elif isinstance(img, wx.Bitmap):
                    image = img
                elif isinstance(img, wx.Image):
                    image = img
                else:
                    image = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU)

            if image is not None:
                img_idx = self.getTreeListCtrlImageIndex(treelistctrl=treelistctrl, image=image, auto_add=True)
                treelistctrl.SetItemImage(item, img_idx)
            else:
                return False
        return True
