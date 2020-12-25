#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object edit dialog_func.
"""

import sys
import operator
import wx
import wx.propgrid

from ...util import log_func
from ...util import spc_func
from ...util import lang_func
from ...util import spc_func
from ...util import global_func

from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import wxbitmap_func
from ...engine.wx import form_manager
from ...engine.wx import treectrl_manager
from ...engine.wx import listctrl_manager
from ...engine.wx import toolbar_manager

from . import refobj_dialogs_proto
from . import wx_editcodeproperty
from . import wx_editlinkproperty

from ...components.data_column import column_types

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

# Readonly fields
NOT_EDITABLE_FIELDS = ('cod', 'type', 'activate', 'dt_edit', 'computer', 'username')

# Tree dummy text
TREE_ITEM_LABEL = u'...'


class iqRefObjRecEditDlg(refobj_dialogs_proto.iqRecEditDlgProto):
    """
    Record edit dialog box.
    """
    def __init__(self, ref_obj=None, record=None, *args, **kwargs):
        """
        Costructor.

        :param ref_obj: Editable ref object.
        :param record: Editable record dictionary.
        """
        refobj_dialogs_proto.iqRecEditDlgProto.__init__(self, *args, **kwargs)
        self.record_propertyGrid.Bind(wx.propgrid.EVT_PG_CHANGED, self.onRecordPropertyGridChanged)

        self.ref_obj = ref_obj

        # Initial record
        self.record = record
        # Edited record
        self.edit_record = record
        if self.edit_record is None:
            self.edit_record = dict()

        self.init()
        
    def getRefObj(self):
        """
        Get reference data object.
        """
        return self.ref_obj
    
    def getRecord(self):
        """
        Editable record dictionary.
        """
        if self.record is None:
            self.record = dict()
        return self.record

    def _createProperty(self, field):
        """
        Create a property object from the field description.

        :param field: Model column object.
        :return: Property object.
        """
        label = field.doc if field.doc else field.name
        default_value = field.default
        if field.name == 'cod':
            # Type conformity check
            if not isinstance(default_value, str):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            property = wx_editcodeproperty.iqEditCodeProperty(label=label, name=field.name, value=default_value)
            property.setRefObj(self.ref_obj)
            property.setPropertyGrid(self.record_propertyGrid)
        elif field.type.__class__ in column_types.SQLALCHEMY_TEXT_TYPES:
            if not isinstance(default_value, str):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            # Text field
            property = wx.propgrid.StringProperty(label=label, name=field.name, value=default_value)
        elif field.type.__class__ in column_types.SQLALCHEMY_FLOAT_TYPES:
            if not isinstance(default_value, float):
                try:
                    default_value = float(default_value)
                except:
                    default_value = 0.0
            property = wx.propgrid.FloatProperty(label=label, name=field.name, value=default_value)
        elif field.type.__class__ in column_types.SQLALCHEMY_INT_TYPES:
            if not isinstance(default_value, int):
                try:
                    default_value = int(default_value)
                except:
                    default_value = 0
            property = wx.propgrid.IntProperty(label=label, name=field.name, value=default_value)
        elif field.type.__class__ in column_types.SQLALCHEMY_DATE_TYPES:
            py_date = datetimefunc.strDateFmt2DateTime(default_value)
            wx_date = datetimefunc.pydate2wxdate(py_date)
            property = wx.propgrid.DateProperty(label=label, name=field.name, value=wx_date)
        elif field.type.__class__ in column_types.SQLALCHEMY_DATETIME_TYPES:
            wx_date = datetimefunc.pydate2wxdate(default_value)
            property = wx.propgrid.DateProperty(label=label, name=field.name, value=wx_date)
        else:
            # If the type is not defined, then just look in text form
            if not isinstance(default_value, str):
                try:
                    default_value = str(default_value)
                except:
                    default_value = u''
            property = wx.propgrid.StringProperty(label=label, name=field.name, value=default_value)
            property.Enable(False)
            log_func.warning(u'Field <%s : %s : %s> edit disabled' % (field.name, field.type.__class__.__name__, label))

        return property

    def init(self):
        """
        Dialog initialization function.
        """
        user = global_func.getUser()
        if user:
            can_active = user.isPermission('active_ref_objects')
            self.activate_checkBox.Enable(can_active)

        # Init cod constructor
        self.cod_constructor.setRefObj(self.ref_obj)

        # Init property editors
        model = self.ref_obj.getModel()
        columns = [col for col_name, col in model.__table__.columns.items()]
        fields = [col for col in columns if col.name != 'id' and col.name not in NOT_EDITABLE_FIELDS]

        model_obj = self.ref_obj.getModelObj()

        rec = self.getRecord()

        is_activate = rec.get(self.ref_obj.getActiveColumnName(), True)
        self.activate_checkBox.SetValue(is_activate)

        cod = rec.get(self.ref_obj.getCodColumnName(), None)
        # log_func.debug(u'Init cod <%s>' % cod)
        self.cod_constructor.setCode(cod)

        for i, field in enumerate(fields):
            field_name = field.name
            column_obj = model_obj.findChild(field_name)

            if column_obj and column_obj.isAttributeValue('link'):
                property = wx_editlinkproperty.iqEditLinkProperty()
                property.setPropertyEditManager(column_obj.getLinkDataObj())
                property.SetValue(rec[field_name])
            elif field is not None:
                property = self._createProperty(field)
                property.SetValue(rec[field_name])
            else:
                # Add as line editing
                property = wx.propgrid.StringProperty(field_name, value=rec[field_name])
            self.record_propertyGrid.Append(property)
        # Moves splitter as left as possible, while still allowing all labels to be shown in full.
        self.record_propertyGrid.SetSplitterLeft()

    def getEditRecord(self):
        """
        Get edited vocabulary entry.
        """
        # Set active
        self.edit_record[self.ref_obj.getActiveColumnName()] = self.activate_checkBox.GetValue()

        # Set actual code
        edit_cod = self.cod_constructor.getCode()
        if self.edit_record and edit_cod:
            self.edit_record[self.ref_obj.getCodColumnName()] = edit_cod

        return self.edit_record

    def validate(self, name, value):
        """
        Validate property values.

        :param name: Attribute name.
        :param value: Value.
        :return: True/False.
        """
        if name == self.ref_obj.getNameColumnName():
            # The name must not be empty
            return bool(value.split() if isinstance(value, str) else False)
        return True

    def validRecord(self, record):
        """
        Validate record.

        :param record: Record dictionary.
        :return: True/False.
        """
        if not isinstance(record, dict):
            log_func.warning(u'Not valid record type <%s>' % record.__class__.__name__)
            return False

        return all([self.validate(name, value) for name, value in record.items()])

    def convertPropertyValue(self, name, str_value, property_type):
        """
        Convert the property value to the type specified in the specification.

        :param name: Property/Attribute name.
        :param str_value: Value as string.
        :param property_type: Value type code. Model column value type code.
        """
        value = None

        if property_type in column_types.SQLALCHEMY_TEXT_TYPES:
            value = str_value
        elif property_type in column_types.SQLALCHEMY_INT_TYPES:
            if str_value.strip().isdigit():
                value = int(str_value.strip())
        elif property_type in column_types.SQLALCHEMY_FLOAT_TYPES:
            if str_value.strip().isdigit():
                value = float(str_value.strip())
        elif property_type in column_types.SQLALCHEMY_DATE_TYPES:
            value = str_value
        elif property_type in column_types.SQLALCHEMY_DATETIME_TYPES:
            value = datetimefunc.strDateTimeFmt2DateTime(str_value.strip())
        else:
            log_func.warning(u'Not supported property type <%s> ' % property_type)
            value = str_value
        return value

    def findRefObjTabFieldSpc(self, field_name):
        """
        Get table field specification by name.

        :param field_name: Field name.
        """
        try:
            model_res = self.ref_obj.getModelObj().getResource()
            for field_spc in model_res[spc_func.CHILDREN_ATTR_NAME]:
                if field_name == field_spc['name']:
                    return field_spc
        except:
            log_func.fatal(u'Error get table field specification by name <%s>' % field_name)
        return None
        
    def onRecordPropertyGridChanged(self, event):
        """
        The handler for changing the field value of an edited record.
        """
        property = event.GetProperty()

        try:
            if property:
                name = property.GetName()
                str_value = property.GetValueAsString()
                # log_func.debug(u'Property [%s]. New value <%s>' % (name, str_value))
            
                field_spc = self.findRefObjTabFieldSpc(name)
                value = self.convertPropertyValue(name, str_value, field_spc['field_type'])
                if self.validate(name, value):
                    self.edit_record[name] = value
                else:
                    msg = u'Property [%s]. Property value not validated <%s>' % (name, str_value)
                    log_func.warning(msg)
                    wxdlg_func.openWarningBox(_(u'WARNING'), msg)
        except:
            log_func.fatal(u'Error change property')
        
        event.Skip()

    def onActivateCheckBox(self, event):
        """
        The handler for the activate checkbox.
        """
        check = event.IsChecked()
        self.cod_constructor.Enable(check)
        self.record_propertyGrid.Enable(check)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        The handler for the <Cancel> button.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        The handler for the <OK> button.
        """
        edit_record = self.getEditRecord()
        # log_func.debug(u'Edit record <%s>' % edit_record)
        if self.validRecord(edit_record):
            self.EndModal(wx.ID_OK)
        else:
            msg = u'Not valid record in <%s>' % self.ref_obj.getDescription()
            log_func.warning(msg)
            wxdlg_func.openWarningBox(_(u'WARNING'), msg)

        event.Skip()


