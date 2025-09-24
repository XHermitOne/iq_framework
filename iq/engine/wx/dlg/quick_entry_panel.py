#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classes and functions of the quick input panel support.
The quick panel is used to enter the recordset information.
The quick input panel is bound and used with list controls such as
wx.ListCtrl, wx.DataListView, etc.
The quick input panel is designed as a wxFormBuilder project.
The quick_entry_panel and quick_entry_dlg functions are used to call the panel.
The input on the quick input panel is carried out using the keyboard
without using a computer mouse:
        F1 - Help window
        ESC - Canceling input
        NUM LOCK ENTER - Confirmation of input
        BACKSPACE - Returning default values
        TAB - Switching between input objects

        CTRL+UP(^) - Switching to the previous list item without saving data
        CTRL+DOWN(v) - Moving to the next item in the list without saving data

        INS - Adding a new element
        DEL - Deleting an existing element

Attention! As input confirmation, NUM LOCK ENTER is used
because the standard ENTER is used in control management.
"""

import wx

from . import quick_entry_panel_ctrl_proto

from iq.util import log_func
from iq.util import lang_func

from iq.engine.wx import form_manager
from iq.engine.wx import wxbitmap_func

__version__ = (0, 3, 1, 1)

_ = lang_func.getTranslation().gettext

GO_PREV_ITEM_CMD = -1
GO_NEXT_ITEM_CMD = 1
ENTRY_CANCEL_CMD = False
ENTRY_OK_CMD = True
ENTRY_ADD_CMD = '+'
ENTRY_DEL_CMD = '-'


class iqQuickEntryPanelCtrl(quick_entry_panel_ctrl_proto.iqQuickEntryPanelCtrlProto):
    """
    The control panel of the quick input panel.
    """
    def __init__(self, parent, quick_entry_panel_class, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window.
        :param quick_entry_panel_class: The class of the quick input panel.
        """
        quick_entry_panel_ctrl_proto.iqQuickEntryPanelCtrlProto.__init__(self, parent)

        if quick_entry_panel_class:
            # Create quick entry panel
            self.quick_entry_panel = quick_entry_panel_class(self, *args, **kwargs)

            panel_sizer = self.GetSizer()
            panel_sizer.Add(self.quick_entry_panel, 0, wx.EXPAND, 5)
            self.Layout()
        else:
            log_func.warning(u'The class of the quick input panel is not defined')

        # Sign of confirmation of the input
        self.entry_check = None

    def onCancelToolClicked(self, event):
        """
        Handler for the input cancellation tool.
        """
        log_func.debug(u'Cancel entry')
        self.entry_check = ENTRY_CANCEL_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkToolClicked(self, event):
        """
        Handler of the input confirmation tool.
        """
        log_func.debug(u'Confirm entry')
        self.entry_check = ENTRY_OK_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onAddToolClicked(self, event):
        """
        The handler of the add new element tool.
        """
        log_func.debug(u'Add item')
        self.entry_check = ENTRY_ADD_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onDelToolClicked(self, event):
        """
        Handler for the existing element deletion tool.
        """
        log_func.debug(u'Delete item')
        self.entry_check = ENTRY_DEL_CMD
        self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def onDefaultToolClicked(self, event):
        """
        The handler of the default setting tool in controls.
        Attention! In the handler, we do not call event.Skip() so that the window does not close
        by default.
        """
        log_func.debug(u'Set default')
        self.GetParent().setDefaults()

    def onHelpToolClicked(self, event):
        """
        The handler of the help tool about hotkeys.
        Attention! In the handler, we do not call event.Skip() so that the window does not close
        by default.
        """
        help_txt = u'''Hot keys:
        F1 - Help window
        ESC - Canceling input
        NUM LOCK ENTER - Confirmation of input
        BACKSPACE - Returning default values
        TAB - Switching between input objects

        CTRL+UP(^) - Switching to the previous list item without saving data
        CTRL+DOWN(v) - Moving to the next item in the list without saving data

        INS - Adding a new element
        DEL - Deleting an existing element
        '''
        log_func.debug(u'Help')
        parent = self   # .GetParent().GetParent()
        wx.MessageBox(help_txt, _(u'HELP'), style=wx.OK | wx.ICON_QUESTION, parent=parent)

    def onPrevToolClicked(self, event):
        """
        Switching to the previous element without saving data.
        """
        log_func.debug(u'Switching to the previous element without saving data')
        self.entry_check = GO_PREV_ITEM_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def onNextToolClicked(self, event):
        """
        Moving to the next element without saving data.
        """
        log_func.debug(u'Moving to the next element without saving data')
        self.entry_check = GO_NEXT_ITEM_CMD
        self.GetParent().EndModal(wx.ID_CANCEL)
        event.Skip()

    def enableTools(self, prev_tool=True, next_tool=True, add_tool=True, del_tool=True,
                    ok_tool=True, cancel_tool=True, default_tool=True, help_tool=True,
                    *args, **kwargs):
        """
        On./Off control tools.
        Together with the tools off/on keyboard shortcuts.

        :param prev_tool: On/off switch to the previous element.
        :param next_tool: On/off the tool for moving to the next element.
        :param add_tool: On/off the tool for adding a new element.
        :param del_tool: On/off tool for deleting an existing element.
        :param ok_tool: On/off the input confirmation tool.
        :param cancel_tool: On/off the input cancellation tool.
        :param default_tool: On/off the default value recovery tool.
        :param help_tool: On/off the help tool.
        :return: True/False. 
        """
        self.ctrl_toolBar.EnableTool(self.prev_tool.GetId(), prev_tool)
        self.ctrl_toolBar.EnableTool(self.next_tool.GetId(), next_tool)
        self.ctrl_toolBar.EnableTool(self.add_tool.GetId(), add_tool)
        self.ctrl_toolBar.EnableTool(self.del_tool.GetId(), del_tool)
        self.ctrl_toolBar.EnableTool(self.ok_tool.GetId(), ok_tool)
        self.ctrl_toolBar.EnableTool(self.cancel_tool.GetId(), cancel_tool)
        self.ctrl_toolBar.EnableTool(self.default_tool.GetId(), default_tool)
        self.ctrl_toolBar.EnableTool(self.help_tool.GetId(), help_tool)

        hot_key_connections = dict()
        if prev_tool:
            hot_key_connections['CTRL_UP'] = self.prev_tool.GetId()
        if next_tool:
            hot_key_connections['CTRL_DOWN'] = self.next_tool.GetId()
        if add_tool:
            hot_key_connections['INS'] = self.add_tool.GetId()
        if del_tool:
            hot_key_connections['DEL'] = self.del_tool.GetId()
        if ok_tool:
            hot_key_connections['ENTER'] = self.ok_tool.GetId()
        if cancel_tool:
            hot_key_connections['ESC'] = self.cancel_tool.GetId()
        if default_tool:
            hot_key_connections['BACKSPACE'] = self.default_tool.GetId()
        if help_tool:
            hot_key_connections['F1'] = self.help_tool.GetId()
        self.GetParent().setPanelWindowAcceleratorTable(win=self, **hot_key_connections)


