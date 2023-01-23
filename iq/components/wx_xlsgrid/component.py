#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx XLSGrid component.
"""

import os.path
import wx
import wx.lib.agw.xlsgrid
import xlrd

from . import spc

from ...util import log_func
from ..wx_widget import component

from ...dialog import dlg_func

__version__ = (0, 0, 0, 1)


class iqWxXLSGrid(wx.lib.agw.xlsgrid.XLSGrid, component.iqWxWidget):
    """
    Wx XLSGrid component.
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

        wx.lib.agw.xlsgrid.XLSGrid.__init__(self, parent=parent)

        self.createChildren()

        xls_filename = self.getXLSFilename()
        if xls_filename:
            self.openXLSFile(xls_filename)

    def openXLSFile(self, xls_filename, worksheet_name=None):
        """
        Open XLS file.

        :param xls_filename: XLS filename.
        :param worksheet_name: Opened worksheet name.
            If not define then get first worksheet.
        :return: True/False.
        """
        try:
            return self._openXLSFile(xls_filename=xls_filename, worksheet_name=worksheet_name)
        except:
            log_func.fatal(u'Error open XLS file <%s : %s>' % (xls_filename, worksheet_name))
        return False

    def _openXLSFile(self, xls_filename, worksheet_name=None):
        """
        Open XLS file.

        :param xls_filename: XLS filename.
        :param worksheet_name: Opened worksheet name.
            If not define then get firsh worksheet.
        :return: True/False.
        """
        if not os.path.isfile(xls_filename):
            dlg_func.openWarningBox(title=u'WARNING',
                                    prompt_text=u'File <%s> not found' % xls_filename)
            return False

        busy = wx.BusyInfo(u'Reading Excel file <%s>, please wait...' % xls_filename)

        workbook = xlrd.open_workbook(xls_filename, formatting_info=1)

        if worksheet_name is None:
            sheets = workbook.sheets()
            worksheet_name = sheets[0].name
            log_func.info(u'XLS file <%s>. Get first worksheet <%s>' % (xls_filename, worksheet_name))

        worksheet = workbook.sheet_by_name(worksheet_name)
        rows, cols = worksheet.nrows, worksheet.ncols

        comments, texts = wx.lib.agw.xlsgrid.ReadExcelCOM(xls_filename, worksheet_name, rows, cols)

        del busy

        self.Show()
        self.PopulateGrid(workbook, worksheet, texts, comments)

        parent = self.getParent()
        if parent:
            parent.Layout()

    def getXLSFilename(self):
        """
        Get default opened XLS filename.
        """
        return self.getAttribute('xls_filename')


COMPONENT = iqWxXLSGrid
