#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Choice reference object WxPython control as tree.
"""

import wx
import wx.lib.agw.customtreectrl
import wx.lib.platebtn

# from . import icspravtreedatasource
# from ic.components import icwidget

from ...util import log_func

from ...passport import passport

from . import refobjtreedatasource

__version__ = (0, 0, 0, 1)

DEFAULT_ENCODING = 'utf-8'


class iqBoxTree(wx.lib.agw.customtreectrl.CustomTreeCtrl):

    def OnPaint(self, event):
        """
        Handles the wx.EVT_PAINT event.
        """
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        if not self._anchor:
            return

        dc.SetFont(self._normalFont)
        dc.SetPen(self._dottedPen)

        align = self.HasFlag(wx.lib.agw.customtreectrl.TR_ALIGN_WINDOWS)
        y = 20
        self.PaintLevel(self._anchor, dc, 0, y, align)


# # Constants
# SPC_IC_SPRAVTREECOMBOCTRL = {'sprav': None,      # Паспорт справочника-источника данных
#                              'root_code': None,  # Код корневого элемента ветки справочника
#                              'view_all': False,  # Показывать все элементы справочника
#                              'level_enable': -1,  # Номер уровня с которого включаются элементы для выбора
#                              'expand': True,      # Распахнуть
#
#                              'get_label': None,  # Функция определения надписи элемента дерева
#                              'find_item': None,  # Функция поиска элемента дерева
#                              'is_choice_list': False,
#                              'get_selected_code': None,  # Функция получения выбранного кода
#                              'set_selected_code': None,  # Функция установки выбранного кода
#
#                              '__parent__': icwidget.SPC_IC_WIDGET,
#                              }


TREE_HIDDEN_ROOT_LABEL = '<hidden root>'
TREE_HIDDEN_ITEM_LABEL = '<hidden item>'

DEFAULT_ENABLE_ITEM_COLOUR = wx.BLACK
DEFAULT_DISABLE_ITEM_COLOUR = wx.Colour(128, 128, 128)


class iqRefObjTreeComboPopup(wx.ComboPopup):
    """
    Reference object popup tree.
    """
    def Init(self):
        """
        Initialization.
        """
        self.root_name = None
        self.value = None
        self.curitem = None

    def clear(self):
        pass
    
    def Create(self, parent):
        try:
            self.tree = wx.lib.agw.customtreectrl.CustomTreeCtrl(parent, style=wx.TR_HIDE_ROOT
                                                                 | wx.TR_HAS_BUTTONS
                                                                 | wx.TR_SINGLE
                                                                 | wx.TR_LINES_AT_ROOT
                                                                 | wx.SIMPLE_BORDER)
            self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
            self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            return True
        except:
            log_func.fatal(u'Error create reference object popup tree')
        return False

    def GetControl(self):
        return self.tree

    def GetStringValue(self):
        if self.value:
            return self.tree.GetItemText(self.value)
        return ''

    def OnPopup(self):
        if self.value:
            self.tree.EnsureVisible(self.value)
            self.tree.SelectItem(self.value)

    def SetStringValue(self, value):
        # this assumes that item strings are unique...
        root = self.tree.GetRootItem()
        if not root:
            return
        found = self.FindItem(root, value)
        if found:
            self.value = found
            self.tree.SelectItem(found)

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.Size(minWidth, min(200, maxHeight))

    def FindItem(self, parent_item, text):
        """
        Find child item by text.
        """
        item, cookie = self.tree.GetFirstChild(parent_item)
        while item:
            if self.tree.GetItemText(item) == text:
                return item
            if self.tree.ItemHasChildren(item):
                item = self.FindItem(item, text)
            item, cookie = self.tree.GetNextChild(parent_item, cookie)
        return wx.TreeItemId()

    def _getRootLabel(self):
        """
        Get root item label.
        """
        if self.root_name:
            return self.root_name
        return TREE_HIDDEN_ROOT_LABEL

    def AddItem(self, value, parent=None, data=None):
        """
        Add item to tree.
        """
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot(self._getRootLabel())
            parent = root

        item = self.tree.AppendItem(parent, value)
        if data is not None:
            self.tree.SetItemData(item, data)
        return item

    def hasHiddenItem(self, parent_item):
        """
        Does the element have hidden child elements?

        :return: True/False.
        """
        return self.FindItem(parent_item, TREE_HIDDEN_ITEM_LABEL).IsOk()

    def OnMotion(self, event):
        """
        Have the selection follow the mouse, like in a real combobox
        """
        item, flags = self.tree.HitTest(event.GetPosition())
        if item and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.tree.SelectItem(item)
            self.curitem = item
        event.Skip()

    def _isEnableItem(self, item):
        """
        Check that a tree item is included for selection.
        """
        colour = self.tree.GetItemTextColour(item)
        # If the text is black then you can select it
        return colour == DEFAULT_ENABLE_ITEM_COLOUR

    def OnLeftDown(self, event):
        """
        Handler for selecting a tree item.
        """
        # do the combobox selection
        self.curitem = None
        item, flags = self.tree.HitTest(event.GetPosition())
        if item and self._isEnableItem(item) and flags & wx.TREE_HITTEST_ONITEMLABEL:
            self.curitem = item
            self.value = item
            self.Dismiss()
        event.Skip()

    def getSelectedCode(self, alter_cod_field=None):
        """
        Get selected cod.

        :param alter_cod_field: Altered cod field.
        """
        item = self.curitem
        if item:
            data_item = self.tree.GetItemData(item)
            if data_item is not None:
                code = data_item.getCode()
                return code
            else:
                log_func.warning(u'Нет данных элемента дерева <%s>' % item)
        return None

    def setSelectedCod(self, src, cod, alter_cod_field=None):
        """
        Set selected cod.

        :param cod: Ref object cod.
        :param alter_cod_field: Altered cod field.
        """
        pref = cod
        value = None
        if src:
            record = src.findRecord(cod)
            if record:
                value = record['name']
                self.curitem = self.findTreeItem(cod)
                if self.curitem is None:
                    log_func.warning(u'Ref object item <%s> not found. Cod <%s>' % (self._getRootLabel(), cod))
                if alter_cod_field is not None:
                    pref = record[alter_cod_field].strip() or pref
        return value, pref

    def findTreeItem(self, cod, item=None):
        """
        Find tree item by cod.

        :param cod: Ref object cod.
        :param item: Start tree item,
            if None, then the search begins with the root element.
        :return: Tree item id, or None if not found.
        """
        if item is None:
            item = self.tree.GetRootItem()
        data = self.tree.GetItemData(item)
        if data is not None and data.getCode() == cod:
            return item
        else:
            if self.tree.HasChildren(item):
                child, cookie = self.tree.GetFirstChild(item)

                while child and child.IsOk():
                    find_item = self.findTreeItem(cod, child)
                    if find_item:
                        return find_item
                    child, cookie = self.tree.GetNextChild(item, cookie)
        return None


class iqRefObjTreeChoiceListComboPopup(iqRefObjTreeComboPopup):
    """
    Ref object popup tree with the ability to select
    an arbitrary list item.
    """
    def Create(self, parent):
        self.parent = parent
        self.tree = iqBoxTree(parent, style=wx.TR_HIDE_ROOT
                              | wx.TR_HAS_BUTTONS
                              | wx.TR_SINGLE
                              | wx.TR_LINES_AT_ROOT
                              | wx.SIMPLE_BORDER)

        self.tree.Bind(wx.EVT_MOTION, self.OnMotion)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.tree.Bind(wx.lib.agw.customtreectrl.EVT_TREE_ITEM_CHECKED, self.OnChecked)
        self.tree.Bind(wx.lib.agw.customtreectrl.EVT_TREE_ITEM_CHECKING, self.OnChecking)
        # Checked items
        self.check_items = []
        self.pref = u''
        self.tbtn = wx.lib.platebtn.PlateButton(self.tree, wx.ID_ANY, u'ок ', None,
                                                style=wx.lib.platebtn.PB_STYLE_SQUARE)
        self.tbtn.SetBackgroundColour(wx.LIGHT_GREY)
        self.tree.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnOk(self, event):
        cod = self._combo.getSelectedCode('s1')
        self.Dismiss()

    def clear(self):
        self.pref = u''

    def AddItem(self, value, parent=None, data=None):
        """
        Add tree item.
        """
        if not parent:
            root = self.tree.GetRootItem()
            if not root:
                root = self.tree.AddRoot(self._getRootLabel())
            parent = root

        item = self.tree.AppendItem(parent, value, ct_type=1)
        cod = value.split(u' ')[0]
        if cod and cod.strip() in self.pref.split(u','):
            self.check_items.append(item)
            item.Check(True)

        if data is not None:
            self.tree.SetItemData(item, data)
        return item

    def GetStringValue(self):
        txt = u','.join([self.tree.GetItemText(item).split(u' ')[0] for item in self.check_items])
        return txt

    def OnMotion(self, event):
        self.tbtn.SetPosition((0, 0))
        event.Skip()

    def OnChecking(self, event):
        """
        Checking tree item handler.
        """
        item = event.GetItem()
        if item and self._isEnableItem(item):
            event.Skip()

    def OnChecked(self, event):
        """
        Checked tree item handler.
        """
        item = event.GetItem()
        if self.tree.IsItemChecked(item) and item not in self.check_items:
            self.check_items.append(item)
        elif item in self.check_items:
            self.check_items.remove(item)
            self.CheckChilds(item, False)

    def CheckChilds(self, item, checked):
        """
        Transverses the tree and checks/unchecks the items. Meaningful only for check items.
        """
        if not item:
            raise Exception('ERROR: Invalid Tree Item')

        (child, cookie) = self.tree.GetFirstChild(item)

        if child in self.check_items:
            self.check_items.remove(child)

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        while child:
            if child.GetType() == 1 and child.IsEnabled():
                self.tree.CheckItem2(child, checked, torefresh=torefresh)
            self.CheckChilds(child, checked)
            (child, cookie) = self.tree.GetNextChild(item, cookie)
            if child in self.check_items:
                self.check_items.remove(child)

    def OnLeftDown(self, event):
        """
        Select tree item handler.
        """
        self.tbtn.SetPosition((0, 0))
        event.Skip()

    def getSelectedCode(self, *arg, **kwarg):
        """
        Get ref object selected cod.
        """
        lst = [self.tree.GetItemData(item).getCode() for item in self.check_items]
        return u','.join(lst)

    def setSelectedCod(self, src, cod, alter_cod_field=None):
        """
        Set ref object selected cod.

        :param cod: Ref object cod.
        :param alter_cod_field: Altered cod field.
        """
        self.check_items = []
        value = u''
        lst = []
        if src:
            for cod in cod.split(','):
                cod = cod.strip()
                record = src.findRecord(cod)
                if record:
                    if alter_cod_field is not None:
                        lst.append(record[alter_cod_field].strip() or cod)

        self.pref = u','.join(lst)
        return value, self.pref


TREE_CHOICE_LIST_POPUP = 1


class iqRefObjTreeComboCtrlProto(wx.ComboCtrl):
    """
    Reference object cod select control as popup tree.
    """
    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        self._level_enable = kwargs.pop('level_enable', -1)
        self._popup_type = kwargs.pop('popup_type', 0)
        self._complex_load = kwargs.pop('complex_load', -1)

        wx.ComboCtrl.__init__(self, *args, **kwargs)
        # Text entry as find item
        self.Bind(wx.EVT_TEXT_ENTER, self.onTextEnter)

        if self._popup_type == TREE_CHOICE_LIST_POPUP:
            self._combo_popup = iqRefObjTreeChoiceListComboPopup()
            self._combo_popup._combo = self
        else:
            self._combo_popup = iqRefObjTreeComboPopup()

        self.SetPopupControl(self._combo_popup)
        # Build tree branch where expand item
        self._combo_popup.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.onItemExpanded)

        # Current tree item
        self._cur_data_item = None

        self._oldCode = None
        self.view_code = None
        self.view_all = False
        self.root_code = None

        self._data_source = None
        self._label_func = None

        # Expand tree?
        self._expand = kwargs.pop('expand', True)

    def setRefObjByPsp(self, refobj_psp):
        """
        Set reference object tree by passport.
        
        :param refobj_psp: Ref object passport.
        """
        if not passport.isPassport(refobj_psp):
            log_func.error(u'Not valid passport <%s>' % refobj_psp)
            return

        self.Clear()
        self.init(refobj_psp, self.view_code, self.view_all)

    def getRefObjPsp(self):
        """
        Get ref object passport.
        """
        log_func.error(u'Not define getRefObjPsp method in <%s> component' % self.__class__.__name__)
        return None

    def setViewAll(self, view_all=True):
        """
        Set view all items.
        """
        self.view_all = view_all
        if self.view_all:
            psp = self.getRefObjPsp()
            if psp:
                self.Clear()
                self.init(psp, self.view_code, self.view_all)
            else:
                log_func.error(u'Not define ref object passport')

    def viewAll(self):
        """
        Set view all items..
        """
        return self.setViewAll(view_all=True)

    def init(self, refobj_psp=None, root_code=None, view_all=False,
             complex_load=True):
        """
        Init reference object tree.

        :param refobj_psp: Ref object passport.
        :param root_code: Root item cod.
        :param view_all: View all items?
        :param complex_load: Comprehensive download of all data.
        """
        self.view_code = root_code
        self.view_all = view_all
        self.root_code = None if self.view_all else self.view_code

        if refobj_psp:
            self._data_source = refobjtreedatasource.iqRefObjTreeDataSource(refobj_psp, self.root_code)
            self._combo_popup.root_name = self._data_source.getRefObjDescription()
        else:
            log_func.error(u'Not define ref object passport in init <%s> component' % self.__class__.__name__)

        if self._data_source:
            self._combo_popup.tree.DeleteAllItems()
            # Because the root element is hidden, then the parent of all objects is None
            if complex_load:
                self._addTree(self._data_source, None)
            else:
                self._addBranch(self._data_source, None)

            # If plowing is defined, then open the root level
            if self._expand:
                self._combo_popup.tree.Expand(self._combo_popup.tree.GetRootItem())

            if self.view_all:
                self._combo_popup.tree.ExpandAll()
        else:
            log_func.error(u'Not define data source in init <%s> component' % self.__class__.__name__)

    def clear(self):
        """
        Clear.
        """
        self._combo_popup.clear()

    # Clear select
    clearSelect = wx.ComboCtrl.Clear

    def getCurDataItem(self):
        """
        Get current data item.
        """
        return self._cur_data_item

    def getDataSource(self):
        """
        Get data source.
        """
        return self._data_source

    def getRefObj(self):
        """
        Get reference object.
        """
        if self._data_source:
            return self._data_source.getRefObj()
        return None

    def getLevelEnable(self):
        """
        The level from which you can select items.
        """
        return self._level_enable

    def setLabelFunc(self, func):
        """
        Set item label function.
        """
        self._label_func = func

    def getLabelFunc(self, item_data=None):
        """
        Get item label function.
        """
        if self._label_func:
            return self._label_func(item_data)
        return None

    def getAlterLabel(self, item_data):
        """
        Get alter item label.
        """
        return item_data.getDescription()

    def getFindItemFunc(self, *args, **kwargs):
        """
        Get alter find function.
        """
        return None

    def getSelectedCodeFunc(self):
        """
        Get selected cod function.
        """
        return None

    def setSelectedCodeFunc(self, *args, **kwargs):
        """
        Set selected cod function.
        """
        return None

    def _isNotSelectable(self, view_code, cur_code):
        """
        Not selectable item?
        """
        if view_code:
            return self.view_all and ((cur_code == view_code) or (view_code not in cur_code))
        return False

    def _isDisabledItem(self, view_code, level_enable, data_src_item):
        """
        Disabled item?
        """
        if data_src_item is None:
            return True

        if view_code:
            cur_code = data_src_item.getCode()
            return self.view_all and ((cur_code == view_code) or (view_code not in cur_code))
        elif level_enable > 0:
            level_idx = data_src_item.getLevelIdx()
            return level_enable > level_idx
        return False

    def _addBranch(self, data_item, parent_item=None):
        """
        Add tree branch.
        """
        children = data_item.getChildren()

        for child in children:
            # Set current item
            self._cur_data_item = child

            get_label_func = self.getLabelFunc(child)
            label = child.getLabel(get_label_func)
            code = child.getCode()
            sprav = self.getRefObj()
            if sprav and sprav.getActive(code):
                item = self._combo_popup.AddItem(label, parent=parent_item, data=child)
                if self._isDisabledItem(self.view_code, self.getLevelEnable(), child):
                    self._combo_popup.tree.SetItemTextColour(item, DEFAULT_DISABLE_ITEM_COLOUR)
                else:
                    self._combo_popup.tree.SetItemTextColour(item, DEFAULT_ENABLE_ITEM_COLOUR)

                if child.hasChildren():
                    # If has children then create fictitious item
                    self._combo_popup.AddItem(TREE_HIDDEN_ITEM_LABEL, parent=item)

        self._cur_data_item = None

    def _addTree(self, data_item, parent_item=None):
        """
        Add tree.
        """
        children = data_item.getChildren()

        for child in children:
            self._cur_data_item = child

            get_label_func = self.getLabelFunc(child)
            label = child.getLabel(get_label_func)
            code = child.getCode()
            ref_obj = self.getRefObj()
            if ref_obj and ref_obj.isActive(code):
                item = self._combo_popup.AddItem(label, parent=parent_item, data=child)
                if self._isDisabledItem(self.view_code, self.getLevelEnable(), child):
                    self._combo_popup.tree.SetItemTextColour(item, DEFAULT_DISABLE_ITEM_COLOUR)
                else:
                    self._combo_popup.tree.SetItemTextColour(item, DEFAULT_ENABLE_ITEM_COLOUR)

                if child.hasChildren():
                    # If has children then create fictitious item
                    self._addTree(child, parent_item=item)

        self._cur_data_item = None

    def onItemExpanded(self, event):
        """
        Expanded tree item handler.
        """
        item = event.GetItem()

        # If there are hidden items in child items, then
        # delete the hidden item and complete the tree branch of the items
        if self._combo_popup.hasHiddenItem(item):
            # Delete hidden item
            self._combo_popup.tree.DeleteChildren(item)
            # Add branch
            data_item = self._combo_popup.tree.GetItemData(item)
            if data_item:
                self._addBranch(data_item, item)

        event.Skip()

    def findItem(self, find_text, run_find_item_func=True, *args, **kwargs):
        """
        Find item by text.

        :param find_text: Find text.
        :param run_find_item_func: Launch alternative search function?
        :return: Tree item of data source.
        """
        if run_find_item_func:
            kwargs['find_text'] = find_text
            result = self.getFindItemFunc(*args, **kwargs)
            if result:
                return result

        if self._data_source:
            return self._data_source.find(find_text)
        return None

    def onTextEnter(self, event):
        """
        Text entry handler.
        """
        find_str = event.GetString()

        find_item_func = self.getFindItemFunc()
        if find_item_func:
            # Altered find function 
            label = find_item_func
        else:
            label = self.findItem(find_str)

        code = self.getSelectedCode(value=label)
        data_item = self._data_source.findItemByCode(code)

        if label and not self._isDisabledItem(self.view_code, self.getLevelEnable(), data_item):
            self.SetValue(label)
        else:
            self.SetValue(u'')

        event.Skip()

    def getSelectedCode(self, selected_code_func=None, value=None):
        """
        Get selected cod.
        
        :param selected_code_func: Altered selected code function.
        :return: Selected cod as string or None, if cod not selected.
        """
        if selected_code_func:
            return selected_code_func

        return self.getRefObjSelectedCode()

    def getRefObjSelectedCode(self, alt_cod_field=None):
        """
        Get ref object selected cod.
        
        :param alt_cod_field: Altered cod field.
        """
        return self._combo_popup.getSelectedCode(alt_cod_field)

    def setRefObjSelectedCode(self, cod, alt_cod_field=None):
        """
        Set ref object selected cod.

        :param cod: Ref object cod.
        :param alt_cod_field: Altered cod field.
        """
        self._oldCode = cod
        value, pref = self._combo_popup.setSelectedCod(self._data_source, cod, alt_cod_field)
        if value or pref:
            str_value = value if isinstance(value, str) else u''
            return self.SetValue(str_value)
        return self.SetValue(u'')

    def setSelectedCode(self, cod=None, run_selected_cod_func=True, *args, **kwargs):
        """
        Set selected cod.

        :param cod: Cod.
        :param run_selected_cod_func: Run an alternate code setting function?
        :return: Selected cod as string or None, if cod not selected.
        """
        if run_selected_cod_func:
            kwargs['value'] = cod
            result = self.setSelectedCodeFunc(*args, **kwargs)
            if result:
                return result

        self.setRefObjSelectedCode(cod)
        return True

    def getValue(self):
        """
        Get control value.
        """
        return self.getSelectedCode()
    
    def setValue(self, value):
        """
        Set control value.

        :param value: Value as string or as record dictionary.
        """
        code = None
        if isinstance(value, str):
            code = value
        elif isinstance(value, dict):
            code = value.get('cod', None)
        elif value is None:
            code = None
            self._combo_popup.curitem = None
        else:
            log_func.error(u'Not valid value type <%s> in <%s> control' % (type(value), self.__class__.__name__))
        return self.setSelectedCode(code)
    
    def getSelectedRecord(self):
        """
        Get selected ref object record as dictionary.
        """
        rec_dict = None
        code = self.getSelectedCode(self.getSelectedCodeFunc())
        if code:
            if self._data_source is not None:
                data_item = self._data_source.findItemByCode(code)
                if data_item is not None:
                    rec_dict = data_item.getRecDict()

        return rec_dict
