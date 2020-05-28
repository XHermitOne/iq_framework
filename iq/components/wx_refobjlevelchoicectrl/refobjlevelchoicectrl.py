#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference object code selection control by level choice.
"""

import wx

from ...util import log_func

__version__ = (0, 0, 0, 1)

DEFAULT_CODE_DELIMETER = u' '
DEFAULT_ENCODING = 'utf-8'


class iqRefObjLevelChoiceCtrlProto(wx.StaticBox):
    """
    Reference object code selection control by level choice.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.StaticBox.__init__(self, *args, **kwargs)

        self.box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrolled_win = wx.ScrolledWindow(self,  wx.ID_ANY,
                                              wx.DefaultPosition, wx.DefaultSize,
                                              wx.HSCROLL | wx.VSCROLL)
        self.scrolled_win.SetScrollRate(5, 5)

        self.sizer = wx.FlexGridSizer(0, 2, 0, 0)
        self.sizer.AddGrowableCol(1)
        self.sizer.SetFlexibleDirection(wx.BOTH)
        self.sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.scrolled_win.SetSizer(self.sizer)
        # self.scrolled_win.Layout()
        # self.sizer.Fit(self.scrolled_win)

        self.box_sizer.Add(self.scrolled_win, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.box_sizer)
        # self.Layout()

        # Ref object
        self._ref_obj = None
        # Current selected cod as list
        self._selected_code = list()

        # Level choice controls
        self._choice_ctrl_list = list()

    def getSelectedCode(self):
        """
        Get selected ref object cod as tuple.
        """
        return tuple(self._selected_code)

    def setRefObj(self, ref_obj):
        """
        Set ref object.

        :param ref_obj: Reference object.
        """
        self._ref_obj = ref_obj

        if self._ref_obj:
            # Title
            label = self.getLabel()
            if not label:
                # If title not defined then get from ref object
                label = self._ref_obj.getDescription()
            self.SetLabel(label)

            # Level choice controls
            self._selected_code = [None] * self._ref_obj.getLevelCount()
            self._choice_ctrl_list = []
            for i, level_label in enumerate(self._ref_obj.getLevelLabels()):
                label = wx.StaticText(self.scrolled_win, wx.ID_ANY, level_label,
                                      wx.DefaultPosition, wx.DefaultSize, 0)

                level_choices = list()
                if not i:
                    for rec in self._ref_obj.getLevelRecsByCod():
                        if self._ref_obj.isActive(rec[self._ref_obj.getCodColumnName()]):
                            level_choice = (rec[self._ref_obj.getCodColumnName()],
                                            rec[self._ref_obj.getNameColumnName()])
                            level_choices.append(level_choice)

                choice_id = wx.NewId()
                choice = wx.Choice(self.scrolled_win, choice_id,
                                   wx.DefaultPosition, wx.DefaultSize)
                for code, name in level_choices:
                    item = choice.Append(name)
                    choice.SetClientData(item, code)

                # Save level index
                choice.level_index = i
                choice.Bind(wx.EVT_CHOICE, self.onLevelCodeChange, id=choice_id)
                # Reg choice control
                self._choice_ctrl_list.append(choice)

                self.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
                self.sizer.Add(choice, 1, wx.ALL | wx.EXPAND, 5)
            # self.scrolled_win.Layout()
            # self.sizer.Fit(self.scrolled_win)

    def getLabel(self):
        """
        Get label.
        """
        return self.GetLabel()

    def getRefObj(self):
        """
        Get ref object.
        """
        return self._ref_obj

    def getCode(self):
        """
        Get selected ref object cod.
        """
        return ''.join([subcode for subcode in self.getSelectedCode() if subcode])

    def findItemIdxByCode(self, level_index, code):
        """
        Find item by code.

        :param level_index: Level index, matching list.
        :param code: Ref object cod.
        :return: Item index or -1 not found.
        """
        choice_ctrl = self._choice_ctrl_list[level_index]
        for item in range(choice_ctrl.GetCount()):
            find_code = choice_ctrl.GetClientData(item)
            if find_code == code:
                return item
        return -1

    def setCode(self, code=None):
        """
        Set ref object code as selected.

        :param code: Ref object cod.
        :return: True/False.
        """
        if code is None:
            # If cod not defined then clear
            return self.clearSelect()

        if self._ref_obj is not None:
            # self._selected_code sets in selectLevelChoice method
            # Do not need to initialize it
            selected_code = self._ref_obj.StrCode2ListCode(code)
            for i, subcode in enumerate(selected_code):
                item = self.findItemIdxByCode(i, subcode)
                if item >= 0:
                    self.selectLevelChoice(i, item, auto_select=False)
            return True
        return False

    getValue = getCode
    setValue = setCode

    def getChoiceSelectedCode(self, choice_ctrl, item=-1):
        """
        Get selected ref object cod from wx.Choice control.

        :param choice_ctrl: wx.Choice control.
        :param item: Item index.
            If -1 then get selected item.
        :return: Selected ref object cod as string.
        """
        if item < 0:
            item = choice_ctrl.GetSelection()
        try:
            return choice_ctrl.GetClientData(item)
        except:
            log_func.fatal(u'Error item data <%d>' % item)
        return None

    def clearLevelChoice(self, min_index=0, max_index=-1):
        """
        Clear level choices.

        :param min_index: First level index.
            If not defined then get 0 level.
        :param max_index: Last level index.
            If not defined then get last level..
        :return: True/False.
        """
        if max_index < 0:
            max_index = len(self._selected_code)-1

        for i in range(min_index, max_index+1):
            # Clear level codes
            self._selected_code[i] = None
            if self._choice_ctrl_list[i]:
                # Clear level choice controls
                self._choice_ctrl_list[i].Clear()
        return True

    def clearSelect(self):
        """
        Clear selection.
        """
        for choice_ctrl in self._choice_ctrl_list:
            choice_ctrl.SetSelection(wx.NOT_FOUND)
        return True

    def initLevelChoice(self, level_index, auto_select=True):
        """
        Init level choice controls.

        :param level_index: Level index, matching list.
        :param auto_select: Auto select first item.
        :return: True/False.
        """
        if self._ref_obj.isEmpty():
            log_func.warning(u'Empty ref object. It is not possible to initialize choice controls')
            return False

        if level_index < 0:
            level_index = 0
        elif level_index >= len(self._selected_code):
            level_index = len(self._selected_code)-1

        # Get level choice control
        choice_ctrl = self._choice_ctrl_list[level_index]
        if choice_ctrl:
            code_list = self._selected_code[:level_index]
            if not code_list:
                log_func.error(u'Subcodes not found <%s : %d>' % (str(self._selected_code), level_index))
                return False

            str_code = ''.join(code_list)

            level_choices = list()
            for rec in self._ref_obj.getLevelRecsByCod(str_code):
                if self._ref_obj and self._ref_obj.isActive(rec[self._ref_obj.getCodColumnName()]):
                    level_choice = (rec[self._ref_obj.getCodColumnName()][len(str_code):],
                                    rec[self._ref_obj.getNameColumnName()])
                    level_choices.append(level_choice)

            for code, name in level_choices:
                item = choice_ctrl.Append(name)
                choice_ctrl.SetClientData(item, code)
            if auto_select:
                self.selectLevelChoice(level_index, auto_select=auto_select)
        return True

    def selectLevelChoice(self, level_index, item=0, auto_select=True):
        """
        Select level cod.

        :param level_index: Level index.
        :param item: Item index.
        :param auto_select: Auto select first item.
        :return: True/False.
        """
        if level_index >= len(self._selected_code):
            return False
        choice_ctrl = self._choice_ctrl_list[level_index]
        choice_ctrl.SetSelection(item)
        # Set level item
        item_code = self.getChoiceSelectedCode(choice_ctrl, item)
        self._selected_code[level_index] = item_code

        # Select code handler
        self.onSelectCode()

        i = choice_ctrl.level_index + 1
        # Clear level choices
        self.clearLevelChoice(i)
        # After filling in the code, you need to define a list of the next level
        if i < len(self._selected_code):
            self.initLevelChoice(i, auto_select=auto_select)

    def getAutoSelect(self):
        """
        Get auto select?

        :return: True/False.
        """
        return True

    def onLevelCodeChange(self, event):
        """
        Level change cod handler.
        """
        choice_ctrl = event.GetEventObject()
        self.selectLevelChoice(choice_ctrl.level_index,
                               choice_ctrl.GetSelection(),
                               auto_select=self.getAutoSelect())
        event.Skip()

    def onSelectCode(self):
        """
        Select code handler.
        The method must be overridden in child classes.
        """
        pass
