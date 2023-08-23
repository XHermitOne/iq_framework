#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control of the selection of a ref object item in a standard
form through the selection window.
"""

from ...util import log_func
from ...engine.wx import wxbitmap_func

from . import wx_refobjchoice_proto

__version__ = (0, 0, 1, 2)

DEFAULT_ENCODING = 'utf-8'


class iqRefObjChoiceProto(wx_refobjchoice_proto.iqWxRefObjChoicePanelProto):
    """
    Control of the selection of a ref object item in a standard
    form through the selection window.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        wx_refobjchoice_proto.iqWxRefObjChoicePanelProto.__init__(self, *args, **kwargs)

        button_bmp = wxbitmap_func.createIconBitmap('dots')
        self.choice_bpButton.SetBitmap(button_bmp)

        # Reference object
        self._ref_object = None

        self._selected_cod = None

        # View field name list
        self._view_fieldnames = None
        # Search field name list
        self._search_fieldnames = None

        self._do_refresh = False

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
            self.choice_textCtrl.SetValue(u'')
            return True

        if self._ref_object is not None:
            name = self._ref_object.getColumnNameValue(code) if code else None
            if name:
                self._selected_cod = code
                self.choice_textCtrl.SetValue(name)

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
                self.choice_textCtrl.SetValue(name)
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
        prev_selected_code = self.getCode()
        selected_code = self.choice()
        if prev_selected_code != selected_code:
            self.onSelect(event=event)

        event.Skip()

    def onChoiceButtonClick(self, event):
        """
        Handler for clicking the left button on the button control.
        """
        prev_selected_code = self.getCode()
        selected_code = self.choice()
        if prev_selected_code != selected_code:
            self.onSelect(event=event)
        event.Skip()

    def onSelect(self, event):
        """
        Choice control change handler.
        """
        pass
