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

__version__ = (0, 0, 2, 1)

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
        if isinstance(item, int):
            # Get item as row
            model = treeview.get_model()
            item = model[item].iter

        assert issubclass(item.__class__, gi.repository.Gtk.TreeIter), u'GtkTreeIter item type error'

        item_data_cache_attribute_name = ITEM_DATA_CACHE_ATTRIBUTE_NAME_FMT % treeview.get_name()
        if not hasattr(self, item_data_cache_attribute_name):
            setattr(self, item_data_cache_attribute_name, dict())
        item_data_cache_attribute = getattr(self, item_data_cache_attribute_name)

        item_id = treeview.get_model().get_value(item, 0)
        if item_id not in item_data_cache_attribute:
            log_func.warning(u'Item <%s> not found in cache' % item_id)
        # log_func.debug(u'Find <%s> item' % item_id)
        return item_data_cache_attribute.get(item_id, None)

    def _setGtkTreeViewData(self, treeview=None, tree_data=None, columns=(),
                            ext_func=None, do_expand_all=False):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param columns: Item data keys for fill columns.
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
        self.appendGtkTreeViewBranch(treeview=treeview, node=tree_data, columns=columns, ext_func=ext_func)

        if do_expand_all:
            treeview.expand_all()
        return True

    def setGtkTreeViewData(self, treeview=None, tree_data=None, columns=(),
                           ext_func=None, do_expand_all=False):
        """
        Set tree data of control GtkTreeView.

        :param treeview: GtkTreeView control.
        :param tree_data: Tree data:
        :param columns: Item data keys for fill columns.
        :param ext_func: Extended function.
        :param do_expand_all: Auto expand all items?
        :return: True/False.
        """
        try:
            return self._setGtkTreeViewData(treeview=treeview, tree_data=tree_data,
                                            columns=columns, ext_func=ext_func, do_expand_all=do_expand_all)
        except:
            log_func.fatal(u'Set tree data of Gtk.TreeView control')
        return False

    def _initGtkTreeViewRow(self, treeview=None, node=None, guid=None, columns=()):
        """
        Init row.

        :param treeview: GtkTreeView control.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param guid: Item GUID.
        :param columns: Item data keys for fill columns.
        :return: GtkTreeview row tuple.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if guid is None:
            guid = id_func.genGUID()

        model = treeview.get_model()
        model_n_columns = model.get_n_columns()
        row = [guid]
        if model_n_columns:
            columns_count = len(columns)
            for i in range(model_n_columns)[1:]:
                column_type = model.get_column_type(i).name
                if i <= columns_count:
                    key = columns[i - 1]
                    if isinstance(node, dict) and key:
                        value = node.get(key, key)
                    elif not isinstance(node, dict) and key:
                        value = key
                    else:
                        log_func.warning(u'Not valid column key <%s> in item data for column <%d>' % (key, i))
                        value = u''
                else:
                    log_func.warning(u'Not define column key in item data for column <%d>' % i)
                    value = u''
                #
                if column_type == 'gchararray':
                    value = str(value) if value is not None else u''
                elif column_type == 'gboolean':
                    value = bool(value) if value else False
                elif column_type in ('gint', 'guint', 'glong', 'gint64', 'guint64'):
                    value = int(value) if value else 0
                elif column_type in ('gfloat', 'gdouble'):
                    value = float(value) if value else 0.0
                else:
                    log_func.warning(u'Not supported column <%d> type <%s> in <%s>' % (i, column_type,
                                                                                       self.__class__.__name__))
                row.append(value)
        # log_func.debug(u'GtkTreeView init row %s' % str(row))
        return tuple(row)

    def _appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None,
                                 columns=(), ext_func=None):
        """
        Add branch data to node of GtkTreeView control.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param columns: Item data keys for fill columns.
        :param ext_func: Extended function.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if parent_item is None:
            if isinstance(node, (list, tuple)):
                log_func.debug(u'Create UNKNOWN root item of GtkTreeView control')
                # parent_item = self.addGtkTreeViewRootItem(treeview=treeview, node=node,
                #                                           columns=columns, ext_func=ext_func)
                for item in node:
                    result = self._appendGtkTreeViewBranch(treeview, parent_item=parent_item,
                                                           # node={spc_func.CHILDREN_ATTR_NAME: node},
                                                           node=item,
                                                           columns=columns, ext_func=ext_func)
                return result
            elif isinstance(node, dict):
                item = self.addGtkTreeViewRootItem(treeview, node, columns=columns, ext_func=ext_func)
            else:
                log_func.warning(u'Node type <%s> not support in GtkTreeView manager' % str(type(node)))
                return False
        else:
            model = treeview.get_model()
            row = self._initGtkTreeViewRow(treeview=treeview, node=node, columns=columns)
            item = model.append(parent_item, row)

            if ext_func:
                try:
                    ext_func(treeview, item, node)
                except:
                    log_func.fatal(u'Extended function <%s> error' % str(ext_func))

            self.setGtkTreeViewItemData(treeview=treeview, item=item, item_data=node)

        # Create children items
        if isinstance(node, dict):
            for child in node.get(spc_func.CHILDREN_ATTR_NAME, list()):
                self._appendGtkTreeViewBranch(treeview, item, child,
                                              columns=columns, ext_func=ext_func)
        elif isinstance(node, list):
            for child in node:
                self._appendGtkTreeViewBranch(treeview, item, child,
                                              columns=columns, ext_func=ext_func)

    def appendGtkTreeViewBranch(self, treeview=None, parent_item=None, node=None,
                                columns=(), ext_func=None):
        """
        Add branch data to node of GtkTreeView control.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent item.
            If None then create root item.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param columns: Item data keys for fill columns.
        :param ext_func: Extended function.
        :return: True/False.
        """
        try:
            return self._appendGtkTreeViewBranch(treeview, parent_item, node,
                                                 columns=columns, ext_func=ext_func)
        except:
            log_func.fatal(u'Add branch to node of GtkTreeView control error')
        return False

    def addGtkTreeViewRootItem(self, treeview=None, node=None, columns=(), ext_func=None):
        """
        Add root item.

        :param treeview: GtkTreeView control.
        :param node: Item data.
            If item data is dictionary then add node.
            If item data is list then add nodes.
        :param columns: Item data keys for fill columns.
        :param ext_func: Extended function.
        :return: Root item.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        model = treeview.get_model()
        row = self._initGtkTreeViewRow(treeview=treeview, node=node, columns=columns)
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
                                   columns=(), image=None, data=None, select=True):
        """
        Add a child item of the tree.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent tree item.
            If not specified, it is considered to be the root element.
        :param columns: Item data keys for fill columns.
        :param image: New item image.
        :param data: Data automatically attached to the new item.
        :param select: Automatically select a new item?
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
            row = self._initGtkTreeViewRow(treeview=treeview, node=data, columns=columns)
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

    def getGtkTreeViewSelectedRow(self, treeview=None):
        """
        Get selected row index.

        :param treeview: GtkTreeView control.
        :return: Selected row index or -1 if not selected.
        """
        selection = treeview.get_selection()
        model, selected_item = selection.get_selected()
        if selected_item:
            path = selected_item.get_selected_rows()[0]
            row_index = path.get_indices()[0]
            return row_index
        return -1

    def getGtkTreeViewSelectedItem(self, treeview=None):
        """
        Get selected item.

        :param treeview: GtkTreeView control.
        :return: Selected item or None if not selected.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        selection = treeview.get_selection()
        model, selected_item = selection.get_selected()
        return selected_item

    def setGtkTreeViewRowColor(self, treeview=None, row=None, store_color_column=-1, color=None):
        """
        Set tree row text color.

        :param treeview: GtkTreeView control.
        :param row: Row index. If not defined then get selected row.
        :param color: Color as text. For example 'green' or '#00ff00'.
        :param store_color_column: Store model column index for color.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if row is None:
            row = self.getGtkTreeViewSelectedRow(treeview=treeview)

        if isinstance(row, int):
            if row >= 0:
                model = treeview.get_model()
                row_obj = model[row]
                model[row_obj.iter][store_color_column] = color
                return True
            else:
                log_func.warning(u'Not valid row index <%s>' % row)
        elif issubclass(row.__class__, gi.repository.Gtk.TreeIter):
            model = treeview.get_model()
            model[row][store_color_column] = color
            return True
        return False

    def setGtkTreeViewRowForegroundColor(self, treeview=None, row=None, store_color_column=-1, color=None):
        """
        Set tree row text color.

        :param treeview: GtkTreeView control.
        :param row: Row index. If not defined then get selected row.
        :param store_color_column: Store model column index for color.
        :param color: Color as text. For example 'green' or '#00ff00'.
        :return: True/False.
        """
        return self.setGtkTreeViewRowColor(treeview=treeview, row=row,
                                           store_color_column=store_color_column, color=color)

    def setGtkTreeViewRowBackgroundColor(self, treeview=None, row=None, store_color_column=-1, color=None):
        """
        Set tree row background color.

        :param treeview: GtkTreeView control.
        :param row: Row index. If not defined then get selected row.
        :param store_color_column: Store model column index for color.
        :param color: Color as text. For example 'green' or '#00ff00'.
        :return: True/False.
        """
        return self.setGtkTreeViewRowColor(treeview=treeview, row=row,
                                           store_color_column=store_color_column, color=color)

    def setGtkTreeViewRowsColorExpression(self, treeview=None,
                                          fg_color=None, bg_color=None,
                                          fg_color_column=-1, bg_color_column=-1,
                                          expression=None, item=None):
        """
        Set rows foreground/background color if expression return True.

        :param treeview: GtkTreeView control.
        :param fg_color: Foreground color, if expression return True.
        :param bg_color: Background color, if expression return True.
        :param fg_color_column: Store model column index for foreground color.
        :param bg_color_column: Store model column index for background color.
        :param expression: lambda expression:
            lambda row: ...
            return True/False.
        :param item: Model item. If None then get root items.
        :return: True/False.
        """
        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if expression is None:
            log_func.warning(u'GtkTreeView. Not define expression for set rows color')
            return False

        if fg_color is None and bg_color is None:
            log_func.warning(u'Not define foreground/background color')
            return False

        model = treeview.get_model()
        result = True
        if item is None:
            for row, model_row in enumerate(model):
                item =model_row.iter
                result = result and self.setGtkTreeViewRowsColorExpression(treeview=treeview,
                                                                           fg_color=fg_color,
                                                                           bg_color=bg_color,
                                                                           fg_color_column=fg_color_column,
                                                                           bg_color_column=bg_color_column,
                                                                           expression=expression,
                                                                           item=item)
        else:
            colorize = expression(item)
            if fg_color and colorize:
                self.setGtkTreeViewRowForegroundColor(treeview=treeview, row=item,
                                                      store_color_column=fg_color_column,
                                                      color=fg_color)
            if bg_color and colorize:
                self.setGtkTreeViewRowBackgroundColor(treeview=treeview, row=item,
                                                      store_color_column=bg_color_column,
                                                      color=bg_color)

            if model.iter_has_child(item):
                child = model.iter_children(item)
                while child is not None:
                    result = result and self.setGtkTreeViewRowsColorExpression(treeview=treeview,
                                                                               fg_color=fg_color,
                                                                               bg_color=bg_color,
                                                                               fg_color_column=fg_color_column,
                                                                               bg_color_column=bg_color_column,
                                                                               expression=expression,
                                                                               item=child)
                    child = model.iter_next(child)
        return result

    def hasGtkTreeViewItemChildren(self, treeview=None, item=None):
        """
        Has tree item children?

        :param treeview: GtkTreeView control.
        :param item: Parent tree item.
            If not specified, it is considered to be the root element.
        :return: True/False.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        try:
            model = treeview.get_model()
            return model.iter_has_child(item)
        except:
            log_func.fatal(u'Error has tree view item children')
        return None

    def getGtkTreeViewFirstChild(self, treeview=None, parent_item=None):
        """
        Get first parent item child.

        :param treeview: GtkTreeView control.
        :param parent_item: Parent tree item.
            If not specified, it is considered to be the root element.
        :return: Item or None.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if parent_item is None:
            parent_item = self.getGtkTreeViewRootItem(treeview=treeview)

        try:
            model = treeview.get_model()
            return model.iter_children(parent_item)
        except:
            log_func.fatal(u'Error get first tree view child')
        return None

    def getGtkTreeViewNextChild(self, treeview=None, item=None):
        """
        Get next parent item child.

        :param treeview: GtkTreeView control.
        :param item: Current tree item.
            If not specified, it is considered to be the root element.
        :return: Item or None.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        try:
            model = treeview.get_model()
            return model.iter_next(item)
        except:
            log_func.fatal(u'Error get next tree view child')
        return None

    def getGtkTreeViewParentItem(self, treeview=None, item=None):
        """
        Get parent item.

        :param treeview: GtkTreeView control.
        :param item: Current tree item.
            If not specified, it is considered to be the selected element.
        :return: Item or None.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            item = self.getGtkTreeViewSelectedItem(treeview=treeview)

        if item is None:
            log_func.warning(u'Not define item for get parent item')
            return None

        try:
            model = treeview.get_model()
            return model.iter_parent(item)
        except:
            log_func.fatal(u'Error get parent item')
        return None

    def expandGtkTreeViewItem(self, treeview=None, item=None, expand_all=False):
        """
        Expand item.

        :param treeview: GtkTreeView control.
        :param item: Parent tree item.
            If not specified, it is considered to be the root element.
        :param expand_all: Expand all children?
        :return: True/False.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        try:
            model = treeview.get_model()
            item_path = model.get_path(item)
            treeview.expand_row(item_path, expand_all)  # doesn't work
            # treeview.expand_to_path(item_path)
            return True
        except:
            log_func.fatal(u'Error expand treeview item')
        return False

    def collapseGtkTreeViewItem(self, treeview=None, item=None):
        """
        Collapse item.

        :param treeview: GtkTreeView control.
        :param item: Parent tree item.
            If not specified, it is considered to be the root element.
        :return: True/False.
        """
        if treeview is None:
            log_func.warning(u'Not define GtkTreeView object')
            return None

        assert issubclass(treeview.__class__, gi.repository.Gtk.TreeView), u'GtkTreeView manager type error'

        if item is None:
            item = self.getGtkTreeViewRootItem(treeview=treeview)

        try:
            model = treeview.get_model()
            item_path = model.get_path(item)
            treeview.collapse_row(item_path)
            return True
        except:
            log_func.fatal(u'Error collapse treeview item')
        return False
