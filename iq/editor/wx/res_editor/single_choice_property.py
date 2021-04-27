#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Single choice property class module.
"""

import wx.propgrid

from ....util import log_func
from ....util import lang_func
# from ....util import file_func

# from ....engine.wx.dlg import wxdlg_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqSingleChoiceDialogAdapter(wx.propgrid.PGEditorDialogAdapter):
    """
    This demonstrates use of wxpg.PGEditorDialogAdapter.
    """
    def __init__(self, choices):
        wx.propgrid.PGEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        """
        Show property edit dialog.

        :param propGrid:
        :param property:
        :return:
        """
        cur_value = property.GetValue()
        try:
            value_idx = self.choices.index(cur_value)
        except IndexError:
            value_idx = 0

        single_choice_value = wx.GetSingleChoice(message=_('Message'),
                                                 caption=_('Caption'),
                                                 choices=self.choices,
                                                 initialSelection=value_idx)

        if single_choice_value:
            self.SetValue(single_choice_value)
            return True

        return False


class iqSingleChoiceProperty(wx.propgrid.StringProperty):
    """
    Single choice property class.
    """
    def __init__(self, label=wx.propgrid.PG_LABEL, name=wx.propgrid.PG_LABEL, choices=(), value=''):
        """
        Constructor.

        :param label: Property label.
        :param name: Property name.
        :param choices: Choices.
        :param value: Property value.
        """
        wx.propgrid.StringProperty.__init__(self, label, name, value)

        self._choices = choices

    def DoGetEditorClass(self):
        return wx.propgrid.PropertyGridInterface.GetEditorByName('TextCtrlAndButton')

    def GetEditorDialog(self):
        # Set what happens on button click
        return iqSingleChoiceDialogAdapter(self._choices)
