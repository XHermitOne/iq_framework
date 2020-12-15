#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controls used in filter constructor.
"""

import wx
import wx.adv
import wx.lib.platebtn

from ...engine.wx.dlg import wxdlg_func
from ...engine.wx import wxbitmap_func
from . import label_event
from ...util import log_func
from ...util import lang_func


__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

DEFAULT_COMBO_SIZE = (200, -1)
DEFAULT_EDIT_SIZE = (100, -1)

DEFAULT_IMG_WIDTH = 16
DEFAULT_IMG_HEIGHT = 16


class iqCustomComboCtrl(wx.ComboCtrl):
    """
    Call control advanced editor base class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.ComboCtrl.__init__(self, *args, **kwargs)
        # Draw button <...>
        self._drawCustomButton()
        
    def _drawCustomButton(self):
        """
        Create a call button for advanced selections.
        """
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.Bitmap(bw, bh)
        dc = wx.MemoryDC(bmp)

        # clear to a specific background colour
        bgcolor = wx.Colour(255, 254, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()

        # draw the label onto the bitmap
        label = '...'
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw-tw)/2, (bw-tw)/2)
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass
    
    def OnButtonClick(self):
        """
        The handler for clicking on the button for advanced selection from the list.
        """
        pass

    def getValue(self, *args, **kwargs):
        return self.GetValue(*args, **kwargs)


class iqCustomChoice(iqCustomComboCtrl):
    """
    The control class is an extended selection from the specified list.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        iqCustomComboCtrl.__init__(self, *args, **kwargs)
        
        # Choices
        self.choice = list()
        
        # Filter environment
        self.filter_env = None
        
        # Selected item index
        self.choice_idx = -1
        
        # Selected data
        self.data = None

    def setData(self, data=None):
        """
        Set data.
        """
        if data is None:
            self.data = list()
        else:
            self.data = data
            choice = [element['description'] for element in self.data]
            self.setChoice(choice)
        return self.data
        
    def setChoice(self, choice=None):
        """
        Set choices.
        """
        if choice is None:
            self.choice = list()
        else:
            self.choice = choice
        
    def OnButtonClick(self):
        """
        The handler for clicking on the button for advanced selection from the list.
        """
        if self.choice:
            idx = wxdlg_func.getSingleChoiceIdxDlg(self, _(u'CHOICE'),
                                                   _(u'Select one of the following items'), self.choice)
            self.choice_idx = idx
            if idx >= 0:
                self.SetValue(self.choice[idx])


class iqArgExtendedEdit(iqCustomComboCtrl):
    """
    The control class of the extended editor of the function argument value.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        iqCustomComboCtrl.__init__(self, *args, **kwargs)

        # Default value
        self.default = None
        # Additional data
        self.data = None

        # Advanced editor call function
        self.ext_edit_func = None

    def OnButtonClick(self):
        """
        The handler for clicking on the button for advanced selection from the list.
        """
        if self.ext_edit_func:
            result = self.ext_edit_func(self, self.data, self.default)
            if result is not None:
                self.SetValue(str(result))


class iqPlateButton(wx.lib.platebtn.PlateButton):
    """
    Native button.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.lib.platebtn.PlateButton.__init__(self, *args, **kwargs)


class iqBitmapButton(wx.BitmapButton):
    """
    Native button with bitmap.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.BitmapButton.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx.WHITE)


class iqBitmapComboBox(wx.adv.BitmapComboBox):
    """
    Combobox with bitmaps.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.adv.BitmapComboBox.__init__(self, *args, **kwargs)
        
        self._cur_selected_item = -1
        
        self.items = None

        self.Bind(wx.EVT_COMBOBOX, self.onCombo, self)
     
    def Select(self, item):
        """
        Select item by index.
        """
        self._cur_selected_item = item
        return wx.adv.BitmapComboBox.Select(self, item)
    
    def onCombo(self, event):
        """
        Combobox item select handler.
        """
        self._cur_selected_item = event.GetSelection()
        event.Skip()
        
    def getCurrentSelection(self):
        """
        Get current selected item.
        """
        return self._cur_selected_item
        
    def appendItems(self, items):
        """
        Add combobox choice items.

        :param items: Item list:
        [{
            'name': 'Item name',
            'description': 'Item description',
            'img': Item image (as expression string),
            'data': Item data
        },...]
        """
        if self.items is None:
            self.items = []
            
        self.items += list(items)
        
        for item in list(items):
            name = item['name']
            description = item['description']
            img = None
            if 'img' in item:
                img = item['img']
                if img and isinstance(img, str):
                    img = wxbitmap_func.createIconBitmap(img)
            if img is None:
                img = wx.Bitmap(DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT)
            
            self.Append(description, img, name)
  
    def getSelectedData(self):
        """
        Get selected item data.
        """
        selected = self.getCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None
        
    def setItems(self, items):
        """
        Set item list.

        :param items: Item list:
        [{
            'name': 'Item name',
            'description': 'Item description',
            'img': Item image (as expression string),
            'data': Item data
        },...]
        """
        self.Clear()
        self.items = None
        self.appendItems(items)
   
    def selectByName(self, name):
        """
        Select combobox item by name.

        :return: Selected item index.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(name)
        except:
            log_func.warning(u'Item <%s> not found in <%s>' % (name, item_names))
            i = -1
        self.Select(i)
        return i


