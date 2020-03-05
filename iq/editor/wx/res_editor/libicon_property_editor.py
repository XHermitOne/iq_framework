#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Library icon property editor class module.
"""

import os.path
import wx.propgrid

from ....util import log_func
from ....util import icon_func

from ....engine.wx.dlg import wximage_browser

__version__ = (0, 0, 0, 1)


class iqLibraryIconPropertyEditor(wx.propgrid.PGTextCtrlAndButtonEditor):
    """
    Library icon property editor.
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
        # log_func.debug(u'Create controls <%s>' % self.__class__.__name__)
        try:
            x, y = pos
            w, h = sz

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString()

            self.tc = wx.TextCtrl(propgrid.GetPanel(), wx.propgrid.PG_SUBID1, s,
                                  (x, y), (w, h),
                                  wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wx.propgrid.PG_SUBID2, '...',
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
            value = wximage_browser.getImageBrowserDlg(parent=None)
            if value is not None:

                lib_icon_path = icon_func.getIconPath()
                value = value.replace(lib_icon_path, '')
                if value.endswith(icon_func.ICON_FILENAME_EXT):
                    value = value.replace(icon_func.ICON_FILENAME_EXT, '')
                if value.startswith(os.path.sep):
                    value = value[1:]

                property.SetValueInEvent(value)
            return True

        return False
