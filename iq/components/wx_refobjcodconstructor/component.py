#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjCodConstructor component.
"""

import wx

from ..wx_widget import component

from . import spc

from ...util import log_func
from ...util import exec_func

from . import refobjcodconstructor

__version__ = (0, 0, 0, 1)


class iqWxRefObjCodConstructor(refobjcodconstructor.iqRefObjCodConstructorProto,
                               component.iqWxWidget):
    """
    Wx RefObjCodConstructor component.
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

        refobjcodconstructor.iqRefObjCodConstructorProto.__init__(self, parent=parent, id=wx.NewId(),
                                                                  size=self.getSize(),
                                                                  pos=self.getPosition(),
                                                                  style=self.getStyle())

        refobj_psp = self.getRefObjPsp()
        ref_obj = self.getKernel().getObject(psp=refobj_psp) if refobj_psp else None
        self.setRefObj(ref_obj)

    def getRefObjPsp(self):
        """
        Get ref object passport.
        """
        return self.getAttribute('ref_obj')

    def getAutoSelect(self):
        """
        Auto-complete?
        """
        return self.getAttribute('auto_select')

    def getLabel(self):
        """
        Get label.
        """
        return self.getAttribute('label')

    def onSelectCode(self):
        """
        Select code handler.
        """
        context = self.getContext()
        context['SELECTED_CODE'] = self._selected_code

        if self.isAttributeValue('on_select_code'):
            function_body = self.getAttribute('on_select_code')

            result = exec_func.execTxtFunction(function=function_body,
                                               context=context)
            return result
        return None


COMPONENT = iqWxRefObjCodConstructor