class iqItemComboBox(wx.ComboBox):
    """
    Combobox class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.ComboBox.__init__(self, *args, **kwargs)
        
        self.items = None

    def appendItems(self, items):
        """
        Append combobox items.

        :param items:
        [{
            'name':'Item name',
            'description':'Item description',
            'data': Item data
        },...]        
        """
        if self.items is None:
            self.items = []
            
        self.items += list(items)
        
        for item in list(items):
            name = item['name']
            description = item['description']
            data = None
            if 'data' in item:
                data = item['data']
            
            self.Append(description, data)
        
    def getSelectedData(self):
        """
        Get selected item data.
        """
        selected = self.GetCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None
    
    def setItems(self, items):
        """
        Set combobox items.

        :param items:
        [{
            'name':'Item name',
            'description':'Item description',
            'data': Item data,
        },...]        
        """
        self.Clear()
        self.items = None
        self.appendItems(items)
        
    def selectByName(self, name):
        """
        Select item by name.

        :return: Selected item index.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(name)
        except:
            log_func.warning(u'Item <%s> not found in <%s>' % (name, item_names))
            i = -1
        self.Select(i)
        return i


class iqLogicOperationsComboBox(iqBitmapComboBox):
    """
    Logic operation combobox class.
    """
    def __init__(self, parent, items=None):
        """
        Constructor.
        """
        if items is None:
            from . import filter_builder_env
            items = filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        iqBitmapComboBox.__init__(self, parent, id=wx.NewId(),
                                  size=DEFAULT_COMBO_SIZE, style=style)
        self.appendItems(items)


class iqRequisiteComboBox(iqItemComboBox):
    """
    Object requisite combobox class.
    """
    def __init__(self, parent, requisites=None):
        """
        Constructor.
        """
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        iqItemComboBox.__init__(self, parent, id=wx.NewId(),
                                size=DEFAULT_COMBO_SIZE, style=style)
        if requisites:
            self.appendItems(requisites)
            
    def getSelectedRequisite(self):
        """
        Get selected requisite item data.
        """
        selection = self.GetCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        


