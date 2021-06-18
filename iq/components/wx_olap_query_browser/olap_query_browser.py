#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Browser of the results of queries to the OLAP server.
"""

import wx

from . import olap_query_browse_panel_proto

from ...util import log_func

from ...engine.wx import panel_manager
from ...engine.wx import toolbar_manager
from ...engine.wx import treectrl_manager

from ..virtual_spreadsheet import spreadsheet_view_manager

__version__ = (0, 0, 0, 1)


class iqOLAPQueryBrowserProto(olap_query_browse_panel_proto.iqOLAPQueryBrowsePanelProto,
                              panel_manager.iqPanelManager,
                              toolbar_manager.iqToolBarManager,
                              treectrl_manager.iqTreeCtrlManager):
    """
    Browser of the results of queries to the OLAP server. Prototype class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        olap_query_browse_panel_proto.iqOLAPQueryBrowsePanelProto.__init__(self, *args, **kwargs)

        # SpreadSheet structure output control manager
        self._spreadsheet_mngr = spreadsheet_view_manager.iqSpreadSheetViewManager(grid=self.spreadsheet_grid)

        # Current pivot table as pandas.DataFrame object
        self._pivot_dataframe = None
        # Current OLAP server data
        self._json_response = None

    def init(self):
        """
        Initialization.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images.
        """
        self.setToolBarLibImages(toolbar=self.ctrl_toolBar,
                                 norm_tool='fatcow/table_columns_insert_right',
                                 total_tool='fatcow/table_layout_grand_totals',
                                 grp_total_tool='fatcow/table_layout_subtotals')

    def initControls(self):
        """
        Init controls.
        """
        pass

    def onCollapseToolClicked(self, event):
        """
        COLLAPSE button handler.
        """
        self.collapsePanelSplitter(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        EXPAND button handler.
        """
        self.expandPanelSplitter(splitter=self.browse_splitter, toolbar=self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool, expand_tool=self.expand_tool)
        event.Skip()

    def onNormToolClicked(self, event):
        """
        Pivot table normalization tool handler.
        """
        self.viewSpreadsheet()
        event.Skip()

    def onTotalToolClicked(self, event):
        """
        A handler for calculating totals by rows.
        """
        self.viewSpreadsheet()
        event.Skip()

    def onGrpTotalToolClicked(self, event):
        """
        Handler for calculating totals for line groups.
        """
        self.viewSpreadsheet()
        event.Skip()

    def onSortToolClicked(self, event):
        """
        Data sorting handler.
        """
        self.viewSpreadsheet()
        event.Skip()

    def onReverseToolClicked(self, event):
        """
        Reverse sorting handler.
        """
        self.viewSpreadsheet()
        event.Skip()

    def refreshPivotTable(self, request_url=None, request=None):
        """
        Refresh the pivot table on demand to the OLAP server.

        :param request_url: OLAP server query URL.
            If not defined, it is taken from the currently selected item in the query tree.
        :param request: Request description structure as dictionary.
            If not defined, it is taken from the currently selected item in the query tree.
        :return: True/False.
        """
        if request is None:
            item_data = self.getTreeCtrlSelectedItemData(treectrl=self.query_treectrl)
            request = item_data.get('__request__', dict())
        if request is None:
            log_func.warning(u'Refresh pivot table. OLAP server request not defined')
            return False

        olap_server = self.query_treectrl.getOLAPServer()

        if request_url is None:
            request_url = request.get('url', None)
        # log.debug(u'URL: <%s>' % request_url)
        request_url = (olap_server.getRequestURL(request) if olap_server else None) if not request_url else request_url
        if request_url:
            log_func.debug(u'OLAP server query. URL <%s>' % request_url)
        else:
            log_func.warning(u'Refresh pivot table. OLAP server request URL not defined')
            return False

        if olap_server:
            self._json_response = olap_server.get_response(request_url)
            if self._json_response:
                if 'drilldown' in request and '|' in request['drilldown']:
                    row_dimension_url, col_dimension_url = request['drilldown'].split('|')
                    row_dimension = self._parseDimensionNames(row_dimension_url, request, olap_server=olap_server)
                    col_dimension = self._parseDimensionNames(col_dimension_url, request, olap_server=olap_server)
                    self._pivot_dataframe = olap_server.to_pivot_dataframe(self._json_response,
                                                                           row_dimension=row_dimension,
                                                                           col_dimension=col_dimension)
                else:
                    row_dimension_url = request.get('drilldown', None)
                    row_dimension = self._parseDimensionNames(row_dimension_url, request, olap_server=olap_server)
                    self._pivot_dataframe = olap_server.to_pivot_dataframe(self._json_response,
                                                                           row_dimension=row_dimension)
            return self.viewSpreadsheet(pivot_dataframe=self._pivot_dataframe,
                                        olap_server=olap_server,
                                        json_response=self._json_response)
        else:
            log_func.warning(u'OLAP server not defined in query browser')
        return False

    def isTotalPivotTable(self):
        """
        Is the calculation of grand totals in the pivot table enabled?

        :return: True/False
        """
        return self.ctrl_toolBar.GetToolState(self.total_tool.GetId())

    def isTotalGroupPivotTable(self):
        """
        Is the calculation of totals by groups in the pivot table enabled?

        :return: True/False
        """
        return self.ctrl_toolBar.GetToolState(self.grp_total_tool.GetId())

    def isSortPivotTable(self):
        """
        Pivot table row sorting enabled?

        :return: True/False
        """
        return self.ctrl_toolBar.GetToolState(self.sort_tool.GetId())

    def isReversePivotTable(self):
        """
        Reverse sorting of pivot table rows enabled?

        :return: True/False
        """
        return self.ctrl_toolBar.GetToolState(self.reverse_tool.GetId())

    def viewSpreadsheet(self, pivot_dataframe=None, olap_server=None, json_response=None):
        """
        Bring the pivot table to the display control.
        Additional changes to the pivot table can be made using
        toolbars.

        :param pivot_dataframe: Pivot table pandas.DataFrame object.
            If not specified, the current pivot table is taken.
        :param olap_server: OLAP server object.
            If not defined, it is taken from the control of the query tree.
        :param json_response: Current data received from OLAP server.
            If not defined, then internal ones are taken.
        :return: True/False.
        """
        if pivot_dataframe is None:
            # It is necessary to take a copy so as not to change the original
            pivot_dataframe = self._pivot_dataframe.copy() if self._pivot_dataframe is not None else None

        if olap_server is None:
            olap_server = self.query_treectrl.getOLAPServer()

        if json_response is None:
            json_response = self._json_response

        try:
            if pivot_dataframe is not None and json_response:
                # Additional pivot table transformations
                if self.isSortPivotTable():
                    # Sorting
                    pivot_dataframe = pivot_dataframe.sort_index(level=list(range(pivot_dataframe.index.nlevels)),
                                                                 ascending=True)
                elif self.isReversePivotTable():
                    # Reverse sorting
                    pivot_dataframe = pivot_dataframe.sort_index(level=list(range(pivot_dataframe.index.nlevels)),
                                                                 ascending=False)
                if self.isTotalGroupPivotTable():
                    # Calculation of group totals
                    pivot_dataframe = olap_server.total_group_pivot_dataframe(pivot_dataframe)
                    log_func.debug(u'Calculation of group totals :\n%s' % str(pivot_dataframe))
                if self.isTotalPivotTable():
                    # Calculation of total
                    pivot_dataframe = olap_server.total_pivot_dataframe(pivot_dataframe)
                    log_func.debug(u'Calculation of total :\n%s' % str(pivot_dataframe))

                # Convert to SpreadSheet
                spreadsheet = olap_server.pivot_to_spreadsheet(json_response, dataframe=pivot_dataframe)
                self._spreadsheet_mngr.view_spreadsheet(spreadsheet)
            else:
                # If there is nothing, then clear the grid completely
                self._spreadsheet_mngr.reCreateGrid(self._spreadsheet_mngr.getSpreadSheetGrid(), 1, 1)

            # To update the grid (For the scrollbars to appear),
            # the control of the grid panel must be rearranged
            self.grid_panel.Layout()
            return True
        except:
            log_func.error(u'Pivot table view error')
            log_func.error(str(pivot_dataframe))
            log_func.fatal()
        return False

    def _parseDimensionNames(self, dimension_url, request, olap_server=None):
        """
        List of dimension names.

        :param dimension_url: Part of the request element.
            For example store_date@ymd:month
        :param request: Request description structure as dictionary.
        :param olap_server: OLAP server.
        :return: List of dimension member names.
        """
        if olap_server is None:
            olap_server = self.query_treectrl.getOLAPServer()

        dimension_names = list()
        if '@' in dimension_url:
            # dimension@hierarchy:level
            cube_name = request.get('cube', None)
            cube = olap_server.findCube(cube_name)
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
            cube_name = request.get('cube', None)
            cube = olap_server.findCube(cube_name)
            dimension_name = dimension_url.split(':')[0]
            dimension = cube.findDimension(dimension_name)
            level_names = [level.getName() for level in dimension.getLevels()]
            hierarchy_level_name = dimension_url.split(':')[1]
            level_names = level_names[:level_names.index(hierarchy_level_name)+1] if level_names else list()
            dimension_names = tuple(['%s.%s' % (dimension_name, level_name) for level_name in level_names])
        else:
            # measure
            dimension_names = tuple([dimension_url])

        return dimension_names


def showOLAPQueryBrowser(parent=None, title=u'Analytical reports', olap_server=None):
    """
    Function of viewing the browser of the results of queries to the OLAP server.

    :param parent: Parent window.
    :param title: Page title.
    :param olap_server: OLAP server object.
    :return: True/False.
    """
    if olap_server is None:
        log_func.warning(u'OLAP server not defined')
        return False

    if parent is None:
        app = wx.GetApp()
        parent = app.GetTopWindow()

    try:
        # Run OLAP server
        olap_server.run()

        browser_panel = iqOLAPQueryBrowserProto(parent=parent)
        browser_panel.init()
        browser_panel.query_treectrl.setOLAPServer(olap_server)

        parent.addPage(browser_panel, title)

        # Stop OLAP server
        olap_server.stop()

        return True
    except:
        log_func.fatal(u'Error show OLAP server query browser')
    return False
