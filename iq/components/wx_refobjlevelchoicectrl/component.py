#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx RefObjLevelChoiceCtrl component.
"""

import wx

from ... import object

from . import spc

from ...util import log_func
from ...util import exec_func

from . import refobjlevelchoicectrl

__version__ = (0, 0, 0, 1)


class iqWxRefObjLevelChoiceCtrl(refobjlevelchoicectrl.iqRefObjLevelChoiceCtrlProto,
                                object.iqObject):
    """
    Wx RefObjLevelChoiceCtrl component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        refobjlevelchoicectrl.iqRefObjLevelChoiceCtrlProto.__init__(self, parent=parent, id=wx.NewId(),
                                                                    size=self.getSize(),
                                                                    pos=self.getPosition(),
                                                                    style=self.getStyle())

        refobj_psp = self.getRefObjPsp()
        ref_obj = self.getKernel().createByPsp(psp=refobj_psp) if refobj_psp else None
        self.setRefObj(ref_obj)

    def getPosition(self):
        """
        Control position.
        """
        return self.getAttribute('position')

    def getSize(self):
        """
        Control size.
        """
        return self.getAttribute('size')

    def getStyle(self):
        """
        Control style.
        """
        return self.getAttribute('style')

    def getForegroundColour(self):
        """
        Get foreground colour.
        """
        return self.getAttribute('foreground_colour')

    def getBackgroundColour(self):
        """
        Get background colour.
        """
        return self.getAttribute('background_colour')

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


COMPONENT = iqWxRefObjLevelChoiceCtrl
