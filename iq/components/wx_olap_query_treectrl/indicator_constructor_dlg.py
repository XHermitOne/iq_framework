#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filter indicator constructor form.
"""

import os.path
import keyword
import wx
import wx.stc

from . import indicator_constructor_dlg_proto

import iq
from ...util import log_func
from ...util import lang_func
from ...util import icon_func
from ...engine.wx import wxbitmap_func

from ...engine.wx import form_manager
from ...engine.wx import listctrl_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

STATE_LABEL = _('State')
UNKNOWN_STATE_NAME_FMT = STATE_LABEL + u' %d'


class iqIndicatorConstructorDlg(indicator_constructor_dlg_proto.iqIndicatorConstructorDlgProto,
                                form_manager.iqFormManager,
                                listctrl_manager.iqListCtrlManager):
    """
    Filter indicator constructor form.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        indicator_constructor_dlg_proto.iqIndicatorConstructorDlgProto.__init__(self, *args, **kwargs)

        # Editable indicator
        self._indicator = list()

    def setIndicator(self, indicator=None, refresh_ctrl=False):
        """
        Set indicator for editing.

        :param indicator: List of editable filter indicator.
        :param refresh_ctrl: Update the constructor controls?
        """
        if indicator is None:
            self._indicator = list()
        else:
            self._indicator = indicator

        if refresh_ctrl:
            self.setIndicatorListCtrl()

    def getIndicator(self):
        """
        Editable indicator.
        """
        return self._indicator

    def setIndicatorListCtrl(self, indicator=None):
        """
        Set the list of indicator states.

        :param indicator: List of editable filter indicator.
        :return: True/False
        """
        if indicator is None:
            indicator = self._indicator

        self.indicator_listCtrl.DeleteAllItems()
        for state_idx, state_indicator in enumerate(indicator):
            self.appendListCtrlRow(listctrl=self.indicator_listCtrl, row=('', ''))
            self.refreshStateRow(state_idx, state_indicator)
        return True

    def init(self):
        """
        Initialization.
        """
        self.initImages()
        self.initControls()
        
    def initImages(self):
        """
        Initializing images.
        """
        pass
        
    def initControls(self):
        """
        Initialization of controls.
        """
        self.initToolbar()
        self.initIndicatorGrid()
        self.initExpressionEdit()

        self.image_filePicker.SetInitialDirectory(icon_func.getIconPath())
        self.image_filePicker.Enable(False)
        self.textcolor_colourPicker.Enable(False)
        self.bgcolor_colourPicker.Enable(False)

    def initIndicatorGrid(self):
        """
        Initialization of the grid indicator.
        """
        self.setListCtrlColumns(listctrl=self.indicator_listCtrl,
                                cols=(dict(label=_(u'Name'), width=200),
                                      dict(label=_(u'Expression'), width=450)))

    def initToolbar(self):
        """
        Toolbar initialization.
        """
        self.ctrl_toolBar.EnableTool(self.moveup_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.movedown_tool.GetId(), False)
        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), False)

    def initExpressionEdit(self):
        """
        Expression editor initialization.
        """
        # Configuring the code browser
        self.expression_edit.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.expression_edit.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.expression_edit.SetProperty('fold', '1')
        self.expression_edit.SetProperty('tab.timmy.whinge.level', '1')
        self.expression_edit.SetMargins(0, 0)

        # Hide empty spaces as dots
        self.expression_edit.SetViewWhiteSpace(False)

        # Indentation and tab stuff
        self.expression_edit.SetIndent(4)                 # Proscribed indent size for wx
        self.expression_edit.SetIndentationGuides(True)   # Show indent guides
        self.expression_edit.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.expression_edit.SetTabIndents(True)          # Tab key indents
        self.expression_edit.SetTabWidth(4)               # Proscribed tab size for wx
        self.expression_edit.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Setting the box to capture folder markers
        self.expression_edit.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.expression_edit.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.expression_edit.SetMarginSensitive(1, True)
        self.expression_edit.SetMarginSensitive(2, True)
        self.expression_edit.SetMarginWidth(1, 25)
        self.expression_edit.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,    'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.expression_edit.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Debug mode markers
        # self.expression_edit.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        # self.expression_edit.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')

    def setDefaultStateCtrlValue(self):
        """
        Set default values for the controls of the indicator state editor.
        """
        self.setStateCtrlValue()

    def getStateCtrlValue(self):
        """
        Get edited state from controls.

        :return: Dictionary of the edited indicator state.
        """
        name = self.name_textCtrl.GetValue()
        if not name.strip():
            name = UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1)

        img_filename = self.image_filePicker.GetPath() if self.image_checkBox.GetValue() else None
        if img_filename:
            img_filename = os.path.basename(img_filename) if img_filename.startswith(icon_func.getIconPath()) else img_filename

        text_color = self.textcolor_colourPicker.GetColour() if self.textcolor_checkBox.GetValue() else None

        bg_color = self.bgcolor_colourPicker.GetColour() if self.bgcolor_checkBox.GetValue() else None

        expression = self.expression_edit.GetValue()
        if not expression.strip():
            expression = None

        return dict(name=name, image=img_filename,
                    text_color=text_color, background_color=bg_color,
                    expression=expression)

    def setStateCtrlValue(self, state_indicator=None):
        """
        Set values to indicator state controls.

        :param state_indicator: Indicator state dictionary:
            {
                'name': State name,
                'image': Image filename,
                'text_color': Text color as (R, G, B),
                'background_color': Background color as (R, G, B),
                'expression': Status check expression code block text,
            }
        :return: True/False.
        """
        if state_indicator is None:
            state_indicator = dict()

        name = state_indicator.get('name',
                                   UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1))
        img_filename = state_indicator.get('image', None)
        text_color = state_indicator.get('text_color', None)
        bg_color = state_indicator.get('background_color', None)
        expression = state_indicator.get('expression', None)

        self.name_textCtrl.SetValue(name)
        self.image_checkBox.SetValue(img_filename is not None)
        if img_filename:
            self.image_filePicker.SetPath(img_filename)
        else:
            bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU, (16, 16))
            self.image_bitmap.SetBitmap(bmp)
        self.textcolor_checkBox.SetValue(text_color is not None)
        if text_color:
            self.textcolor_colourPicker.SetColour(text_color)
        self.bgcolor_checkBox.SetValue(bg_color is not None)
        if bg_color:
            self.bgcolor_colourPicker.SetColour(bg_color)
        if expression is None:
            self.expression_edit.ClearAll()
        else:
            self.expression_edit.SetValue(expression)

        return True

    def refreshStateRow(self, state_idx, state_indicator):
        """
        Update the line of the indicator list with the corresponding state.

        :param state_idx: Status list index .
        :param state_indicator: Indicator state dictionary:
            {
                'name': State name,
                'image': Image filename,
                'text_color': Text color as (R, G, B),
                'background_color': Background color as (R, G, B),
                'expression': Status check expression code block text,
            }
        :return: True/False
        """
        if state_idx < 0:
            log_func.warning(u'Incorrect state index')
            return False

        if state_indicator is None:
            state_indicator = dict(name=UNKNOWN_STATE_NAME_FMT % (self.indicator_listCtrl.GetItemCount() + 1),
                                   image=None, text_color=None, background_color=None,
                                   expression=None)

        self._indicator[state_idx] = state_indicator

        name = state_indicator.get('name', u'')
        image = None
        img_filename = state_indicator.get('image', None)
        if img_filename:
            if os.path.exists(img_filename):
                # Absolute path to file
                image = wxbitmap_func.createBitmap(img_filename)
            else:
                # In all other cases, consider that this is a library file
                image = wxbitmap_func.createIconBitmap(img_filename)
        line = u''
        expression = state_indicator.get('expression', None)
        if expression:
            lines = expression.splitlines()
            line = lines[0] + u' ...'

        text_color = state_indicator.get('text_color', None)
        bg_color = state_indicator.get('background_color', None)

        self.setListCtrlRow(listctrl=self.indicator_listCtrl, item=state_idx,
                            row=(name, line))
        if image:
            # self.indicator_listCtrl.SetItemImage(state_idx, image)
            self.setListCtrlItemImage(listctrl=self.indicator_listCtrl, item=state_idx, image=image)

        if text_color:
            log_func.debug(u'Text color %s' % str(text_color))
            self.indicator_listCtrl.SetItemTextColour(state_idx, text_color)
        else:
            self.indicator_listCtrl.SetItemTextColour(state_idx, wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        if bg_color:
            log_func.debug(u'Background color %s' % str(bg_color))
            self.indicator_listCtrl.SetItemBackgroundColour(state_idx, bg_color)
        else:
            self.indicator_listCtrl.SetItemBackgroundColour(state_idx, wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        return True

    def onMoveUpToolClicked(self, event):
        """
        Moving the state up the list.
        """
        event.Skip()

    def onMoveDownToolClicked(self, event):
        """
        Move the state down the list.
        """
        event.Skip()

    def onAddToolClicked(self, event):
        """
        Handler for the button for adding an indicator state.
        """
        try:
            self.setDefaultStateCtrlValue()
            state_indicator = self.getStateCtrlValue()
            new_name = state_indicator['name']
            # new_image = state_indicator.get('image', None)
            # new_exp = state_indicator.get('expression', None)

            # Add indicator state to the list
            self._indicator.append(state_indicator)

            # Add a line to the list
            self.appendListCtrlRow(listctrl=self.indicator_listCtrl, row=(new_name, None, None),
                                   auto_select=True)
            #
            self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), True)
        except:
            log_func.fatal(u'Error adding indicator state')
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Handler for the button for deleting the indicator state.
        """
        event.Skip()

    def onSaveToolClicked(self, event):
        """
        Handler for the button for saving the indicator state.
        """
        try:
            state_indicator = self.getStateCtrlValue()
            idx = self.getListCtrlSelectedRowIdx(self.indicator_listCtrl)
            self.refreshStateRow(idx, state_indicator)
        except:
            log_func.fatal(u'Error saving indicator state')
        event.Skip()

    def onImageCheckBox(self, event):
        """
        Handler for on/off the indicator status picture.
        """
        checkbox_state = event.IsChecked()
        self.image_filePicker.Enable(checkbox_state)
        # if not checkbox_state:
        #     self.image_filePicker.SetPath(u'')
        event.Skip()

    def onTextColorCheckBox(self, event):
        """
        Handler for on/off the color of the indicator status text.
        """
        checkbox_state = event.IsChecked()
        self.textcolor_colourPicker.Enable(checkbox_state)
        event.Skip()

    def onBGColorCheckBox(self, event):
        """
        Handler for on/off the background color of the indicator state.
        """
        checkbox_state = event.IsChecked()
        self.bgcolor_colourPicker.Enable(checkbox_state)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        CANCEL button handler.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        OK button handler.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onImageFileChanged(self, event):
        """
        Image file change handler.
        """
        img_filename = event.GetPath()
        if img_filename and os.path.exists(img_filename):
            bmp = wxbitmap_func.createBitmap(img_filename)
            self.image_bitmap.SetBitmap(bmp)
        event.Skip()

    def onIndicatorListItemSelected(self, event):
        """
        Handler for selecting an indicator state from the list.
        """
        idx = event.GetIndex()
        state_indicator = self._indicator[idx]
        log_func.debug(u'Edit indicator %s' % str(state_indicator))
        self.setStateCtrlValue(state_indicator=state_indicator)

        self.ctrl_toolBar.EnableTool(self.save_tool.GetId(), True)

        event.Skip()


def showIndicatorConstructorDlg(parent=None):
    """
    Open indicator constructor dialog
    :param parent: Parent window.
    :return: True/False.
    """
    try:
        if parent is None:
            parent = iq.getMainWin()

        dlg = iqIndicatorConstructorDlg(parent)
        dlg.init()
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            return True
    except:
        log_func.fatal(u'Error open indicator constructor dialog')
    return False


def editIndicatorConstructorDlg(parent=None, indicator=None):
    """
    Start editing the filter indicator.

    :param parent: Parent window.
    :param indicator: Indicator description list.
    :return: Edited indicator list or None if CANCEL is pressed.
    """
    try:
        if parent is None:
            parent = iq.getMainWin()

        dlg = iqIndicatorConstructorDlg(parent)
        dlg.init()
        dlg.setIndicator(indicator=indicator, refresh_ctrl=True)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            indicator = dlg.getIndicator()
            dlg.Destroy()
            log_func.debug(u'List of edited filter indicator %s' % str(indicator))
            return indicator
    except:
        log_func.fatal(u'Filter indicator editing error')
    return None
