#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Cubes OLAP server dialog form.
"""

import keyword

import wx
import wx.stc
from . import cubes_olap_srv_test_dlg_proto

from ...util import log_func
from ...util import str_func

from ..virtual_spreadsheet import spreadsheet_view_manager


__version__ = (0, 0, 0, 1)


class iqCubesOLAPSrvTestDialog(cubes_olap_srv_test_dlg_proto.iqCubesOLAPSrvTestDialogProto):
    """
    Test Cubes OLAP server dialog form.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        cubes_olap_srv_test_dlg_proto.iqCubesOLAPSrvTestDialogProto.__init__(self, *args, **kwargs)

        # Configuring the Code Browser
        self.json_scintilla.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.json_scintilla.SetKeyWords(0, ' '.join(keyword.kwlist))

        self.json_scintilla.SetProperty('fold', '1')
        self.json_scintilla.SetProperty('tab.timmy.whinge.level', '1')
        self.json_scintilla.SetMargins(0, 0)

        # Don't see empty spaces as dots
        self.json_scintilla.SetViewWhiteSpace(False)

        # Indentation and tab stuff
        self.json_scintilla.SetIndent(4)                 # Proscribed indent size for wx
        self.json_scintilla.SetIndentationGuides(True)   # Show indent guides
        self.json_scintilla.SetBackSpaceUnIndents(True)  # Backspace unindents rather than delete 1 space
        self.json_scintilla.SetTabIndents(True)          # Tab key indents
        self.json_scintilla.SetTabWidth(4)               # Proscribed tab size for wx
        self.json_scintilla.SetUseTabs(False)            # Use spaces rather than tabs, or

        # Setting the box to capture folder markers
        self.json_scintilla.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.json_scintilla.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.json_scintilla.SetMarginSensitive(1, True)
        self.json_scintilla.SetMarginSensitive(2, True)
        self.json_scintilla.SetMarginWidth(1, 25)
        self.json_scintilla.SetMarginWidth(2, 12)

        # and now set up the fold markers
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUSCONNECTED,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, 'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_LCORNER,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_VLINE,    'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS,  'white', 'black')
        self.json_scintilla.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS, 'white', 'black')
        # Debug mode markers
        # self.json_scintilla.MarkerDefine(self.icBreakpointMarker,       stc.STC_MARK_CIRCLE, 'black', 'red')
        # self.json_scintilla.MarkerDefine(self.icBreakpointBackgroundMarker, stc.STC_MARK_BACKGROUND, 'black', 'red')

        # OLAP server
        self._OLAP_server = None

        # SpreadSheet structure output control manager
        self._spreadsheet_mngr = spreadsheet_view_manager.iqSpreadSheetViewManager(grid=self.spreadsheet_grid)

    def setOLAPServer(self, olap_server):
        """
        Set OLAP server.

        :param olap_server: OLAP server
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            self.request_panel.setOLAPServer(self._OLAP_server)

    def onCloseButtonClick(self, event):
        """
        CLOSE button handler.
        """
        self.EndModal(wx.ID_CLOSE)
        event.Skip()

    def _parseDimensionNames(self, dimension_url):
        """
        Dimension name list .

        :param dimension_url: Part of the request element .
            For example: store_date@ymd:month
        :return: Dimension member names list.
        """
        dimension_names = list()
        if '@' in dimension_url:
            # dimension@hierarchy:level
            cube_idx = self.request_panel.cube_choice.GetSelection()
            cube = self._OLAP_server.getCubes()[cube_idx]
            dimension_name = dimension_url.split('@')[0]
            dimension = cube.findDimension(dimension_name)
            hierarchy_name = dimension_url.split('@')[1].split(':')[0]
            hierarchy = dimension.findHierarchy(hierarchy_name)
            level_names = hierarchy.getLevelNames()
            hierarchy_level_name = dimension_url.split('@')[1].split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        elif ':' in dimension_url:
            # dimension:level
            cube_idx = self.request_panel.cube_choice.GetSelection()
            cube = self._OLAP_server.getCubes()[cube_idx]
            dimension_name = dimension_url.split(':')[0]
            dimension = cube.findDimension(dimension_name)
            level_names = [level.getName() for level in dimension.getLevels()]
            hierarchy_level_name = dimension_url.split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        else:
            # dimension
            dimension_names = tuple([dimension_url])

        return dimension_names

    def onRefreshToolClicked(self, event):
        """
        REFRESH button handler.
        """
        if self._OLAP_server:
            request_url = self.request_panel.getRequestURL()
            self.request_panel.request_textCtrl.SetValue(request_url)

            result = self._OLAP_server.getResponse(request_url)

            # self.json_scintilla.SetText(str(result))
            self.json_scintilla.ClearAll()
            self.json_scintilla.AddText(str_func.data2txt(result))

            if result:
                if self.request_panel.drilldown_checkBox.GetValue() and '|' in self.request_panel.drilldown_textCtrl.GetValue():
                    row_dimension_url, col_dimension_url = self.request_panel.drilldown_textCtrl.GetValue().split('|')
                    row_dimension = self._parseDimensionNames(row_dimension_url)
                    col_dimension = self._parseDimensionNames(col_dimension_url)
                    dataframe = self._OLAP_server.to_pivot_dataframe(result, row_dimension=row_dimension,
                                                                     col_dimension=col_dimension)

                    # spreadsheet = self._OLAP_server.pivot_to_spreadsheet(result, dataframe=dataframe)
                else:
                    row_dimension_url = self.request_panel.drilldown_textCtrl.GetValue()
                    row_dimension = self._parseDimensionNames(row_dimension_url)
                    # col_dimension = self._parseDimensionNames(col_dimension_url)
                    dataframe = self._OLAP_server.to_pivot_dataframe(result, row_dimension=row_dimension)

                spreadsheet = self._OLAP_server.pivot_to_spreadsheet(result, dataframe=dataframe)
                #     spreadsheet = self._OLAP_server.to_spreadsheet(result)
                # log.debug(u'SpreadSheet: %s' % str(spreadsheet))
                self._spreadsheet_mngr.viewSpreadSheet(spreadsheet)
            else:
                # Clear grid
                self._spreadsheet_mngr.reCreateGrid(self._spreadsheet_mngr.getSpreadSheetGrid(), 1, 1)

            # For the scrollbars to appear, the grid control needs to be layout
            self.spreadsheet_panel.Layout()

        event.Skip()


def showCubesOLAPServerTestDlg(parent=None, olap_srv=None):
    """
    Show Cubes OLAP server test dialog.

    :param parent: Parent window.
        If not defined then get top window.
    :param olap_srv: OLAP server.
    :return: True/False.
    """
    if olap_srv is None:
        log_func.warning(u'OLAP server not defined for testing')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Run OLAP server
        olap_srv.run()

        dlg = iqCubesOLAPSrvTestDialog(parent=parent)
        dlg.setOLAPServer(olap_srv)

        dlg.ShowModal()

        # Stop OLAP server
        olap_srv.stop()

        return True
    except:
        # Stop OLAP server
        olap_srv.stop()

        log_func.fatal(u'Error show Cubes OLAP server test dialog')
    return False
