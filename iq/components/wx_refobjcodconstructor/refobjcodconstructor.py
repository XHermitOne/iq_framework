#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference object cod constructor control.
"""

import wx

from ...util import log_func
from ...util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_COD_SIGN = '0'


class iqRefObjCodConstructorProto(wx.StaticBox):
    """
    Reference object cod constructor control.
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

        self.sizer = wx.FlexGridSizer(0, 4, 0, 0)
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
        # Level clear buttons
        self._clear_buttons = list()
        # Level cod text ctrl
        self._cod_textctrls = list()

    def getSelectedCode(self):
        """
        Get selected ref object cod as tuple.
        """
        return tuple(self._selected_code)

    def refreshTitle(self):
        """
        Refresh title cod constructor.

        :return:
        """
        label = self.getLabel()
        if not label:
            # If title not defined then get from ref object
            label = self._ref_obj.getDescription()
        current_cod = u''.join([sub_cod if sub_cod else '' for sub_cod in self._selected_code])
        title = u'%s (%s): %s' % (_('Cod'), label, current_cod)
        self.SetLabel(title)

    def setRefObj(self, ref_obj):
        """
        Set ref object.

        :param ref_obj: Reference object.
        """
        self._ref_obj = ref_obj

        if self._ref_obj:
            # Level choice controls
            self._selected_code = [None] * self._ref_obj.getLevelCount()

            self._choice_ctrl_list = list()
            self._clear_buttons = list()
            self._cod_textctrls = list()

            for i, level_label in enumerate(self._ref_obj.getLevelLabels()):
                # Label
                label = wx.StaticText(self.scrolled_win, wx.ID_ANY, level_label,
                                      wx.DefaultPosition, wx.DefaultSize, 0)

                level_choices = list()
                if not i:
                    for rec in self._ref_obj.getLevelRecsByCod():
                        if self._ref_obj.isActive(rec[self._ref_obj.getCodColumnName()]):
                            level_choice = (rec[self._ref_obj.getCodColumnName()],
                                            rec[self._ref_obj.getNameColumnName()])
                            level_choices.append(level_choice)

                # Level code choice
                choice_id = wx.NewId()
                choice = wx.Choice(self.scrolled_win, choice_id,
                                   wx.DefaultPosition, wx.DefaultSize)
                item = choice.Append(u'')
                choice.SetClientData(item, None)
                for code, name in level_choices:
                    item = choice.Append(name)
                    choice.SetClientData(item, code)

                # Save level index
                choice.level_index = i
                choice.Bind(wx.EVT_CHOICE, self.onLevelCodeChange, id=choice_id)
                # Reg choice control
                self._choice_ctrl_list.append(choice)

                # Clear button
                button_id = wx.NewId()
                clear_button = wx.BitmapButton(self.scrolled_win, button_id,
                                               bitmap=wx.ArtProvider.GetBitmap('gtk-clear', wx.ART_MENU))
                clear_button.level_index = i
                clear_button.Bind(wx.EVT_BUTTON, self.onClearButtonClick, id=button_id)
                self._clear_buttons.append(clear_button)

                # Cod text control
                txtctrl_id = wx.NewId()
                txtctrl = wx.TextCtrl(self.scrolled_win, txtctrl_id,
                                      size=wx.Size(150, -1), style=wx.TE_PROCESS_ENTER)
                txtctrl.SetMaxLength(self._ref_obj.getLevelCodLen(i))
                txtctrl.level_index = i
                txtctrl.Bind(wx.EVT_TEXT, self.onSubCodText, id=txtctrl_id)
                txtctrl.Bind(wx.EVT_TEXT_ENTER, self.onSubCodTextEnter, id=txtctrl_id)
                self._cod_textctrls.append(txtctrl)

                self.sizer.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
                self.sizer.Add(choice, 1, wx.ALL | wx.EXPAND, 5)
                self.sizer.Add(clear_button, 2, wx.ALL | wx.EXPAND, 5)
                self.sizer.Add(txtctrl, 3, wx.ALL | wx.EXPAND, 5)

            self.initCodTextCtrl()
            # Title
            self.refreshTitle()

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
            result = self.clearSelect()
            self.initCodTextCtrl()
            # Title
            self.refreshTitle()
            return result

        if self._ref_obj is not None:
            # self._selected_code sets in selectLevelChoice method
            # Do not need to initialize it
            selected_code = self._ref_obj.getCodAsTuple(code)
            for i, subcode in enumerate(selected_code):
                item = self.findItemIdxByCode(i, subcode)
                if item >= 0:
                    self.selectLevelChoice(i, item, auto_select=True)
            self.initCodTextCtrl()
            # Title
            self.refreshTitle()
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
            # log_func.debug(u'Choice item [%d] client data' % item)
            return choice_ctrl.GetClientData(item) if item > 0 else None
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
            max_index = len(self._selected_code) - 1

        for i in range(min_index, max_index + 1):
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

    def initLevelChoice(self, level_index, auto_select=False):
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
            level_index = len(self._selected_code) - 1

        # Get level choice control
        choice_ctrl = self._choice_ctrl_list[level_index]
        if choice_ctrl:
            code_list = self._selected_code[:level_index]
            if not code_list:
                log_func.warning(u'Subcodes not found <%s : %d>' % (str(self._selected_code), level_index))
                return False

            if None not in code_list:
                # log_func.debug(u'Code list %s' % str(code_list))
                str_code = ''.join(code_list)

                level_choices = list()
                for rec in self._ref_obj.getLevelRecsByCod(str_code):
                    if self._ref_obj and self._ref_obj.isActive(rec[self._ref_obj.getCodColumnName()]):
                        level_choice = (rec[self._ref_obj.getCodColumnName()][len(str_code):],
                                        rec[self._ref_obj.getNameColumnName()])
                        level_choices.append(level_choice)

                item = choice_ctrl.Append(u'')
                choice_ctrl.SetClientData(item, None)
                for code, name in level_choices:
                    item = choice_ctrl.Append(name)
                    choice_ctrl.SetClientData(item, code)
                if auto_select:
                    self.selectLevelChoice(level_index, auto_select=auto_select)
            # else:
            #     i = code_list.index(None)
            #     self.clearLevelChoice(i)
        return True

    def selectLevelChoice(self, level_index, item=0, auto_select=False):
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
        if item:
            item_code = self.getChoiceSelectedCode(choice_ctrl, item)
            # log_func.debug(u'Level [%d]. Item code <%s>' % (level_index, item_code))
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
        try:
            selection = choice_ctrl.GetSelection()
            self.selectLevelChoice(choice_ctrl.level_index,
                                   selection,
                                   auto_select=self.getAutoSelect())
            # Enable text controls
            self.initCodTextCtrl()
            # Title
            self.refreshTitle()
        except:
            log_func.fatal(u'Error select level')
        event.Skip()

    def initCodTextCtrl(self):
        """
        Init text controls.

        :return: True/False.
        """
        try:
            is_last = False
            for i in range(self._ref_obj.getLevelCount()):
                choice_ctrl = self._choice_ctrl_list[i]
                txt_ctrl = self._cod_textctrls[i]
                is_select = bool(choice_ctrl.GetSelection())
                if is_select:
                    selected_cod = self.getChoiceSelectedCode(choice_ctrl=choice_ctrl)
                    txt_ctrl.SetValue(selected_cod if selected_cod else u'')
                    self._selected_code[i] = selected_cod
                else:
                    # level_cod_len = self._ref_obj.getLevelCodLen(i)
                    # cod = (DEFAULT_COD_SIGN * level_cod_len) if level_cod_len > 0 else ''
                    cod = self.genAutoLevelCode(level=i, selected_code=self._selected_code)
                    log_func.debug(u'New level code <%s>' % cod)
                    txt_ctrl.SetValue(cod)
                    self._selected_code[i] = cod
                txt_ctrl.Enable(not is_last and not is_select)
                if is_last:
                    txt_ctrl.ChangeValue('')
                    self._selected_code[i] = None
                is_last = not is_select
        except:
            log_func.fatal(u'Error init cod text controls')

    def genAutoLevelCode(self, level=0, selected_code=(), start_i=1):
        """
        Generate automatic level code.

        :param level: Level index.
        :param selected_code: Selected code list.
        :param start_i: Start number for code generate.
        :return: Level code as text.
        """
        try:
            level_cod_len = self._ref_obj.getLevelCodLen(level)
            # cod = (DEFAULT_COD_SIGN * level_cod_len) if level_cod_len > 0 else ''
            str_start_i = str(start_i)
            cod = DEFAULT_COD_SIGN * (level_cod_len - len(str_start_i)) + str_start_i
            cod = cod[-level_cod_len:]
            new_cod = ''.join([subcode for subcode in selected_code[:level] if subcode])
            new_cod = new_cod + cod
            if self._ref_obj.hasCod(new_cod):
                return self.genAutoLevelCode(level=level, selected_code=selected_code, start_i=start_i+1)
            return cod
        except:
            log_func.fatal(u'Error generate automatic level code')
        return u''

    def onSelectCode(self):
        """
        Select code handler.
        The method must be overridden in child classes.
        """
        pass

    def onClearButtonClick(self, event):
        """
        Clear button click handler.
        """
        clear_button = event.GetEventObject()
        choice_ctrl = self._choice_ctrl_list[clear_button.level_index]
        choice_ctrl.SetSelection(0)

        self.initCodTextCtrl()
        self.refreshTitle()

        event.Skip()

    def onSubCodTextEnter(self, event):
        """
        Sub cod text change after press enter handler.
        """
        txt_ctrl = event.GetEventObject()
        level_idx = txt_ctrl.level_index
        try:
            level_cod_len = self._ref_obj.getLevelCodLen(level=level_idx)
            cur_text = txt_ctrl.GetValue().strip()
            new_sub_cod = DEFAULT_COD_SIGN * (level_cod_len - len(cur_text)) + cur_text[:level_cod_len]
            self._selected_code[level_idx] = new_sub_cod
            log_func.debug(u'New sub cod <%s : %s>' % (cur_text, new_sub_cod))
            if cur_text and len(cur_text) < level_cod_len:
                txt_ctrl.ChangeValue(new_sub_cod)
            self.refreshTitle()

            if txt_ctrl.IsEnabled():
                new_cod = self.getCode()
                if self._ref_obj.hasCod(new_cod):
                    txt_ctrl.SetBackgroundColour(wx.RED)
                else:
                    txt_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            else:
                txt_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        except:
            log_func.fatal(u'Error sub cod text change after press enter handler')
        event.Skip()

    def onSubCodText(self, event):
        """
        Sub cod text change handler.
        """
        txt_ctrl = event.GetEventObject()
        level_idx = txt_ctrl.level_index
        try:
            level_cod_len = self._ref_obj.getLevelCodLen(level=level_idx)
            cur_text = txt_ctrl.GetValue().strip()
            new_sub_cod = DEFAULT_COD_SIGN * (level_cod_len - len(cur_text)) + cur_text[:level_cod_len]
            if cur_text == new_sub_cod:
                self._selected_code[level_idx] = new_sub_cod
                log_func.debug(u'New sub cod <%s : %s>' % (cur_text, new_sub_cod))
                self.refreshTitle()

            if txt_ctrl.IsEnabled():
                new_cod = self.getCode()
                if self._ref_obj.hasCod(new_cod):
                    txt_ctrl.SetBackgroundColour(wx.RED)
                else:
                    txt_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            else:
                txt_ctrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        except:
            log_func.fatal(u'Error sub cod text change handler')
        event.Skip()