class iqFuncComboBox(iqBitmapComboBox):
    """
    Select requisite comparison function combobox class.
    """
    def __init__(self, parent, compare_funcs=None):
        """
        Constructor.
        """
        style = wx.CB_READONLY | wx.CB_DROPDOWN
        iqBitmapComboBox.__init__(self, parent, id=wx.NewId(),
                                  size=DEFAULT_COMBO_SIZE, style=style)
        if compare_funcs:
            self.appendItems(compare_funcs)
            
    def getSelectedFunc(self):
        """
        Get selected function data.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        
        
    
class iqArgEdit(wx.TextCtrl):
    """
    The editor of the argument. Base class.
    """
    def __init__(self, parent, arg=None):
        """
        Constructor.

        :param parent: Parent window.
        :param arg: Argument data.
        """
        wx.TextCtrl.__init__(self, parent, id=wx.NewId(),
                             size=DEFAULT_EDIT_SIZE)
        
        tool_tip = None
        if 'description' in arg:
            tool_tip = arg['description']
        if tool_tip:
            self.SetToolTip(str(tool_tip))
            
        default = None
        if 'default' in arg:
            default = arg['default']
        if default:
            self.SetValue(str(default))
            
    def getValue(self, *args, **kwargs):
        return self.GetValue(*args, **kwargs)

    def setValue(self, *args, **kwargs):
        return self.SetValue(*args, **kwargs)


class iqNumArgEdit(iqArgEdit):
    """
    Numeric argument editor.
    """
    def __init__(self, parent, arg=None):
        """
        Constructor.

        :param parent: Parent window.
        :param arg: Argument data.
        """
        iqArgEdit.__init__(self, parent, arg)


class iqStrArgEdit(iqArgEdit):
    """
    String argument editor.
    """
    def __init__(self, parent, arg=None):
        """
        Constructor.

        :param parent: Parent window.
        :param arg: Argument data.
        """
        iqArgEdit.__init__(self, parent, arg)


class iqCustomArgEdit(iqCustomComboCtrl):
    """
    Argument editor with advanced editor.
    """
    def __init__(self, parent, arg=None):
        """
        Constructor.

        :param parent: Parent window.
        :param arg: Argument data.
        """
        iqCustomComboCtrl.__init__(self, parent, -1, size=wx.Size(-1, 20))


class iqLabelChoice(wx.StaticText):
    """
    Static text selection control. Base class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.StaticText.__init__(self, *args, **kwargs)
        
        # Current selected item
        self._cur_selected_item = -1
        
        # Item label format
        self._format = '%s'
        
        # Not selected label
        self._none_label_txt = '<...>'
        
        # Items
        self.items = None
        
        # Auxiliary dictionary for matching menu mitem
        # identifiers with selection items
        self._menuitem_item_dict = None
        
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseClick)
                
    def eventLabelChange(self):
        """
        Event <label_event.EVT_LABEL_CHANGE>.
        """
        event = label_event.iqLabelChangeEvent(label_event.EVT_LABEL_CHANGE_TYPE, self.GetId())
        event.setObject(self)
        return self.GetEventHandler().AddPendingEvent(event)
    
    def setItems(self, items):
        """
        Set items.
        """
        self.items = items
        
    def Select(self, item):
        """
        Select item.
        """
        if isinstance(item, int):
            self._cur_selected_item = item
            label_txt = self._format % self.items[self._cur_selected_item]['description']
        elif isinstance(item, dict):
            try:
                self._cur_selected_item = self.items.index(item)
                label_txt = self._format % self.items[self._cur_selected_item]['description']
            except ValueError:
                self._cur_selected_item = -1
                label_txt = self._none_label_txt
        else:
            self._cur_selected_item = -1
            label_txt = self._none_label_txt
        self.SetLabel(label_txt)
   
    def _createSelectMenu(self, items):
        """
        Create select menu.
        """
        self._menuitem_item_dict = {}
        
        menu = wx.Menu()
        if items:
            for item in items:
                text = item['description'] if item['description'] else item['name']
                img = None
                if 'img' in item:
                    img = item['img']
            
                menuitem_id = wx.NewId()
                menu_item = wx.MenuItem(menu, menuitem_id, text)
                if img:
                    menu_item.SetBitmap(img)
                menu.Append(menu_item)
                self.Bind(wx.EVT_MENU, self.onSelectMenuItem, id=menuitem_id)
            
                self._menuitem_item_dict[menuitem_id] = item
        else:
            log_func.warning(u'Filter constructor. Items not defined')

        return menu
        
    def onMouseClick(self, event):
        """
        Mouse click handler.
        """
        old_selected = self.getCurrentSelection()
        
        menu = self._createSelectMenu(self.items)
        self.PopupMenu(menu)
        menu.Destroy()
        
        new_selected = self.getCurrentSelection()
        
        if old_selected != new_selected:
            self.eventLabelChange()
            
        event.Skip()
        
    def onSelectMenuItem(self, event):
        """
        Select menu item handler.
        """
        menu_item_id = event.GetId()
        selected_item = self._menuitem_item_dict[menu_item_id]
        self.Select(selected_item)
        
        self._menuitem_item_dict = None
        event.Skip()
        
    def getCurrentSelection(self):
        """
        Get current selected item.
        """
        return self._cur_selected_item
        
    def getSelectedData(self):
        """
        Get selected item data.
        """
        selected = self.getCurrentSelection()
        if selected >= 0:
            return self.items[selected]
        return None

    def selectByName(self, name):
        """
        Select item by name.

        :return: Selected item index.
        """
        item_names = [item['name'] for item in self.items]
        try:
            i = item_names.index(name)
        except:
            log_func.warning(u'Item <%s> not found in <%s>' % (name, item_names))
            i = -1
        self.Select(i)
        return i
    
    def getLabelStrip(self):
        """
        Get label.
        """
        return self.GetLabel().strip()


class iqLogicLabelChoice(iqLabelChoice):
    """
    Logic operation choice control.
    """
    def __init__(self, parent, items=None):
        """
        Constructor.
        """
        if items is None:
            from . import filter_builder_env
            items = filter_builder_env.DEFAULT_ENV_LOGIC_OPERATIONS
        iqLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self.SetForegroundColour(wx.Colour(128, 0, 0))
        if items:
            self.setItems(items)


class iqRequisiteLabelChoice(iqLabelChoice):
    """
    Requisite choice control.
    """
    def __init__(self, parent, requisites=None):
        """
        Constructor.
        """
        iqLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self._format = '[%s]'
        self.SetForegroundColour(wx.Colour(0, 0, 128))
        if requisites:
            self.setItems(requisites)
            
    def getSelectedRequisite(self):
        """
        Get selected requisite data.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        

    def getLabelStrip(self):
        """
        Get label.
        """
        return self.GetLabel()[1:-1].strip()


class iqFuncLabelChoice(iqLabelChoice):
    """
    Function choice control.
    """        
    def __init__(self, parent, compare_funcs=None):
        """
        Constructor.
        """
        iqLabelChoice.__init__(self, parent, wx.NewId(), '<...>')
        self.SetForegroundColour(wx.Colour(0, 128, 0))
        if compare_funcs:
            self.setItems(compare_funcs)
        
    def getSelectedFunc(self):
        """
        Get selected function data.
        """
        selection = self.getCurrentSelection()
        if selection >= 0:
            return self.items[selection]
        return None        


class iqDateArgExtEdit(wx.adv.DatePickerCtrl):
    """
    Select date argument editor control.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx.adv.DatePickerCtrl.__init__(self, *args, **kwargs)

        # Default value
        self.default = None