class iqRefObjRecCreateDlg(iqRefObjRecEditDlg):
    """
    Record create dialog box.
    """
    def __init__(self, *args, **kwargs):
        """
        Costructor.
        """
        iqRefObjRecEditDlg.__init__(self, *args, **kwargs)

    def validate(self, name, value):
        """
        Validate property values.

        :param name: Attribute name.
        :param value: Value.
        :return: True/False.
        """
        if name == self.ref_obj.getCodColumnName():
            # Code must not be registered
            return not self.ref_obj.hasCod(value)
        elif name == self.ref_obj.getNameColumnName():
            # The name must not be empty
            return bool(value.split() if isinstance(value, str) else False)
        return True


class iqRefObjEditDlg(refobj_dialogs_proto.iqEditDlgProto,
                      form_manager.iqFormManager,
                      treectrl_manager.iqTreeCtrlManager,
                      listctrl_manager.iqListCtrlManager,
                      toolbar_manager.iqToolBarManager):
    """
    Ref object edit dialog box.
    """
    def __init__(self, ref_obj=None, *args, **kwargs):
        """
        Constructor.

        :param ref_obj: Reference data object.
        """
        refobj_dialogs_proto.iqEditDlgProto.__init__(self, *args, **kwargs)

        self.ref_obj = ref_obj

        if self.ref_obj:
            description = self.ref_obj.getDescription() if self.ref_obj.getDescription() else self.ref_obj.getName()
            title = _(u'Edit') + u' <%s>' % description
            self.SetTitle(title)

        # Codes found matching search string
        self.search_codes = list()
        # Current found code in the list of found codes
        self.search_code_idx = 0
        # A sign of the need to update the list of searched codes
        self.not_actual_search = False

        self.init()
        
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onRefObjTreeItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onRefObjTreeItemCollapsed)
        
    def init(self):
        """
        Dialog initialization function.
        """
        # self.initImages()
        self.initCtrl()
        self.setRefObjTree()

    def initImages(self):
        """
        Initialization of control images.
        """
        # <wx.Tool>
        bmp = wxbitmap_func.createIconBitmap('fatcow/magnifier')
        tool_id = self.search_tool.GetId()
        # Not use <tool.SetNormalBitmap(bmp)>
        # Use <toolbar.SetToolNormalBitmap(tool_id, bmp)>
        self.search_toolBar.SetToolNormalBitmap(tool_id, bmp)
        # After changing tool images call <Realize>
        self.search_toolBar.Realize()        

        bmp = wxbitmap_func.createIconBitmap('fatcow/plus')
        tool_id = self.add_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/pencil')
        tool_id = self.edit_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)
        
        bmp = wxbitmap_func.createIconBitmap('fatcow/minus')
        tool_id = self.del_tool.GetId()
        self.ctrl_toolBar.SetToolNormalBitmap(tool_id, bmp)

        # After changing tool images call <Realize>
        self.ctrl_toolBar.Realize()

    def getEditableFields(self):
        """
        List of resource descriptions of editable table fields.
        """
        model = self.ref_obj.getModel()
        columns = [col for col_name, col in model.__table__.columns.items()]
        fields = [col for col in columns if col.name != 'id' and col.name not in NOT_EDITABLE_FIELDS]
        return fields
    
    def initCtrl(self):
        """
        Initialization of controls.
        """
        user = global_func.getUser()
        if user:
            self.enableToolbarTools(toolbar=self.ctrl_toolBar,
                                    add_tool=user.isPermission('new_ref_objects'),
                                    edit_tool=user.isPermission('change_ref_objects'),
                                    del_tool=user.isPermission('del_ref_objects'))

        # Add columns
        self.recs_listCtrl.ClearAll()
        # Define table fields
        fields = self.getEditableFields()
        
        for i, field in enumerate(fields):
            col_name = field.doc if field.doc else field.name
            self.recs_listCtrl.InsertColumn(i, col_name, 
                                            width=wx.LIST_AUTOSIZE_USEHEADER)
           
    def setRefObjTreeItem(self, parent_item, record):
        """
        Set tree item.

        :param parent_item: Parent tree item.
        :param record: Record associated with an item.
        """
        # item_level = self.getTreeCtrlItemLevelIdx(treectrl=self.refobj_treeCtrl, item=parent_item)
        # Record as dictionary
        # rec_dict = self.ref_obj.getStorage().getSpravFieldDict(record, level_idx=item_level)
        name = str(record['name'])
        # For multi-line items, select only the first line
        name = [line.strip() for line in name.split(u'\n')][0]
        item = self.refobj_treeCtrl.AppendItem(parent_item, name)
        self.setTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=item, data=record)

        active = record.get(self.ref_obj.getActiveColumnName(), None)
        sys_colour_value = wx.SYS_COLOUR_WINDOWTEXT if active else wx.SYS_COLOUR_GRAYTEXT
        item_colour = wx.SystemSettings.GetColour(sys_colour_value)
        self.setTreeCtrlItemForegroundColour(treectrl=self.refobj_treeCtrl,
                                             item=item, colour=item_colour)

        code = record['cod']
        if self.ref_obj.hasChildrenCodes(code):
            # There are subcodes. To display a tree in the control, you need to add a dummy element
            self.refobj_treeCtrl.AppendItem(item, TREE_ITEM_LABEL)
        
    def setRefObjTree(self):
        """
        Set tree data.
        """
        # Add root item
        title = self.ref_obj.getDescription() if self.ref_obj.getDescription() else self.ref_obj.getName()
        # For multi-line items, select only the first line
        title = [line.strip() for line in title.split(u'\n')][0]

        self.root = self.refobj_treeCtrl.AddRoot(title)
        
        if self.ref_obj.isEmpty():
            # No need to fill
            log_func.warning(u'Ref object is empty')
            return
        
        self.setRefObjLevelTree(self.root)

        # Set list data
        self.setRefObjList(self.root)

        # Expand root item
        self.refobj_treeCtrl.Expand(self.root)
        
    def setRefObjLevelTree(self, parent_item, code=None, do_sort=True):
        """
        Add tree level.
        
        :param parent_item: The tree item to add to.
        :param code: The code associated with the tree item.
        """
        # Add first level tree
        level_data = self.ref_obj.getLevelRecsByCod(code)
        # Sort
        if do_sort and isinstance(level_data, list):
            sorted(level_data, key=operator.itemgetter('cod'))

        for record in level_data:
            self.setRefObjTreeItem(parent_item, record)

    def addRefObjListRow(self, record, is_col_autosize=True):
        """
        Add a new row to the list.

        :param record: Record associated with a list line.
        :param is_col_autosize: Do you automatically re-size the columns after adding a row?
        """
        fields = self.getEditableFields()
        list_item = -1
        for i, field in enumerate(fields):
            value = str(record[field.name])
            # For multi-line items, select only the first line
            value = [line.strip() for line in value.split(u'\n')][0]

            if i == 0:
                list_item = self.recs_listCtrl.InsertItem(sys.maxsize, value, i)
                self._list_ctrl_dataset.append(record)
            else:
                self.recs_listCtrl.SetItem(list_item, i, value)

            active = record.get(self.ref_obj.getActiveColumnName(), None)
            sys_colour_value = wx.SYS_COLOUR_WINDOWTEXT if active else wx.SYS_COLOUR_GRAYTEXT
            item_colour = wx.SystemSettings.GetColour(sys_colour_value)
            self.setListCtrlRowForegroundColour(listctrl=self.recs_listCtrl,
                                                item=list_item,colour=item_colour)

        if is_col_autosize:
            # Re-size columns
            for i, field in enumerate(fields):
                self.recs_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        
    def setRefObjList(self, tree_item=None):
        """
        Set list data.

        :param tree_item: The tree item for which you want to display a list.
            If not defined, then consider this to be the root element.
        """
        if tree_item is None:
            tree_item = self.root
            
        self.recs_listCtrl.DeleteAllItems()
        # List of records of the selected level
        self._list_ctrl_dataset = list()
        
        child_item, cookie = self.refobj_treeCtrl.GetFirstChild(tree_item)
        while child_item.IsOk():
            record = self.getTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=child_item)

            self.addRefObjListRow(record, False)
            
            child_item, cookie = self.refobj_treeCtrl.GetNextChild(tree_item, cookie)

        # Re-size columns
        fields = self.getEditableFields()
        for i in range(len(fields)):
            self.recs_listCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

    def findTreeChildItem(self, item_text, cur_item=None):
        """
        Search for a child of a tree by text.

        :param item_text: Tree item text.
        """
        if cur_item is None:
            cur_item = self.root
            
        find_item = None
        child_item, cookie = self.refobj_treeCtrl.GetFirstChild(cur_item)
        while child_item.IsOk():
            if item_text == self.refobj_treeCtrl.GetItemText(child_item):
                find_item = child_item
                break
            child_item, cookie = self.refobj_treeCtrl.GetNextChild(cur_item, cookie)
        return find_item

    def isNotInitLevelTree(self, item):
        """
        Verification. Is the tree element branch initialized / loaded?

        :param item: Tree item.
        :return: True/False.
        """
        find_item = self.findTreeChildItem(TREE_ITEM_LABEL, item)
        return bool(find_item)

    def initLevelTree(self, item):
        """
        Initialize a tree element branch.

        :param item: Tree item.
        """
        find_item = self.findTreeChildItem(TREE_ITEM_LABEL, item)
        if find_item:
            self.refobj_treeCtrl.Delete(find_item)

        # Empty level filling
        if not self.refobj_treeCtrl.ItemHasChildren(item):
            record = self.getTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=item)
            code = record['cod']
            self.setRefObjLevelTree(item, code)
        
    def refreshRefObjTreeItem(self, parent_item, code=None, record=None):
        """
        Refresh tree item.

        :param parent_item: Parent tree item.
        :param code: The code associated with the tree item.
        :param record: The record associated with the tree item.
        """
        find_item = self.findRefObjTreeItem(parent_item, code)
        if find_item:
            self.setTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=find_item, data=record)
            self.refobj_treeCtrl.SetItemText(find_item, record['name'])

            active = record.get(self.ref_obj.getActiveColumnName(), None)
            sys_colour_value = wx.SYS_COLOUR_WINDOWTEXT if active else wx.SYS_COLOUR_GRAYTEXT
            item_colour = wx.SystemSettings.GetColour(sys_colour_value)
            self.setTreeCtrlItemForegroundColour(treectrl=self.refobj_treeCtrl,
                                                 item=find_item, colour=item_colour)

    def refreshRefObjListItem(self, code=None, record=None):
        """
        Refresh list item.

        :param code: The code associated with the tree item.
        :param record: The record associated with the tree item.
        """
        find_idx = self.findRefObjListItem(code)
        if find_idx >= 0:
            self._list_ctrl_dataset[find_idx] = record

            fields = self.getEditableFields()
            for i, field in enumerate(fields):
                log_func.debug(u'Record <%s : %s>' % (str(record), record.__class__.__name__))
                value = str(record[field.name])
                self.recs_listCtrl.SetItem(find_idx, i, value)

            active = record.get(self.ref_obj.getActiveColumnName(), None)
            sys_colour_value = wx.SYS_COLOUR_WINDOWTEXT if active else wx.SYS_COLOUR_GRAYTEXT
            item_colour = wx.SystemSettings.GetColour(sys_colour_value)
            self.setListCtrlRowForegroundColour(listctrl=self.recs_listCtrl,
                                                item=find_idx, colour=item_colour)

    def delRefObjTreeItem(self, parent_item, code=None):
        """
        Delete tree item.

        :param parent_item: Parent tree item.
        :param code: The code associated with the tree item.
        """
        find_item = self.findRefObjTreeItem(parent_item, code)
        if find_item:
            self.refobj_treeCtrl.Delete(find_item)

    def delRefObjListItem(self, code=None):
        """
        Delete list item.

        :param code: The code associated with the item.
        """
        find_idx = self.findRefObjListItem(code)
        if find_idx > 0:
            del self._list_ctrl_dataset[find_idx]
            self.recs_listCtrl.DeleteItem(find_idx)
        else:
            log_func.warning(u'Not found list item by cod <%s>' % code)

    def addRefObjTreeItem(self, parent_item, new_record):
        """
        Add tree item.

        :param parent_item: Parent tree item.
        :param new_record: New record added.
        """
        item = self.refobj_treeCtrl.AppendItem(parent_item, new_record['name'])
        self.setTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=item, data=new_record)

        active = new_record.get(self.ref_obj.getActiveColumnName(), None)
        sys_colour_value = wx.SYS_COLOUR_WINDOWTEXT if active else wx.SYS_COLOUR_GRAYTEXT
        item_colour = wx.SystemSettings.GetColour(sys_colour_value)
        self.setTreeCtrlItemForegroundColour(treectrl=self.refobj_treeCtrl,
                                             item=item, colour=item_colour)

    def addRefObjListItem(self, new_record=None):
        """
        Add list item.

        :param new_record: New record added.
        """
        self.addRefObjListRow(new_record)

    def findRefObjTreeItem(self, parent_item, code=None):
        """
        Search for a reference tree element by code.

        :param parent_item: Parent tree item.
        :param code: The code associated with the tree item.
        :return: The tree item found, or None if the item is not found.
        """
        # Search code in current item
        record = self.getTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=parent_item)
        if record:
            if code == record['cod']:
                return parent_item
        
        # Search in child elements
        find_result = None
        child_item, cookie = self.refobj_treeCtrl.GetFirstChild(parent_item)
        while child_item.IsOk():
            record = self.getTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=child_item)
            if record:
                if code == record['cod']:
                    find_result = child_item
                    break
            child_item, cookie = self.refobj_treeCtrl.GetNextChild(parent_item, cookie)
        
        # Nothing was found at this level. Need to go down one level
        if not find_result:
            child_item, cookie = self.refobj_treeCtrl.GetFirstChild(parent_item)
            while child_item.IsOk():
                self.initLevelTree(child_item)
                find_result = self.findRefObjTreeItem(child_item, code)
                if find_result:
                    break
                child_item, cookie = self.refobj_treeCtrl.GetNextChild(parent_item, cookie)
            
        return find_result

    def findRefObjListItem(self, code=None):
        """
        Find list item by code.

        :param code: The code associated with the item.
        :return: The index of the found list item or None if nothing is found.
        """
        find_result = None
        for idx, record in enumerate(self._list_ctrl_dataset):
            if code == record['cod']:
                find_result = idx
                break
        return find_result

    def selectRefObjTreeItem(self, code, parent_item=None):
        """
        Find and select a tree element by code.
        
        :param code: The code associated with the item.
        :return: The tree item found, or None if the item is not found.
        """
        if parent_item is None:
            parent_item = self.root
        
        item = self.findRefObjTreeItem(parent_item, code)
        if item:
            self.refobj_treeCtrl.SelectItem(item)
            return item
        return None        
        
    def onRefObjTreeItemCollapsed(self, event):
        """
        Tree item collapse handler.
        """
        event.Skip()

    def onRefObjTreeItemExpanded(self, event):
        """
        Tree item expand handler.
        """
        item = event.GetItem()
        self.initLevelTree(item)
            
        event.Skip()

    def onRefObjTreeSelChanged(self, event):
        """
        A handler for changing a tree item selection.
        """
        item = event.GetItem()

        self.initLevelTree(item)
        # Set list data
        self.setRefObjList(item)
        
        event.Skip()

    def onEditToolClicked(self, event):
        """
        Record editing tool handler.
        """
        rec_idx = self.recs_listCtrl.GetFirstSelected()
        if rec_idx != -1:
            record = self._list_ctrl_dataset[rec_idx]
            edit_rec = editRefObjRecordDlg(parent=self, ref_obj=self.ref_obj,
                                           record=record)
            if edit_rec:
                # Update record in ref object
                self.ref_obj.save(**edit_rec)
                self.refreshRefObjTreeItem(self.refobj_treeCtrl.GetSelection(),
                                           edit_rec['cod'], edit_rec)
                self.refreshRefObjListItem(edit_rec['cod'], edit_rec)
                
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Delete record tool handler.
        """
        rec_idx = self.recs_listCtrl.GetFirstSelected()
        if rec_idx != -1:
            record = self._list_ctrl_dataset[rec_idx]
            del_code = record['cod']
            if wxdlg_func.openAskBox(_(u'DELETE'),
                                     _(u'Delete record <%s>. Are you sure?' % record['name'])):
                self.ref_obj.delRecByCod(cod=del_code)
                self.delRefObjTreeItem(self.refobj_treeCtrl.GetSelection(),
                                       del_code)
                self.delRefObjListItem(del_code)
        event.Skip()

    def addRecord(self):
        """
        Add new record of ref object.

        :return: True/False.
        """
        # Filling a record with default values
        model = self.ref_obj.getModel()
        default_record = dict(
            [(col_name,
              col.default.arg if col.default else None) for col_name,
                                                            col in model.__table__.columns.items() if col_name != 'id'])
        # Set default code
        parent_rec = self.getTreeCtrlItemData(treectrl=self.refobj_treeCtrl, item=self.refobj_treeCtrl.GetSelection())
        struct_parent_code = self.ref_obj.getCodAsTuple(parent_rec['cod']) if parent_rec else list()
        struct_parent_code = [sub_code for sub_code in struct_parent_code if sub_code]
        level_idx = len(struct_parent_code)
        struct_code = struct_parent_code
        struct_code += ['0' * self.ref_obj.getCodLen()[level_idx]]
        default_record['cod'] = ''.join(struct_code)

        add_rec = createRefObjRecordDlg(parent=self, ref_obj=self.ref_obj,
                                        record=default_record)

        log_func.debug(u'New ref obj record %s' % str(add_rec))
        if add_rec:
            # Existing code control
            if not self.ref_obj.hasCod(add_rec['cod']):
                self.ref_obj.addRec(add_rec)
                self.addRefObjTreeItem(self.refobj_treeCtrl.GetSelection(),
                                       add_rec)
                self.addRefObjListItem(add_rec)
            else:
                msg = u'Code <%s> already present in the ref object <%s>' % (add_rec['cod'],
                                                                             self.ref_obj.getDescription())
                log_func.warning(msg)
                wxdlg_func.openWarningBox(_(u'WARNING'), msg)

    def onAddToolClicked(self, event):
        """
        Add new record tool handler.
        """
        try:
            self.addRecord()
        except:
            log_func.fatal(u'Error add new record of ref object <%s>' % self.ref_obj.getName())
            
        event.Skip()

    def findAndSelectItem(self, find_text=None):
        """
        Search/Find item by text.

        :param find_text: Find text.
        :return: True/False.
        """
        if find_text is None:
            find_text = self.search_textCtrl.GetValue()

        if find_text:
            do_find = True
            if self.not_actual_search:
                # search_codes = self.ref_obj.getStorage().search(find_text)
                search_records = self.ref_obj.searchRecsByColValues()
                search_codes = self.ref_obj.searchCodes(find_text)
                if search_codes:
                    self.search_codes = search_codes
                    self.search_codes.sort()
                    self.search_code_idx = 0
                else:
                    wxdlg_func.openWarningBox(_(u'WARNING'),
                                              _(u'No records found matching search string'))
                    do_find = False
                self.not_actual_search = False
            else:
                # If you do not need to update the list of found codes,
                # then look for the next code in the list
                self.search_code_idx += 1
                if self.search_code_idx >= len(self.search_codes):
                    self.search_code_idx = 0

            if do_find:
                find_code = self.search_codes[self.search_code_idx]
                self.selectRefObjTreeItem(find_code)
        else:
            wxdlg_func.openWarningBox(_(u'WARNING'),
                                      _(u'No search string selected'))

    def onSearchToolClicked(self, event):
        """
        Record name search tool handler.
        """
        try:
            self.findAndSelectItem()
        except:
            log_func.fatal(u'Error find item by text')

        event.Skip()        

    def findWordInRecords(self, find_word, start_row=None, start_col=None):
        """
        Search for a word in the current list of entries.

        :param find_word: Search word.
        :param start_row: Start line to start the search.
            If not specified, then the first.
        :param start_col: Start column to start the search.
            If not specified, then the first.
        :return: Post index, index of the field where the word is found.
            Or None if nothing is found.
        """
        if start_row is None:
            start_row = 0
        if start_col is None:
            start_col = 0

        find_word = find_word.lower()
        fields = self.getEditableFields()
        for i_row, row in enumerate(self._list_ctrl_dataset[start_row:]):
            if i_row == 0:
                for i_col, field in enumerate(fields[start_col:]):
                    field_name = field['name']
                    value = str(row[field_name]).lower()
                    if find_word in value:
                        log_func.debug(u'Found matching %s <%s> in <%s>' % (field_name, find_word, value))
                        return start_row+i_row, start_col+i_col
            else:
                for i_col, field in enumerate(fields):
                    field_name = field['name']
                    value = str(row[field_name]).lower()
                    if find_word in value:
                        log_func.debug(u'Found matching in field %s <%s> : <%s>'  % (field_name, find_word, value))
                        return start_row+i_row, i_col
        log_func.warning(u'Not found <%s>. Search over.' % find_word)
        return None

    def findWordInRecordsListCtrl(self, start_row=None):
        """
        The procedure for finding a word in the list of current entries.

        :param start_row: The initial search string. If not defined,
             then the search is performed from the currently selected line.
        """
        cur_row = start_row
        if cur_row is None:
            cur_row = self.getItemSelectedIdx(self.recs_listCtrl)

        find_word = self.find_textCtrl.GetValue()
        find_result = self.findWordInRecords(find_word, start_row=cur_row + 1)

        do_find = find_result is not None

        if do_find:
            find_row, find_col = find_result
            self.selectItem_list_ctrl(self.recs_listCtrl, find_row)
        else:
            msg = u'No search word found. Start the search from the beginning?'
            if wxdlg_func.openAskBox(_(u'SEARCH'), msg):
                self.findWordInRecordsListCtrl(-1)

    def onFindToolClicked(self, event):
        """
        Keyword search tool handler.
        """
        find_txt = self.find_textCtrl.GetValue()
        if find_txt:
            self.findWordInRecordsListCtrl()
        else:
            wxdlg_func.openWarningBox(_(u'WARNING'),
                                      _(u'No search string selected'))
            
        event.Skip()        
        
    def onSearchText(self, event):
        """
        Search text modifier.
        """
        search_txt = event.GetString()
        log_func.debug(u'Change search text <%s>' % search_txt)
        self.not_actual_search = True
        event.Skip()
        
    def onOkButtonClick(self, event):
        """
        <OK> button handler.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()
        
        
