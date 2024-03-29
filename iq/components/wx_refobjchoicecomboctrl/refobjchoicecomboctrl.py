#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control of the selection of a ref object item in a standard
form through the selection window.
"""

import wx

from ...util import log_func

__version__ = (0, 0, 2, 1)

DEFAULT_ENCODING = 'utf-8'


class iqRefObjChoiceComboCtrlProto(wx.ComboCtrl):
    """
    Control of the selection of a ref object item in a standard
    form through the selection window.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # Make read only
        style = wx.CB_READONLY
        if 'style' in kwargs:
            style = kwargs['style'] | wx.CB_READONLY
        kwargs['style'] = style

        wx.ComboCtrl.__init__(self, *args, **kwargs)

        self.makeCustomButton()

        # Reference object
        self._ref_object = None

        self._selected_cod = None

        # View field name list
        self._view_fieldnames = None
        # Search field name list
        self._search_fieldnames = None

        self._do_refresh = False

        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)

    def Enable(self, *args, **kwargs):
        """
        Overriding Enable method.
        """
        wx.ComboCtrl.Enable(self, *args, **kwargs)

        if not self.IsEnabled():
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))
        else:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    def makeCustomButton(self):
        """
        Create button '...'.
        """
        # make a custom bitmap showing "..."
        bw, bh = 16, 16
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
        dc.DrawText(label, round((bw-tw)/2), round((bw-tw)/2))
        del dc

        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)

        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)

    def setRefObj(self, ref_object):
        """
        Set reference object.
        """
        self._ref_object = ref_object

    def setViewFieldnames(self, fieldnames):
        """
        Set view field name list.
        """
        self._view_fieldnames = fieldnames

    def setSearchFieldnames(self, fieldnames):
        """
        Set search field name list.
        """
        self._search_fieldnames = fieldnames

    def getRefObj(self):
        """
        Get reference object.
        """
        return self._ref_object

    def getSelectedCode(self):
        """
        Get selected cod.
        """
        return self._selected_cod

    def setCode(self, code):
        """
        Set selected cod.

        :param code: Cod.
        :return: True/False.
        """
        if code is None:
            # An empty value can also be set in the control
            self._selected_cod = None
            self.SetValue(u'')
            return True

        if self._ref_object is not None:
            name = self._ref_object.getColumnNameValue(code)
            if name:
                self._selected_cod = code
                self.SetValue(name)

                self.onSelect(event=None)
                return True
        else:
            log_func.warning(u'Not define ref object in <%s>' % self.getName())
        return False

    getCode = getSelectedCode
    getValue = getCode
    setValue = setCode

    def clear(self):
        """
        Clear value.
        """
        return self.setValue(None)

    def isSelected(self):
        """
        Something selected?

        :return: True/False.
        """
        return self.getValue() is not None

    def refresh(self):
        """
        Refresh control.

        :return: True/False.
        """
        self._do_refresh = True

    def choice(self):
        """
        Call selection.

        :return: Selected cod.
        """
        if self._ref_object is not None:
            selected_record = self._ref_object.choice(parent=self,
                                                      view_fields=self._view_fieldnames,
                                                      search_fields=self._search_fieldnames,
                                                      clear_cache=self._do_refresh)
            self._do_refresh = False
            if selected_record:
                code = selected_record.get(self._ref_object.getCodColumnName())
                name = selected_record.get(self._ref_object.getNameColumnName())
                self._selected_cod = code
                self.SetValue(name)
                return self._selected_cod
            else:
                log_func.warning(u'Error choice ref object item <%s>' % self._ref_object.getName())
        else:
            log_func.warning(u'Not define ref object in control <%s>' % self.getName())
        return None

    def onMouseLeftDown(self, event):
        """
        Handler for clicking the left button on the control.
        """
        # [NOTE] No need to call self.choice(). It is enough to call
        # event.Skip() and the machine will be called self.OnButtonClick()
        event.Skip()

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        self.choice()

    def DoSetPopupControl(self, popup):
        """
        Overridden from ComboCtrl to avoid assert since there is no ComboPopup.
        """
        pass

    def onSelect(self, event):
        """
        Combobox change handler.
        """
        pass