class iqQuickEntryPanelDialog(wx.Dialog, form_manager.iqDialogManager):
    """
    The background of the quick input panel.
    It is made in the form of a dialog box, because the dialog box provides
    opening in modal mode.
    """
    def __init__(self, parent, title, pos, size, quick_entry_panel_class, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window.
        :param title: Title.
        :param pos: The display position of the quick input panel.
        :param size: The size of the display of the quick input panel.
        :param quick_entry_panel_class: The class of the quick input panel.
        """
        wx.Dialog.__init__(self, parent, title=title,
                           pos=pos if pos else wx.DefaultPosition,
                           size=size if size else wx.DefaultSize,
                           style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fugue/stickman-run-dash')))

        self.ctrl_panel = iqQuickEntryPanelCtrl(self, quick_entry_panel_class, *args, **kwargs)
        if self.ctrl_panel.quick_entry_panel:
            accord = self.findDialogAccord(panel=self.ctrl_panel.quick_entry_panel)
            # log_func.debug(u'Accord %s' % str(accord))
            self.setDialogAccord(**accord)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.defaults = None

        ext_data = self.loadFormData(self.getExtDataName())
        if pos is None and ext_data:
            new_pos = ext_data.get('pos', wx.DefaultPosition)
            self.SetPosition(new_pos)
        if size is None and ext_data:
            new_size = ext_data.get('size', wx.DefaultSize)
            self.SetSize(new_size)

    def getExtDataName(self):
        """
        The file name of the additional saved form data.
        """
        return self.ctrl_panel.quick_entry_panel.__class__.__name__

    def setDefaults(self, defaults=None):
        """
        Set default values.

        :param defaults: Dictionary of default values.
        :return: True/False.
        """
        if defaults is not None:
            self.defaults = defaults
        if self.defaults is not None:
            self.setDialogCtrlData(self.ctrl_panel.quick_entry_panel, self.defaults)
        else:
            log_func.warning(u'Default dictionary is not defined')

    def onClose(self, event):
        """
        Window closing handler.
        """
        self.saveFormData(name=self.getExtDataName(),
                          data=dict(pos=tuple(self.GetPosition()), size=tuple(self.GetSize())))
        event.Skip()


def openQuickEntryCtrl(parent, title=u'', pos=None, size=None,
                       quick_entry_panel_class=None, defaults=None,
                       tool_disabled=None,
                       *args, **kwargs):
    """
    Calling and displaying the quick input panel.

    :param parent: Parent window.
    :param title: Title.
    :param pos: The display position of the quick input panel.
        If not defined, then the saved user position is taken.
    :param size: The size of the display of the quick input panel.
        If not defined, then the saved custom size is taken.
    :param quick_entry_panel_class: The class of the quick input panel.
    :param defaults: Dictionary of default values.
    :param tool_disabled: A list of disabled management tools.
        If not defined, then all tools are enabled.
        The list is defined for example as ('add', 'del').
        That is, the add and remove tools are disabled.
    :return: A tuple of two elements:
        1. True - the input data is confirmed. Saving of the entered data is required.
           False - the data is not confirmed. No data saving is required
           None - execution error.
           -1 - The transition to the previous element is made without saving data
            1 - The transition to the next element is made without saving data
        2. Dictionary of filled values
    """
    dlg = None
    result = None
    try:
        # Creating a substrate
        dlg = iqQuickEntryPanelDialog(parent=parent, title=title, pos=pos, size=size,
                                      quick_entry_panel_class=quick_entry_panel_class,
                                      *args, **kwargs)
        # Disable unnecessary tools
        if tool_disabled:
            tool_disabled_arg = dict([(tool_name+'_tool', False) for tool_name in tool_disabled])
            dlg.ctrl_panel.enableTools(**tool_disabled_arg)
        else:
            dlg.ctrl_panel.enableTools()

        # Setting the default values
        if defaults:
            dlg.setDefaults(defaults)
        dlg.ShowModal()
        result = (dlg.ctrl_panel.entry_check, dlg.getPanelCtrlData(panel=dlg.ctrl_panel.quick_entry_panel))
        dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Quick input window error')
    return result


def openQuickEntryEditDlg(parent, title=u'', pos=None, size=None,
                          quick_entry_panel_class=None, defaults=None, *args, **kwargs):
    """
    Calling and displaying the quick input dialog in edit mode.

    :param parent: Parent window.
    :param title: Title.
    :param pos: The display position of the quick input panel.
        If not defined, then the saved user position is taken.
    :param size: The size of the display of the quick input panel.
        If not defined, then the saved custom size is taken.
    :param quick_entry_panel_class: The class of the quick input panel.
    :param defaults: Dictionary of default values.
    :return: Dictionary of filled values, either -1 or 1 value for
        switching to an element without saving, or None if pressed <Cancel>.
    """
    entry_check, entry_data = openQuickEntryCtrl(parent, title=title, pos=pos, size=size,
                                                 quick_entry_panel_class=quick_entry_panel_class,
                                                 defaults=defaults, tool_disabled=('add', 'del'),
                                                 *args, **kwargs)
    if entry_check is ENTRY_OK_CMD:
        return entry_data
    elif entry_check in (GO_PREV_ITEM_CMD, GO_NEXT_ITEM_CMD):
        return entry_check
    # The add and remove tools are disabled, so we don't process them here
    return None
