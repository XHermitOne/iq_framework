#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx filter choice control component.
"""

try:
    import wx
except ImportError:
    print(u'Import error wx')

from . import spc

from ...util import log_func
from ...util import lang_func
from ...util import exec_func
from ...util import file_func
from ...util import global_func

from . import filter_choicectrl

from ...role import component as role

from ..wx_widget import component

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

EDIT_PERMISSION = dict(name='edit_filter', description=_('Can edit filters'), type='DATA')
role.addPermision(**EDIT_PERMISSION)


class iqWxFilterChoiceCtrl(filter_choicectrl.iqFilterChoiceCtrlProto,
                           component.iqWxWidget):
    """
    Wx filter choice control component.
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

        filter_choicectrl.iqFilterChoiceCtrlProto.__init__(self, parent=parent, id=wx.NewId(),
                                                           pos=self.getPosition(),
                                                           size=self.getSize(),
                                                           style=self.getStyle(),
                                                           name=self.getName())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        self.createChildren()

        self._filter_filename = self.getSaveFilename()
        self._environment = self.getEnvironment()
        self._limit = self.getLimit()

        # Load filters
        self.loadFilter()
        self.SetValue(self.getStrFilter())

    def _canEditFilter(self):
        cur_user = global_func.getUser()
        can_edit = cur_user.isPermission('edit_filter')
        log_func.info(u'User <%s : %s>. Can edit filters ... %s' % (cur_user.getName(),
                                                                    cur_user.getDescription(), can_edit))
        return can_edit

    def OnButtonClick(self):
        """
        Overridden from ComboCtrl, called when the combo button is clicked.

        [NOTE] Not valid:
        def OnButtonClick(self):
            ok = self.doDlgChoiceFilter(self)
            if ok:
                self.eval_attr('onChange')
            self.SetFocus()
        wxPython (v 3.0.0) call <Segmentation fault>
        """
        self._dlg = filter_choicectrl.iqFilterChoiceDlg(self)
        # Lock edit buttons
        can_edit_filter = self._canEditFilter()
        self._dlg.addButton.Enable(can_edit_filter)
        self._dlg.delButton.Enable(can_edit_filter)

        self._dlg.setEnvironment(self._environment)
        self._dlg.setFilters(self._filter)
        self._dlg.setLimitLabel(self._limit, self._over_limit)

        if self._dlg.ShowModal() == wx.ID_OK:
            self._filter = self._dlg.getFilter()
            self.saveFilter()
            str_filter = self.getStrFilter()
            self.SetValue(str_filter)
            # Run handler
            self.onChange(None)
        self._dlg.Destroy()
        self._dlg = None
        self.SetFocus()

    def onChange(self, event):
        """
        Change filter handler.
        """
        context = self.getContext()
        context['self'] = self
        context['event'] = event
        function_body = self.getAttribute('on_change')
        if function_body:
            return exec_func.execTxtFunction(function=function_body,
                                             context=context)

    def getSaveFilename(self):
        """
        Filter storage filename.
        """
        res_save_filename = self.getAttribute('save_filename')
        if res_save_filename:
            return file_func.getNormalPath(res_save_filename)
        return None

    def getEnvironment(self):
        """
        Get environment.
        """
        if self._environment is None:
            if self.isAttributeValue('get_env'):
                context = self.getContext()
                function_body = self.getAttribute('get_env')
                if function_body:
                    self._environment = exec_func.execTxtFunction(function=function_body,
                                                                  context=context)
        return self._environment

    def getLimit(self):
        """
        Get record limit.
        """
        if self._limit is None:
            self._limit = self.getAttribute('limit')
        return self._limit


COMPONENT = iqWxFilterChoiceCtrl
