#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog form for ref object element / code selection.
All data is presented in tree view.
"""

import os.path
import operator
import wx

from . import refobj_dialogs_proto

from ...util import log_func
from ...util import str_func
from ...util import lang_func
from ...util import file_func

from ...engine.wx import wxbitmap_func
from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import wxobj_func

from ...engine.wx import form_manager
from ...engine.wx import stored_wx_form_manager
from ...engine.wx import treelistctrl_manager

from . import wx_editdlg

__version__ = (0, 0, 1, 2)

_ = lang_func.getTranslation().gettext

# Tree dummy text
TREE_ITEM_LABEL = u'...'

# Dialog cache to optimize call selection
CHOICE_DLG_CACHE = dict()

SORT_REVERSE_SIGN = '-'


class iqRefObjChoiceTreeDlg(refobj_dialogs_proto.iqChoiceTreeDlgProto,
                            form_manager.iqFormManager,
                            stored_wx_form_manager.iqStoredWxFormsManager,
                            treelistctrl_manager.iqTreeListCtrlManager):
    """
    Dialog form for ref object element / code selection.
    """
    def __init__(self, ref_obj=None, default_selected_code=None,
                 *args, **kwargs):
        """
        Constructor.

        :param ref_obj: Reference data object.
        :param default_selected_code: Selected default code.
        """
        refobj_dialogs_proto.iqChoiceTreeDlgProto.__init__(self, *args, **kwargs)

        self.ref_obj = ref_obj

        # Set title as ref object description
        self.SetTitle(self.ref_obj.getDescription() if self.ref_obj is not None else u'')

        # List of table field names displayed in the tree control as columns
        self.refobj_col_names = ['cod', 'name']

        # List of table field names that can be searched
        self.refobj_search_col_names = ['name', 'cod']

        # Codes found matching search string
        self.search_codes = list()
        # Current found code in the list of found codes
        self.search_code_idx = 0
        # A sign of the need to update the list of searched codes
        self.not_actual_search = False

        # Column name to sort
        self.sort_column = None

        # Sorting Image Indexes
        self.sort_ascending_img = -1
        self.sort_descending_img = -1

        # You must remember the image library object
        # Otherwise, when using it will occur <Segmentation fault>
        self.refobj_treeListCtrl_img_list = None

        self.default_selected_code = default_selected_code

        # Pop-up window for additional information
        self.popup_win = None

        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onRefObjTreeItemExpanded)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onItemSelectChanged)

        # Mouse click on the header
        header_list_ctrl = self.refobj_treeListCtrl.GetHeaderWindow()
        header_list_ctrl.Bind(wx.EVT_LEFT_DOWN, self.onHeaderMouseLeftClick)

    def onInitDlg(self, event):
        """
        Dialog initialization.
        """
        # log_func.debug(u'onInit')
        if self.default_selected_code:
            log_func.info(u'Select code <%s> in ref object [%s]' % (self.default_selected_code,
                                                                    self.ref_obj.getName()))
            if self.ref_obj.hasCod(self.default_selected_code):
                self.selectRefObjTreeItem(self.default_selected_code)
            else:
                log_func.warning(u'Code <%s> not found in ref object [%s]' % (self.default_selected_code,
                                                                              self.ref_obj.getName()))
        event.Skip()

    def onCloseDlg(self, event):
        """
        Close dialog box.
        """
        self.hidePopupInfo()
        event.Skip()

    def init(self, fields, search_fields):
        """
        Dialog initialization function.

        :param fields: List of field names to be displayed in the tree control.
            If no fields are specified, only <Code> and <Name> are displayed.
        :param search_fields: Search fields.
        """
        self.initImages()

        self.initColumns(*fields)
        self.initSearch(*search_fields)
        self.setRefObjTree()

        # Checking user permission to edit the directory
        can_edit = self.ref_obj.canEdit()
        self.edit_button.Enable(can_edit)

    def initImages(self):
        """
        Initialization of control images.
        """
        if self.refobj_treeListCtrl_img_list is None:
            img_list = wx.ImageList(wxbitmap_func.DEFAULT_ICON_WIDTH,
                                    wxbitmap_func.DEFAULT_ICON_WIDTH)

            self.sort_ascending_img = img_list.Add(wxbitmap_func.createIconBitmap('fatcow/bullet_arrow_up'))
            self.sort_descending_img = img_list.Add(wxbitmap_func.createIconBitmap('fatcow/bullet_arrow_down'))

            self.refobj_treeListCtrl.SetImageList(img_list)

            self.refobj_treeListCtrl_img_list = img_list

    def getFieldLabel(self, field):
        """
        Determine the inscription corresponding to the field by its description.

        :param field: DataColumn object.
        :return: Label text.
        """
        if field is None:
            return TREE_ITEM_LABEL
        label = field.getDescription() if field.getDescription() else field.getName()
        return str(label)

    def initColumns(self, *fields):
        """
        Initialization of control columns of the directory tree.

        :param fields: List of field names to be displayed in the tree control.
            If no fields are specified, only <Code> and <Name> are displayed.
        """
        field_names = ['cod', 'name']
        if fields:
            field_names += fields
        self.refobj_col_names = field_names
            
        if self.ref_obj is None:
            log_func.warning(u'Not define ref object for selecting code')
            return
        
        model_obj = self.ref_obj.getModelObj()
        # Dictionary table field specifications dictionary
        if model_obj:
            field_dict = {field.getName(): field for field in model_obj.getChildren()}
        else:
            log_func.warning(u'Not define model in ref object <%s>' % self.ref_obj.getName())
            field_dict = dict()
        
        for field_name in field_names:
            field = field_dict.get(field_name, None)
            if field:
                column_label = self.getFieldLabel(field)
                self.refobj_treeListCtrl.AddColumn(column_label)
            else:
                log_func.warning(u'Not define field <%s> in model <%s>' % (field_name, model_obj.getName()))

        # Refresh sorted columns
        self.refreshSortColumn(self.sort_column)

    def initSearch(self, *search_fields):
        """
        Initializing search selection controls by fields.

        :param search_fields: Search fields.
        """
        field_names = ['name', 'cod']
        if search_fields:
            field_names += search_fields
        self.refobj_search_col_names = field_names

        if self.ref_obj is None:
            log_func.warning(u'Not define ref object')
            return

        model_obj = self.ref_obj.getModelObj()
        field_dict = {field.getName(): field for field in model_obj.getChildren()}

        choices = list()
        for field_name in field_names:
            field = field_dict.get(field_name, None)
            if field:
                choice_label = self.getFieldLabel(field)
                choices.append(choice_label)
            else:
                log_func.warning(u'Not found field <%s> in model <%s>' % (field_name, model_obj.getName()))
        self.search_field_choice.Clear()
        self.search_field_choice.AppendItems(choices)
        self.search_field_choice.Select(0)

    def setRefObjTree(self, is_progress=True, sort_column=None):
        """
        Set ref object tree data.

        :param is_progress: Display a progress bar for building a directory tree?
        :param sort_column: Sort column names.
        """
        # Add the root element of the tree
        title = self.ref_obj.getDescription() if self.ref_obj.getDescription() else self.ref_obj.getName()
        # We take only the first row
        title = [line.strip() for line in title.split(u'\n')][0]

        self.root = self.refobj_treeListCtrl.AddRoot(title)
        
        if self.ref_obj.isEmpty():
            # No need to fill
            log_func.warning(u'Ref object <%s> is empty' % self.ref_obj.getName())
            return

        if sort_column is None:
            sort_column = self.sort_column
        self.setRefObjLevelTree(self.root, is_progress=is_progress, sort_column=sort_column)

        # Expand root element
        self.refobj_treeListCtrl.Expand(self.root)

    def refreshRefObjTree(self, is_progress=True, sort_column=None):
        """
        Update ref object tree data.

        :param is_progress: Derive a progressbar for building a tree?
        :param sort_column: Sort column names.
        """
        # Remember selected tree item
        selected_code = self.getSelectedCode()

        # First delete all tree items
        self.refobj_treeListCtrl.DeleteAllItems()

        title = self.ref_obj.getDescription() if self.ref_obj.getDescription() else self.ref_obj.getName()
        # For multi-line items, select only the first line
        title = [line.strip() for line in title.split(u'\n')][0]

        self.root = self.refobj_treeListCtrl.AddRoot(title)

        if self.ref_obj.isEmpty():
            log_func.warning(u'Ref object <%s> is empty' % self.ref_obj.getName())
            return

        if sort_column is None:
            sort_column = self.sort_column
        self.setRefObjLevelTree(self.root, is_progress=is_progress, sort_column=sort_column)

        if selected_code is not None:
            self.selectRefObjTreeItem(selected_code)
        else:
            self.refobj_treeListCtrl.Expand(self.root)

    def setRefObjLevelTree(self, parent_item, code=None,
                           is_progress=True, sort_column=None):
        """
        Add tree level.

        :param parent_item: The tree item to add to.
        :param code: The code associated with the tree item.
        :param sort_column: Sort column names.
        :param is_progress: Sign of display of loading progress.
        """
        # Add first level tree
        level_data = self.ref_obj.getLevelRecsByCod(parent_cod=code)
        # Sort
        if sort_column is not None:
            log_func.debug(u'Set sort column <%s>' % sort_column)
            level_data = self.sortRefObjRecordset(level_data, sort_column=sort_column)

        if level_data is None:
            log_func.warning(u'No data')
            return

        # log_func.debug(u'Ref object level data %s' % str(level_data))
        title = self.ref_obj.getDescription() if self.ref_obj.getDescription() else self.ref_obj.getName()
        label = _(u'Open ref object') + ' <%s>' % title
        len_level_data = len(level_data) if isinstance(level_data, list) else 0
        if is_progress:
            wxdlg_func.openProgressDlg(self, _(u'Ref object'), label, 0, len_level_data)

        try:
            for i, record in enumerate(level_data):
                self.setRefObjTreeItem(parent_item, record)

                if is_progress:
                    wxdlg_func.updateProgressDlg(i + 1, label)

            # Set auto column width
            for i, field_name in enumerate(self.refobj_col_names):
                self.refobj_treeListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        except:
            log_func.fatal(u'Error building a tree')

        if is_progress:
            wxdlg_func.closeProgressDlg()

    def getSortField(self, sort_column='name'):
        """
        Determine the name of the sort field by specifying the name / index of the sort column.

        :param sort_column: Specify sort column name / index.
        :return: Sort field name or None if error.
        """
        sort_field = None
        if isinstance(sort_column, int):
            # An increase of 1 is made in order to take
            # into account the first column with index 0
            #                      V
            i = abs(sort_column) - 1
            sort_field = self.refobj_col_names[i]
        elif isinstance(sort_column, str):
            if sort_column.startswith(SORT_REVERSE_SIGN):
                sort_field = sort_column[1:]
            else:
                sort_field = sort_column
            if sort_field not in self.refobj_col_names:
                log_func.warning(u'Sort. Field <%s> not found in %s.' % (sort_field, self.refobj_col_names))
                sort_field = None
        else:
            log_func.warning(u'Error sort field/column type <%s>' % type(sort_column))
        return sort_field

    def getSortFieldIdx(self, sort_column='name'):
        """
        Define the sort field index by the name / index of the sort column.

        :param sort_column: Specify sort column name / index.
        :return: Sort field index or None if error.
        """
        sort_field_idx = None
        if isinstance(sort_column, int):
            # An increase of 1 is made in order to take
            # into account the first column with index 0
            #                         V
            return abs(sort_column) - 1
        elif isinstance(sort_column, str):
            if sort_column.startswith(SORT_REVERSE_SIGN):
                sort_field = sort_column[1:]
            else:
                sort_field = sort_column
            if sort_field in self.refobj_col_names:
                sort_field_idx = self.refobj_col_names.index(sort_field)
            else:
                log_func.warning(u'Sort. Field <%s> not found in %s.' % (sort_field, self.refobj_col_names))
                sort_field_idx = None
        else:
            log_func.warning(u'Error sort field/column type <%s>' % type(sort_column))
        return sort_field_idx

    def isReverseSort(self, sort_column='name'):
        """
        Reverse sort check.

        :param sort_column: Specify sort column name / index.
        :return: True - reverse sort / False - normal sort ascending.
        """
        if isinstance(sort_column, int):
            return sort_column < 0
        elif isinstance(sort_column, str):
            return sort_column.startswith(SORT_REVERSE_SIGN)
        # The default is normal ascending sorting
        return False

    def sortRefObjRecordset(self, recordset, sort_column='name'):
        """
        Sort the list of entries by column.

        :param recordset: Record list.
        :param sort_column: Sort column.
            The column can be specified by name or by index.
            If the name is preceded by <-> or the index is negative,
            it is considered that sorting is in reverse order.
            For instance:
            'name' - sort by 'name' field
            '-name' - sort by 'name' field in reverse order
            1 - sorting by field with index 0
            -1 - sort by field with index 0 in reverse order.
            Accordingly, if the entry is specified by a dictionary,
            then specify the field name as the field.
            If the record is specified in the list, then the field is indicated by the index.
        :return: Sorted list of records.
        """
        if not isinstance(recordset, list):
            log_func.warning(u'Error sort records type <%s>' % type(recordset))
            return recordset

        if not recordset:
            # If the list of entries is empty, then do not sort
            return recordset

        sort_field = self.getSortField(sort_column)
        # log_func.debug(u'Sort column <%s>' % sort_field)

        if sort_field is not None:
            # The analysis is performed on the first record
            first_record = recordset[0]
            # log_func.debug(u'First record %s\tFields: %s\tRecord type: %s' % (str(first_record),
            #                                                                   self.refobj_col_names, type(first_record)))
            if isinstance(first_record, dict):
                # Sorting occurs in several fields at once
                # Define a sequence of sorting fields
                # (exclude the code field only if we explicitly sort by it)
                field_sequence = [sort_field] + [fld for fld in self.refobj_col_names if fld not in ('cod', sort_field)]
                is_reverse = self.isReverseSort(sort_column)
                # log_func.debug(u'Sort columns: %s\tis reverse: %s' % (field_sequence, is_reverse))
                # Used operator.itemgetter
                # to determine the sort grouping order
                # operator.itemgetter('a', 'b', 'c') is analog
                # lambda rec: (rec['a'], rec['b'], rec['c'])
                # but faster
                new_recordset = sorted(recordset,
                                       key=operator.itemgetter(*field_sequence),
                                       reverse=is_reverse)
            elif isinstance(first_record, list) or isinstance(first_record, tuple):
                # Get record field indices.
                # We get the recordset from the directory and the order of the fields
                # may not correspond to the order of the displayed fields
                sort_field_idx = self.getSortFieldIdx(sort_column)
                # Sorting occurs in several fields at once
                # Define a sequence of sorting fields
                # (exclude the code field only if we explicitly sort by it)
                field_sequence_idx = [sort_field_idx] + [i for i in range(len(self.refobj_col_names)) if i not in (0, sort_field_idx)]
                field_names = self.ref_obj.getStorage().getSpravFieldNames()
                new_field_sequence_idx = [field_names.index(self.refobj_col_names[i]) for i in field_sequence_idx]
                is_reverse = self.isReverseSort(sort_column)
                # log_func.debug(u'Sort:\n\t%s\n\t%s' % (str(recordset), str(new_field_sequence_idx)))
                # log_func.debug(u'Sort columns: %s\tis reverse: %s' % (new_field_sequence_idx, is_reverse))
                new_recordset = sorted(recordset,
                                       key=operator.itemgetter(*new_field_sequence_idx),
                                       reverse=is_reverse)
            else:
                log_func.warning(u'Sort. Not supported record types <%s>' % type(first_record))
                new_recordset = recordset

            return new_recordset
        # If any error occurs, return unsorted recordset
        return recordset

    def setRefObjTreeItem(self, parent_item, record):
        """
        Set tree item.

        :param parent_item: Tree item parent.
        :param record: Record associated with an item.
        """
        # item_level = self.getTreeListCtrlItemLevelIdx(treelistctrl=self.refobj_treeListCtrl, item=parent_item)
        code = record.get(self.ref_obj.getCodColumnName(), None)
        # Code Activity Check
        if self.ref_obj and self.ref_obj.isActive(code):
            item = self.refobj_treeListCtrl.AppendItem(parent_item, code)
            self.setTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=item, data=record)
            # Column filling
            for i, field_name in enumerate(self.refobj_col_names[1:]):
                value = record.get(field_name, u'')
                # Type checking
                if value is None:
                    value = u''
                elif not isinstance(value, str):
                    value = str(value)
                # log_func.debug(u'Value <%s>. Index %s' % (value, i))
                self.refobj_treeListCtrl.SetItemText(item, value, i + 1)
        
            if self.ref_obj.isChildrenCodes(code):
                # There are subcodes. To display + in the tree control, you need to add a dummy element
                self.refobj_treeListCtrl.AppendItem(item, TREE_ITEM_LABEL)

    def findTreeChildItem(self, item_text, cur_item=None):
        """
        Search for a child of a tree by text.

        :param item_text: Tree item text.
        """
        if cur_item is None:
            cur_item = self.root
            
        find_item = None
        child_item, cookie = self.refobj_treeListCtrl.GetFirstChild(cur_item)
        while child_item and child_item.IsOk():
            if item_text == self.refobj_treeListCtrl.GetItemText(child_item):
                find_item = child_item
                break
            child_item, cookie = self.refobj_treeListCtrl.GetNextChild(cur_item, cookie)
        return find_item

    def initLevelTree(self, item):
        """
        Initialize a tree item branch.

        :param item: Tree item.
        """
        find_item = self.findTreeChildItem(TREE_ITEM_LABEL, item)
        if find_item:
            self.refobj_treeListCtrl.Delete(find_item)

        # Заполнение пустого уровня
        if not self.refobj_treeListCtrl.ItemHasChildren(item):
            record = self.getTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=item)
            code = record['cod']
            self.setRefObjLevelTree(item, code)
  
    def findRefObjTreeItem(self, parent_item, code=None):
        """
        Search for a tree item by code.

        :param parent_item: Parent tree item.
        :param code: The code associated with the tree item.
        :return: The tree item found, or None if the item is not found
        """
        # Search code in current item
        record = self.getTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=parent_item)
        if record:
            if code == record['cod']:
                return parent_item
        
        # Search in child elements
        find_result = None
        child_item, cookie = self.refobj_treeListCtrl.GetFirstChild(parent_item)
        while child_item and child_item.IsOk():
            record = self.getTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=child_item)
            if record:
                if code == record['cod']:
                    find_result = child_item
                    break
            child_item, cookie = self.refobj_treeListCtrl.GetNextChild(parent_item, cookie)
        
        # Found nothing at this level
        # Need to go down one level
        if not find_result:
            child_item, cookie = self.refobj_treeListCtrl.GetFirstChild(parent_item)
            while child_item and child_item.IsOk():
                self.initLevelTree(child_item)
                find_result = self.findRefObjTreeItem(child_item, code)
                if find_result:
                    break
                child_item, cookie = self.refobj_treeListCtrl.GetNextChild(parent_item, cookie)

        if find_result:
            # If found in this thread then open it
            self.refobj_treeListCtrl.Expand(parent_item)
            
        return find_result
  
    def selectRefObjTreeItem(self, code, parent_item=None):
        """
        Find and select a tree element by code.
        
        :param code: The code associated with the tree item.
        :return: The tree item found, or None if the item is not found
        """
        if parent_item is None:
            parent_item = self.root
        
        item = self.findRefObjTreeItem(parent_item, code)
        if item:
            # Scroll to the selected tree item
            self.refobj_treeListCtrl.ScrollTo(item)
            # Select tree item
            self.refobj_treeListCtrl.SelectItem(item)
            # The component loses focus when the search button is pressed
            # Further, when a tree element is selected, the selected element is not highlighted
            # To restore the highlight of an element,
            # you need to return focus to the tree component
            self.refobj_treeListCtrl.SetFocus()
            return item
        return None        

    def getSelectedCode(self):
        """
        Get selected code.
        """
        item = self.refobj_treeListCtrl.GetSelection()
        if item and item.IsOk():
            record = self.getTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=item)
            return record.get('cod', None) if record is not None else None
        return None
    
    def editRefObj(self):
        """
        Edit ref object.
        """
        return wx_editdlg.editRefObjDlg(parent=self, ref_obj=self.ref_obj)
        
    def onEditButtonClick(self, event):
        """
        Button handler <Editing ...>
        """
        ok_edit = self.editRefObj()
        if ok_edit:
            # If editing is successful, then update the tree
            self.refobj_treeListCtrl.DeleteAllItems()
            self.setRefObjTree()
            # Delete search text
            self.search_textCtrl.SetValue(u'')            
            
        self.hidePopupInfo()
        event.Skip()
        
    def onCancelButtonClick(self, event):
        """
        <Cancel> button handler.
        """
        self.EndModal(wx.ID_CANCEL)
        self.hidePopupInfo()
        event.Skip()
        
    def onOkButtonClick(self, event):
        """
        <OK> button handler.
        """
        self.EndModal(wx.ID_OK)
        self.hidePopupInfo()
        event.Skip()
        
    def onRefObjTreeItemExpanded(self, event):
        """
        Tree item expand handler.
        """
        item = event.GetItem()
        self.initLevelTree(item)
        event.Skip()

    def getSearchFieldname(self):
        """
        Determine the selected field name by which we search.
        """
        idx = self.search_field_choice.GetSelection()
        return self.refobj_search_col_names[idx] if 0 <= idx < len(self.refobj_search_col_names) else 'name'

    def clearSearch(self):
        """
        Clear search options. Used when caching forms.
        """
        # Codes found matching search string
        self.search_codes = list()
        # Current found code in the list of found codes
        self.search_code_idx = 0
        # A sign of the need to update the list of searched codes
        self.not_actual_search = False

        self.search_field_choice.Select(0)
        self.search_textCtrl.SetValue(u'')

    def getSearchCodes(self, search_txt, search_fieldname=None):
        """
        Update found codes matching search parameters.

        :param search_txt: search text.
        :param search_fieldname: Search field.
        :return: A list of codes matching the search parameters or
            an empty list in case of an error.
        """
        if search_fieldname is None:
            search_fieldname = self.getSearchFieldname()

        # --- Processing sort options ---
        order_by = None
        is_reverse = False
        if self.sort_column:
            sort_field = self.getSortField(self.sort_column)
            is_reverse = self.isReverseSort(self.sort_column)
            order_by = [sort_field] + [fld for fld in self.refobj_col_names if fld not in ('cod', sort_field)]
        # ----------------------------------------

        try:
            search_codes = self.ref_obj.searchCodesByColValue(search_txt, search_fieldname,
                                                              sort_columns=order_by, reverse=is_reverse)
        except:
            log_func.fatal(u'Error searching codes by text')
            search_codes = list()

        # log_func.debug(u'Search codes: %s Order by: %s Is desc: %s' % (search_codes, sort_columns, reverse))
        if search_codes:
            # Remember the codes found in the buffer
            self.search_codes = search_codes
            self.search_code_idx = 0
        return search_codes

    def onSearchToolClicked(self, event):
        """
        Record name search tool handler.
        """
        search_txt = self.search_textCtrl.GetValue()
        if search_txt:
            do_find = True
            if self.not_actual_search:
                search_codes = self.getSearchCodes(search_txt)
                log_func.debug(u'Search codes %s' % str(search_codes))
                if not search_codes:
                    wxdlg_func.openWarningBox(_(u'WARNING'),
                                              _(u'No records found matching search string'))
                    do_find = False
                self.not_actual_search = False
            else:
                # If you do not need to update the list of found codes,
                # then simply search for the next code in the list
                self.search_code_idx += 1
                if self.search_code_idx >= len(self.search_codes):
                    self.search_code_idx = 0
                    
            if do_find and self.search_codes:
                find_code = self.search_codes[self.search_code_idx]
                self.selectRefObjTreeItem(find_code)
        else:
            wxdlg_func.openWarningBox(_(u'WARNING'), _(u'No search bar selected'))
            
        event.Skip()        
        
    def onSearchText(self, event):
        """
        Search text modify handler.
        """
        # search_txt = event.GetString()
        # log_func.debug(u'Change search text <%s>' % search_txt)
        self.not_actual_search = True
        event.Skip()

    def onItemSelectChanged(self, event):
        """
        Tree item selection handler.
        """
        item = event.GetItem()
        if item:
            record = self.getTreeListCtrlItemData(treelistctrl=self.refobj_treeListCtrl, item=item)
            if record and str_func.isMultiLineText(record['name']):
                # If the text is multi-line, then display an additional pop-up window
                self.hidePopupInfo()
                self.showPopupInfo(item, record['name'])
            else:
                self.hidePopupInfo()
        event.Skip()

    def calcPopupInfoPos(self, item=None):
        """
        Calculation of the position of the pop-up window for the selected tree element.

        :param item: The element of the tree to which the displayed text belongs.
        :return: x, y - Estimated position values.
        """
        if item is None:
            # If the item is not defined, then the pop-up window is not attached to it
            r_x, r_y, r_w, r_h = 0, 0, 0, 0
        else:
            r_x, r_y, r_w, r_h = self.refobj_treeListCtrl.GetBoundingRect(item, False)

        if r_x == 0 and r_y == 0:
            # Most likely we just can’t determine the coordinates
            return -1, -1

        scr_x, scr_y = self.refobj_treeListCtrl.GetScreenPosition()
        pos_x, pos_y = self.refobj_treeListCtrl.GetPosition()
        col_w = sum(
            [self.refobj_treeListCtrl.GetColumnWidth(col) for col in range(self.refobj_treeListCtrl.GetColumnCount())])
        x = scr_x + pos_x + col_w
        y = scr_y + pos_y + r_y
        return x, y

    def showPopupInfo(self, item=None, txt=u'', position=None):
        """
        Display multi-line text to view complex title.
            Used for example to display simple patterns.

        :param item: The element of the tree to which the displayed text refers.
        :param txt: Multi-line text.
        :param position: Popup display coordinates.
        :return: True/False.
        """
        if position is None:
            x, y = self.calcPopupInfoPos(item)
        else:
            x, y = position

        if x == -1 and y == -1:
            # Most likely we just can’t determine the coordinates
            return

        if self.popup_win is None:
            self.popup_win = wx.PopupWindow(self, wx.SIMPLE_BORDER)
            panel = wx.Panel(self.popup_win)
            panel.SetBackgroundColour('CORNSILK')

            static_txt = wx.StaticText(panel, -1, txt, pos=(10, 10))
            font = wx.Font(pointSize=10,
                           family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL,
                           faceName='Courier New')
            static_txt.SetFont(font)

            size = static_txt.GetBestSize()
            self.popup_win.SetSize((size.width+20, size.height+20))
            panel.SetSize((size.width+20, size.height+20))

            self.popup_win.Position(wx.Point(x, y), (0, 0))
            self.popup_win.Show()

    def hidePopupInfo(self):
        """
        Hide additional data in popup.
        """
        if self.popup_win:
            self.popup_win.Show(False)
            self.popup_win = None

    def getSelectedColIdx(self, mouse_x):
        """
        Determine the index of the selected column.

        :param mouse_x: Mouse coordinate in the list header.
        :return: Index of the column that was clicked on with the mouse.
            If the column is not found, then returns -1.
        """
        i = 0
        column_areas = list()
        for i_col in range(self.refobj_treeListCtrl.GetColumnCount()):
            width = self.refobj_treeListCtrl.GetColumnWidth(i_col)
            column_areas.append((i, i + width))
            i += width
        find_col = [i for i, area in enumerate(column_areas) if area[0] < mouse_x < area[1]]
        find_col = find_col[0] if find_col else -1
        return find_col

    def refreshSortColumn(self, sort_column=None):
        """
        Refresh the sorted column of the list control.

        :param sort_column: Sort column.
        :return: True/False. 
        """
        if sort_column is None:
            sort_column = self.sort_column

        if sort_column is None:
            # Remove all characters
            for i_col in range(self.refobj_treeListCtrl.GetColumnCount()):
                self.refobj_treeListCtrl.SetColumnImage(i_col, -1)
        elif isinstance(sort_column, int) and sort_column > 0:
            i_col = self.getSortFieldIdx(sort_column)
            self.refobj_treeListCtrl.SetColumnImage(i_col, self.sort_ascending_img)
        elif isinstance(sort_column, int) and sort_column < 0:
            i_col = self.getSortFieldIdx(sort_column)
            self.refobj_treeListCtrl.SetColumnImage(i_col, self.sort_descending_img)
        elif isinstance(sort_column, str) and not sort_column.startswith(SORT_REVERSE_SIGN):
            i_col = self.getSortFieldIdx(sort_column)
            self.refobj_treeListCtrl.SetColumnImage(i_col, self.sort_ascending_img)
        elif isinstance(sort_column, str) and sort_column.startswith(SORT_REVERSE_SIGN):
            i_col = self.getSortFieldIdx(sort_column)
            self.refobj_treeListCtrl.SetColumnImage(i_col, self.sort_descending_img)
        return True

    def onHeaderMouseLeftClick(self, event):
        """
        The mouse click handler on the header of the list.
        """
        find_col = self.getSelectedColIdx(event.GetX())

        if find_col >= 0:
            # An increase of 1 was made in order to take into account
            # the first column with index 0
            find_col_name = self.getSortField(find_col + 1)
            if self.sort_column is None:
                # Sort was not enabled
                # Set sort ascending
                self.refobj_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            elif self.sort_column > 0 and self.sort_column == find_col_name:
                # Sorting in increasing order for this column has already been enabled
                # Set sort descending
                self.refobj_treeListCtrl.SetColumnImage(find_col, self.sort_descending_img)
                self.sort_column = SORT_REVERSE_SIGN + find_col_name
            elif self.sort_column < 0 and self.sort_column == find_col_name:
                # Descending order has already been enabled for this column
                # Set sort ascending
                self.refobj_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            elif self.sort_column != find_col_name:
                # Sort by another column
                # Disable sorting the previous column
                prev_col = -1
                if isinstance(self.sort_column, str):
                    prev_col_name = self.sort_column if not self.sort_column.startswith(SORT_REVERSE_SIGN) else self.sort_column[1:]
                    prev_col = self.refobj_col_names.index(prev_col_name)
                elif isinstance(self.sort_column, int):
                    prev_col = abs(self.sort_column) - 1
                self.refobj_treeListCtrl.SetColumnImage(prev_col, -1)
                # Enable ascending sort for new column
                self.refobj_treeListCtrl.SetColumnImage(find_col, self.sort_ascending_img)
                self.sort_column = find_col_name
            else:
                log_func.warning(u'Error define sort column <%s>. Prev value <%s>' % (find_col, self.sort_column))
                self.sort_column = None

            if self.sort_column is not None:
                self.refreshRefObjTree(is_progress=False, sort_column=self.sort_column)
                # Changed sorting -> the search order has changed
                self.not_actual_search = True

        event.Skip()


def choiceRefObjCodDlg(parent=None, ref_obj=None, fields=None,
                       default_selected_code=None, search_fields=None,
                       clear_cache=False):
    """
    Function for calling the ref object code selection dialog box.
    Dialogs are cached in the cache dictionary CHOICE_DLG_CACHE.
    Dialogs are created only for the first time, then only their call occurs.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param fields: List of field names that
         must be displayed in the tree control.
         If no fields are specified, only
         <Code> and <Name>.
    :param default_selected_code: The selected code is the default.
         If None, then nothing is selected.
    :param search_fields: Fields to search for.
         If not specified, then the displayed fields are taken.
    :param clear_cache: Clear cache?
    :return: Selected ref object item cod or None if error.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for choice')
        return None

    code = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHOICE_DLG_CACHE
        if clear_cache:
            CHOICE_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_choice_dlg.dat')

        if refobj_name not in CHOICE_DLG_CACHE or wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = iqRefObjChoiceTreeDlg(ref_obj=ref_obj,
                                        default_selected_code=default_selected_code,
                                        parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHOICE_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHOICE_DLG_CACHE and not wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = CHOICE_DLG_CACHE[refobj_name]
            dlg.clearSearch()

        result = None
        if dlg:
            result = dlg.ShowModal()
            dlg.saveCustomData(save_filename=ext_data_filename,
                               save_data=dict(sort_column=dlg.sort_column))

        if result == wx.ID_OK:
            code = dlg.getSelectedCode()
        
        # dlg.Destroy()
    except:
        log_func.fatal(u'Error choice ref object <%s> code' % refobj_name)
    return code


def choiceRefObjRecDlg(parent=None, ref_obj=None, fields=None,
                       default_selected_code=None, search_fields=None,
                       clear_cache=False):
    """
    Function for calling the ref object record selection dialog box.
    Dialogs are cached in the cache dictionary CHOICE_DLG_CACHE.
    Dialogs are created only for the first time, then only their call occurs.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param fields: List of field names that
         must be displayed in the tree control.
         If no fields are specified, only
         <Code> and <Name>.
    :param default_selected_code: The selected code is the default.
         If None, then nothing is selected.
    :param search_fields: Fields to search for.
         If not specified, then the displayed fields are taken.
    :param clear_cache: Clear cache?
    :return: Selected ref object item record dictionary or None if error.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for choice')
        return None

    selected_rec = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHOICE_DLG_CACHE
        if clear_cache:
            CHOICE_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_choice_dlg.dat')

        if refobj_name not in CHOICE_DLG_CACHE or wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = iqRefObjChoiceTreeDlg(ref_obj=ref_obj,
                                        default_selected_code=default_selected_code,
                                        parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHOICE_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHOICE_DLG_CACHE and not wxobj_func.isWxDeadObject(CHOICE_DLG_CACHE[refobj_name]):
            dlg = CHOICE_DLG_CACHE[refobj_name]
            dlg.clearSearch()

        result = None
        if dlg:
            result = dlg.ShowModal()
            dlg.saveCustomData(save_filename=ext_data_filename,
                               save_data=dict(sort_column=dlg.sort_column))

        if result == wx.ID_OK:
            code = dlg.getSelectedCode()
            selected_rec = ref_obj.getRecByCod(code)

        # dlg.Destroy()
    except:
        log_func.fatal(u'Error choice ref object <%s> record' % refobj_name)
    return selected_rec


def delCachedChoiceRefObjDlg(ref_obj=None):
    """
    Remove the selection dialog box from the cache.

    :param ref_obj: Reference data object.
    :return: True - form removed from cache/False - form not removed from cache for some reason.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for remove choice dialog from cache')
        return False

    global CHOICE_DLG_CACHE

    sprav_name = ref_obj.getName()
    if sprav_name in CHOICE_DLG_CACHE:
        dlg = CHOICE_DLG_CACHE[sprav_name]
        dlg.Destroy()

        del CHOICE_DLG_CACHE[sprav_name]
        return True
    return False

