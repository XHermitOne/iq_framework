#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkTreeView manager.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func
from ...util import spc_func

from . import base_manager

__version__ = (0, 0, 0, 1)

ITEM_DATA_ATTRIBUTE_NAME = '__gtktreeview_item_data_%s__'


class iqGtkTreeViewManager(base_manager.iqBaseManager):
    """
    GtkTreeView manager.
    """
    def setGtkTreeViewItemData(self, treeview=None, item=None, item_data=None):
        """
        Set item data.

        :param treeview: GtkTreeView control.
        :param item: GtkTreeIter model store item.
        :param item_data: Item data.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'
        assert issubclass(item.__class__, gi.repository.Gtk.TreeIter), u'GtkTreeIter item type error'

        item_data_attribute_name = ITEM_DATA_ATTRIBUTE_NAME % treeview.get_name()
        if not hasattr(self, item_data_attribute_name):
            setattr(self, item_data_attribute_name, dict())
        item_data_attrubute = getattr(self, item_data_attribute_name)
        item.user_data3 = len(item_data_attrubute)
        item_data_attrubute[item.user_data3] = item_data
        return True

    def getGtkTreeViewItemData(self, treeview=None, item=None):
        """
        Set item data.

        :param treeview: GtkTreeView control.
        :param item: Model store item.
        :return: Item data or None.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            model = treeview.get_model()
            row = model[0]
            item = row.iter

        assert issubclass(item.__class__, gi.repository.Gtk.TreeIter), u'GtkTreeIter item type error'

        item_data_attribute_name = ITEM_DATA_ATTRIBUTE_NAME % treeview.get_name()
        if not hasattr(self, item_data_attribute_name):
            setattr(self, item_data_attribute_name, dict())
        item_data_attrubute = getattr(self, item_data_attribute_name)
        return item_data_attrubute.get(item.user_data3, None)

    def _setGtkTreeViewData(self, treeview=None, tree_data=None, label='name',
                            ext_func=None, do_expand_all=False):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if not tree_data:
            log_func.warning(u'Not define tree data of GtkTreeView control')
            return False

        model = treeview.get_model()
        model.clear()
        self.appendGtkTreeViewBranch(treeview=treeview, node=tree_data, label=label, ext_func=ext_func)

        if do_expand_all:
            treeview.ExpandAll()
        return True

    def setGtkTreeViewData(self, treeview=None, tree_data=None, label='name',
                           ext_func=None, do_expand_all=False):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setGtkTreeViewData(treeview, tree_data, label, ext_func, do_expand_all)
        except:
            log_func.fatal(u'Set tree data of Gtk.TreeView control')
        return False

    def _appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None, label='name', ext_func=None):
        """
        Add branch data to node of GtkTreeView control.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param label: Key as label. For example 'name'.
        :param ext_func: Extended function.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if parent_item is None:
            if isinstance(node, (list, tuple)):
                log_func.debug(u'Create UNKNOWN root item of GtkTreeView control')
                parent_item = treeview.AddRoot(base_manager.UNKNOWN)
                result = self._appendGtkTreeViewBranch(treeview, parent_item=parent_item,
                                                       node={spc_func.CHILDREN_ATTR_NAME: node},
                                                       label=label, ext_func=ext_func)
                return result
            elif isinstance(node, dict):
                item = self.addGtkTreeViewRootItem(treeview, node, label, ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in GtkTreeView manager' % str(type(node)))
                return False
        else:
            item_label = str(node.get(label, u''))
            log_func.debug(u'Append tree item data <%s> %s' % (item_label, str(node.get(spc_func.CHILDREN_ATTR_NAME, None))))
            model = treeview.get_model()
            item = model.append(parent_item, [item_label])

            if ext_func:
                try:
                    ext_func(treeview, item, node)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            self.setGtkTreeViewItemData(treeview=treeview, item=item, item_data=node)

        # Create children items
        for child in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            self._appendGtkTreeViewBranch(treeview, item, child, label=label, ext_func=ext_func)

    def appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None, label='name', ext_func=None):
        """
        Add branch data to node of GtkTreeView control.

        :param treeview: GtkTreeView control.
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
            return self._appendGtkTreeViewBranch(treeview, parent_item, node, label, ext_func)
        except:
            log_func.fatal(u'Add branch to node of GtkTreeView control error')
        return False

    def addGtkTreeViewRootItem(self, treeview=None, node=None, label='name', ext_func=None):
        """
        Add root item.

        :return:
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        root_label = str(node.get(label, base_manager.UNKNOWN))
        model = treeview.get_model()
        parent_item = model.append(None, [root_label])
        log_func.debug(u'Add root item <%s>' % root_label)

        self.setGtkTreeViewItemData(treeview=treeview, item=parent_item, item_data=node)

        if ext_func:
            try:
                ext_func(treeview, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))
        return parent_item

    def getGtkTreeViewSelectedItemData(self, treeview=None):
        """
        Get selected item data.

        :param treeview: GtkTreeView control.
        :return: Item struct data or None if error.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        model, selected_item = widget.get_selected()
        if selected_item:
            return self.getGtkTreeViewItemData(treeview=treeview, item=selected_item)
        return None
