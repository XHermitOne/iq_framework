#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx GroupListView component.
"""

import wx
import ObjectListView

from ..wx_widget import component

from . import spc

from ...util import log_func
from ...util import exec_func

from ...engine.wx import wxcolour_func
from ... import passport

__version__ = (0, 0, 0, 1)


class iqWxGroupListView(ObjectListView.GroupListView,
                        component.iqWxWidget):
    """
    Wx group list view component.
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

        ObjectListView.GroupListView.__init__(self, parent=parent, id=wx.NewId(),
                                              style=self.getStyle(),
                                              sortable=self.getSortable(),
                                              useAlternateBackColors=True,
                                              showItemCounts=self.getShowItemsCount())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

        colour = self.getEvenRowsBackgroundColour()
        self.evenRowsBackColor = colour if colour else wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        colour = self.getOddRowsBackgroundColour()
        self.oddRowsBackColor = colour if colour else wxcolour_func.getTintColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))

        self._data_src_obj = None

        # Set columns
        self.createChildren()
        # resource = self.getResource()
        # self.setColumns(*resource['_children_'])
        columns = self.getChildren()
        self.setColumns(*columns)
        self.rowFormatter = self.rowFormatterFunction

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected, id=self.GetId())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated, id=self.GetId())

        self.SetFocus()

        self.refreshDataset()

    def getSortable(self):
        """
        Can sort?
        """
        return self.getAttribute('sortable')

    def getShowItemsCount(self):
        """
        Show group items count?
        """
        return self.getAttribute('show_items_count')

    def getEvenRowsBackgroundColour(self):
        """
        Get even rows background colour.
        """
        colour = self.getAttribute('even_rows_background_colour')
        log_func.debug(u'Even rows background colour %s' % str(colour))
        return colour

    def getOddRowsBackgroundColour(self):
        """
        Get odd rows background colour.
        """
        colour = self.getAttribute('odd_rows_background_colour')
        log_func.debug(u'Odd rows background colour %s' % str(colour))
        return colour

    def getDataSource(self):
        """
        Get data source object.
        """
        if self._data_src_obj is None:
            data_src_psp = self.getAttribute('data_src')
            if data_src_psp:
                self._data_src_obj = self.getKernel().createByPsp(psp=data_src_psp)
            else:
                log_func.warning(u'Not define data source in <%s>' % self.getName())
        return self._data_src_obj

    def setDataSource(self, data_source):
        """
        Set data source object.
        """
        self._data_src_obj = data_source

    def setColumns(self, *columns):
        """
        Create columns.

        :param columns: Column object list.
        """
        cols = list()
        auto_sort_col = None
        for column in columns:
            activate = column.isActivate()
            if not activate:
                # Skip disabled columns
                continue

            name = column.getDataName()
            label = column.getLabel()
            width = column.getWidth()
            new_col = ObjectListView.ColumnDefn(title=label,
                                                align='left',
                                                width=width,
                                                valueGetter=name,
                                                minimumWidth=40,
                                                maximumWidth=400,
                                                groupKeyGetter=self._create_getColGroupKeyFunction(column),
                                                groupKeyConverter=self._create_convertColGroupKeyFunction(column)
                                                )
            if column.isSort():
                auto_sort_col = new_col

            cols.append(new_col)
        if cols:
            self.SetColumns(cols)

            if auto_sort_col:
                self.SetSortColumn(auto_sort_col)

    def _create_getColGroupKeyFunction(self, column):
        """
        Creating a column key retrieval function.

        :param column: Column data.
        """
        if column.isAttributeValue('get_group_key'):
            def getColGroupKey(RECORD):
                """
                Get column group key.

                :param RECORD: Record dictionary.
                """
                function_body = column.getAttribute('get_group_key')
                result = exec_func.execTxtFunction(function=function_body,
                                                   context=locals())
                log_func.info(u'Get column <%s> group key. Result <%s>' % (column['name'], result))
                return result

            return getColGroupKey
        return None

    def _create_convertColGroupKeyFunction(self, column):
        """
        Creating a column group title retrieval function.

        :param column: Column data.
        """
        if column.isAttributeValue('get_group_title'):
            def convertColGroupKey(GROUP_KEY):
                """
                Convert group key to group title.

                :param GROUP_KEY: Group key.
                """
                function_body = column.getAttribute('get_group_title')
                result = exec_func.execTxtFunction(function=function_body,
                                                   context=locals())
                log_func.info(u'Get column <%s> group title. Result <%s>' % (column['name'], result))
                return result

            return convertColGroupKey
        return None

    def geDataSourcetDataset(self, data_source=None, data_src_filter=None):
        """
        Get dataset from data source object.

        :param data_source: Data source as passport or object.
        :param data_src_filter: Additional filter.
        :return: Record dictionary list.
        """
        if data_source is None:
            data_source = self.getAttribute('data_src')

        if not self._data_src_obj:
            self._data_src_obj = None
            if passport.isPassport(data_source):
                self._data_src_obj = self.getKernel().createByPsp(psp=data_source)
            else:
                self._data_src_obj = data_source
        if self._data_src_obj:
            if data_src_filter:
                self._data_src_obj.setFilter(data_src_filter)
            dataset = self._data_src_obj.getDataset()
            return dataset
        else:
            log_func.error(u'Not define data source in control <%s>' % self.getName())
        return None

    def setDataset(self, dataset=None, data_src_filter=None):
        """
        Set dataset.

        To object context for methods <conv_dataset> and <conv_record>
        save:
            DATASET - Record dictionary list.
            RECORD - Currecnt record dictionary.

        :param dataset: Record dictionary list.
        :param data_src_filter: Addition filter.
        """
        if dataset is None:
            data_src = self.getDataSource()
            if not data_src:
                function_body = self.getAttribute('get_dataset')
                dataset = exec_func.execTxtFunction(function=function_body,
                                                    context=self.getContext())
            else:
                dataset = self.geDataSourcetDataset(data_src, data_src_filter)

        if dataset is None:
            data_src_name = self._data_src_obj.getName() if self._data_src_obj else u'Not defined'
            log_func.error(u'Not define DATASET for object <%s>. DataSource: <%s>' % (self.getName,
                                                                                      data_src_name))
        else:
            if self.isAttributeValue('conv_dataset'):
                context = self.getContext()
                context['DATASET'] = dataset
                function_body = self.getAttribute('conv_dataset')
                dataset = exec_func.execTxtFunction(function=function_body,
                                                    context=context)

        if self.isAttributeValue('conv_record'):
            result_dataset = list()
            context = self.getContext()
            function_body = self.getAttribute('conv_record')
            for record in dataset:
                context['RECORD'] = record
                new_record = exec_func.execTxtFunction(function=function_body,
                                                       context=context)
                result_dataset.append(new_record)
        else:
            result_dataset = dataset

        return self.SetObjects(result_dataset)

    def refreshDataset(self, data_src_filter=None):
        """
        Refresh dataset.

        :param data_src_filter: Addition filter.
        """
        return self.setDataset(data_src_filter=data_src_filter)

    def onItemSelected(self, event):
        """
        Item select handler.
        """
        self.SetFocus()
        event.Skip()

        current_item = self.GetFocusedRow()

        context = self.getContext()
        context['self'] = self
        context['event'] = event
        context['ROW'] = current_item
        context['VALUES'] = self.GetObjectAt(current_item)

        if self.getSelectedRecord():
            function_body = self.getAttribute('on_selected')
            exec_func.execTxtFunction(function=function_body,
                                      context=context)

    def onItemActivated(self, event):
        """
        Item activate (Enter/DobleClick) handler.
        """
        current_item = self.GetFocusedRow()

        context = self.getContext()
        context['self'] = self
        context['event'] = event
        context['ROW'] = current_item
        values = self.GetObjectAt(current_item)
        context['VALUES'] = values

        function_body = self.getAttribute('on_activated')
        exec_func.execTxtFunction(function=function_body,
                                  context=context)
        event.Skip()

    def getSelectedRecord(self):
        """
        Get selected record.
        """
        return self.GetSelectedObject()

    def getSelectedObjGUID(self):
        """
        Get selected object GUID.

        :return: Selected object GUID or None if object not selected.
        """
        selected_rec = self.getSelectedRecord()
        if selected_rec:
            if isinstance(selected_rec, dict):
                return selected_rec.get('guid', None)
            else:
                return selected_rec[self.getColumnCount()]
        return None

    def getColumnCount(self):
        """
        Get column count.
        """
        return len(self.columns)

    def rowFormatterFunction(self, list_item, record):
        """
        Row formatter function.

        :param list_item: wx.ListItem item.
        :param record: Row record.
        """
        context = self.getContext()
        context['RECORD'] = record

        text_colour = None
        if self.isAttributeValue('get_row_text_colour'):
            function_body = self.getAttribute('get_row_text_colour')
            text_colour = exec_func.execTxtFunction(function=function_body,
                                                    context=context)
        bg_colour = None
        if self.isAttributeValue('get_row_background_colour'):
            function_body = self.getAttribute('get_row_background_colour')
            bg_colour = exec_func.execTxtFunction(function=function_body,
                                                  context=context)

        if text_colour and isinstance(text_colour, wx.Colour):
            list_item.SetTextColour(text_colour)
        else:
            foreground_colour = self.getForegroundColour()
            if foreground_colour:
                text_colour = wx.Colour(*foreground_colour)
                list_item.SetTextColour(text_colour)
        if bg_colour and isinstance(bg_colour, wx.Colour):
            list_item.SetBackgroundColour(bg_colour)
        else:
            background_colour = self.getBackgroundColour()
            if background_colour:
                bg_colour = wx.Colour(*background_colour)
                list_item.SetBackgroundColour(bg_colour)


COMPONENT = iqWxGroupListView
