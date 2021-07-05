#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OLAP cube pivot table request panel.
"""

from . import cubes_olap_srv_request_panel_proto

from ...util import log_func
from ...util import lang_func
from ...util import global_func
from ...dialog import dlg_func

from ...engine.wx.dlg import info_window
from ...engine.wx import listctrl_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

CUT_HELP = u'Slice cell specification, for example: date:2004,1|category:2|entity:12345'


class iqCubesPivotTabRequestPanel(cubes_olap_srv_request_panel_proto.iqCubesPivotTabRequestPanelProto,
                                  listctrl_manager.iqListCtrlManager):
    """
    OLAP cube pivot table request panel.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        cubes_olap_srv_request_panel_proto.iqCubesPivotTabRequestPanelProto.__init__(self, *args, **kwargs)

        # OLAP server
        self._OLAP_server = None

        self._help_popup_win = None
        self.init()

    def setOLAPServer(self, olap_server, refresh=False):
        """
        Set OLAP server.

        :param olap_server: OLAP server.
        :param refresh: Refresh controls?
        """
        self._OLAP_server = olap_server

        if self._OLAP_server and refresh:
            self.refreshCubeChoice()

    def refreshCubeChoice(self, i_cube=0):
        """
        Refresh cube list.

        :param i_cube: Cube index.
        """
        if self._OLAP_server:
            choices = [cube.getLabel() for cube in self._OLAP_server.getCubes()]
            self.cube_choice.Clear()
            self.cube_choice.AppendItems(choices)
            if choices:
                self.cube_choice.SetSelection(i_cube)
                self.refreshDimensionChoice(i_cube)
                self.refreshAggregateChoice(i_cube)

    def refreshDimensionChoice(self, i_cube):
        """
        Refresh the list of dimensions based on the selected cube.

        :param i_cube: Cube index.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [u''] + [dimension.getLabel() for dimension in cube.getDimensions()]

            self.row_dimension_choice.Clear()
            self.row_dimension_choice.AppendItems(choices[1:])
            self.row_dimension_choice.SetSelection(0)

            self.col_dimension_choice.Clear()
            self.col_dimension_choice.AppendItems(choices)
            self.col_dimension_choice.SetSelection(0)

            self.cut_dimension_choice.Clear()
            self.cut_dimension_choice.AppendItems(choices)
            self.cut_dimension_choice.SetSelection(0)

    def refreshAggregateChoice(self, i_cube):
        """
        Refresh aggregate list.

        :param i_cube: Cube index.
        """
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        if cube:
            choices = [aggregate.getLabel() for aggregate in cube.getAggregates()]

            self.aggregate_checkList.Clear()
            self.aggregate_checkList.AppendItems(choices)
            self.checkListCtrlAllItems(listctrl=self.aggregate_checkList)

    def init(self):
        """
        Init panel.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images.
        """
        pass

    def initControls(self):
        """
        Init controls.
        """
        self.setListCtrlColumns(listctrl=self.cut_listCtrl,
                                cols=(dict(label=_(u'Dimension'), width=250),
                                      dict(label=_(u'Name'), width=150),
                                      dict(label=_(u'Value'), width=300)))

    def showHelpPopupWin(self, button, info_text):
        """
        Show/Hide help popup window.

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

    def onHelpCutButtonClick(self, event):
        """
        Help button handler for slice.
        """
        self.showHelpPopupWin(self.cut_help_bpButton,
                              info_text=CUT_HELP)
        event.Skip()

    def _parseDrilldown(self, drilldown):
        """
        Parser of representation of a part of a query of dimensions by rows and columns.

        :param drilldown: Drilldown request part.
        :return: Tuple:
            (Row dimension name, Row dimension level name,
            Column dimension name, Column dimension level name)
        """
        row_drilldown_dimension = None
        row_drilldown_level = None
        col_drilldown_dimension = None
        col_drilldown_level = None

        if drilldown and '|' in drilldown:
            drilldown_list = drilldown.split('|')
            drilldown_row, drilldown_col = drilldown_list[0], drilldown_list[1]
            if ':' in drilldown_row:
                row_drilldown_dimension, row_drilldown_level = drilldown_row.split(':')
            else:
                row_drilldown_dimension = drilldown_row
            if ':' in drilldown_col:
                col_drilldown_dimension, col_drilldown_level = drilldown_col.split(':')
            else:
                col_drilldown_dimension = drilldown_col

        elif drilldown and '|' not in drilldown:
            drilldown_row = drilldown
            if ':' in drilldown_row:
                row_drilldown_dimension, row_drilldown_level = drilldown_row.split(':')
            else:
                row_drilldown_dimension = drilldown_row
        return row_drilldown_dimension, row_drilldown_level, col_drilldown_dimension, col_drilldown_level

    def setRequest(self, request):
        """
        Set OLAP server request as struct.

        :param request: OLAP server request struct params.
        :return: True/False.
        """
        try:
            return self._setRequest(request=request)
        except:
            log_func.fatal(u'Error set OLAP server request')
        return False

    def _setRequest(self, request):
        """
        Set OLAP server request as struct.

        :param request: OLAP server request struct params.
        :return: True/False.
        """
        if request is None:
            request = dict()

        cube_name = request.get('cube', None)
        cubes = self._OLAP_server.getCubes()
        cube = None
        if cube_name:
            cube_names = [cube.getName() for cube in cubes]
            try:
                i_cube = cube_names.index(cube_name)
                cube = cubes[i_cube]
                self.refreshCubeChoice(i_cube=i_cube)
            except ValueError:
                log_func.error(u'Cube <%s> not found in %s' % (cube_name, str(cube_names)))

        if cube is None and cubes:
            log_func.warning(u'Cube not defined. Default selected first')
            cube = cubes[0]
            self.refreshCubeChoice(i_cube=0)
        elif cube is None and not cubes:
            log_func.warning(u'Not define cubes in OLAP server')
            return False

        # Row and column dimensions
        drilldown = request.get('drilldown', u'')
        row_drilldown_dimension, row_drilldown_level, col_drilldown_dimension, col_drilldown_level = self._parseDrilldown(drilldown=drilldown)

        if row_drilldown_dimension:
            i_dimension = [dimension.getName() for dimension in cube.getDimensions()].index(row_drilldown_dimension)
            self.row_dimension_choice.SetSelection(i_dimension)
            if row_drilldown_level:
                dimension = cube.getDimensions()[i_dimension]
                choices = [level.getLabel() for level in dimension.getLevels()]
                self.row_level_choice.SetItems([u''] + choices)
                level_names = [level.getName() for level in dimension.getLevels()]
                i_level = level_names.index(row_drilldown_level)
                self.row_level_choice.SetSelection(i_level + 1)
            else:
                self.row_dimension_choice.SetSelection(0)
                self.row_level_choice.SetItems([u''])
                self.row_level_choice.SetSelection(0)
        else:
            self.row_dimension_choice.SetSelection(0)
            self.row_level_choice.SetItems([u''])
            self.row_level_choice.SetSelection(0)

        if col_drilldown_dimension:
            i_dimension = [dimension.getName() for dimension in cube.getDimensions()].index(col_drilldown_dimension)
            self.col_dimension_choice.SetSelection(i_dimension + 1)
            if col_drilldown_level:
                dimension = cube.getDimensions()[i_dimension]
                choices = [level.getLabel() for level in dimension.getLevels()]
                self.col_level_choice.SetItems([u''] + choices)
                level_names = [level.getName() for level in dimension.getLevels()]
                i_level = level_names.index(col_drilldown_level)
                self.col_level_choice.SetSelection(i_level + 1)
            else:
                self.col_dimension_choice.SetSelection(0)
                self.col_level_choice.SetItems([u''])
                self.col_level_choice.SetSelection(0)
        else:
            self.col_dimension_choice.SetSelection(0)
            self.col_level_choice.SetItems([u''])
            self.col_level_choice.SetSelection(0)

        # Aggregates
        aggregates = request.get('aggregates', u'')
        if aggregates.strip():
            aggregates = aggregates.strip().split('|')
            all_aggregate_names = [aggregate.getName() for aggregate in cube.getAggregates()]
            checked_list = [all_aggregate_names.index(aggregate) for aggregate in aggregates]
            self.aggregate_checkList.SetCheckedItems(checked_list)

        # Cuts
        cut = request.get('cut', u'')
        if cut.strip():
            cut = cut.strip().split('|')
            cut_list = [sub_cut.split(':') for sub_cut in cut]
            rows = tuple([(cube.findDimension(cut[0]).getLabel(), cut[0], cut[1]) for cut in cut_list])
            self.setListCtrlRows(listctrl=self.cut_listCtrl, rows=rows)

        return True

    def getRequest(self):
        """
        Get OLAP server request as struct.

        :return: Dictionary of query parameters to the OLAP server.
             The dictionary is filled in according to the selected
             panel control parameters.
        """
        try:
            return self._getRequest()
        except:
            log_func.fatal(u'Error get OLAP server request')
        return dict()

    def _getRequest(self):
        """
        Get OLAP server request as struct.

        :return: Dictionary of query parameters to the OLAP server.
             The dictionary is filled in according to the selected
             panel control parameters.
        """
        request = dict()
        i_cube = self.cube_choice.GetSelection()
        cube = self._OLAP_server.getCubes()[i_cube] if i_cube >= 0 else None
        cube_name = cube.getName() if cube else None
        if cube_name:
            request['cube'] = cube_name

        request['method'] = 'aggregate'

        # Fill pivot table rows and columns
        row_param = u''
        i_dimension = self.row_dimension_choice.GetSelection()
        if i_dimension >= 0:
            dimension_name = [dimension.getName() for dimension in cube.getDimensions()][i_dimension]
            dimension = cube.findDimension(dimension_name)
            i_level = self.row_level_choice.GetSelection()
            if i_level > 0:
                level_name = [level.getName() for level in dimension.getLevels()][i_level - 1]
                row_param = u'%s:%s' % (dimension_name, level_name)
            else:
                row_param = dimension_name
        col_param = u''
        i_dimension = self.col_dimension_choice.GetSelection()
        if i_dimension > 0:
            dimension_name = [dimension.getName() for dimension in cube.getDimensions()][i_dimension - 1]
            dimension = cube.findDimension(dimension_name)
            i_level = self.col_level_choice.GetSelection()
            if i_level > 0:
                level_name = [level.getName() for level in dimension.getLevels()][i_level - 1]
                col_param = u'%s:%s' % (dimension_name, level_name)
            else:
                col_param = dimension_name

        if row_param and not col_param:
            request['drilldown'] = row_param
        elif row_param and col_param:
            request['drilldown'] = u'%s|%s' % (row_param, col_param)

        # Aggregates
        aggregate_checked = self.getListCtrlCheckedItems(listctrl=self.aggregate_checkList,
                                                         check_selected=True)
        aggregates = cube.getAggregates()
        request['aggregates'] = u'|'.join([aggregates[check_idx].getName() for check_idx in aggregate_checked])

        # Cuts
        rows = self.getListCtrlRows(listctrl=self.cut_listCtrl)
        request['cut'] = u'|'.join([u'%s:%s' % (row[1], row[2]) for row in rows])

        log_func.debug(u'Request data: %s' % str(request))
        return request

    def getRequestURL(self, request=None):
        """
        Get the URL of the request to the OLAP server by its structural description.

        :return: Dictionary of query parameters to the OLAP server.
             If not defined, then it is taken from controls.
        """
        if request is None:
            request = self.getRequest()

        try:
            full_request_url = self._OLAP_server.getRequestURL(request)
            return full_request_url
        except:
            log_func.fatal(u'Error get OLAP server request URL')

        return u''

    def onRowDimensionChoice(self, event):
        """
        Dimension change handler in pivot table row settings.
        """
        i_dimension = event.GetSelection()
        i_cube = self.cube_choice.GetSelection()
        if i_dimension >= 0:
            cube = self._OLAP_server.getCubes()[i_cube]
            dimension = cube.getDimensions()[i_dimension]
            choices = [u''] + [level.getLabel() for level in dimension.getLevels()]

            self.row_level_choice.Clear()
            self.row_level_choice.AppendItems(choices)
            self.row_level_choice.SetSelection(0)
        else:
            self.row_level_choice.Clear()

        event.Skip()

    def onColDimensionChoice(self, event):
        """
        Dimension change handler in pivot table column settings.
        """
        i_dimension = event.GetSelection()
        i_cube = self.cube_choice.GetSelection()
        if i_dimension > 0:
            cube = self._OLAP_server.getCubes()[i_cube]
            dimension = cube.getDimensions()[i_dimension - 1]
            choices = [u''] + [level.getLabel() for level in dimension.getLevels()]

            self.col_level_choice.Clear()
            self.col_level_choice.AppendItems(choices)
            self.col_level_choice.SetSelection(0)
        else:
            self.col_level_choice.Clear()

        event.Skip()

    def onAddCutToolClicked(self, event):
        """
        Handler for adding a slice to the list.
        """
        i_cube = self.cube_choice.GetSelection()
        i_dimension = self.cut_dimension_choice.GetSelection()

        if i_dimension <= 0:
            dlg_func.openWarningBox(_(u'CUT'), _(u'Cut dimension not selected'))
        else:
            value = self.cut_value_textCtrl.GetValue()
            if not value.strip():
                dlg_func.openWarningBox(_(u'CUT'), _(u'Cut value not specified'))
            else:
                cube = self._OLAP_server.getCubes()[i_cube]
                dimension = cube.getDimensions()[i_dimension - 1]
                row = (dimension.getLabel(), dimension.getName(), value)
                self.appendListCtrlRow(listctrl=self.cut_listCtrl, row=row)

                # After adding, clear the controls
                self.cut_dimension_choice.SetSelection(0)
                self.cut_value_textCtrl.SetValue(u'')

        event.Skip()

    def onDelCutToolClicked(self, event):
        """
        A handler for removing a slice from a list.
        """
        i_del_row = self.getListCtrlSelectedRowIdx(listctrl_or_event=self.cut_listCtrl)
        if i_del_row < 0:
            dlg_func.openWarningBox(_(u'CUT'), _(u'No cut selected to be removed from the list'))
        else:
            self.cut_listCtrl.DeleteItem(i_del_row)
        event.Skip()


def showCubesPivotTableRequestPanel(title=u''):
    """
    Display the pivot table query panel to OLAP server.

    :param title: Page title.
    """
    try:
        main_win = global_func.getMainWin()

        panel = iqCubesPivotTabRequestPanel(parent=main_win)
        main_win.addPage(panel, title)
    except:
        log_func.fatal(u'Error show cubes pivot table request panel')
