#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python script property editor class module.
"""

import os.path
import wx.propgrid

from ....util import log_func
from ....util import file_func

from ....engine.wx.dlg import python_script_dialog

__version__ = (0, 0, 0, 1)


class iqScriptPropertyEditor(wx.propgrid.PGTextCtrlAndButtonEditor):
    """
    Python script property editor.
    """
    property_edit_manager = None

    @classmethod
    def setPropertyEditManager(cls, manager):
        cls.property_edit_manager = manager

    @classmethod
    def GetEditor(cls):
        """
        Set editor to have button.
        """
        return 'TextCtrlAndButton'

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, text, flags):
        """
        If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        value = text    # self.str_to_val_user_property(text, self.property_edit_manager)
        return True, value

    def CreateControls(self, propgrid, property, pos, sz):
        """
        Create the actual wxPython controls here for editing the
            property value.

            You must use propgrid.GetPanel() as parent for created controls.

            Return value is either single editor control or tuple of two
            editor controls, of which first is the primary one and second
            is usually a button.
        """
        try:
            x, y = pos
            w, h = sz

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString()

            self.tc = wx.TextCtrl(propgrid.GetPanel(), wx.ID_ANY, s,
                                  (x, y), (w, h),
                                  wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wx.ID_ANY, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)
            return wx.propgrid.PGWindowList(self.tc, btn)
        except:
            log_func.fatal(u'Create the actual controls error <%s>' % self.__class__.__name__)

    def OnEvent(self, propgrid, property, ctrl, event):
        """
        Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        eventType = event.GetEventType()

        if eventType == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            property_value = property.GetValue() if property.GetValue() not in (None, 'None') else ''
            value = python_script_dialog.getPythonScriptDialog(script=property_value)
            if value == '':
                property.SetValueInEvent(None)
            elif value is not None:
                property.SetValueInEvent(value)
            return True

        return False
