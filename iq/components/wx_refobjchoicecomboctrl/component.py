#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjChoiceComboCtrl component.
"""

import wx

from ..wx_widget import component

from . import spc

from ...util import log_func
from ...util import exec_func

from . import refobjchoicecomboctrl

__version__ = (0, 1, 1, 1)


class iqWxRefObjChoiceComboCtrl(refobjchoicecomboctrl.iqRefObjChoiceComboCtrlProto,
                                component.iqWxWidget):
    """
    Wx RefObjChoiceComboCtrl component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        component.iqWxWidget.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        refobjchoicecomboctrl.iqRefObjChoiceComboCtrlProto.__init__(self, parent=parent,
                                                                    id=wx.NewId(),
                                                                    pos=self.getPosition(),
                                                                    size=self.getSize(),
                                                                    style=self.getStyle())

        # Set ref object
        ref_obj_psp = self.getRefObjPsp()
        ref_obj = self.getKernel().getObject(psp=ref_obj_psp) if ref_obj_psp else None
        self.setRefObj(ref_obj)

        self.setViewFieldnames(self.getViewFieldnames())
        self.setSearchFieldnames(self.getSearchFieldnames())

    def getRefObjPsp(self):
        """
        Get ref object passport.
        """
        return self.getAttribute('ref_obj')

    def getViewFieldnames(self):
        """
        Get view field names.
        """
        return self.getAttribute('view_fields')

    def getSearchFieldnames(self):
        """
        Get search field names.
        """
        return self.getAttribute('search_fields')

    def onSelect(self, event):
        """
        Combobox change handler.
        """
        context = self.getContext()
        context['self'] = self
        context['event'] = event
        context['REF_OBJ'] = self.getRefObj()
        context['SELECTED_COD'] = self.getCode()

        function_body = self.getAttribute('on_select')
        if function_body:
            exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)

        if event:
            event.Skip()

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.
        """
        prev_selected_code = self.getCode()
        selected_code = self.choice()
        if prev_selected_code != selected_code:
            self.onSelect(event=None)


COMPONENT = iqWxRefObjChoiceComboCtrl
