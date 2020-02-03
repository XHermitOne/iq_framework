#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль класса - менеджера абстрактного спискового контрола WX.
"""

# Подключение библиотек
import sys
import hashlib
import wx
import wx.adv
import wx.gizmos
import wx.dataview
import wx.grid
import ic.contrib.ObjectListView

from ic.log import log
from ic.utils import strfunc
from ic.utils import wxfunc
from ic.bitmap import bmpfunc
from ic import config


__version__ = (0, 1, 7, 1)

# Размер картинок элементов дерева по умолчанию
DEFAULT_ITEM_IMAGE_WIDTH = 16
DEFAULT_ITEM_IMAGE_HEIGHT = 16
DEFAULT_ITEM_IMAGE_SIZE = (DEFAULT_ITEM_IMAGE_WIDTH, DEFAULT_ITEM_IMAGE_HEIGHT)

LIST_CTRL_IMAGE_LIST_CACHE_NAME = '__image_list_cache'


class icListCtrlManager(object):
    """
    Менеджер WX спискового контрола.
    В самом общем случае в этот класс перенесены функции работы
    со списковыми контролами из менеджера форм.
    Перенос сделан с целью рефакторинга.
    Также этот класс могут наследовать классы специализированных
    менеджеров, которые работают со списками записей/объектов.
    """

    def _get_wxDataViewListCtrl_data(self, ctrl):
        """
        Получить данные из контрола wxDataViewListCtrl.

        :param ctrl: Объект контрола.
        :return: Список словарей - строк контрола.
        """
        recordset = list()
        store = ctrl.GetStore()
        # Определить имена колонок контрола
        self_col_names = [name for name in dir(self) if
                          issubclass(getattr(self, name).__class__, wx.dataview.DataViewColumn)]
        # По именом определить объекты колонок определенные в диалоговой форме
        self_cols = [getattr(self, name) for name in self_col_names]

        for i_row in range(store.GetCount()):
            record = dict()
            for i_col in range(ctrl.GetColumnCount()):
                # Колонка контрола
                col = ctrl.GetColumn(i_col)
                # Если можно определить имя колонки, то берем имя
                # иначе берем в качестве имени индекс
                col_name = self_col_names[wxfunc.get_index_wx_object_in_list(col, self_cols)] if wxfunc.is_wx_object_in_list(col, self_cols) else i_col
                # Добавить значение колонки в запись
                record[col_name] = ctrl.GetValue(i_row, i_col)
            recordset.append(record)

        return recordset

    def _set_wxDataViewListCtrl_data(self, ctrl, records):
        """
        Установить данные в контрол wxDataViewListCtrl.

        :param ctrl: Объект контрола.
        :param records: Список словарей - записей.
            Имя колонки в записи может задаваться как именем,
            так и индексом.
        :return: True/False.
        """
        # Сначала очистить контрол от записей
        ctrl.DeleteAllItems()

        # Определить имена колонок контрола
        self_col_names = [name for name in dir(self) if
                          issubclass(getattr(self, name).__class__, wx.dataview.DataViewColumn)]
        # По именом определить объекты колонок определенные в диалоговой форме
        self_cols = [getattr(self, name) for name in self_col_names]

        for record in records:
            wx_rec = [u''] * ctrl.GetColumnCount()
            for colname, value in record.items():
                if isinstance(colname, str):
                    # Колонка задается именем
                    if colname in self_col_names:
                        i_colname = self_col_names.index(colname)
                        idx = wxfunc.get_index_wx_object_in_list(self_cols[i_colname],
                                                                 ctrl.GetColumns())
                        wx_rec[idx] = strfunc.toUnicode(value)
                    else:
                        log.warning(u'Не найдено имя колонки <%s> при заполнении wxDataViewListCtrl контрола данными' % colname)
                elif isinstance(colname, int):
                    # Колонка задается индексом
                    wx_rec[colname] = strfunc.toUnicode(value)
                else:
                    log.warning(u'Не поддерживаемый тип имени колонки <%s> при заполнении wxDataViewListCtrl контрола данными' % colname)
            ctrl.AppendItem(wx_rec)

        return True

    def refresh_DataViewListCtrl(self, ctrl, data_list=None, columns=None):
        """
        Обновить список строк контрола типа wx.dataview.DataViewListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        # Удаляем все строки
        ctrl.DeleteAllItems()
        for row in data_list:
            ctrl.AppendItem(row)

    def refresh_ListCtrl(self, ctrl, data_list=None, columns=None):
        """
        Обновить список строк контрола типа wx.ListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if data_list is None:
            data_list = list()

        if columns is not None:
            data_list = [[rec[col] for col in columns] for rec in data_list]

        self.setRows_list_ctrl(ctrl, data_list)

    def refresh_list_ctrl(self, ctrl=None, data_list=None, columns=None):
        """
        Обновить список строк контрола.

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            self.refresh_DataViewListCtrl(ctrl, data_list, columns)
        elif isinstance(ctrl, wx.ListCtrl):
            self.refresh_ListCtrl(ctrl, data_list, columns)
        else:
            log.warning(u'Обновление списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)

    def moveUpRow_DataViewListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                                   columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле типа wx.dataview.DataViewListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx > 0:
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_DataViewListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx-1]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx-1, i_col)
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx, i_col)
            ctrl.SelectRow(idx - 1)
            return True
        else:
            log.warning(u'Не выбрана перемещаемая строка списка')
        return False

    def moveUpRow_ListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                           columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле типа wx.ListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx > 0:
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx - 1][n_col]
                data_list[idx - 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx - 1]
            data_list[idx - 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_ListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx-1]):
                    ctrl.SetStringItem(idx-1, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
            ctrl.Select(idx - 1)
            return True
        else:
            log.warning(u'Не выбрана перемещаемая строка списка')
        return False

    def moveUpRow_list_ctrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                            columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку выше в контроле.

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return False

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            return self.moveUpRow_DataViewListCtrl(ctrl=ctrl, data_list=data_list,
                                                   idx=idx, columns=columns, n_col=n_col,
                                                   do_refresh=do_refresh)
        elif isinstance(ctrl, wx.ListCtrl):
            return self.moveUpRow_ListCtrl(ctrl=ctrl, data_list=data_list,
                                           idx=idx, columns=columns, n_col=n_col,
                                           do_refresh=do_refresh)
        else:
            log.warning(u'Перемещение строки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def moveDownRow_DataViewListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                                     columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле типа wx.dataview.DataViewListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_DataViewListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx, i_col)
                for i_col, value in enumerate(data_list[idx+1]):
                    ctrl.SetTextValue(value if isinstance(value, str) else str(value), idx+1, i_col)
            ctrl.SelectRow(idx + 1)
            return True
        else:
            log.warning(u'Не выбрана строка списка для перемещения')
        return False

    def moveDownRow_ListCtrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                             columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле типа wx.ListCtrl

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if idx != wx.NOT_FOUND and idx < (len(data_list) - 1):
            # Поменять номер строки если необходимо
            if n_col is not None:
                value = data_list[idx][n_col]
                data_list[idx][n_col] = data_list[idx + 1][n_col]
                data_list[idx + 1][n_col] = value
            # Поменять значения строк
            value = data_list[idx + 1]
            data_list[idx + 1] = data_list[idx]
            data_list[idx] = value

            if do_refresh:
                # Обновляем полностью контрол
                self.refresh_ListCtrl(ctrl, data_list, columns=columns)
            else:
                # Обновляем конкретные строки
                for i_col, value in enumerate(data_list[idx]):
                    ctrl.SetStringItem(idx, i_col, value if isinstance(value, str) else str(value))
                for i_col, value in enumerate(data_list[idx+1]):
                    ctrl.SetStringItem(idx+1, i_col, value if isinstance(value, str) else str(value))
            ctrl.Select(idx + 1)
            return True
        else:
            log.warning(u'Не выбрана строка списка для перемещения')
        return False

    def moveDownRow_list_ctrl(self, ctrl, data_list=None, idx=wx.NOT_FOUND,
                              columns=None, n_col=None, do_refresh=False):
        """
        Переместить строку ниже в контроле.

        :param ctrl: Объект контрола.
        :param data_list: Данные списка.
        :param idx: Индекс перемещаемой строки.
        :param columns: Список/кортеж колонок в случае если строки списка
            задаются словарями.
        :param n_col: Наименование/индекс колонки номера строки.
            Если не определено, то нет такой колонки.
        :param do_refresh: Произвести полное обновление контрола?
        :return: True - было сделано перемещение, False - перемещения не было.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для обновления')
            return False

        if isinstance(ctrl, wx.dataview.DataViewListCtrl):
            return self.moveDownRow_DataViewListCtrl(ctrl=ctrl, data_list=data_list,
                                                     idx=idx, columns=columns, n_col=n_col,
                                                     do_refresh=do_refresh)
        elif isinstance(ctrl, wx.ListCtrl):
            return self.moveDownRow_ListCtrl(ctrl=ctrl, data_list=data_list,
                                             idx=idx, columns=columns, n_col=n_col,
                                             do_refresh=do_refresh)
        else:
            log.warning(u'Перемещение строки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def appendColumn_ListCtrl(self, ctrl, label=u'', width=-1, align='LEFT'):
        """
        Добавить колонку в wx.ListCtrl.
        ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
            Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param label: Надпись колонки.
        :param width: Ширина колонки.
        :param align: Выравнивание: LEFT/RIGHT.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        try:
            i = ctrl.GetColumnCount()
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
            ctrl.InsertColumn(i, label, width=width, format=col_format)
            return True
        except:
            log.fatal(u'Ошибка добавления колонки в контрол wx.ListCtrl')
        return False

    def appendColumn_list_ctrl(self, ctrl=None, label=u'', width=-1, align='LEFT'):
        """
        Добавить колонку в контрол списка.

        :param ctrl: Объект контрола.
        :param label: Надпись колонки.
        :param width: Ширина колонки.
        :param align: Выравнивание: LEFT/RIGHT.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления колонки')
            return False

        if isinstance(ctrl, ic.contrib.ObjectListView.GroupListView):
            # Список с группировкой
            return self.appendColumn_GroupListView(ctrl=ctrl, label=label, width=width)
        elif isinstance(ctrl, wx.ListCtrl):
            # Обычный контрол списка
            return self.appendColumn_ListCtrl(ctrl=ctrl, label=label, width=width)
        else:
            log.warning(u'Добавление колонки списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setColumns_list_ctrl(self, ctrl=None, cols=()):
        """
        Установить колонки в контрол списка.

        :param ctrl: Объект контрола.
        :param cols: Список описаний колонок.
            колонка может описываться как списком
            ('Заголовок колонки', Ширина колонки, Выравнивание)
            так и словарем:
            {'label': Заголовок колонки,
            'width': Ширина колонки,
            'align': Выравнивание}
            ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
                Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления колонки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            result = True
            ctrl.ClearAll()
            for col in cols:
                if isinstance(col, dict):
                    result = result and self.appendColumn_ListCtrl(ctrl=ctrl, **col)
                elif isinstance(col, list) or isinstance(col, tuple):
                    result = result and self.appendColumn_ListCtrl(ctrl, *col)
            return result

        elif isinstance(ctrl, wx.gizmos.TreeListCtrl):
            col_count = ctrl.GetColumnCount()
            if col_count:
                for i_col in range(col_count-1, -1, -1):
                    ctrl.RemoveColumn(i_col)
            for i_col, col in enumerate(cols):
                if isinstance(col, dict):
                    ctrl.AddColumn(col.get('label', u''))
                    ctrl.SetColumnWidth(i_col, col.get('width', wx.COL_WIDTH_AUTOSIZE))
                elif isinstance(col, list) or isinstance(col, tuple):
                    ctrl.AddColumn(col[0])
                    ctrl.SetColumnWidth(i_col, col[1])
                else:
                    log.warning(u'Не поддерживаемый тип данных колонки')
            # Назначить первую колонку главной
            ctrl.SetMainColumn(0)
            return True
        elif isinstance(ctrl, wx.grid.Grid):
            col_count = ctrl.GetNumberCols()
            cols_len = len(cols)
            if col_count < cols_len:
                # Добавить не достающие колонки
                ctrl.AppendCols(cols_len - col_count)
            elif col_count > cols_len:
                # Удалить лишние колонки
                ctrl.DeleteCols(cols_len, cols_len - col_count)
            for i_col, col in enumerate(cols):
                label = col.get('label', u'')
                width = col.get('width', wx.COL_WIDTH_AUTOSIZE)
                # align = col.get('align', None)
                ctrl.SetColLabelValue(i_col, label)
                ctrl.SetColSize(i_col, width)
                # if align:
                #     ctrl.SetColLabelAlignment()
            return True
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            result = True
            for i_col, col in enumerate(cols):
                if isinstance(col, dict):
                    label = col.get('label', u'')
                    width = col.get('width', 100)
                elif isinstance(col, list) or isinstance(col, tuple):
                    label = col[0]
                    width = col[1]
                else:
                    label = u''
                    width = 100
                if i_col >= ctrl.GetColumnCount():
                    ctrl.AppendTextColumn(label=label, width=width)
                else:
                    column = ctrl.GetColumn(i_col)
                    column.SetTitle(label)
                    column.SetWidth(width)
            return result
        else:
            log.warning(u'Добавление колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setColumnsAutoSize_list_ctrl(self, ctrl=None):
        """
        Установить авторазмер колонок контрола списка.
        ВНИМАНИЕ! На старых ОС (...-16.04) wx.LIST_AUTOSIZE_USEHEADER не работает!!!
            Поэтому для автоширины используем везде wx.LIST_AUTOSIZE.

        :param ctrl: Объект контрола.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки авторазмеров списка')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            # Обновить размер колонок
            for i in range(ctrl.GetColumnCount()):
                ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            return True
        else:
            log.warning(u'Установление авторазмера колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setColumnLabel(self, ctrl=None, n_column=0, label=u''):
        """
        Установить надпись колонки.

        :param ctrl: Объект контрола списка (wx.ListCtrl и т.п.).
        :param n_column: Идекс колонки.
        :param label: Надпись колонки.
        :return: True/False.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки надписи колонки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            if 0 <= n_column < ctrl.GetColumnCount():
                column = ctrl.GetColumn(n_column)
                column.SetText(label)
                ctrl.SetColumn(n_column, column)
                return True
            else:
                log.warning(u'Не корректный индекс колонки [%s] контрола списка <%s>' % (n_column, str(ctrl)))
        else:
            log.warning(u'Не поддерживаемы тип контрола <%s> в функции установки надписи колонки' % ctrl.__class__.__name__)
        return False

    def appendRow_ListCtrl(self, ctrl, row=(),
                           evenBackgroundColour=wxfunc.DEFAULT_COLOUR, oddBackgroundColour=wxfunc.DEFAULT_COLOUR,
                           auto_select=False):
        """
        Добавить строку в контрол wx.ListCtrl.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param row: Список строки по полям.
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :param auto_select: Автоматически выбрать добавленную строку?
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if not isinstance(row, (list, tuple)):
            log.warning(u'Не корректный тип списка строки <%s> объекта wx.ListCtrl' % type(row))
            return False
        try:
            row_idx = -1
            # Ограничить список количеством колонок
            row = row[:ctrl.GetColumnCount()]
            for i, value in enumerate(row):
                if value is None:
                    value = u''
                elif isinstance(value, (int, float)):
                    value = str(value)
                # elif isinstance(value, str):
                #    value = unicode(value, config.DEFAULT_ENCODING)
                elif isinstance(value, str):
                    pass
                else:
                    value = str(value)

                if i == 0:
                    # row_idx = ctrl.InsertStringItem(sys.maxsize, value)
                    row_idx = ctrl.InsertItem(sys.maxsize, value)
                else:
                    # ctrl.SetStringItem(row_idx, idx, value)
                    ctrl.SetItem(row_idx, i, value)

            if row_idx != -1:
                if evenBackgroundColour and not (row_idx & 1):
                    # Добавляемая строка четная?
                    colour = self.defaultEvenRowsBGColour() if wxfunc.isDefaultColour(evenBackgroundColour) else evenBackgroundColour
                    # log.debug(u'Установка цвета фона четной строки %s' % str(colour))
                    ctrl.SetItemBackgroundColour(row_idx, colour)
                elif oddBackgroundColour and (row_idx & 1):
                    # Добавляемая строка не четная?
                    colour = self.defaultOddRowsBGColour() if wxfunc.isDefaultColour(oddBackgroundColour) else oddBackgroundColour
                    # log.debug(u'Установка цвета фона не четной строки %s' % str(colour))
                    ctrl.SetItemBackgroundColour(row_idx, colour)

                if auto_select:
                    # Автоматически выбрать добавленную строку?
                    ctrl.Select(row_idx)
            return True
        except:
            log.fatal(u'Ошибка добавления строки %s в контрол wx.ListCtrl' % str(row))
        return False

    def appendRow_GroupListView(self, ctrl, row=(),
                                evenBackgroundColour=wxfunc.DEFAULT_COLOUR, oddBackgroundColour=wxfunc.DEFAULT_COLOUR,
                                auto_select=False):
        """
        Добавить строку в контрол wx.ListCtrl.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param row: Список строки по полям.
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :param auto_select: Автоматически выбрать добавленную строку?
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if not isinstance(row, (list, tuple)):
            log.warning(u'Не корректный тип списка строки <%s> объекта GroupListView' % type(row))
            return False
        try:
            # colour = self.defaultEvenRowsBGColour() if wxfunc.isDefaultColour(evenBackgroundColour) else evenBackgroundColour
            # if ctrl.evenRowsBackColour != colour:
            #     ctrl.evenRowsBackColour = colour
            # colour = self.defaultOddRowsBGColour() if wxfunc.isDefaultColour(oddBackgroundColour) else oddBackgroundColour
            # if ctrl.oddRowsBackColour != colour:
            #     ctrl.oddRowsBackColour = colour

            # Ограничить список количеством колонок
            row = row[:ctrl.GetColumnCount()]
            # Исключаем колонку указателя свертывания/развертывания группы------------------------V
            row_dict = dict([(column.valueGetter, row[i]) for i, column in enumerate(ctrl.columns[1:])])
            # log.debug(u'Добавляемая запись %s' % str(row_dict))
            ctrl.AddObject(row_dict)
            if auto_select and ctrl.lastGetObjectIndex:
                ctrl.Select(ctrl.lastGetObjectIndex)
            return True
        except:
            log.fatal(u'Ошибка добавления строки %s в контрол GroupListView' % str(row))
        return False

    def appendRow_list_ctrl(self, ctrl=None, row=(),
                            evenBackgroundColour=wxfunc.DEFAULT_COLOUR, oddBackgroundColour=wxfunc.DEFAULT_COLOUR,
                            auto_select=False):
        """
        Добавить строку в контрол списка.

        :param ctrl: Объект контрола.
        :param row: Список строки по полям.
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :param auto_select: Автоматически выбрать добавленную строку?
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления строки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            return self.appendRow_ListCtrl(ctrl=ctrl, row=row,
                                           evenBackgroundColour=evenBackgroundColour,
                                           oddBackgroundColour=oddBackgroundColour,
                                           auto_select=auto_select)
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            ctrl.AppendItem(row)
            return True
        elif isinstance(ctrl, wx.grid.Grid):
            ctrl.AppendRows(1)

            colour = None
            # Определяем цвет фона линий
            row_idx = ctrl.GetNumberRows() - 1
            if row_idx != -1:
                if evenBackgroundColour and not (row_idx & 1):
                    # Добавляемая строка четная?
                    colour = self.defaultEvenRowsBGColour() if wxfunc.isDefaultColour(evenBackgroundColour) else evenBackgroundColour
                elif oddBackgroundColour and (row_idx & 1):
                    # Добавляемая строка не четная?
                    colour = self.defaultOddRowsBGColour() if wxfunc.isDefaultColour(oddBackgroundColour) else oddBackgroundColour
            # Заполняем строку
            for i_col, cell in enumerate(row):
                if cell is not None:
                    ctrl.SetCellValue(row_idx, i_col, str(cell))
                    if colour:
                        # Если цвет фона линии определен, то устанавливаем
                        ctrl.SetCellBackgroundColour(row=row_idx, col=i_col, colour=colour)
            return True
        else:
            log.warning(u'Добавление колонок списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def removeRow_list_ctrl(self, ctrl=None, item=None):
        """
        Удалить строку из контрола списка.

        :param ctrl: Объект контрола.
        :param item: Индекс удаляемой строки.
            Если не определено, то берется текущая выбранная строка.
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для удаления строки')
            return False

        if isinstance(ctrl, wx.ListCtrl):
            if item is None:
                item = self.getItemSelectedIdx(ctrl)
            if 0 <= item < ctrl.GetItemCount():
                ctrl.DeleteItem(item=item)
                return True
            else:
                log.warning(u'Не корректный индекс [%d] удаляемой строки контрола списка' % item)
        else:
            log.warning(u'Удаление строк списка контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRow_list_ctrl(self, ctrl=None, row_idx=-1, row=(),
                         evenBackgroundColour=wxfunc.DEFAULT_COLOUR, oddBackgroundColour=wxfunc.DEFAULT_COLOUR,
                         doSavePos=False):
        """
        Установить строку контрола списка.

        :param ctrl: Объект контрола.
        :param row_idx: Индекс строки. Если -1, то строка не устанавливается.
        :param row: Cтрока.
            Строка представляет собой список/кортеж:
            (Значение 1, Значение 2, ..., Значение N),
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :param doSavePos: Сохранять позицию курсора?
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для установки строки')
            return False
        if row_idx == -1:
            log.warning(u'Не указан индекс устанавливаемой строки')
            return False
        if not isinstance(row, list) and not isinstance(row, tuple):
            log.warning(u'Не корректный тип данных строки <%s>' % row.__class__.__name__)
            return False

        if isinstance(ctrl, wx.ListCtrl):
            row_count = ctrl.GetItemCount()
            if 0 > row_idx > row_count:
                log.warning(u'Не корректный индекс <%d> контрола <%s>' % (row_idx, ctrl.__class__.__name__))
                return False
            cursor_pos = None
            if doSavePos:
                cursor_pos = ctrl.GetFirstSelected()

            for i, item in enumerate(row):
                item_str = strfunc.toUnicode(item, config.DEFAULT_ENCODING)
                # ctrl.SetStringItem(row_idx, idx, item_str)
                ctrl.SetItem(row_idx, i, item_str)
                if evenBackgroundColour and not (row_idx & 1):
                    # Четная строка?
                    colour = self.defaultEvenRowsBGColour() if wxfunc.isDefaultColour(evenBackgroundColour) else evenBackgroundColour
                    # log.debug(u'Устанавливаемый цвет фона четной строки %s' % str(colour))
                    ctrl.SetItemBackgroundColour(row_idx, colour)
                elif oddBackgroundColour and (row_idx & 1):
                    # Не четная строка?
                    colour = self.defaultOddRowsBGColour() if wxfunc.isDefaultColour(oddBackgroundColour) else oddBackgroundColour
                    # log.debug(u'Устанавливаемый цвет фона не четной строки %s' % str(colour))
                    ctrl.SetItemBackgroundColour(row_idx, colour)
            if cursor_pos not in (None, -1) and cursor_pos < row_count:
                ctrl.Select(cursor_pos)
            return True
        else:
            log.warning(u'Установка строки контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def setRows_list_ctrl(self, ctrl=None, rows=(),
                          evenBackgroundColour=wxfunc.DEFAULT_COLOUR, oddBackgroundColour=wxfunc.DEFAULT_COLOUR,
                          doSavePos=False):
        """
        Установить строки в контрол списка.

        :param ctrl: Объект контрола.
        :param rows: Список строк.
            Строка представляет собой список:
            [
            (Значение 1, Значение 2, ..., Значение N), ...
            ]
        :param evenBackgroundColour: Цвет фона четных строк.
        :param oddBackgroundColour: Цвет фона нечетных строк.
        :param doSavePos: Сохранять позицию курсора?
        :return: True - все прошло нормально / False - какая-то ошибка.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол для добавления строк')
            return False

        result = True
        cursor_pos = None

        if isinstance(ctrl, ic.contrib.ObjectListView.GroupListView):
            if doSavePos:
                cursor_pos = ctrl.GetFocusedRow()
            # Исключаем колонку указателя свертывания/развертывания группы--------------------------V
            dict_rows = [dict([(column.valueGetter, row[i]) for i, column in enumerate(ctrl.columns[1:])]) for row in rows]
            ctrl.SetObjects(dict_rows)
            if cursor_pos not in (None, -1):
                ctrl.Select(cursor_pos)
                ctrl.Focus(cursor_pos)
            return result

        elif isinstance(ctrl, wx.ListCtrl):
            if doSavePos:
                cursor_pos = ctrl.GetFirstSelected()
            ctrl.DeleteAllItems()
            for row in rows:
                if isinstance(row, list) or isinstance(row, tuple):
                    result = result and self.appendRow_ListCtrl(ctrl=ctrl, row=row,
                                                                evenBackgroundColour=evenBackgroundColour,
                                                                oddBackgroundColour=oddBackgroundColour)
            if cursor_pos not in (None, -1):
                try:
                    len_rows = len(rows)
                    if cursor_pos < len_rows:
                        ctrl.Select(cursor_pos)
                        # Использую для прокрутки скролинга до выбранного элемента
                        ctrl.Focus(cursor_pos)
                    elif len_rows:
                        ctrl.Select(len_rows - 1)
                        # Использую для прокрутки скролинга до выбранного элемента
                        ctrl.Focus(len_rows - 1)
                except:
                    log.fatal(u'Ошибка восставления выбора элемента списка')
            return result
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            if doSavePos:
                cursor_pos = ctrl.GetSelection()
            ctrl.DeleteAllItems()
            for row in rows:
                if isinstance(row, list) or isinstance(row, tuple):
                    try:
                        ctrl.AppendItem(row)
                        result = result and True
                    except:
                        log.fatal(u'Ошибка доавления строки %s в контрол <%s>' % (str(row), ctrl.__class__.__name__))
                        result = False
            if cursor_pos not in (None, -1):
                try:
                    len_rows = len(rows)
                    if cursor_pos < len_rows:
                        ctrl.SelectRow(cursor_pos)
                    elif len_rows:
                        ctrl.SelectRow(len_rows - 1)
                except:
                    log.fatal(u'Ошибка восставления выбора элемента списка')
            return result
        else:
            log.warning(u'Добавление колонок контрола типа <%s> не поддерживается' % ctrl.__class__.__name__)
        return False

    def getRows_list_ctrl(self, ctrl=None):
        """
        Получить список строк в виде списка кортежей.

        :param ctrl: Объект контрола списка.
        :return: Список строк.
            Строка представляет собой список:
            [
            (Значение 1, Значение 2, ..., Значение N), ...
            ]
        """
        rows = list()
        if ctrl is None:
            log.warning(u'Не определен контрол для получения списка строк')
            return rows

        if isinstance(ctrl, wx.ListCtrl):
            for i_row in range(ctrl.GetItemCount()):
                row = [ctrl.GetItemText(i_row, col=i_col) for i_col in range(ctrl.GetColumnCount())]
                rows.append(row)
        elif isinstance(ctrl, wx.dataview.DataViewListCtrl):
            for i_row in range(ctrl.GetItemCount()):
                row = [ctrl.GetValue(i_row, col=i_col) for i_col in range(ctrl.GetColumnCount())]
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
            item = self.getItemSelectedIdx(obj=ctrl)

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

    def getItemSelectedIdx(self, obj):
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
                ctrl.Select(self.getItemSelectedIdx(ctrl), 0)
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
                ctrl.SetSelection(self.getItemSelectedIdx(ctrl), 0)
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
                i_row = self.getItemSelectedIdx(ctrl)
            ctrl.CheckItem(i_row, check=check)
            return True
        elif isinstance(ctrl, wx.CheckListBox):
            if i_row < 0:
                i_row = self.getItemSelectedIdx(ctrl)
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
                selected = self.getItemSelectedIdx(ctrl)
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
                selected = self.getItemSelectedIdx(ctrl)
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

    def getListCtrlImageList(self, ctrl=None, image_width=DEFAULT_ITEM_IMAGE_WIDTH,
                             image_height=DEFAULT_ITEM_IMAGE_HEIGHT):
        """
        Получить список картинок элементов контрола дерева wx.ListCtrl.

        :param ctrl: Объект контрола wx.ListCtrl.
        :param image_width: Ширина картинки.
        :param image_height: Высота картинки.
        :return: Объект списка образов.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.ListCtrl')
            return None

        image_list = ctrl.GetImageList(wx.IMAGE_LIST_SMALL)
        if not image_list:
            image_list = wx.ImageList(image_width, image_height)
            # ВНИМАНИЕ! Здесь необходимо вставить хотя бы пустой Bitmap
            # Иначе при заполнении контрол валиться
            empty_dx = image_list.Add(bmpfunc.createEmptyBitmap(image_width, image_height))
            ctrl.SetImageList(image_list, wx.IMAGE_LIST_SMALL)
        return image_list

    def getListCtrlImageListCache(self, ctrl=None):
        """
        Кеш списка образов.

        :param ctrl: Объект контрола wx.ListCtrl.
        """
        if ctrl is None:
            log.warning(u'Не определен контрол wx.ListCtrl')
            return None

        if not hasattr(ctrl, LIST_CTRL_IMAGE_LIST_CACHE_NAME):
            setattr(ctrl, LIST_CTRL_IMAGE_LIST_CACHE_NAME, dict())
        return getattr(ctrl, LIST_CTRL_IMAGE_LIST_CACHE_NAME)

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
            item_idx = self.getItemSelectedIdx(ctrl)
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

    def getImageIndex_list_ctrl(self, ctrl=None, image=None, auto_add=True):
        """
        Поиск образа в списке образов wx.ListCtrl.

        :param ctrl: Объект контрола списка.
        :param image: Объект образа.
        :param auto_add: Автоматически добавить в список, если отсутствует?
        :return: Индекс образа или -1 если образ не найден.
        """
        if image is None:
            return -1

        if isinstance(image, wx.Bitmap):
            img = image.ConvertToImage()
            img_id = hashlib.md5(img.GetData()).hexdigest()
        elif isinstance(image, wx.Image):
            img_id = hashlib.md5(image.GetData()).hexdigest()
        else:
            log.warning(u'Не обрабатываемый тип образа <%s>' % image.__class__.__name__)
            return -1

        # Сначала проверяем в кеше
        img_cache = self.getListCtrlImageListCache(ctrl=ctrl)

        img_idx = -1
        if img_id in img_cache:
            img_idx = img_cache[img_id]
        else:
            if auto_add:
                image_list = self.getListCtrlImageList(ctrl=ctrl)
                img_idx = image_list.Add(image)
                # Запоминаем в кеше
                img_cache[img_id] = img_idx
        return img_idx

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
