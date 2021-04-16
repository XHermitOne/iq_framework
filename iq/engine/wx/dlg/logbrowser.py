#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Browser of the program message log.

The program message log is saved in a file  *.log
Log format:
2016-11-18 08:22:11 INFO Message
    ^         ^      ^      ^
    |         |      |      +-- Message text
    |         |      +--------- Message type
    |         +---------------- Log time
    +-------------------------- Log date
The message text can be multi-line. Mostly for critical errors.
All programs should output messages in this format.
"""

import datetime
import os
import os.path
import wx
from . import log_browser_proto

from ....util import logfile_func
from ....util import log_func
from ....util import global_func
from ....util import lang_func
from .. import wxdatetime_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

TIME_FMT = '%H:%M:%S'

LOG_TYPE_COLOUR_NAMES = {
                         logfile_func.INFO_LOG_TYPE: 'DARKGREEN',
                         logfile_func.WARNING_LOG_TYPE: 'GOLDENROD',
                         logfile_func.ERROR_LOG_TYPE: 'RED4',
                         logfile_func.FATAL_LOG_TYPE: 'RED3',
                         logfile_func.DEBUG_LOG_TYPE: 'BLUE4',
                         logfile_func.DEBUG_SERVICE_LOG_TYPE: 'CYAN4',
                         logfile_func.SERVICE_LOG_TYPE: 'CYAN4',
                        }

LOG_TYPE_LABELS = {
                   logfile_func.INFO_LOG_TYPE: _(u'Information'),
                   logfile_func.WARNING_LOG_TYPE: _(u'Warning'),
                   logfile_func.ERROR_LOG_TYPE: _(u'Error'),
                   logfile_func.FATAL_LOG_TYPE: _(u'Critical error'),
                   logfile_func.DEBUG_LOG_TYPE: _(u'Debug'),
                   logfile_func.DEBUG_SERVICE_LOG_TYPE: _(u'Debug service message'),
                   logfile_func.SERVICE_LOG_TYPE: _(u'Service message'),
                   }

LOG_TYPE_ICONS = {
                  logfile_func.INFO_LOG_TYPE: wx.ICON_INFORMATION,
                  logfile_func.WARNING_LOG_TYPE: wx.ICON_WARNING,
                  logfile_func.ERROR_LOG_TYPE: wx.ICON_ERROR,
                  logfile_func.FATAL_LOG_TYPE: wx.ICON_HAND,
                  logfile_func.DEBUG_LOG_TYPE: wx.ICON_ASTERISK,
                  logfile_func.DEBUG_SERVICE_LOG_TYPE: wx.ICON_EXCLAMATION,
                  logfile_func.SERVICE_LOG_TYPE: wx.ICON_EXCLAMATION,
                  }


class iqLogBrowserPanelManager:
    """
    Manager of work with the browser panel.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        self.filter_panel = self

        if 'filter_panel' in kwargs:
            self.filter_panel = kwargs['filter_panel']
            del kwargs['filter_panel']

        # The current list of records being processed
        self.records = list()

        # List of additional filters
        self.ext_filters = ()

    def init(self):
        """
        Init panel.
        """
        self.initControls()

    def initControls(self):
        """
        Init controls.
        """
        # Message list columns
        self.filter_panel.msg_listCtrl.InsertColumn(0, _(u'Date/Time'), width=200)
        self.filter_panel.msg_listCtrl.InsertColumn(1, _(u'Type'), width=100)
        self.filter_panel.msg_listCtrl.InsertColumn(2, _(u'Message'), width=wx.LIST_AUTOSIZE)

        self.filter_panel.start_timeControl.BindSpinButton(self.filter_panel.start_spinBtn)
        self.filter_panel.stop_timeControl.BindSpinButton(self.filter_panel.stop_spinBtn)

    def getSelectedLogTypes(self):
        """
        List of selected message types .

        :return:
        """
        result = list()

        if self.filter_panel.info_checkBox.IsChecked():
            result.append(logfile_func.INFO_LOG_TYPE)
        if self.filter_panel.warning_checkBox.IsChecked():
            result.append(logfile_func.WARNING_LOG_TYPE)
        if self.filter_panel.error_checkBox.IsChecked():
            result.append(logfile_func.ERROR_LOG_TYPE)
        if self.filter_panel.fatal_checkBox.IsChecked():
            result.append(logfile_func.FATAL_LOG_TYPE)
        if self.filter_panel.debug_checkBox.IsChecked():
            result.append(logfile_func.DEBUG_LOG_TYPE)
        if self.filter_panel.service_checkBox.IsChecked():
            result.append(logfile_func.DEBUG_SERVICE_LOG_TYPE)
            result.append(logfile_func.SERVICE_LOG_TYPE)
        return tuple(result)

    def getSelectedStartDT(self):
        """
        Selected start time.

        :return:
        """
        result = None
        if self.filter_panel.start_checkBox.IsChecked():
            wx_date = self.filter_panel.start_datePicker.GetValue()
            wx_time = self.filter_panel.start_timeControl.GetValue()
            py_date = wxdatetime_func.wxDateTime2date(wx_date)
            py_time = datetime.datetime.strptime(wx_time, TIME_FMT)
            result = py_time.replace(year=py_date.year, month=py_date.month, day=py_date.day)
        return result

    def getSelectedStopDT(self):
        """
        Selected end time.

        :return:
        """
        result = None
        if self.filter_panel.stop_checkBox.IsChecked():
            wx_date = self.filter_panel.stop_datePicker.GetValue()
            wx_time = self.filter_panel.stop_timeControl.GetValue()
            py_date = wxdatetime_func.wxDateTime2date(wx_date)
            py_time = datetime.datetime.strptime(wx_time, TIME_FMT)
            result = py_time.replace(year=py_date.year, month=py_date.month, day=py_date.day)
        return result

    def getSelectedFilters(self):
        """
        Selected additional filters.

        :return:
        """
        check_idx = [i for i in range(self.filter_panel.filter_checkList.GetCount()) if self.filter_panel.filter_checkList.IsChecked(i)]
        result = [self.ext_filters[i][1] for i in check_idx]
        return tuple(result)

    def setFilters(self, filter_logic=logfile_func.AND_FILTER_LOGIC, *ext_filters):
        """
        Set additional filters.

        :param filter_logic: Filter processing logic.
        :param ext_filters: List of additional filters:
            ((u'Filter name',
            Additional filter function/lambda),...)
            The additional filter function takes a dictionary of the entry and
            returns True / False
        :return: True/False
        """
        self.filter_panel.logic_radioBox.SetSelection(0 if filter_logic == logfile_func.AND_FILTER_LOGIC else 1)
        if ext_filters:
            self.ext_filters = ext_filters
            for ext_filter in ext_filters:
                if type(ext_filter) in (list, tuple):
                    label, filter_func = ext_filter
                    self.filter_panel.filter_checkList.Append(label)
                else:
                    log_func.warning(u'Incorrect extended filter type <%s>. Filter consist of (u\'Filer name\', Additional filter function/lambda)' % str(ext_filter))
            return True
        return False

    def setLogFilename(self, log_filename=None):
        """
        Set log file to view.

        :param log_filename: Log filename.
        :return:
        """
        if log_filename is not None and os.path.exists(log_filename):
            self.filter_panel.log_filePicker.SetPath(log_filename)

    def setDatetimeFilterRange(self, dt_start_filter=None, dt_stop_filter=None):
        """
        Set filter by time range.

        :param dt_start_filter: Start datetime of the filter by time.
        :param dt_stop_filter: End datetime filter by time.
        """
        self.filter_panel.start_checkBox.SetValue(dt_start_filter is not None)
        self.filter_panel.stop_checkBox.SetValue(dt_stop_filter is not None)
        if dt_start_filter:
            self.filter_panel.start_datePicker.Enable(dt_start_filter is not None)
            self.filter_panel.start_timeControl.Enable(dt_start_filter is not None)
            self.filter_panel.start_spinBtn.Enable(dt_start_filter is not None)
            wx_date = wxdatetime_func.date2wxDateTime(dt_start_filter)
            wx_time_str = dt_start_filter.strftime(TIME_FMT)
            self.filter_panel.start_datePicker.SetValue(wx_date)
            self.filter_panel.start_timeControl.SetValue(wx_time_str)
        if dt_stop_filter:
            self.filter_panel.stop_datePicker.Enable(dt_stop_filter is not None)
            self.filter_panel.stop_timeControl.Enable(dt_stop_filter is not None)
            self.filter_panel.stop_spinBtn.Enable(dt_stop_filter is not None)
            wx_date = wxdatetime_func.date2wxDateTime(dt_stop_filter)
            wx_time_str = dt_stop_filter.strftime(TIME_FMT)
            self.filter_panel.stop_datePicker.SetValue(wx_date)
            self.filter_panel.stop_timeControl.SetValue(wx_time_str)

    def setLogTypesFilter(self, *log_types):
        """
        Filter by message types.

        :param log_types: List of message types.
        """
        if log_types:
            for log_type in log_types:
                if log_type == logfile_func.INFO_LOG_TYPE:
                    self.filter_panel.info_checkBox.SetValue(True)
                elif log_type == logfile_func.WARNING_LOG_TYPE:
                    self.filter_panel.warning_checkBox.SetValue(True)
                elif log_type == logfile_func.ERROR_LOG_TYPE:
                    self.filter_panel.error_checkBox.SetValue(True)
                elif log_type == logfile_func.FATAL_LOG_TYPE:
                    self.filter_panel.fatal_checkBox.SetValue(True)
                elif log_type == logfile_func.DEBUG_LOG_TYPE:
                    self.filter_panel.debug_checkBox.SetValue(True)
                elif log_type in (logfile_func.SERVICE_LOG_TYPE, logfile_func.DEBUG_SERVICE_LOG_TYPE):
                    self.filter_panel.service_checkBox.SetValue(True)

    def getRecords(self, log_filename=None, log_types=None,
                   dt_start_filter=None, dt_stop_filter=None,
                   filters=None, filter_logic=None):
        """
        Get a list of messages that match the set filters.

        :param log_filename: Log filename.
        :param log_types: Log message types.
        :param dt_start_filter: Start datetime of the filter by time.
            If not specified, then the selection occurs from the beginning of the file.
        :param dt_stop_filter: End datetime filter by time.
            If not specified, then the selection occurs to the end of the file.
        :param filters: Tuple / list of additional filtering methods.
            Filtering methods are specified as lambda or functions that take
            dictionary entries, but return True - entry falls into the selection / False - does not.
        :param filter_logic: Command for processing additional filters
            AND - For a record to be included in the selection, all filters must be positively executed,
            OR - For the entry to be included in the selection, a positive execution of one filter is sufficient.
        :return: Message record list.
        """
        if log_filename is None:
            log_filename = self.filter_panel.log_filePicker.GetPath()

        if not log_filename:
            log_func.warning(u'Program message log file not defined')
            return ()

        if log_types is None:
            log_types = self.getSelectedLogTypes()

        if dt_start_filter is None:
            dt_start_filter = self.getSelectedStartDT()
        if dt_stop_filter is None:
            dt_stop_filter = self.getSelectedStopDT()

        if filters is None:
            filters = self.getSelectedFilters()

        if filter_logic is None:
            filter_logic = logfile_func.OR_FILTER_LOGIC if self.filter_panel.logic_radioBox.GetSelection() == 1 else logfile_func.AND_FILTER_LOGIC

        records = logfile_func.getRecordsLogFile(log_filename, log_types,
                                                 dt_start_filter, dt_stop_filter,
                                                 filters, filter_logic)
        return records

    def refresh(self):
        """
        Refresh the list of messages that match the set filters.

        :return: True/False
        """
        self.filter_panel.msg_listCtrl.DeleteAllItems()
        self.records = self.getRecords()
        for i, record in enumerate(self.records):
            item_idx = self.filter_panel.msg_listCtrl.InsertItem(i, record['dt'].strftime(logfile_func.DATETIME_LOG_FMT))
            self.filter_panel.msg_listCtrl.SetItem(i, 1, record.get('type', u''))
            self.filter_panel.msg_listCtrl.SetItem(i, 2, record.get('short', u''))

            colour_name = LOG_TYPE_COLOUR_NAMES.get(record['type'], None)
            colour = wx.Colour(colour_name) if colour_name else wx.BLACK
            self.filter_panel.msg_listCtrl.SetItemTextColour(i, colour)

        # Resize the column of the message text
        self.filter_panel.msg_listCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)

    def onRefreshButtonClick(self, event):
        """
        Refresh button handler.
        """
        self.refresh()
        event.Skip()

    def onStartCheckBox(self, event):
        """
        Start time on / off handler.
        """
        check = event.IsChecked()
        self.filter_panel.start_datePicker.Enable(check)
        self.filter_panel.start_timeControl.Enable(check)
        self.filter_panel.start_spinBtn.Enable(check)
        event.Skip()

    def onStopCheckBox(self, event):
        """
        End time on / off handler.
        """
        check = event.IsChecked()
        self.filter_panel.stop_datePicker.Enable(check)
        self.filter_panel.stop_timeControl.Enable(check)
        self.filter_panel.stop_spinBtn.Enable(check)
        event.Skip()

    def onMsgListItemActivated(self, event):
        """
        Handler for selecting a message from the list.
        """
        item_idx = event.GetIndex()
        try:
            record = self.records[item_idx]
        except IndexError:
            record = None
        if record and isinstance(record, dict):
            full_msg = record.get('text', record.get('short', u''))
            dt_title = _(u'Time') + ': ' + str(record.get('dt', u''))
            title = LOG_TYPE_LABELS.get(record.get('type', u''), u'') + u'. ' + dt_title
            icon = LOG_TYPE_ICONS.get(record.get('type', u''), wx.ICON_HAND)
            wx.MessageBox(full_msg, title, style=wx.OK | icon)
        else:
            log_func.warning(u'Error log message record type <%s>' % str(record))

        event.Skip()


