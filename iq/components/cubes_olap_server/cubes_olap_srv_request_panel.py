#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cubes OLAP server request panel.
"""

import wx
from . import cubes_olap_srv_request_panel_proto

from ...util import log_func

from ...engine.wx import panel_manager
from ...engine.wx.dlg import info_window


__version__ = (0, 0, 0, 1)

OLAP_METHODS = ('aggregate', 'members', 'facts', 'fact', 'cell', 'report')

CUT_PARAMETER_HELP = u'cut - cut cell specification, For example: cut=date:2004,1|category:2|entity:12345'
DRILLDOWN_PARAMETER_HELP = u'''drilldown - dimension, which one needs "drilldown". For example drilldown=date will give rows for each value 
next level of measurement date. You can explicitly specify the level for granularity in the form: dimension:level,
such as: drilldown=date:month. To specify the hierarchy use dimension@hierarchy how in
drilldown=date@ywd for implicit level or drilldown=date@ywd:week explicitly state the level.'''
AGGREGATES_PARAMETER_HELP = u'''aggregates – list of aggregates for calculation, shared with |,
For example: aggergates=amount_sum|discount_avg|count'''
MEASURES_PARAMETER_HELP = u'''measures – a list of measures for which their respective aggregates will be calculated.
Shared with |, For example: aggergates=proce|discount'''
PAGE_PARAMETER_HELP = u'page - page number for pagination'
PAGESIZE_PARAMETER_HELP = u'pagesize - page size for pagination'
ORDER_PARAMETER_HELP = u'order - list of attributes to sort'
SPLIT_PARAMETER_HELP = u'''split – split cell, the same syntax as slice, defines a virtual binary (flag) dimension that indicates whether a cell is 
belongs to the split cut (true) or no (false). The dimension attribute is called __within_split__.
Refer to the backend you are using for more information if this feature is supported or not.'''

OLAP_SERVER_URL_FMT = 'cube/%s/%s'


class iqCubesOLAPSrvRequestPanel(cubes_olap_srv_request_panel_proto.iqCubesOLAPSrvRequestPanelProto,
                                 panel_manager.iqPanelManager):
    """
    Cubes OLAP server request panel.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        cubes_olap_srv_request_panel_proto.iqCubesOLAPSrvRequestPanelProto.__init__(self, *args, **kwargs)

        # OLAP server
        self._OLAP_server = None

        self._help_popup_win = None
        self.init()

    def setOLAPServer(self, olap_server):
        """
        Set OLAP server.

        :param olap_server: OLAP server.
        """
        self._OLAP_server = olap_server

        if self._OLAP_server:
            choices = [cube.description if cube.description else cube.name for cube in self._OLAP_server.getCubes()]
            self.cube_choice.Clear()
            self.cube_choice.AppendItems(choices)
            if choices:
                self.cube_choice.setSelection(0)
                self.method_choice.setSelection(0)
                self.refreshDimensionChoice(0)

    def refreshDimensionChoice(self, i_cube):
        """
        Refresh the list of dimensions based on the selected cube.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [u''] + [dimension.getLabel() for dimension in cube.getDimensions()]

            self.dimension_choice.Clear()
            self.dimension_choice.AppendItems(choices)
            if choices:
                self.dimension_choice.setSelection(0)

    def init(self):
        """
        Init panel.
        """
        self.initImages()
        self.initControls()
        
    def initImages(self):
        """
        Init control images.
        """
        pass
        
    def initControls(self):
        """
        Init controls.
        """
        self.method_choice.AppendItems(OLAP_METHODS)

        # Enable all options
        self.cut_textCtrl.Enable(False)
        self.drilldown_textCtrl.Enable(False)
        self.aggregates_textCtrl.Enable(False)
        self.measures_textCtrl.Enable(False)
        self.page_textCtrl.Enable(False)
        self.pagesize_textCtrl.Enable(False)
        self.order_textCtrl.Enable(False)
        self.split_textCtrl.Enable(False)

    # def onCubeChoice(self, event):
    #     """
    #     Select cube handler.
    #     """
    #     i_cube = event.GetSelection()
    #     self.refreshDimensionChoice(i_cube)
    #
    #     event.Skip()

    def onAggregatesCheckBox(self, event):
        """
        Aggregate parameter enable handler.
        """
        enable = event.IsChecked()
        self.aggregates_textCtrl.Enable(enable)
        event.Skip()

    def showHelpPopupWin(self, button, info_text):
        """
        Show / hide help popup.

        :param button: Help window button.
        :param info_text: Help text.
        :return:
        """
        if self._help_popup_win:
            self._help_popup_win.close()
            self._help_popup_win = None
        else:
            self._help_popup_win = info_window.showInfoWindow(parent=self,
                                                              ctrl=button,
                                                              info_text=info_text)

    def onAggregatesHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.aggregates_hlp_bpButton,
                              info_text=AGGREGATES_PARAMETER_HELP)
        event.Skip()

    def onCutCheckBox(self, event):
        """
        Cut parameter enable handler.
        """
        enable = event.IsChecked()
        self.cut_textCtrl.Enable(enable)
        event.Skip()

    def onCutHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.cut_hlp_bpButton,
                              info_text=CUT_PARAMETER_HELP)
        event.Skip()

    def onDrilldownCheckBox(self, event):
        """
        Drilldown parameter enable handler.
        """
        enable = event.IsChecked()
        self.drilldown_textCtrl.Enable(enable)
        event.Skip()

    def onDrilldownHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.drilldown_hlp_bpButton,
                              info_text=DRILLDOWN_PARAMETER_HELP)
        event.Skip()

    def onMeasuresCheckBox(self, event):
        """
        Measures parameter enable handler.
        """
        enable = event.IsChecked()
        self.measures_textCtrl.Enable(enable)
        event.Skip()

    def onMeasuresHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.measures_hlp_bpButton,
                              info_text=MEASURES_PARAMETER_HELP)
        event.Skip()

    def onOrderCheckBox(self, event):
        """
        Order parameter enable handler.
        """
        enable = event.IsChecked()
        self.order_textCtrl.Enable(enable)
        event.Skip()

    def onOrderHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.order_hlp_bpButton,
                              info_text=ORDER_PARAMETER_HELP)
        event.Skip()

    def onPageCheckBox(self, event):
        """
        Page parameter enable handler.
        """
        enable = event.IsChecked()
        self.page_textCtrl.Enable(enable)
        event.Skip()

    def onPageHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.page_hlp_bpButton,
                              info_text=PAGE_PARAMETER_HELP)
        event.Skip()

    def onPagesizeCheckBox(self, event):
        """
        Pagesize parameter enable handler.
        """
        enable = event.IsChecked()
        self.pagesize_textCtrl.Enable(enable)
        event.Skip()

    def onPagesizeHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.pagesize_hlp_bpButton,
                              info_text=PAGESIZE_PARAMETER_HELP)
        event.Skip()

    def onSplitCheckBox(self, event):
        """
        Split parameter enable handler.
        """
        enable = event.IsChecked()
        self.split_textCtrl.Enable(enable)
        event.Skip()

    def onSplitHelpButtonClick(self, event):
        """
        Parameter hint.
        """
        self.showHelpPopupWin(self.split_hlp_bpButton,
                              info_text=SPLIT_PARAMETER_HELP)
        event.Skip()

    def setRequest(self, request):
        """
        Set request to OLAP server as struct.

        :param request: Request dictionary.
        :return: True/False.
        """
        if request is None:
            request = dict()

        if 'url' in request:
            self.request_textCtrl.SetValue(request['url'])

        cube_name = request.get('cube', None)
        cube = None
        if cube_name:
            cubes = self._OLAP_server.getCubes()
            cube_names = [cube.getName() for cube in cubes]
            try:
                i_cube = cube_names.index(cube_name)
                cube = cubes[i_cube]
                self.cube_choice.setSelection(i_cube)
            except ValueError:
                log_func.error(u'Cube <%s> not found in %s' % (cube_name, str(cube_names)))

        method_name = request.get('method', None)
        if method_name:
            try:
                i_method = OLAP_METHODS.index(method_name)
            except ValueError:
                log_func.error(u'Method <%s> not found in %s' % (method_name, str(OLAP_METHODS)))
                i_method = 0
            self.method_choice.setSelection(i_method)

        dimension_name = request.get('dimension', None)
        if dimension_name and cube:
            dimensions = cube.getDimensions()
            dimension_names = [dimension.getName() for dimension in dimensions]
            try:
                i_dimension = dimension_names.index(dimension_name) + 1
            except ValueError:
                log_func.error(u'Dimension <%s> not found in %s' % (dimension_name, str(dimension_names)))
                i_dimension = 0
            self.dimension_choice.setSelection(i_dimension)

        self.cut_checkBox.SetValue('cut' in request)
        self.cut_textCtrl.Enable('cut' in request)
        self.cut_textCtrl.SetValue(request.get('cut', u''))

        self.drilldown_checkBox.SetValue('drilldown' in request)
        self.drilldown_textCtrl.Enable('drilldown' in request)
        self.drilldown_textCtrl.SetValue(request.get('drilldown', u''))

        self.aggregates_checkBox.SetValue('aggregates' in request)
        self.aggregates_textCtrl.Enable('aggregates' in request)
        self.aggregates_textCtrl.SetValue(request.get('aggregates', u''))

        self.measures_checkBox.SetValue('measures' in request)
        self.measures_textCtrl.Enable('measures' in request)
        self.measures_textCtrl.SetValue(request.get('measures', u''))

        self.page_checkBox.SetValue('page' in request)
        self.page_textCtrl.Enable('page' in request)
        self.page_textCtrl.SetValue(request.get('page', u''))

        self.pagesize_checkBox.SetValue('pagesize' in request)
        self.pagesize_textCtrl.Enable('pagesize' in request)
        self.pagesize_textCtrl.SetValue(request.get('pagesize', u''))

        self.order_checkBox.SetValue('order' in request)
        self.order_textCtrl.Enable('order' in request)
        self.order_textCtrl.SetValue(request.get('order', u''))

        self.split_checkBox.SetValue('split' in request)
        self.split_textCtrl.Enable('split' in request)
        self.split_textCtrl.SetValue(request.get('split', u''))

        return True

    def getRequest(self):
        """
        Get request to OLAP server as struct.

        :return: Request struct as dictionary.
        """
        request = dict()
        i_cube = self.cube_choice.GetSelection()
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        cube_name = cube.getName() if cube else None
        if cube_name:
            request['cube'] = cube_name

        i_func = self.method_choice.GetSelection()
        method_name = OLAP_METHODS[i_func] if i_func >= 0 else None
        if method_name:
            request['method'] = method_name

        i_dimension = self.dimension_choice.GetSelection() - 1
        dimension = (cube.getDimensions()[i_dimension] if cube else None) if i_dimension >= 0 else None
        if dimension:
            request['dimension'] = dimension.getName()

        # Set parameters
        if self.cut_checkBox.GetValue():
            param = self.cut_textCtrl.GetValue().strip()
            if param:
                request['cut'] = param
        if self.drilldown_checkBox.GetValue():
            param = self.drilldown_textCtrl.GetValue().strip()
            if param:
                request['drilldown'] = param
        if self.aggregates_checkBox.GetValue():
            param = self.aggregates_textCtrl.GetValue().strip()
            if param:
                request['aggregates'] = param
        if self.measures_checkBox.GetValue():
            param = self.measures_textCtrl.GetValue().strip()
            if param:
                request['measures'] = param
        if self.page_checkBox.GetValue():
            param = self.page_textCtrl.GetValue().strip()
            if param:
                request['page'] = param
        if self.pagesize_checkBox.GetValue():
            param = self.pagesize_textCtrl.GetValue().strip()
            if param:
                request['pagesize'] = param
        if self.order_checkBox.GetValue():
            param = self.order_textCtrl.GetValue().strip()
            if param:
                request['order'] = param
        if self.split_checkBox.GetValue():
            param = self.split_textCtrl.GetValue().strip()
            if param:
                request['split'] = param
        return request

    def getRequestURL(self, request=None):
        """
        Get request URL to OLAP server.

        :return: Request struct as dictionary.
        """
        if request is None:
            request = self.getRequest()

        try:
            full_request_url = self._OLAP_server.getRequestURL(request)
            return full_request_url
        except:
            log_func.fatal(u'Error get request URL to OLAP server')

        return u''


def showCubesOLAPServerRequestPanel(parent=None, title=u''):
    """
    Open Cubes OLAP server request panel page.

    :param parent: Parent window.
    :param title: Title.
    """
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        panel = iqCubesOLAPSrvRequestPanel(parent=parent)
        # panel.init()
        parent.addPage(panel, title)
    except:
        log_func.fatal(u'Error open Cubes OLAP server request panel page')
