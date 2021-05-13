#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx TableChoiceCtrl component.
"""

import wx

from ..wx_widget import component

from . import spc

from ...util import log_func
from ...util import exec_func

from . import tablechoicectrl

__version__ = (0, 0, 0, 1)


class iqWxTableChoiceCtrl(tablechoicectrl.iqTableChoiceCtrlProto,
                          component.iqWxWidget):
    """
    Wx TableChoiceCtrl component.
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

        tablechoicectrl.iqTableChoiceCtrlProto.__init__(self, parent=parent,
                                                        id=wx.NewId(),
                                                        pos=self.getPosition(),
                                                        size=self.getSize(),
                                                        style=self.getStyle())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        table_psp = self.getTablePsp()
        self.createTableDataSource(table_psp=table_psp)

        self.Bind(wx.EVT_COMBOBOX, self.onComboBox)

    def getTablePsp(self):
        """
        Get table object passport.
        """
        return self.getAttribute('table')

    def createTableDataSource(self, table_psp=None, **kwargs):
        """
        Create a table object-source of data according to its passport.

        :param table_psp: The passport of the table data source object.
             If the passport is not defined, then it is taken from the resource description.
        :param kwargs: Extra name arguments.
            Additional parameters for generating executable text
            SQL query for example.
        :return: Tabular data source object.
        """
        if table_psp is None:
            table_psp = self.getTablePsp()
        table = self.getKernel().createByPsp(psp=table_psp) if table_psp else None
        # log_func.debug(u'Table object <%s> : %s' % (str(table_psp), str(table)))
        self.setTableDataSource(table, **kwargs)
        return table

    def refreshChoices(self, **kwargs):
        """
        Refresh selection list.

        :param kwargs: Extra name arguments.
            Additional parameters for generating executable text
            SQL query for example.
        """
        self.createTableDataSource(**kwargs)

    def getCodeField(self):
        """
        List item code field.
        """
        return self.getAttribute('code_field')

    def getLabelField(self):
        """
        List item label field.
        """
        return self.getAttribute('label_field')

    def isLabelFunc(self):
        """
        Have you defined a function to get the list item label?

        :return: True/False.
        """
        return self.isAttributeValue('get_label')

    def getLabelFunc(self, *arg, **kwarg):
        """
        Get the function for determining the caption of a list item.
        """
        context = self.getContext()
        context['self'] = self
        context['args'] = arg
        context.update(kwarg)

        function_body = self.getAttribute('get_label')
        if function_body:
            result = exec_func.execTxtFunction(function=function_body, context=context)
            return result
        return None

    def getFilterFunc(self, *arg, **kwarg):
        """
        Get a function for additional filtering of list items.
        """
        context = self.getContext()
        context['self'] = self
        context['args'] = arg
        context.update(kwarg)

        function_body = self.getAttribute('get_filter')
        if function_body:
            result = exec_func.execTxtFunction(function=function_body, context=context)
            return result
        return None

    def isFilterFunc(self):
        """
        Defined a function for additional filtering of table data?

        :return: True/False.
        """
        return self.isAttributeValue('get_filter')

    def getCanEmpty(self):
        """
        Is it possible to choose an empty value?
        """
        return self.getAttribute('can_empty')

    def onComboBox(self, event):
        """
        Element selection handler.
        """
        # Call parent class handler
        # [NOTE] Skip we do not execute
        tablechoicectrl.iqTableChoiceCtrlProto.onComboBox(self, None)

        # Calling a custom handler
        context = self.getContext()
        context['self'] = self
        context['event'] = event
        function_body = self.getAttribute('on_change')
        if function_body:
            exec_func.execTxtFunction(function=function_body, context=context)

        # At the end, Skip is executed
        event.Skip()


COMPONENT = iqWxTableChoiceCtrl
