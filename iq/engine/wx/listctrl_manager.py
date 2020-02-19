#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ListCtrl manager.
"""

import sys
import wx

from ...util import log_func

from . import wxcolour_func
from . import base_manager

__version__ = (0, 0, 0, 1)


class iqListCtrlManager(base_manager.iqBaseManager):
    """
    ListCtrl manager.
    """
    def refreshListCtrl(self, listctrl, data_list=None, columns=None):
        """
        Refresh rows wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param columns: Column list.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        self.setListCtrlRows(listctrl, data_list)

    def moveUpListCtrlRow(self, listctrl, data_list=None, idx=wx.NOT_FOUND,
                          columns=None, n_col=None, do_refresh=False):
        """
        Move up row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param idx: Moving row index.
        :param columns: Column list.
        :param n_col: Number column name/index.
        :param do_refresh: Make a complete update control?
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if idx != wx.NOT_FOUND and idx > 0:

            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value

            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                self.refreshListCtrl(listctrl, data_list, columns=columns)
            else:
                for i_col, value in enumerate(data_list[idx-1]):
                    listctrl.SetStringItem(idx - 1, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx]):
                    listctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
            listctrl.Select(idx - 1)
            return True
        else:
            log_func.warning(u'Not select moving row')
        return False

    def moveDownListCtrlRow(self, listctrl, data_list=None, idx=wx.NOT_FOUND,
                            columns=None, n_col=None, do_refresh=False):
        """
        Move down row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param data_list: Data list.
        :param idx: Moving row index.
        :param columns: Column list.
        :param n_col: Number column name/index.
        :param do_refresh: Make a complete update control?
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value

            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                self.refreshListCtrl(listctrl, data_list, columns=columns)
            else:
                for i_col, value in enumerate(data_list[idx]):
                    listctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx+1]):
                    listctrl.SetStringItem(idx + 1, i_col, value if isinstance(value, str) else str(value))
            listctrl.Select(idx + 1)
            return True
        else:
            log_func.warning(u'Not select moving row')
        return False

    def appendListCtrlColumn(self, listctrl, label=u'', width=-1, align='LEFT'):
        """
        Append column in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param label: Column label string.
        :param width: Column width.
        :param align: Column text align LEFT/RIGHT/CENTRE.
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        try:
            i = listctrl.GetColumnCount()
            if width <= 0:
                width = wx.LIST_AUTOSIZE

            col_align = str(align).strip().upper()
            if col_align == 'RIGHT':
                col_format = wx.LIST_FORMAT_RIGHT
            elif col_align == 'CENTRE':
                col_format = wx.LIST_FORMAT_CENTRE
            elif col_align == 'CENTER':
                col_format = wx.LIST_FORMAT_CENTER
            else:
                col_format = wx.LIST_FORMAT_LEFT
            listctrl.InsertColumn(i, label, width=width, format=col_format)
            return True
        except:
            log_func.fatal(u'Append column in wx.ListCtrl object error')
        return False

    def setListCtrlColumns(self, listctrl=None, cols=()):
        """
        Set columns in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param cols: List of column definitions.
            As tuple ('Column title', width, align)
            or as dictionary:
            {'label': 'Column title',
            'width': Column width,
            'align': Column align}
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        result = True
        listctrl.ClearAll()
        for col in cols:
            if isinstance(col, dict):
                result = result and self.appendListCtrlColumn(listctrl=listctrl, **col)
            elif isinstance(col, (list, tuple)):
                result = result and self.appendListCtrlColumn(listctrl, *col)
        return result

    def setListCtrlColumnsAutoSize(self, listctrl=None):
        """
        Set auto-size columns in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        for i in range(listctrl.GetColumnCount()):
            listctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        return True

    def setListCtrlColumnLabel(self, listctrl=None, column_idx=0, label=u''):
        """
        Set column label.

        :param listctrl: wx.ListCtrl object.
        :param column_idx: Column index.
        :param label: Column label.
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if 0 <= column_idx < listctrl.GetColumnCount():
            column = listctrl.GetColumn(column_idx)
            column.SetText(label)
            listctrl.SetColumn(column_idx, column)
            return True
        else:
            log_func.error(u'Not valid column index [%s] ListCtrl object <%s>' % (column_idx, str(listctrl)))
        return False

    def appendListCtrlRow(self, listctrl, row=(),
                          even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                          odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                          auto_select=False):
        """
        Append row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param row: List of rows by fields.
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param auto_select: Automatically select the added row?
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if not isinstance(row, (list, tuple)):
            log_func.error(u'Row typeerror <%s> in wx.ListCtrl object' % type(row))
            return False

        try:
            row_idx = -1

            row = row[:listctrl.GetColumnCount()]
            for i, value in enumerate(row):
                if value is None:
                    value = u''
                elif isinstance(value, (int, float)):
                    value = str(value)
                elif isinstance(value, str):
                    pass
                else:
                    value = str(value)

                if i == 0:
                    row_idx = listctrl.InsertItem(sys.maxsize, value)
                else:
                    listctrl.SetItem(row_idx, i, value)

            if row_idx != -1:
                if even_background_colour and not (row_idx & 1):

                    colour = self.defaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                    listctrl.SetItemBackgroundColour(row_idx, colour)
                elif odd_background_colour and (row_idx & 1):
                    colour = self.defaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                    listctrl.SetItemBackgroundColour(row_idx, colour)

                if auto_select:
                    listctrl.Select(row_idx)
            return True
        except:
            log_func.fatal(u'Append row %s  error in wx.ListCtrl object' % str(row))
        return False

    def delListCtrlRow(self, listctrl=None, row_idx=None):
        """
        Delete row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param row_idx: Row index.
            If not defined, the current selected row is taken.
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if row_idx is None:
            row_idx = self.getListCtrlelectedRowIdx(listctrl)
        if 0 <= row_idx < listctrl.GetItemCount():
            listctrl.DeleteItem(item=row_idx)
            return True
        else:
            log_func.warning(u'Not valid row index [%d] on wx.ListCtrl object' % row_idx)
        return False

    def setListCtrlRow(self, listctrl=None, row_idx=-1, row=(),
                       even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                       odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                       keep_pos=False):
        """
        Set row in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param row_idx: Row index.
        :param row: Row as tuple.
            (value 1, value 2, ..., value N),
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        if row_idx == -1:
            log_func.error(u'The row index to be set is not specified')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log_func.error(u'Invalid row data type <%s>' % row.__class__.__name__)
            return False

        row_count = listctrl.GetItemCount()
        if 0 > row_idx > row_count:
            log_func.error(u'Not valid row index [%d] in <%s>' % (row_idx, listctrl.__class__.__name__))
            return False

        cursor_pos = None
        if keep_pos:
            cursor_pos = listctrl.GetFirstSelected()

        for i, item in enumerate(row):
            item_str = str(item)

            listctrl.SetItem(row_idx, i, item_str)
            if even_background_colour and not (row_idx & 1):
                colour = self.defaultEvenRowsBGColour() if wxcolour_func.isDefaultColour(even_background_colour) else even_background_colour
                listctrl.SetItemBackgroundColour(row_idx, colour)
            elif odd_background_colour and (row_idx & 1):
                colour = self.defaultOddRowsBGColour() if wxcolour_func.isDefaultColour(odd_background_colour) else odd_background_colour
                listctrl.SetItemBackgroundColour(row_idx, colour)
        if cursor_pos not in (None, -1) and cursor_pos < row_count:
            listctrl.Select(cursor_pos)
        return True

    def setListCtrlRows(self, listctrl=None, rows=(),
                        even_background_colour=wxcolour_func.DEFAULT_COLOUR,
                        odd_background_colour=wxcolour_func.DEFAULT_COLOUR,
                        keep_pos=False):
        """
        Set rows in wx.ListCtrl object.

        :param listctrl: wx.ListCtrl object.
        :param rows: Row list.
            [
            (value 1, value 2, ..., value N), ...
            ]
        :param even_background_colour: Even line background color.
        :param odd_background_colour: Odd line background color.
        :param keep_pos: Keep cursor position?
        :return: True/False.
        """
        assert issubclass(listctrl, wx.ListCtrl), u'ListCtrl manager type error'

        result = True
        cursor_pos = None

        if keep_pos:
            cursor_pos = listctrl.GetFirstSelected()

        listctrl.DeleteAllItems()
        for row in rows:
            if isinstance(row, list) or isinstance(row, tuple):
                result = result and self.appendListCtrlRow(listctrl=listctrl, row=row,
                                                           even_background_colour=even_background_colour,
                                                           odd_background_colour=odd_background_colour)
        if cursor_pos not in (None, -1):
            try:
                len_rows = len(rows)
                if cursor_pos < len_rows:
                    listctrl.Select(cursor_pos)
                    listctrl.Focus(cursor_pos)
                elif len_rows:
                    listctrl.Select(len_rows - 1)
                    listctrl.Focus(len_rows - 1)
            except:
                log_func.fatal(u'List item selection recovery error')
        return result

    def getListCtrlRows(self, listctrl=None):
        """
        Получить список строк в виде списка кортежей.

        :param listctrl: Объект контрола списка.
        :return: Список строк.
            Строка представляет собой список:
            [
            (Значение 1, Значение 2, ..., Значение N), ...
            ]
        """
        rows = list()
        if listctrl is None:
            log.warning(u'Не определен контрол для получения списка строк')
            return rows

        if isinstance(listctrl, wx.ListCtrl):
            for i_row in range(listctrl.GetItemCount()):
                row = [listctrl.GetItemText(i_row, col=i_col) for i_col in range(listctrl.GetColumnCount())]
                rows.append(row)
        elif isinstance(listctrl, wx.dataview.DataViewListCtrl):
            for i_row in range(listctrl.GetItemCount()):
                row = [listctrl.GetValue(i_row, col=i_col) for i_col in range(listctrl.GetColumnCount())]
                rows.append(row)
        return rows

    def getRow_list_ctrl(self, ctrl=None, item=-1):
        """
        Получить строку по индексу в виде кортежа.

        :param ctrl: Объект контрола списка.
        :param item: Индекс запрашиваемой строки.
            Если не определен, то возвращается индекс текущей строки.
        :return: Кортеж строки или None в случае ошибки.
            Строка представляет собой кортеж:
            (Значение 1, Значение 2, ..., Значение N)
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для получения списка строк')
            return None
        if 0 > item or item is None:
            item = self.getListCtrlelectedRowIdx(obj=ctrl)

        row = None
        if 0 <= item:
            if isinstance(ctrl, wx.ListCtrl):
                row = [ctrl.GetItemText(item, col=i_col) for i_col in range(ctrl.GetColumnCount())]
            elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
                row = [ctrl.GetValue(item, col=i_col) for i_col in range(ctrl.GetColumnCount())]
            else:
                log.warning(u'Не поддерживаемый тип контрола списка <%s> в функции getRow_list_ctrl' % ctrl.__class__.__name__)
        return row

    def setRowColour_list_ctrl_requirement(self, ctrl=None, rows=(),
                                           fg_colour=None, bg_colour=None, requirement=None):
        """
        Установить цвет строки в контроле списка по определенному условию.

        :param ctrl: Объект контрола.
        :param rows: Список строк.
        :param fg_colour: Цвет текста, если условие выполненно.
        :param bg_colour: Цвет фона, если условие выполненно.
        :param requirement: lambda выражение, формата:
            lambda idx, row: ...
            Которое возвращает True/False.
            Если True, то установка цвета будет сделана.
            False - строка не расцвечивается.
        :return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if requirement is None:
            log.warning(u'Не определено условие установки цвета')
            return False
        if fg_colour is None and bg_colour is None:
            log.warning(u'Не определены цвета')
            return False

        for i, row in enumerate(rows):
            colorize = requirement(i, row)
            if fg_colour and colorize:
                self.setRowForegroundColour_list_ctrl(ctrl, i, fg_colour)
            if bg_colour and colorize:
                self.setRowBackgroundColour_list_ctrl(ctrl, i, bg_colour)
        return True

    def setRowForegroundColour_list_ctrl(self, ctrl=None, i_row=0, colour=None):
        """
        Установить цвет текста строки в контроле списка.

        :param ctrl: Объект контрола.
        :param i_row: Индекс строки.
        :param colour: Цвет текста строки.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT)

        if isinstance(ctrl, ic.contrib.ObjectListView.GroupListView):
            # У списков с группировкой цвета строк устанавливаются через rowFormat
            return True
        elif isinstance(ctrl, wx.ListCtrl):
            try:
                colour = colour if not wxfunc.isDefaultColour(colour) else wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT)
                # log.debug(u'Устанавливаемый цвет текста строки %s' % str(colour))
                ctrl.SetItemTextColour(i_row, colour)
            except:
                log.warning(u'Не корректный индекс строки <%s>' % i_row)
                return False
            return True
        else:
            log.warning(u'Установление цвета строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRowBackgroundColour_list_ctrl(self, ctrl=None, i_row=0, colour=None):
        """
        Установить цвет фона строки в контроле списка.

        :param ctrl: Объект контрола.
        :param i_row: Индекс строки.
        :param colour: Цвет фона строки.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установления цвета строки')
            return False
        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION)

        if isinstance(ctrl, wx.ListCtrl):
            try:
                colour = colour if not wxfunc.isDefaultColour(colour) else wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
                # log.debug(u'Устанавливаемый цвет фона строки %s' % str(colour))
                ctrl.SetItemBackgroundColour(i_row, colour)
            except:
                log.warning(u'Не корректный индекс строки <%s>' % i_row)
                return False
            return True
        else:
            log.warning(u'Установление цвета строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def getListCtrlelectedRowIdx(self, obj):
        """
        Получить индекс выбранного элемента контрола.
        Т.к. индекс выбранного элемента может возвращать объекты разных
        типов (контролы и события) то:
        Эта функция нужна чтобы не заботиться о названии функции
        для каждого контрола/события.

        :param obj: Объект контрола или события.
        :return: Индекс выбранного элемента или -1 если ничего не выбрано.
        """
        if isinstance(obj, wx.ListEvent):
            return obj.Index
        elif isinstance(obj, ic.contrib.ObjectListView.GroupListView):
            selected_object = obj.GetSelectedObject()
            try:
                return obj.modelObjects.index(selected_object) if selected_object else -1
            except IndexError:
                return -1
        elif isinstance(obj, wx.ListCtrl):
            return obj.GetFirstSelected()
        elif isinstance(obj, wx.dataview.DataViewListCtrl):
            return obj.GetSelectedRow()
        elif isinstance(obj, wx.CheckListBox) or isinstance(obj, wx.ListBox):
            idx = obj.GetSelection()
            return -1 if idx == wx.NOT_FOUND else idx

        log.warning(u'Объект типа <%s> не поддерживается как определитель выбранного элемента контрола' % obj.__class__.__name__)
        return -1

    def selectItem_list_ctrl(self, ctrl=None, item_idx=-1,
                             is_focus=True, deselect_prev=False):
        """
        Выбрать элемент контрола списка по индексу.

        :param ctrl: Объект контрола.
        :param is_focus: Автоматически переместить фокус на элемент?
        :param deselect_prev: Произвести отмену выбора предыдущего выбранного элемента?
        :return: True - выбор прошел успешно.
        """
        if ctrl is None:
            log.warning(u'Не указан контрол списка для выбора элемента')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            if (0 > item_idx) or (item_idx >= ctrl.GetItemCount()):
                log.warning(u'Не корректный индекс <%d> контрола списка <%s>' % (item_idx, ctrl.__class__.__name__))
                return False
            if deselect_prev:
                ctrl.Select(self.getListCtrlelectedRowIdx(ctrl), 0)
            ctrl.Select(item_idx)
            if is_focus:
                ctrl.Focus(item_idx)
            return True
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            try:
                ctrl.SelectRow(item_idx)
            except:
                log.fatal(u'Ошибка индекса <%d> контрола списка <%s>' % (item_idx, ctrl.__class__.__name__))
                return False
            return True
        elif isinstance(ctrl, wx.CheckListBox) or isinstance(ctrl, wx.ListBox):
            if (0 > item_idx) or (item_idx >= ctrl.GetCount()):
                log.warning(u'Не корректный индекс <%d> контрола списка <%s>' % (item_idx, ctrl.__class__.__name__))
                return False
            if deselect_prev:
                ctrl.SetSelection(self.getListCtrlelectedRowIdx(ctrl), 0)
            ctrl.SetSelection(item_idx)
            return True
        else:
            log.warning(u'Объект типа <%s> не поддерживается для выбора элемента контрола' % ctrl.__class__.__name__)
        return False

    def getItemCount(self, obj):
        """
        Получить количество элементов контрола.
        Т.к.  количество элементов контрола может возвращать объекты разных
        типов, то:
        Эта функция нужна чтобы не заботиться о названии функции
        для каждого контрола.

        :param obj: Объект контрола списка элементов.
        :return: Количество элементов контрола списка.
        """
        if isinstance(obj, wx.ListCtrl):
            return obj.GetItemCount()
        elif isinstance(obj, wx.dataview.DataViewListCtrl):
            log.warning(u'ВНИМАНИЕ! В этой версии wxPython не реализована функция получения количества элементов для контрола <%s>' % obj.__class__.__name__)
            return 0
        elif isinstance(obj, wx.CheckListBox) or isinstance(obj, wx.ListBox):
            return obj.GetCount()

        log.warning(u'Объект типа <%s> не поддерживается как определитель количества элементов контрола' % obj.__class__.__name__)
        return 0

    def getLastItemIdx(self, obj):
        """
        Индекс последнего элемента списка.

        :param obj: Объект контрола списка элементов.
        :return: Индекс последнего элемента контрола списка или -1 если
            в списке нет элементов.
        """
        item_count = self.getItemCount(obj)
        return item_count - 1

    def checkAllItems_list_ctrl(self, ctrl, check=True):
        """
        Установить галки всех элементов контрола списка.

        :param check: Вкл./выкл.
        :return: True/False.
        """
        return self.checkItems_list_ctrl(ctrl, check=check)

    def checkItems_list_ctrl(self, ctrl, check=True, n_begin=-1, n_end=-1):
        """
        Установить галки элементов контрола списка.

        :param ctrl: Объект контрола.
        :param check: Вкл./выкл.
        :param n_begin: Номер первого обрабатываемого элемента.
            Если не определен, то берется самый первый элемент.
        :param n_end: Номер последнего обрабатываемого элемента.
        :return: True/False.
        """
        if isinstance(ctrl, wx.ListCtrl):
            if n_begin < 0:
                n_begin = 0
            if n_end < 0:
                n_end = ctrl.GetItemCount() - 1
            for i in range(n_begin, n_end + 1):
                ctrl.CheckItem(i, check=check)
            return True
        elif isinstance(ctrl, wx.CheckListBox):
            if n_begin < 0:
                n_begin = 0
            if n_end < 0:
                n_end = ctrl.GetCount() - 1
            for i in range(n_begin, n_end + 1):
                ctrl.Check(i, check=check)
            return True

        log.warning(u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
        return False

    def checkItem_list_ctrl(self, ctrl, check=True, i_row=-1):
        """
        Установить галки элементов контрола списка.

        :param ctrl: Объект контрола.
        :param check: Вкл./выкл.
        :param i_row: Индекс обрабатываемого элемента.
            Если не определен, то берется текущий выбранный элемент.
        :return: True/False.
        """
        if isinstance(ctrl, wx.ListCtrl):
            if i_row < 0:
                i_row = self.getListCtrlelectedRowIdx(ctrl)
            ctrl.CheckItem(i_row, check=check)
            return True
        elif isinstance(ctrl, wx.CheckListBox):
            if i_row < 0:
                i_row = self.getListCtrlelectedRowIdx(ctrl)
            ctrl.Check(i_row, check=check)
            return True

        log.warning(u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
        return False

    def checkItems_requirement(self, ctrl=None, rows=(), requirement=None,
                               bSet=False):
        """
        Наити и пометить строку списка по определенному условию.

        :param ctrl: Объект контрола.
        :param rows: Список строк.
        :param requirement: lambda выражение, формата:
            lambda idx, row: ...
            Которое возвращает True/False.
            Если True, то считаем что строка удовлетворяет условию.
            False - строка не удовлетворяет.
        :param bSet: Произвести установку меток всех элементов
            в соответствии с условием.
        :return: Список индексов помеченных строк.
        """
        check_list = list()

        if not rows:
            # Нет строк. И не надо обрабатывать
            return check_list

        for i, row in enumerate(rows):
            checked = requirement(i, row)
            if checked:
                check_list.append(i)
            if bSet:
                self.checkItems_list_ctrl(ctrl=ctrl, check=checked,
                                          n_begin=i, n_end=i)
            elif not bSet and checked:
                self.checkItem_list_ctrl(ctrl=ctrl, check=True, i_row=i)
        return check_list

    def getCheckedItems_list_ctrl(self, ctrl, check_selected=False):
        """
        Получить список индексов помеченных/отмеченных элементов контрола списка.

        :param ctrl: Объект контрола списка элементов.
        :param check_selected: Считать выделенный элемент списка как помеченный?
            Если да, то выделенный элемент считается помеченным только когда
            ни один другой элемент не помечен.
        :return: Список индексов помеченных элементов контрола списка.
            Либо None в случае ошибки.
        """
        try:
            if isinstance(ctrl, wx.ListCtrl):
                indexes = [i for i in range(ctrl.GetItemCount()) if ctrl.IsChecked(i)]
            elif isinstance(ctrl, wx.CheckListBox):
                indexes = [i for i in range(ctrl.GetCount()) if ctrl.IsChecked(i)]
            else:
                log.warning(
                    u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
                return None

            if not indexes and check_selected:
                selected = self.getListCtrlelectedRowIdx(ctrl)
                if selected >= 0:
                    indexes = [selected]
            return indexes
        except:
            log.fatal(u'Ошибка определения индексов отмеченных элементов контрола <%s>' % ctrl.__class__.__name__)
        return None

    def getCheckedItemRecords_list_ctrl(self, ctrl, records, check_selected=False):
        """
        Получить список помеченных/отмеченных записей элементов контрола списка.

        :param ctrl: Объект контрола списка элементов.
        :param records: Список записей.
        :param check_selected: Считать выделенный элемент списка как помеченный?
            Если да, то выделенный элемент считается помеченным только когда
            ни один другой элемент не помечен.
        :return: Список записей помеченных элементов контрола списка.
            Либо None в случае ошибки.
        """
        try:
            if isinstance(ctrl, wx.ListCtrl):
                check_records = [records[i] for i in range(ctrl.GetItemCount()) if ctrl.IsChecked(i)]
            elif isinstance(ctrl, wx.CheckListBox):
                check_records = [records[i] for i in range(ctrl.GetCount()) if ctrl.IsChecked(i)]
            else:
                log.warning(
                    u'Объект типа <%s> не поддерживается вкл./выкл. элментов контрола' % ctrl.__class__.__name__)
                return None

            if not check_records and check_selected:
                selected = self.getListCtrlelectedRowIdx(ctrl)
                if selected >= 0:
                    check_records = [self.records[selected]]
            return check_records
        except:
            log.fatal(u'Ошибка определения отмеченных записей контрола <%s>' % ctrl.__class__.__name__)
        return None

    def defaultEvenRowsBGColour(self):
        """
        Цвет фона четных строк по умолчанию.
        """
        colour = tuple(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))[:-1]
        return wx.Colour(*colour)

    def defaultOddRowsBGColour(self):
        """
        Цвет фона не четных строк по умолчанию.
        """
        return wxfunc.getTintColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))

    def setRowsBackgroundColour(self, ctrl, evenBackgroundColour=wxfunc.DEFAULT_COLOUR,
                                oddBackgroundColour=wxfunc.DEFAULT_COLOUR):
        """
        Просто раскрасить фон четных и не четных строк.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки цвета')
            return False

        for row_idx in range(ctrl.GetItemCount()):
            if evenBackgroundColour and not (row_idx & 1):
                # Добавляемая строка четная?
                colour = self.defaultEvenRowsBGColour() if wxfunc.isDefaultColour(evenBackgroundColour) else evenBackgroundColour
                log.debug(u'Установка цвета фона строки %s' % str(colour))
                ctrl.SetItemBackgroundColour(row_idx, colour)
            elif oddBackgroundColour and (row_idx & 1):
                # Добавляемая строка не четная?
                colour = self.defaultOddRowsBGColour() if wxfunc.isDefaultColour(oddBackgroundColour) else oddBackgroundColour
                log.debug(u'Установка цвета фона строки %s' % str(colour))
                ctrl.SetItemBackgroundColour(row_idx, colour)

    def findRowIdx_requirement(self, ctrl=None, rows=(), requirement=None, auto_select=False):
        """
        Наити индекс строки списка по определенному условию.

        :param ctrl: Объект контрола.
        :param rows: Список строк.
        :param requirement: lambda выражение, формата:
            lambda idx, row: ...
            Которое возвращает True/False.
            Если True, то считаем что строка удовлетворяет условию.
            False - строка не удовлетворяет.
        :param auto_select: Произвести автоматическое выделение строки в контроле
        :return: индекс найденной строки или None если строка не найдена.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для поиска строки')
            return False
        if requirement is None:
            log.warning(u'Не определено условие для поиска строки')
            return False

        for i, row in enumerate(rows):
            is_found = requirement(i, row)
            if is_found:
                if auto_select:
                    self.selectItem_list_ctrl(ctrl, item_idx=i, is_focus=True, deselect_prev=True)
                return i
        return True

    def selectRow_requirement(self, ctrl=None, rows=(), requirement=None):
        """
        Наити и выделить индекс строки списка по определенному условию.

        :param ctrl: Объект контрола.
        :param rows: Список строк.
        :param requirement: lambda выражение, формата:
            lambda idx, row: ...
            Которое возвращает True/False.
            Если True, то считаем что строка удовлетворяет условию.
            False - строка не удовлетворяет.
        :return: индекс найденной строки или None если строка не найдена.
        """
        return self.findRowIdx_requirement(ctrl=ctrl, rows=rows, requirement=requirement)

    def setItemImage_list_ctrl(self, ctrl=None, item=None, image=None):
        """
        Установить картинку элемента списка.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param item: Элемент списка.
            Элемент списка может задаваться как индексом так и объектом wx.ListItem.
            Если None, то имеется текущий выбранный элемент.
        :param image: Объект картинки wx.Bitmap.
            Если не определен, то картинка удаляется.
        :return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.ListCtrl')
            return None

        if item is None:
            item_idx = self.getListCtrlelectedRowIdx(ctrl)
            item = ctrl.GetItem(item_idx)
        elif isinstance(item, wx.ListItem):
            item_idx = item.GetId()
        elif isinstance(item, int):
            item_idx = item
            item = ctrl.GetItem(item_idx)

        if image is None:
            ctrl.SetItemImage(item, None)
        else:
            if item_idx >= 0:
                try:
                    img_idx = self.getImageIndex_list_ctrl(ctrl=ctrl, image=image, auto_add=True)
                    # log.debug(u'Индекс образа в списке [%d]' % img_idx)
                    ctrl.SetItemImage(item_idx, img_idx, selImage=wx.TreeItemIcon_Normal)
                except:
                    log.fatal(u'Ошибка установки образа [%d] элемента списка <%s>' % (img_idx, item))
            else:
                log.warning(u'Не корректный индекс строки <%s>' % str(item_idx))
        return True

    def clear_list_ctrl(self, ctrl=None):
        """
        Очистка контрола списка.

        :param ctrl: Объект контрола списка.
        :return: True/False.
        """
        try:
            if isinstance(ctrl, wx.ListCtrl):
                ctrl.DeleteAllItems()
                return True
            elif isinstance(ctrl, wx.CheckListBox):
                ctrl.Clear()
                return True
            elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
                ctrl.DeleteAllItems()
                return True
            else:
                log.warning(u'Не поддерживается очистка контрола списка для <%s>' % self.__class__.__name__)
        except:
            log.fatal(u'Ошибка очистки контрола списка')
        return False