class iqLogBrowserPanel(iqLogBrowserPanelManager,
                        log_browser_proto.iqLogBrowserPanelProto):
    """
    The program message log browser panel.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        iqLogBrowserPanelManager.__init__(self, filter_panel=self)
        log_browser_proto.iqLogBrowserPanelProto.__init__(self, *args, **kwargs)


class iqLogBrowserDlg(iqLogBrowserPanelManager,
                      log_browser_proto.iqLogBrowserDialogProto):
    """
    The program message log browser dialog box.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        log_browser_proto.iqLogBrowserDialogProto.__init__(self, *args, **kwargs)
        iqLogBrowserPanelManager.__init__(self, filter_panel=self.browser_panel)

        self.browser_panel.refresh_bpButton.Bind(wx.EVT_BUTTON, self.onRefreshButtonClick)
        self.browser_panel.start_checkBox.Bind(wx.EVT_CHECKBOX, self.onStartCheckBox)
        self.browser_panel.stop_checkBox.Bind(wx.EVT_CHECKBOX, self.onStopCheckBox)
        self.browser_panel.msg_listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onMsgListItemActivated)

    def init(self):
        """
        Init panel.
        """
        self.initControls()

    def onOkButtonClick(self, event):
        """
        Button handler <Ok>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()


def getLogBrowserPanel(parent=None, log_filename=None, log_types=None,
                       dt_start_filter=None, dt_stop_filter=None,
                       filters=None, filter_logic=None):
    """
    The function of getting the object of the panel for viewing the program message log.

    :param parent: Parent window.
        If not specified, the main window is taken.
    :param log_filename: Log filename.
    :param log_types: Log message types.
    :param dt_start_filter: Start datetime of the filter by time.
        If not specified, then the selection occurs from the beginning of the file.
    :param dt_stop_filter: End datetime filter by time.
        If not specified, then the selection occurs to the end of the file.
    :param filters: Tuple / list of additional filtering methods.
        Filtering methods are specified as lambda or functions that take
        dictionary entries, but return True - entry falls into the selection / False - does not.
    :param filter_logic: Command for processing additional filters
        AND - For a record to be included in the selection, all filters must be positively executed,
        OR - For the entry to be included in the selection, a positive execution of one filter is sufficient.
    :return: Panel object or None if error.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    if log_filename is None:
        log_filename = global_func.getLogFilename()

    panel = iqLogBrowserPanel(parent=parent)
    panel.init()
    panel.setLogFilename(log_filename)
    panel.setDatetimeFilterRange(dt_start_filter, dt_stop_filter)
    panel.setLogTypesFilter(*(log_types if log_types else ()))
    panel.setFilters(filter_logic, *(filters if filters else ()))
    panel.refresh()
    return panel


