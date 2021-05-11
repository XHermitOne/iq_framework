#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View transform dataset dialog
"""

import wx
import wx.propgrid

from . import view_transform_datasource_dlg_proto

import iq
from iq.util import log_func
from iq.util import global_func
from iq.util import txtgen_func
from iq.dialog import dlg_func

from iq.engine.wx import form_manager
from iq.engine.wx import listctrl_manager
from iq.engine.wx import toolbar_manager

from .. import data_query

__version__ = (0, 0, 0, 1)

ERROR_FIELD = (u'Error', )
ERROR_COL_WIDTH = 700


class iqViewTransformDataSourceDialog(view_transform_datasource_dlg_proto.iqViewTransformDataSourceDialogProto,
                                      form_manager.iqDialogManager,
                                      listctrl_manager.iqListCtrlManager,
                                      toolbar_manager.iqToolBarManager):
    """
    View transform dataset dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        view_transform_datasource_dlg_proto.iqViewTransformDataSourceDialogProto.__init__(self, *args, **kwargs)

        # Testing component
        self.testing_component = None

        # Data retrieval context variables
        self.variables = dict()

    def init(self):
        """
        Init dialog.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images method.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)

    def setTestingComponent(self, component):
        """
        Set testing component.

        :param component: Testing component.
        :return:
        """
        self.testing_component = component
        log_func.info(u'Testing component <%s>' % (self.testing_component.getName() if self.testing_component is not None else None))

        tab_datasource = component.getTabDataSource() if component else None
        if tab_datasource is None:
            msg = u'The table datasource object is not set in the transform datasource results view window\nResult is empty'
            log_func.warning(msg)
            dlg_func.openWarningBox(title=u'WARNING', prompt_text=msg)
        elif isinstance(tab_datasource, data_query.COMPONENT):
            sql_query = tab_datasource.getSQLText()
            if txtgen_func.isGenered(sql_query):
                var_names = txtgen_func.getReplaceNames(sql_query)
                self.variables = dict([(name, u'') for name in var_names])
                self.setVariables(self.variables)
        else:
            log_func.warning(u'Type error table datasource for testing <%s>' % tab_datasource.__class__.__name__)

    def setVariables(self, variables):
        """
        Set the transform datasource variables for editing.

        :param variables: Variables dictionary.
        :return: True/False.
        """
        if variables is None:
            variables = self.variables

        if not isinstance(variables, dict):
            log_func.warning(u'Error variables type <%s>' % type(variables))
            return False

        var_names = list(variables.keys())
        var_names.sort()

        self.var_propertyGrid.Clear()
        for var_name in var_names:
            wx_property = wx.propgrid.StringProperty(var_name, value=u'')
            self.var_propertyGrid.Append(wx_property)

    def getVariables(self):
        """
        Get variables dictionary.

        :return: Variables dictionary.
        """
        variables = dict()
        for property_name in self.variables.keys():
            value = self.var_propertyGrid.GetPropertyValueAsString(property_name)
            variables[property_name] = value
        return variables

    def refreshDataList(self, variables=None):
        """
        Refresh transform result dataset.

        :param variables: Variables dictionary.
        :return: True/False
        """
        if variables is None:
            variables = self.variables

        try:
            dataframe = self.testing_component.transform(**variables)
            # log_func.debug(u'Transformed DataFrame:')
            # log_func.debug(str(dataframe))
            dataset = self.testing_component.exportData(dataframe)
            if dataset:
                # Columns
                fields = dataset[0].keys()
                if fields == ERROR_FIELD:
                    cols = [dict(label=field_name, width=ERROR_COL_WIDTH) for field_name in fields]
                else:
                    cols = [dict(label=field_name, width=-1) for field_name in fields]
                # Rows
                row_count = len(dataset)

                # Limit records
                limit = self.limit_spinCtrl.GetValue()
                if limit:
                    # log_func.debug(u'Limit records <%s>' % limit)
                    dataset = dataset[:limit]

                rows = [[rec.get(field, u'') for field in fields] for rec in dataset]
                self.setListCtrlColumns(listctrl=self.records_listCtrl, cols=cols)
                self.setListCtrlRows(listctrl=self.records_listCtrl, rows=rows)
                if rows:
                    # Autosize columnns
                    self.setListCtrlColumnsAutoSize(listctrl=self.records_listCtrl)

                self.count_textCtrl.SetValue(str(row_count))
                return True
            else:
                log_func.warning(u'Empty dataset')
        except:
            log_func.fatal(u'Error refresh transform datasource result list')
        return False

    def onCollapseToolClicked(self, event):
        """
        Colapse panel handler.
        """
        self.collapsePanelSplitter(splitter=self.panel_splitter,
                                   toolbar=self.ctrl_toolBar,
                                   collapse_tool=self.collapse_tool,
                                   expand_tool=self.expand_tool)
        event.Skip()

    def onExpandToolClicked(self, event):
        """
        Expand panel handler.
        """
        self.expandPanelSplitter(splitter=self.panel_splitter,
                                 toolbar=self.ctrl_toolBar,
                                 collapse_tool=self.collapse_tool,
                                 expand_tool=self.expand_tool)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        OK button click handler.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRefreshToolClicked(self, event):
        """
        Refresh SQL result dataset handler.
        """
        self.variables = self.getVariables()
        # self.refreshSQLText(variables=self.variables)
        self.refreshDataList(variables=self.variables)
        event.Skip()


def viewTransforDataSourceDlg(parent=None, component=None):
    """
    View transform datasource result dialog.

    :param parent: Parent window.
    :param component: Testing component.
    :return: True/False.
    """
    if component is None:
        log_func.warning(u'Type error testing component')
        return False

    if parent is None:
        parent = global_func.getMainWin()

    dlg = None
    try:
        dlg = iqViewTransformDataSourceDialog(parent)

        dlg.setTestingComponent(component)

        dlg.init()
        dlg.ShowModal()

        dlg.Destroy()
        return True
    except:
        log_func.fatal(u'Error view transform datasource result dialog')

    if dlg:
        dlg.Destroy()
    return False

