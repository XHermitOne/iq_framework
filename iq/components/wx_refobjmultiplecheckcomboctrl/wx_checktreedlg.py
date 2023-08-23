#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog form for ref object element / code check selection.
All data is presented in tree view.
"""

import os.path
import wx

from ...util import log_func
from ...util import file_func

# from ...engine.wx import wxbitmap_func
# from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import wxobj_func

from ..data_ref_object import wx_choicetreedlg

__version__ = (0, 0, 0, 1)

# Dialog cache to optimize call selection
CHECK_DLG_CACHE = dict()


class iqRefObjCheckTreeDlg(wx_choicetreedlg.iqRefObjChoiceTreeDlg):
    """
    Dialog form for ref object element / code check selection.
    """
    def __init__(self, ref_obj=None, default_selected_code=None,
                 *args, **kwargs):
        """
        Constructor.

        :param ref_obj: Reference data object.
        :param default_selected_code: Selected default code.
        """
        wx_choicetreedlg.iqRefObjChoiceTreeDlg.__init__(self, ref_obj=ref_obj,
                                                        default_selected_code=default_selected_code,
                                                        *args, **kwargs)

    def onInitDlg(self, event):
        """
        Dialog initialization.
        """
        # log_func.debug(u'onInit')
        if self.default_selected_code:
            log_func.info(u'Check codes %s in ref object [%s]' % (self.default_selected_code,
                                                                  self.ref_obj.getName()))
            for checked_cod in self.default_selected_code:
                if self.ref_obj.hasCod(checked_cod):
                    self.checkRefObjTreeItem(checked_cod)
                else:
                    log_func.warning(u'Code <%s> not found in ref object [%s]' % (checked_cod,
                                                                                  self.ref_obj.getName()))
        event.Skip()

    def checkRefObjTreeItem(self, code, parent_item=None):
        """
        Find and check a tree element by code.

        :param code: The code associated with the tree item.
        :return: The tree item found, or None if the item is not found
        """
        if parent_item is None:
            parent_item = self.root

        item = self.findRefObjTreeItem(parent_item, code)
        if item:
            # Scroll to the selected tree item
            self.refobj_treeListCtrl.ScrollTo(item)
            # Check tree item
            self.refobj_treeListCtrl.CheckItem(item, checked=True)
            # The component loses focus when the search button is pressed
            # Further, when a tree element is selected, the selected element is not highlighted
            # To restore the highlight of an element,
            # you need to return focus to the tree component
            # self.refobj_treeListCtrl.SetFocus()
            return item
        return None

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
            item = self.refobj_treeListCtrl.AppendItem(parent_item, code, ct_type=1)
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
                self.refobj_treeListCtrl.AppendItem(item, wx_choicetreedlg.TREE_ITEM_LABEL)

    def getCheckedCodes(self):
        """
        Get checked codes.

        :return: Checked code list.
        """
        checked_records = self.getTreeListCtrlCheckedItemsDataList(treelistctrl=self.refobj_treeListCtrl)
        checked_codes = [record.get('cod', None) for record in checked_records]
        return checked_codes

    def getCheckedRecords(self):
        """
        Get checked records.

        :return: Checked record list.
        """
        checked_records = self.getTreeListCtrlCheckedItemsDataList(treelistctrl=self.refobj_treeListCtrl)
        return checked_records


def checkRefObjCodesDlg(parent=None, ref_obj=None, fields=None,
                        default_checked_codes=None, search_fields=None,
                        clear_cache=False):
    """
    Function for calling the ref object code selection dialog box.
    Dialogs are cached in the cache dictionary CHECK_DLG_CACHE.
    Dialogs are created only for the first time, then only their call occurs.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
    :param fields: List of field names that
         must be displayed in the tree control.
         If no fields are specified, only
         <Code> and <Name>.
    :param default_checked_codes: The checked codes is the default.
         If None, then nothing is checked.
    :param search_fields: Fields to search for.
         If not specified, then the displayed fields are taken.
    :param clear_cache: Clear cache?
    :return: Selected ref object item cod or None if error.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for check')
        return None

    code = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHECK_DLG_CACHE
        if clear_cache:
            CHECK_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_check_dlg.dat')

        if refobj_name not in CHECK_DLG_CACHE or wxobj_func.isWxDeadObject(CHECK_DLG_CACHE[refobj_name]):
            dlg = iqRefObjCheckTreeDlg(ref_obj=ref_obj,
                                       default_selected_code=default_checked_codes,
                                       parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHECK_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHECK_DLG_CACHE and not wxobj_func.isWxDeadObject(CHECK_DLG_CACHE[refobj_name]):
            dlg = CHECK_DLG_CACHE[refobj_name]
            dlg.clearSearch()

        result = None
        if dlg:
            result = dlg.ShowModal()
            dlg.saveCustomData(save_filename=ext_data_filename,
                               save_data=dict(sort_column=dlg.sort_column))

        if result == wx.ID_OK:
            code = dlg.getCheckedCodes()

        # dlg.Destroy()
    except:
        log_func.fatal(u'Error check ref object <%s> code' % refobj_name)
    return code


def checkRefObjRecsDlg(parent=None, ref_obj=None, fields=None,
                       default_selected_code=None, search_fields=None,
                       clear_cache=False):
    """
    Function for calling the ref object record selection dialog box.
    Dialogs are cached in the cache dictionary CHECK_DLG_CACHE.
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
        log_func.warning(u'Not define ref object for check')
        return None

    selected_rec = None
    refobj_name = ref_obj.getName()
    try:
        if parent is None:
            app = wx.GetApp()
            main_win = app.GetTopWindow()
            parent = main_win

        global CHECK_DLG_CACHE
        if clear_cache:
            CHECK_DLG_CACHE = dict()

        dlg = None
        # Additional data filename
        ext_data_filename = os.path.join(file_func.getProjectProfilePath(),
                                         refobj_name + '_check_dlg.dat')

        if refobj_name not in CHECK_DLG_CACHE or wxobj_func.isWxDeadObject(CHECK_DLG_CACHE[refobj_name]):
            dlg = iqRefObjCheckTreeDlg(ref_obj=ref_obj,
                                       default_selected_code=default_selected_code,
                                       parent=parent)
            # Download additional data
            ext_data = dlg.loadCustomData(save_filename=ext_data_filename)
            dlg.sort_column = ext_data.get('sort_column', None) if ext_data else None

            fields = list() if fields is None else fields
            search_fields = fields if search_fields is None else search_fields
            dlg.init(fields, search_fields)

            CHECK_DLG_CACHE[refobj_name] = dlg
        elif refobj_name in CHECK_DLG_CACHE and not wxobj_func.isWxDeadObject(CHECK_DLG_CACHE[refobj_name]):
            dlg = CHECK_DLG_CACHE[refobj_name]
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
        log_func.fatal(u'Error check ref object <%s> record' % refobj_name)
    return selected_rec


def delCachedCheckRefObjDlg(ref_obj=None):
    """
    Remove the selection dialog box from the cache.

    :param ref_obj: Reference data object.
    :return: True - form removed from cache/False - form not removed from cache for some reason.
    """
    if ref_obj is None:
        log_func.warning(u'Not define ref object for remove check dialog from cache')
        return False

    global CHECK_DLG_CACHE

    sprav_name = ref_obj.getName()
    if sprav_name in CHECK_DLG_CACHE:
        dlg = CHECK_DLG_CACHE[sprav_name]
        dlg.Destroy()

        del CHECK_DLG_CACHE[sprav_name]
        return True
    return False