def showLogBrowserDlg(parent=None, log_filename=None, log_types=None,
                      dt_start_filter=None, dt_stop_filter=None,
                      filters=None, filter_logic=None):
    """
    Bring up the log message browser dialog box.

    :param parent: Parent window.
        If not specified, the main window is taken.
    :param log_filename: Log filename.
    :param log_types: Log message types.
    :param dt_start_filter: Start datetime of the filter by time.
        If not specified, then the selection occurs from the beginning of the file.
    :param dt_stop_filter: End datetime filter by time.
        If not specified, then the selection occurs to the end of the file.
    :param filters: Tuple / list of additional filtering methods.
        Filtering methods are specified as lambda or functions that take
        dictionary entries, but return True - entry falls into the selection / False - does not.
    :param filter_logic: Command for processing additional filters
        AND - For a record to be included in the selection, all filters must be positively executed,
        OR - For the entry to be included in the selection, a positive execution of one filter is sufficient.
    :return: True/False.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    if log_filename is None:
        log_filename = global_func.getLogFilename()

    log_func.debug(u'Log filename <%s : %s>' % (log_filename, os.path.exists(log_filename)))

    dlg = iqLogBrowserDlg(parent=parent)
    dlg.init()
    dlg.setLogFilename(log_filename)
    dlg.setDatetimeFilterRange(dt_start_filter, dt_stop_filter)
    dlg.setLogTypesFilter(*(log_types if log_types else ()))
    dlg.setFilters(filter_logic, *(filters if filters else ()))
    dlg.refresh()
    result = dlg.ShowModal()
    return result == wx.ID_OK
