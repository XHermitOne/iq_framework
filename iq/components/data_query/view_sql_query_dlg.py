#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View SQL result dialog_func.
"""

import traceback
import wx
import wx.propgrid
from. import view_sql_query_dlg_proto

import iq
from iq.util import log_func
from iq.util import txtgen_func
from iq.util import global_func

from iq.engine.wx import form_manager 
from iq.engine.wx import listctrl_manager
from iq.engine.wx import toolbar_manager


__version__ = (0, 0, 0, 1)

UNIX_CR = '\n'
WIN_CR = '\r\n'

ERROR_FIELD = (u'Error', )
ERROR_COL_WIDTH = 700


class iqViewSQLQueryDialog(view_sql_query_dlg_proto.iqViewSQLQueryDialogProto,
                           form_manager.iqDialogManager,
                           listctrl_manager.iqListCtrlManager,
                           toolbar_manager.iqToolBarManager):
    """
    View SQL result dialog_func.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        view_sql_query_dlg_proto.iqViewSQLQueryDialogProto.__init__(self, *args, **kwargs)

        # SQL template
        self.sql_query = u''

        # SQL variables
        self.variables = dict()

        # Database
        self.db = None

    def setDB(self, db):
        """
        Set database.
        
        :param db: DB object.
        """
        self.db = db
        if self.db is None:
            log_func.warning(u'The database object is not installed in the SQL query results view window')
            log_func.warning(u'SQL queries will not be executed')

    def setSQLQuery(self, sql_txt):
        """
        Install SQL query for viewing.

        :param sql_txt: SQL query text.
        :return: True/False.
        """
        if not sql_txt:
            log_func.warning(u'SQL query text not defined')
            return False

        sql_txt = sql_txt.replace('\\n', UNIX_CR)

        self.sql_query = sql_txt

        if txtgen_func.isGenered(self.sql_query):
            var_names = txtgen_func.getReplaceNames(self.sql_query)
            self.variables = dict([(name, u'') for name in var_names])
            self.setVariables(self.variables)
        return True

    def setVariables(self, variables):
        """
        Set the SQl query variables for editing.

        :param variables: Variables dictionary.
        :return: True/False.
        """
        if variables is None:
            variables = self.variables

        if not isinstance(variables, dict):
            log_func.warning(u'Error SQL variables type <%s>' % type(variables))
            return False

        var_names = list(variables.keys())
        var_names.sort()

        self.var_propertyGrid.Clear()
        for var_name in var_names:
            wx_property = wx.propgrid.StringProperty(var_name, value=u'')
            self.var_propertyGrid.Append(wx_property)

    def getSQLText(self, sql_query=None, variables=None):
        """
        Get SQL query text.

        :param sql_query: SQL query template.
        :param variables: Variables dictionary.
        :return: SQL query text.
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        return txtgen_func.generate(sql_query, variables)

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

    def refreshSQLText(self, sql_query=None, variables=None):
        """
        Refresh SQL query text.

        :param sql_query: SQL query template.
        :param variables: Variables dictionary.
        :return: True/False
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        sql_text = self.getSQLText(sql_query, variables)
        if sql_text:
            self.sql_textCtrl.SetValue(sql_text)
            return True
        else:
            log_func.warning(u'Error get SQL query text')
        return False

    def refreshDataList(self, sql_query=None, variables=None):
        """
        Refresh SQL result dataset.

        :param sql_query: SQL query template.
        :param variables: Variables dictionary.
        :return: True/False
        """
        if sql_query is None:
            sql_query = self.sql_query
        if variables is None:
            variables = self.variables

        sql_text = self.getSQLText(sql_query, variables)
        if sql_text:
            dataset = self.getSQLDataset(sql_text)
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
        return False

    def getSQLDataset(self, sql_text):
        """
        Get SQL result dataset.

        :param sql_text: SQL query text.
        :return: Result dataset or traceback lines if error.
        """
        if self.db is None:
            error_txt = u'Not define DB object for SQL query'
        else:
            try:
                dataset = self.db.executeSQL(sql_text)
                return dataset
            except:
                error_txt = traceback.format_exc()
                log_func.fatal(u'Error get SQL result dataset <%s>' % sql_text)
        error_list = error_txt.split(UNIX_CR)
        return [dict(error=line) for line in error_list]

    def init(self):
        """
        Init dialog.
        """
        self.initControls()

    def initControls(self):
        """
        Init dialog form controls.
        """
        self.ctrl_toolBar.EnableTool(self.expand_tool.GetId(), False)
        self.refreshSQLText()

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
        self.refreshSQLText(variables=self.variables)
        self.refreshDataList(variables=self.variables)
        event.Skip()


def viewSQLQueryDlg(parent=None, db=None, sql_txt=None):
    """
    View SQL query result dialog.

    :param parent: Parent window.
    :param db: Database object.
    :param sql_txt: SQL query text.
    :return: True/False.
    """
    if parent is None:
        parent = global_func.getMainWin()

    try:
        dlg = iqViewSQLQueryDialog(parent)

        dlg.setDB(db)
        dlg.setSQLQuery(sql_txt)

        dlg.init()
        dlg.ShowModal()
        return True
    except:
        log_func.fatal(u'Error view SQL query result dialog')

    return False
