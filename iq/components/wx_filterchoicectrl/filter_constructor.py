#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter constructor control.
"""

import wx
from wx.lib.agw import hypertreelist

from ...engine.wx import wxbitmap_func
from ...util import log_func
from ...util import lang_func

from . import label_event

from . import filter_builder_ctrl

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_ITEM_LABEL = ''


class iqFilterConstructorTreeList(hypertreelist.HyperTreeList):
    """
    Filter constructor control.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        kwargs['agwStyle'] = wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_DEFAULT_STYLE
        hypertreelist.HyperTreeList.__init__(self, *args, **kwargs)

        self.SetHilightFocusColour(wx.WHITE)
        self.SetHilightNonFocusColour(wx.WHITE)
        pen = wx.Pen(wx.WHITE)
        self.SetBorderPen(pen)

        # Environment
        self.environment = None
        
        # Root item
        self.root = None
        
        # Current selected item
        self._selected_item = None

    def clear(self):
        """
        Clear items.
        """
        if self.GetMainWindow():
            self._selected_item = None
            result = self.GetMainWindow().DeleteAllItems()
            if self.root:
                self.GetMainWindow().DeleteItemWindow(self.root)
            return result
        return None
        
    def setEnvironment(self, env=None):
        """
        Set environment.

        :param env: Environment.
            Format: filter_builder_env.FILTER_ENVIRONMENT.
        """
        self.environment = env
        
    def getFilterData(self):
        """
        Get filter data.
        """
        return self._getFilterData()

    def setFilterData(self, result):
        """
        Set filter data.
        """
        self._addDefaultColumn()
        self.clear()
        result = self._setFilterData(result)
        # Expand root item
        self.expandRoot()
        return result
        
    def getColumnCount(self):
        """
        Get column count.
        """
        if self.GetMainWindow():
            return self.GetMainWindow().GetColumnCount()
        return -1
    
    _column_width = (75, 200, 100, 250, 250)

    def _addDefaultColumn(self):
        """
        Add columns by default.
        """
        cols = [_(u'Group'),
                _(u'Attribute'),
                _(u'Compare'),
                _(u'Argument 1'),
                _(u'Argument 2')]
        if self.getColumnCount() <= 0:
            for i in range(5):
                self.AddColumn(cols[i], width=self._column_width[i])
        
    def expandRoot(self):
        """
        Expand root item.
        """
        if self.root:
            self.Expand(self.root)
     
    def addGroup(self, item=None, auto_expand=True):
        """
        Add group into item.

        :return: New item.
        """
        logic_combobox = filter_builder_ctrl.iqLogicLabelChoice(self.GetMainWindow(),
                                                                self.environment['logic'])
        logic_combobox.Select(0)

        plus_small_img = wxbitmap_func.createIconBitmap('fugue/plus-small')
        add_button = filter_builder_ctrl.iqBitmapButton(self.GetMainWindow(), -1,
                                                        bitmap=plus_small_img,
                                                        size=(plus_small_img.GetWidth() + 8,
                                                              plus_small_img.GetHeight() + 8),
                                                        style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.onAddButtonMouseClick, add_button)
        
        if item is None:
            # If item is None then add root item
            self.root = self.AddRoot(DEFAULT_ITEM_LABEL, wnd=add_button)
            item = self.root
            new_item = self.root
        else:
            new_item = self.Append(item, DEFAULT_ITEM_LABEL, wnd=add_button)
        self.SetPyData(new_item, 'group')

        # Set controls
        self.SetItemWindow(new_item, logic_combobox, 1)

        if auto_expand:
            if not self.IsExpanded(item):
                self.Expand(item)
        return new_item

    def delGroup(self, item=None):
        """
        Delete group.
        """
        if item:
            if item == self.root:
                # If the root item is deleted, then clear everything and create a default root
                pass
            else:
                parent = self.GetItemParent(item)
                prev_item = self.GetPrevSibling(item)
                self.Delete(item)
                if prev_item:
                    self.SelectItem(prev_item)
                elif parent:
                    self.SelectItem(parent)
                
    def addCompare(self, item=None, auto_expand=True):
        """
        Add compare.

        :return: New item.
        """
        requisite_combobox = filter_builder_ctrl.iqRequisiteLabelChoice(self.GetMainWindow(),
                                                                        self.environment['requisites'])
        requisite_combobox.Bind(label_event.EVT_LABEL_CHANGE,
                                self.onRequisiteChangeComboBox)

        cross_small_img = wxbitmap_func.createIconBitmap('fugue/cross-small')
        del_button = filter_builder_ctrl.iqBitmapButton(self.GetMainWindow(), -1,
                                                        bitmap=cross_small_img,
                                                        size=(cross_small_img.GetWidth() + 8,
                                                              cross_small_img.GetHeight() + 8),
                                                        style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.onDelButtonMouseClick, del_button)
        
        new_item = self.AppendItem(item, DEFAULT_ITEM_LABEL, wnd=del_button)
        self.SetPyData(new_item, 'compare')

        self.SetItemWindow(new_item, requisite_combobox, 1)

        if auto_expand:
            if not self.IsExpanded(item):
                self.Expand(item)
        return new_item
                
    def delCompare(self, item=None):
        """
        Delete compare.
        """
        if item:
            parent = self.GetItemParent(item)
            prev_item = self.GetPrevSibling(item)
            self.Delete(item)
            if prev_item:
                self.SelectItem(prev_item)
            elif parent:
                self.SelectItem(parent)
        
    def setFuncChoice(self, item, requisite_combobox):
        """
        Set in the specified control element the selection of
        functions corresponding to the selected attribute.
        """
        requisite = requisite_combobox.getSelectedRequisite()
        func_lst = self._getFuncList(requisite['funcs'], self.environment)
        # If there are already controls in the element that depend
        # on the selected attribute, then delete them
        for i_col in range(2, self.GetColumnCount()):
            item.DeleteWindow(i_col)
            
        # Add combobox selection function comparison
        func_combobox = filter_builder_ctrl.iqFuncLabelChoice(self.GetMainWindow(), func_lst)

        func_combobox.Bind(label_event.EVT_LABEL_CHANGE, self.onFuncChangeComboBox)
        # Set controls
        self.SetItemWindow(item, func_combobox, 2)
        
    def setArgsEdit(self, item, function_combobox):
        """
        Set the controls for editing the arguments corresponding
        to the selected function to the specified element.
        """
        from . import filter_builder_env

        func = function_combobox.getSelectedFunc()
        args_lst = func['args']
        # If there are already controls in the element that depend
        # on the selected attribute, then delete them
        for i_col in range(3, self.GetColumnCount()):
            item.DeleteWindow(i_col)
        # Add argument editor
        i_col = 3
        for arg in args_lst:
            if 'type' not in arg:
                if 'ext_edit' in arg and arg['ext_edit']:
                    if not arg['ext_edit']:
                        # Advanced editor not defined
                        arg_edit = filter_builder_ctrl.iqCustomArgEdit(self.GetMainWindow(), arg)
                    else:
                        ext_args = ()
                        if 'ext_args' in arg and arg['ext_args']:
                            ext_args = arg['ext_args']
                        ext_kwargs = ()
                        if 'ext_kwargs' in arg and arg['ext_kwargs']:
                            ext_kwargs = arg['ext_kwargs']
                        # The advanced editor is set explicitly
                        arg_edit = arg['ext_edit'](parent=self.GetMainWindow(),
                                                   id=wx.NewId(), *ext_args, **ext_kwargs)

                        requisite_combobox = self.GetItemWindow(item, 1)
                        requisite = requisite_combobox.getSelectedData() or {}
                        if requisite.get('type', None) == filter_builder_env.REQUISITE_TYPE_REF:
                            psp = requisite.get('link_psp', None)
                            # log_func.debug(u'Ref edit %s : %s' % (str(psp), str(arg_edit)))
                            if psp:
                                arg_edit.setRefObjByPsp(psp)
                            else:
                                log_func.warning(u'Not define ref object passport in requisite <%s>' % requisite['requisite'])
                        else:
                            log_func.warning(u'Incorrect requisite type <%s : %s : %s : %s>' % (requisite.get('name', None), requisite.get('type', None), str(arg_edit), str(requisite_combobox)))
                else:
                    # Create string editor by default
                    arg_edit = filter_builder_ctrl.iqStrArgEdit(self.GetMainWindow(), arg)
            else:
                if arg['type'] == filter_builder_env.REQUISITE_TYPE_STR:
                    arg_edit = filter_builder_ctrl.iqStrArgEdit(self.GetMainWindow(), arg)
                elif arg['type'] in (filter_builder_env.REQUISITE_TYPE_INT,
                                     filter_builder_env.REQUISITE_TYPE_FLOAT,
                                     filter_builder_env.REQUISITE_TYPE_NUM):
                    arg_edit = filter_builder_ctrl.iqNumArgEdit(self.GetMainWindow(), arg)
                else:
                    log_func.warning(u'Not define type <%s> of argument <%s>' % (arg['type'], arg))
                    return None
        
            # Set controls
            if arg_edit:
                arg_edit_size = wx.Size(self.GetColumnWidth(i_col), -1)
                arg_edit.SetSize(arg_edit_size)

            self.SetItemWindow(item, arg_edit, i_col)
            i_col += 1
        
    def _getFuncList(self, funcs, env):
        """
        Get compare function list.
        """
        func_lst = list()
        if funcs:
            for func in funcs:
                if isinstance(func, str):
                    # The comparison function is given a name
                    func_lst.append(env['funcs'][func])
                else:
                    func_lst.append(func)
        else:
            log_func.warning(u'Filter constructor. Not define compare function list')
        return func_lst
        
    def _findItemByCtrl(self, ctrl, item=None):
        """
        Find which item corresponds to the specified control.
        """
        if item is None:
            item = self.root
        if item:
            col_count = self.getColumnCount()
            # Search by columns in the current item
            for i in range(col_count):
                window = self.GetItemWindow(item, i)
                if window == ctrl:
                    return item
            if item.HasChildren():
                # If not found in the current item, then search in child
                for child in item.GetChildren():
                    find_item = self._findItemByCtrl(ctrl, child)
                    if find_item:
                        return find_item
        # Not found
        return None
        
    def _getSelectedItem(self):
        """
        Get selected item.
        """
        return self._selected_item
    
    def _setSelectedItem(self, item):
        """
        Set selected item.
        """
        if self.GetMainWindow().GetRootItem():
            self._selected_item = item
            if self._selected_item:
                self.SelectItem(self._selected_item)
        
    def onAddButtonMouseClick(self, event):
        """ 
        The handler for clicking on the add new item button.
        """
        add_button = event.GetEventObject()
        # If you clicked on a button, then select the appropriate item
        tree_item = self._findItemByCtrl(add_button)
        self._setSelectedItem(tree_item)
            
        # Popup menu
        menu = wx.Menu()
        
        menuitem_id = wx.NewId()
        item = wx.MenuItem(menu, menuitem_id, _(u'Add compare'))
        bmp = wxbitmap_func.createIconBitmap('fugue/node-select-child')
        item.SetBitmap(bmp)
        menu.Append(item)
        self.Bind(wx.EVT_MENU, self.onAddCompareMenuItem, id=menuitem_id)
        
        menuitem_id = wx.NewId()
        item = wx.MenuItem(menu, menuitem_id, _(u'Add group'))
        bmp = wxbitmap_func.createIconBitmap('fugue/node-select')
        item.SetBitmap(bmp)
        menu.Append(item)
        self.Bind(wx.EVT_MENU, self.onAddGroupMenuItem, id=menuitem_id)
        
        if tree_item != self.root:
            menu.AppendSeparator()
            menuitem_id = wx.NewId()
            item = wx.MenuItem(menu, menuitem_id, _(u'Delete group'))
            bmp = wxbitmap_func.createIconBitmap('fugue/node-delete-previous')
            item.SetBitmap(bmp)
            menu.Append(item)
            self.Bind(wx.EVT_MENU, self.onClearMenuItem, id=menuitem_id)
        
        self.PopupMenu(menu)
        menu.Destroy()
        
        event.Skip()

    def onAddCompareMenuItem(self, event):
        """
        Add compare handler.
        """
        self.addCompare(self._getSelectedItem())
        event.Skip()
        
    def onAddGroupMenuItem(self, event):
        """
        Add group handler.
        """
        self.addGroup(self._getSelectedItem())
        event.Skip()
        
    def onClearMenuItem(self, event):
        """
        Clear all handler.
        """
        self.delGroup(self._getSelectedItem())
        event.Skip()

    def onDelButtonMouseClick(self, event):
        """
        Delete button mouse click handler.
        """
        del_button = event.GetEventObject()
        self._setSelectedItem(self._findItemByCtrl(del_button))
        self.delCompare(self._getSelectedItem())
        event.Skip()

    def onRequisiteChangeComboBox(self, event):
        """
        Change requisite in combobox handler.
        """
        # log_func.debug(u'Event <%s>' % str(event))
        requisite_combobox = event.getObject()
        self._setSelectedItem(self._findItemByCtrl(requisite_combobox))
        self.setFuncChoice(self._getSelectedItem(), requisite_combobox)
        event.Skip()
        
    def onFuncChangeComboBox(self, event):
        """
        Change compare function in combobox handler.
        """
        func_combobox = event.getObject()
        self._setSelectedItem(self._findItemByCtrl(func_combobox))
        self.setArgsEdit(self._getSelectedItem(), func_combobox)
        event.Skip()
        
    def setDefault(self):
        """
        Set default.
        """
        self._addDefaultColumn()
        self.clear()
        # Add root group item
        self.addGroup()
        # Expand root item
        self.expandRoot()
       
    def clearTree(self):
        """
        Clear filter tree.
        """
        self.clear()
        # Add root group item
        self.addGroup()
        # Expand root item
        self.expandRoot()
    
    def _getFilterData(self, item=None, add_pre_sql=False):
        """
        Get filter data.
        """
        if item is None:
            item = self.root
            
        item_data = {}
        
        type_item = self.GetPyData(item)
        if type_item == 'group':
            # Group
            item_data['type'] = type_item
            logic_combobox = self.GetItemWindow(item, 1)
            item_data['name'] = logic_combobox.getSelectedData()['name']
            item_data['logic'] = item_data['name']
            item_data['children'] = []
        elif type_item == 'compare':
            # Compare
            item_data['type'] = type_item
            
            requisite_combobox = self.GetItemWindow(item, 1)
            requisite = requisite_combobox.getSelectedData() or {'name': None}
            item_data['requisite'] = requisite['name']
            
            func_combobox = self.GetItemWindow(item, 2)
            func = None
            if func_combobox:
                func = func_combobox.getSelectedData() or {'name': None}
                item_data['function'] = func['name']

            for i_col in range(3, self.GetColumnCount()):
                arg_edit = self.GetItemWindow(item, i_col)
                if arg_edit:
                    key = 'arg_' + str(i_col - 2)
                    item_data[key] = arg_edit.getValue()

            # Additional function to get arguments
            if 'get_args' in func:
                item_data['get_args'] = func['get_args']

            # Add additional data to the filter data
            # for subsequent SQL generation
            if add_pre_sql:
                kwargs = dict()
                kwargs['requisite'] = requisite
                if func:
                    args = func['args']
                    for i, arg in enumerate(args):
                        value = item_data['arg_'+str(i+1)]
                        kwargs[arg['name']] = value
                    compare_function = func['function']
                    if compare_function:   
                        item_data['__sql__'] = compare_function(**kwargs)
        else:
            log_func.warning(u'Error define filter constructor item type <%s>' % type_item)
            return None
        
        # Add children items
        for cur_item in item.GetChildren():
            child = self._getFilterData(cur_item, add_pre_sql)
            if self._isValidRequisite(child):
                item_data['children'].append(child)
        return item_data
        
    def _isValidRequisite(self, req):
        """
        """
        if not req:
            return False
        
        if req.get('type', None) == 'compare' and (req.get('function', None) and
           req.get('requisite', None)):
            return True
        elif req.get('type', None) == 'group':
            return True
        return False
        
    def _setFilterData(self, data, item=None):
        """
        Set filter data.
        The function can only be launched after the environment is initialized.
        """
        result = True
        
        if item is None:
            self.clear()
            
        if data['type'] == 'group':
            # Add group
            grp_item = self.addGroup(item)
            
            logic_combobox = self.GetItemWindow(grp_item, 1)
            if logic_combobox:
                logic_combobox.selectByName(data['name'])
                
            if 'children' in data:
                # Add children items
                for child in data['children']:
                    result = result and self._setFilterData(child, grp_item)
                
        elif data['type'] == 'compare':
            # Add compare
            compare_item = self.addCompare(item)
            
            requisite_combobox = self.GetItemWindow(compare_item, 1)
            if requisite_combobox:
                requisite_combobox.selectByName(data['requisite'])
                self.setFuncChoice(compare_item, requisite_combobox)
                
            func_combobox = self.GetItemWindow(compare_item, 2)
            if func_combobox:
                func_combobox.selectByName(data['function'])
                self.setArgsEdit(compare_item, func_combobox)
                
            for i_col in range(3, self.GetColumnCount()):
                arg_edit = self.GetItemWindow(compare_item, i_col)
                if arg_edit:
                    arg_edit.setValue(data['arg_' + str(i_col - 2)])
        else:
            log_func.warning(u'Error define filter constructor item type <%s>' % data['type'])
            return False
        return result
     
    def setVistaTheme(self):
        """
        Set Windows Vista theme.
        """
        self.EnableSelectionGradient(False)
        self.EnableSelectionVista(True)
