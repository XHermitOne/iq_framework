#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GtkTreeView manager.

NOTE:
To store the attached data of tree items,
the first column in the model
must be the item's GUID as gchararray.
"""

import gi
gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from ...util import log_func
from ...util import spc_func
from ...util import id_func

from . import base_manager

__version__ = (0, 0, 1, 1)

ITEM_DATA_CACHE_ATTRIBUTE_NAME_FMT = '__gtktreeview_item_data_cache_%s__'


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

        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        assert issubclass(item.__class__, gi.repository.Gtk.TreeIter), u'GtkTreeIter item type error'

        item_data_cache_attribute_name = ITEM_DATA_CACHE_ATTRIBUTE_NAME_FMT % treeview.get_name()
        if not hasattr(self, item_data_cache_attribute_name):
            setattr(self, item_data_cache_attribute_name, dict())
        item_data_cache_attribute = getattr(self, item_data_cache_attribute_name)

        try:
            item_id = treeview.get_model().get_value(item, 0)
        except:
            item_id = id_func.genGUID()
            log_func.warning(u'New generate GUID <%s> for cache' % item_id)
        item_data_cache_attribute[item_id] = item_data
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
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        assert issubclass(item.__class__, gi.repository.Gtk.TreeIter), u'GtkTreeIter item type error'

        item_data_cache_attribute_name = ITEM_DATA_CACHE_ATTRIBUTE_NAME_FMT % treeview.get_name()
        if not hasattr(self, item_data_cache_attribute_name):
            setattr(self, item_data_cache_attribute_name, dict())
        item_data_cache_attribute = getattr(self, item_data_cache_attribute_name)

        item_id = treeview.get_model().get_value(item, 0)
        # log_func.debug(u'Find <%s> in %s' % (item_id, item_id in item_data_cache_attribute))
        return item_data_cache_attribute.get(item_id, None)

    def _setGtkTreeViewData(self, treeview=None, tree_data=None, label='name',
                            ext_func=None, do_expand_all=False, column_keys=()):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :param column_keys: Item data keys for fill columns.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if not tree_data:
            log_func.warning(u'Not define tree data of GtkTreeView control')
            return False

        model = treeview.get_model()
        model.clear()
        self.appendGtkTreeViewBranch(treeview=treeview, node=tree_data, label=label, ext_func=ext_func,
                                     column_keys=column_keys)

        # if do_expand_all:
        #     treeview.ExpandAll()
        return True

    def setGtkTreeViewData(self, treeview=None, tree_data=None, label='name',
                           ext_func=None, do_expand_all=False, column_keys=()):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param label: Key as label.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :param column_keys: Item data keys for fill columns.
        :return: True/False.
        """
        try:
            return self._setGtkTreeViewData(treeview, tree_data, label, ext_func, do_expand_all,
                                            column_keys=column_keys)
        except:
            log_func.fatal(u'Set tree data of Gtk.TreeView control')
        return False

    def _initGtkTreeViewRow(self, treeview=None, node=None, guid=None, label='name', column_keys=()):
        """
        Init row.

        :param treeview: GtkTreeView control.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param guid: Item GUID.
        :param label: Key as label. For example 'name'.
        :param column_keys: Item data keys for fill columns.
        :return: GtkTreeview row tuple.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        item_label = str(node.get(label, label)) if isinstance(node, dict) else label
        if guid is None:
            guid = id_func.genGUID()

        columns = treeview.get_columns()
        row = [guid, item_label]
        if columns:
            column_keys_count = len(column_keys)
            for i, column in enumerate(columns[1:]):
                column_name = column.get_name()
                column_type = treeview.get_model().get_column_type(i + 1).name
                if i < column_keys_count:
                    key = column_keys[i]
                    if isinstance(node, dict) and key:
                        value = node.get(key, u'')
                    elif isinstance(node, dict) and column_name in node:
                        value = node.get(column_name, u'')
                    else:
                        log_func.warning(u'Not valid column key <%s> in item data for column <%s>' % (key, column_name))
                        value = u''
                else:
                    log_func.warning(u'Not define column key in item data for column <%s>' % column_name)
                    value = u''
                #
                if column_type == 'gchararray':
                    value = str(value)
                elif column_type == 'gboolean':
                    value = bool(value) if value else False
                elif column_type in ('gint', 'guint', 'glong', 'gint64', 'guint64'):
                    value = int(value) if value else 0
                elif column_type in ('gfloat', 'gdouble'):
                    value = float(value) if value else 0.0
                else:
                    log_func.warning(u'Not supported column <%s> type <%s> in <%s>' % (column_name,
                                                                                       column_type,
                                                                                       self.__class__.__name__))
                row.append(value)
        log_func.debug(u'GtkTreeView init row %s' % str(row))
        return tuple(row)

    def _appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None, label='name',
                                 ext_func=None, column_keys=()):
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
        :param column_keys: Item data keys for fill columns.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if parent_item is None:
            if isinstance(node, (list, tuple)):
                log_func.debug(u'Create UNKNOWN root item of GtkTreeView control')
                parent_item = self.addGtkTreeViewRootItem(treeview=treeview, node=node,
                                                          label=base_manager.UNKNOWN, ext_func=ext_func,
                                                          column_keys=column_keys)
                result = self._appendGtkTreeViewBranch(treeview, parent_item=parent_item,
                                                       node={spc_func.CHILDREN_ATTR_NAME: node},
                                                       label=label, ext_func=ext_func,
                                                       column_keys=column_keys)
                return result
            elif isinstance(node, dict):
                item = self.addGtkTreeViewRootItem(treeview, node, label, ext_func,
                                                   column_keys=column_keys)
            else:
                log_func.warning(u'Node type <%s> not support in GtkTreeView manager' % str(type(node)))
                return False
        else:
            model = treeview.get_model()
            row = self._initGtkTreeViewRow(treeview=treeview, node=node, label=label, column_keys=column_keys)
            item = model.append(parent_item, row)

            if ext_func:
                try:
                    ext_func(treeview, item, node)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            self.setGtkTreeViewItemData(treeview=treeview, item=item, item_data=node)

        # Create children items
        for child in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
            self._appendGtkTreeViewBranch(treeview, item, child, label=label, ext_func=ext_func,
                                          column_keys=column_keys)

    def appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None, label='name',
                                ext_func=None, column_keys=()):
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
        :param column_keys: Item data keys for fill columns.
        :return: True/False.
        """
        try:
            return self._appendGtkTreeViewBranch(treeview, parent_item, node, label, ext_func,
                                                 column_keys=column_keys)
        except:
            log_func.fatal(u'Add branch to node of GtkTreeView control error')
        return False

    def addGtkTreeViewRootItem(self, treeview=None, node=None, label='name', ext_func=None, column_keys=()):
        """
        Add root item.

        :param treeview: GtkTreeView control.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param label: Key as label.
        :param ext_func: Extended function.
        :param column_keys: Item data keys for fill columns.
        :return: Root item.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        model = treeview.get_model()
        row = self._initGtkTreeViewRow(treeview=treeview, node=node, label=label, column_keys=column_keys)
        parent_item = model.append(None, row)

        self.setGtkTreeViewItemData(treeview=treeview, item=parent_item, item_data=node)

        if ext_func:
            try:
                ext_func(treeview, parent_item, node)
            except:
                log_func.fatal(u'Extended function <%s> error' % str(ext_func))
        return parent_item

    def getGtkTreeViewRootItem(self, treeview=None):
        """
        Gte root item of tree.

        :param treeview: GtkTreeView control.
        :return: Root item or None if error.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        try:
            model = treeview.get_model()
            row = model[0]
            root_item = row.iter
            return root_item
        except:
            log_func.fatal(u'Error get root item in <%s>' % treeview.get_name())
        return None

    def getGtkTreeViewSelectedItemData(self, treeview=None):
        """
        Get selected item data.

        :param treeview: GtkTreeView control.
        :return: Item struct data or None if error.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        selection = treeview.get_selection()
        model, selected_item = selection.get_selected()
        if selected_item:
            return self.getGtkTreeViewItemData(treeview=treeview, item=selected_item)
        return None

    def setGtkTreeViewSelectedItemData(self, treeview=None, data=None):
        """
        Set selected item data.

        :param treeview: GtkTreeView control.
        :param data: Item data.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        selection = treeview.get_selection()
        model, selected_item = selection.get_selected()
        if selected_item:
            return self.setGtkTreeViewItemData(treeview=treeview, item=selected_item, data=data)
        return False

    def clearGtkTreeView(self, treeview=None):
        """
        Delete all items from GtkTreeView control.

        :param treeview: GtkTreeView control.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'
        try:
            model = treeview.get_model()
            model.clear()

            # Clear item data cache
            item_data_attribute_name = ITEM_DATA_CACHE_ATTRIBUTE_NAME_FMT % treeview.get_name()
            if hasattr(self, item_data_attribute_name):
                setattr(self, item_data_attribute_name, dict())

            return True
        except:
            log_func.fatal(u'Error clear GtkTreeView control')
        return False

    def appendGtkTreeViewChildItem(self, treeview=None, parent_item=None,
                                   label='name', image=None, data=None, select=True,
                                   column_keys=()):
        """
        Add a child item of the tree.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent tree item.
            If not specified, it is considered to be the root element.
        :param label: New item label.
        :param image: New item image.
        :param data: Data automatically attached to the new item.
        :param select: Automatically select a new item?
        :param column_keys: Item data keys for fill columns.
        :return: New tree item or None on error.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if parent_item is None:
            parent_item = self.getGtkTreeViewRootItem(treeview=treeview)

        # img_idx = self.getTreeCtrlImageIndex(treectrl=treectrl, image=image, auto_add=True)

        try:
            model = treeview.get_model()
            row = self._initGtkTreeViewRow(treeview=treeview, node=data, label=label, column_keys=column_keys)
            new_item = model.append(parent_item, row)
            # log_func.debug(u'Append item <%s>' % label)
            if data is not None:
                self.setGtkTreeViewItemData(treeview=treeview, item=new_item, item_data=data)

            if select:
                # treectrl.SelectItem(new_item)
                pass
            return new_item
        except:
            log_func.fatal(u'Error adding child item')
        return None
