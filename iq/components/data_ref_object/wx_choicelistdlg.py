#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog box for selecting an item by level in a list form.
"""

import sys
import os
import os.path
import wx
import gettext

from . import refobj_dialogs_proto

import iq
from ...util import log_func
from ...util import lang_func
from ... import passport

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqRefObjChoiceListDialog(refobj_dialogs_proto.iqChoiceListDlgProto):
    """
    Dialog box for selecting an item by level in a list form.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        refobj_dialogs_proto.iqChoiceListDlgProto.__init__(self, *args, **kwargs)

        self._ref_object = None
        self._selected_cod = None

        self._cur_cod = (None,)

        # Last searched string
        self._last_search_value = None
        # Last result found
        self._last_search_result = None
        self._last_search_idx = 0

        self.refobj_list_ctrl.InsertColumn(0, _(u'Cod'))
        self.refobj_list_ctrl.InsertColumn(1, _(u'Name'))
        self.refobj_list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.refobj_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

    def _getStrCode(self, code=None):
        """
        Convert structural code to string form.
        
        :param code: Code as tuple.
        :return: Code as string or None if empty code.
        """
        if code is None:
            code = self._cur_cod
        return u'' if code and code[0] is None else ''.join(code)

    def isEmptyCode(self, code=None):
        """
        Check for empty code.

        :param code: Code as tuple.
        :return: True/False.
        """
        if code is None:
            code = self._cur_cod
        result = False
        if not code:
            result = True
        elif code and code[0] is None:
            result = True
        return result

    def setNextCurCode(self, code):
        """
        Set the next level of code.

        :param code: Code.
        :return: Current level code.
        """
        code_list = [subcode for subcode in self._ref_object.getCodAsTuple(code) if subcode]
        self._cur_cod = tuple(code_list)

        code_path = self.getCodePath(self._cur_cod)
        self.path_statictext.SetLabel(code_path)

        return self._cur_cod

    def setPrevCurCode(self):
        """
        Set previous code level.

        :return: Previous level code.
        """
        if len(self._cur_cod) > 1:
            self._cur_cod = self._cur_cod[:-1]
        else:
            if self._cur_cod[0]:
                self._cur_cod = (None,)

        code_path = self.getCodePath(self._cur_cod)
        self.path_statictext.SetLabel(code_path)
        return self._cur_cod

    def getCodePath(self, code):
        """
        Путь справочника по структурному коду.

        :param code: Код справочника в виде кортежа.
        :return:
        """
        names = []
        for i, cod in enumerate(code):
            if cod:
                name = self._ref_object.Find(u''.join(code[:i + 1]))
                if name:
                    names.append(name)
        return u' -> '.join(names)

    def setRefObj(self, ref_obj):
        """
        Set active reference object.

        :param ref_obj: Reference object.
        """
        self._ref_object = ref_obj

        if self._ref_object is not None:
            description = self._ref_object.description if self._ref_object.description else self._ref_object.name
            self.SetLabel(description)
            code = self._getStrCode()
            dataset = self._ref_object.getStorage().getLevelTable(code)
            self.setDataset(dataset)
        else:
            log_func.error(u'Not define ref object for choice')

    def setDataset(self, dataset):
        """
        set ref object dataset.
        """
        if dataset:
            self.refobj_list_ctrl.DeleteAllItems()

            for record in dataset:
                code = record[0]
                name = record[1]

                index = self.refobj_list_ctrl.InsertStringItem(sys.maxsize, code)
                self.refobj_list_ctrl.SetStringItem(index, 1, name)
            self.refobj_list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.refobj_list_ctrl.SetColumnWidth(1, wx.LIST_AUTOSIZE)

            # On/off buttons to go to the parent level
            self.dlg_toolbar.EnableTool(self.return_tool.GetId(),
                                        not self.isEmptyCode())
        else:
            log_func.error(u'Not define ref object dataset (cod <%s>) for choice' % self._getStrCode())

    def selectCode(self, code):
        """
        Select a code and display it in the list.
        """
        code_list = self._ref_object.getCodAsTuple(code)
        if code_list:
            code_list = [sub_code for sub_code in code_list if sub_code]
            self._cur_cod = code_list[:-1]
        else:
            self._cur_cod = (None,)
        self.setSelectedCode(code)

        parent_code = self._getStrCode()
        dataset = self._ref_object.getStorage().getLevelTable(parent_code)
        self.setDataset(dataset)

        code_path = self.getCodePath(self._cur_cod)
        self.path_statictext.SetLabel(code_path)

        try:
            codes = [rec[0] for rec in dataset]
            idx = codes.index(code)
            self.refobj_list_ctrl.Select(idx)
            self.refobj_list_ctrl.Focus(idx)
        except ValueError:
            log_func.error(u'Error define ref object code <%s> when choosing from <%s>' % (code, parent_code))

    def getRefObj(self):
        """
        Get reference object.
        """
        return self._ref_object

    def getSelectedCode(self):
        """
        Get seleced cod.
        """
        return self._selected_cod

    def setSelectedCode(self, code):
        """
        Set selected code.
        """
        self._selected_cod = code

    def onCancelButtonClick(self, event):
        """
        """
        self._selected_cod = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onSpravListItemActive(self, event):
        """
        Double-click handler on a list item.
        """
        current_item = event.Index
        self.setSelectedCode(self.refobj_list_ctrl.GetItemText(current_item))
        dataset = self._ref_object.getStorage().getLevelTable(self._selected_cod)
        if dataset:
            self.setNextCurCode(self._selected_cod)
        self.setDataset(dataset)

        event.Skip()

    def onSpravListItemSelect(self, event):
        """
        List item selection handler.
        """
        current_item = event.Index
        self.setSelectedCode(self.refobj_list_ctrl.GetItemText(current_item))
        event.Skip()

    def onReturnToolClick(self, event):
        """
        Return to previous level button.
        """
        self.setPrevCurCode()
        code = self._getStrCode()
        dataset = self._ref_object.getStorage().getLevelTable(code)
        self.setDataset(dataset)
        event.Skip()

    def onSearchToolClick(self, event):
        """
        Search button click handler.
        """
        search_value = self.search_textctrl.GetValue()
        if search_value and search_value != self._last_search_value:
            # Search by name
            search_result = self._ref_object.getStorage().search(search_value)
            code = search_result[0]
            self.selectCode(code)
            self._last_search_value = search_value
            self._last_search_result = search_result
            self._last_search_idx = 0
        elif search_value and search_value == self._last_search_value:
            # Just go to the next line in the list of found
            self._last_search_idx += 1
            if self._last_search_idx >= len(self._last_search_result):
                self._last_search_idx = 0
            code = self._last_search_result[self._last_search_idx]
            self.selectCode(code)

        event.Skip()


def getRefObjChoiceListDlg(parent=None, ref_obj=None):
    """
    Calling up the directory code selection dialog box.

    :param parent: Parent window.
    :param ref_obj: Reference data object.
        It can be set by both an object and a passport.
    :return: Selected code.
    """
    result = None
    if parent is None:
        parent = wx.GetApp().GetTopWindow()
    if ref_obj:
        if passport.isPassport(ref_obj):
            ref_obj = iq.KERNEL.getObject(ref_obj)

        dlg = None
        try:
            dlg = iqRefObjChoiceListDialog(parent)
            dlg.setRefObj(ref_obj)
            dlg.ShowModal()
            result = dlg.getSelectedCode()
            dlg.Destroy()
            dlg = None
        except:
            if dlg:
                dlg.Destroy()
            log_func.fatal(u'Error choice ref object code')
    else:
        log_func.error(u'Not define ref object for choice code')
    return result