def editRefObjDlg(parent=None, ref_obj=None):
    """
    Ref object edit form call.
    
    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :return: True/False.
    """
    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    result = False
    dlg = None
    try:
        dlg = iqRefObjEditDlg(ref_obj=ref_obj, parent=parent)
        # dlg.init()
        result = dlg.ShowModal() == wx.ID_OK
        dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error edit ref object dialog')

    return result


def editRefObjRecordDlg(parent=None, ref_obj=None, record=None):
    """
    Record edit form call.
    
    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param record: Editing record dictionary.
    :return: Edited record dictionary or None in case of error.
    """
    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    dlg = iqRefObjRecEditDlg(ref_obj=ref_obj, record=record, parent=parent)
    # dlg.init()
    result = dlg.ShowModal()
    
    edit_record = None
    if result == wx.ID_OK:
        edit_record = dlg.getEditRecord()
    dlg.Destroy()
    return edit_record


def createRefObjRecordDlg(parent=None, ref_obj=None, record=None):
    """
    Record new form call.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param record: Editing record dictionary.
    :return: Edited record dictionary or None in case of error.
    """
    if parent is None:
        app = wx.GetApp()
        main_win = app.GetTopWindow()
        parent = main_win

    dlg = iqRefObjRecCreateDlg(ref_obj=ref_obj, record=record, parent=parent)
    # dlg.init()
    result = dlg.ShowModal()

    edit_record = None
    if result == wx.ID_OK:
        edit_record = dlg.getEditRecord()
    dlg.Destroy()
    return edit_record
