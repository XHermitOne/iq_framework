#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ref object code property editor.
"""

import gettext
import wx
import wx.propgrid

from ...util import log_func
from ...util import lang_func
from ...engine.wx.dlg import edit_masked_txt_dlg

_ = lang_func.getTranslation().gettext

__version__ = (0, 0, 0, 1)

DEFAULT_ENCODE = 'utf-8'


class iqEditCodeProperty(wx.propgrid.StringProperty):
    """
    Ref object code property editor.
    """
    def __init__(self, label, name=wx.propgrid.PG_LABEL, value=u''):
        wx.propgrid.StringProperty.__init__(self, label, name, value)

        self.ref_obj = None
        
        self.property_grid = None
        
    def setRefObj(self, ref_obj):
        """
        Set ref object.
        """
        self.ref_obj = ref_obj
        
    def setPropertyGrid(self, property_grid):
        """
        Set property grid.
        """
        self.property_grid = property_grid
        
    def GetEditor(self):
        """
        Set editor to have button.
        """
        return 'TextCtrlAndButton'

    def _getMask(self, ref_obj, code):
        """
        Identify mask by code.

        Masks:

        =========  ==========================================================
        Character   Function
        =========  ==========================================================
            #       Allow numeric only (0-9)
            N       Allow letters and numbers (0-9)
            A       Allow uppercase letters only
            a       Allow lowercase letters only
            C       Allow any letter, upper or lower
            X       Allow string.letters, string.punctuation, string.digits
            &       Allow string.punctuation only (doesn't include all unicode symbols)
            \*      Allow any visible character
            |       explicit field boundary (takes no space in the control; allows mix
                    of adjacent mask characters to be treated as separate fields,
                    eg: '&|###' means "field 0 = '&', field 1 = '###'", but there's
                    no fixed characters in between.
        =========  ==========================================================

        :param ref_obj: Ref object.
        :param code: Ref object code.
        """
        # Get the structural code
        struct_code = self.ref_obj.StrCode2ListCode(code)
        # Filter out last empty subcodes
        struct_mask = [sub_code for sub_code in struct_code if sub_code]
        # We can only edit the last subcode
        struct_mask[-1] = 'X{%d}' % (len(struct_mask[-1]))
        struct_mask = [''.join(['\\'+s for s in list(sub_code)]) for sub_code in struct_mask[:-1]] + [struct_mask[-1]]
        mask = ''.join(struct_mask)
        return mask

    def _getRegExp(self, ref_obj, code):
        """
        Define a regular expression of control by code.
        <\W+?> - Added to regex to support punctuation in codes.
        
        :param ref_obj: Ref object.
        :param code: Ref object record code.
        """
        # Get the structural code
        struct_code = self.ref_obj.StrCode2ListCode(code)
        # Filter out last empty subcodes
        struct_exp = [sub_code for sub_code in struct_code if sub_code]
        # We can only edit the last subcode
        struct_exp[-1] = r'[\W+?0-9a-zA-Z]{%d}' % (len(struct_exp[-1]))
        reg_exp = r''.join(struct_exp)
        return reg_exp
        
    def _getEditDlg(self, attr, value, pos=wx.DefaultPosition, size=wx.DefaultSize,
                    style=wx.DEFAULT_DIALOG_STYLE,
                    property_editor=None, *arg, **kwarg):
        """
        Dialog for editing a property / attribute.

        :param parent: Parent window.
        :param attr: Attribute name.
        :param value: Current value.
        :param pos: Dialog position.
        :param size: Dialog size.
        :param style: Dialog style.
        :param property_editor: Property editor.
        :return: Edited value.
        """
        if property_editor:
            mask = self._getMask(self.ref_obj, value)
            log_func.debug(u'Code editor mask <%s>' % mask)
            reg_exp = self._getRegExp(self.ref_obj, value)
            log_func.debug(u'Code editor control regular expression <%s>' % reg_exp)
            
            value = edit_masked_txt_dlg.editMaskedTextDlg(parent=property_editor,
                                                          title=u'Редактирование кода записи справочника',
                                                          label=u'Введите код:',
                                                          default_txt=value,
                                                          mask=mask, reg_exp=reg_exp)
            if value:
                return str(value)
            return None
        else:
            log_func.error(u'Not define property editor')
        return u''

    def OnEvent(self, propgrid, primaryEditor, event):
        """
        Property editor event handler.

        :param propgrid:
        :param primaryEditor:
        :param event:
        :return:
        """
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            value = self._getEditDlg(self.GetName(), self.GetValue(),
                                     pos=wx.GetMousePosition(),
                                     property_editor=self.property_grid)
            self.SetValueInEvent(value)
            return True
        return False

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, text, argFlags):
        """
        If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        value = str(text)
        return True, value

    def ValidateValue(self, value, validationInfo):
        """
        Control / validation function.
        """
        if isinstance(value, str):
            return True, value
        else:
            return False
