#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалоговое окно выбора элементов связанных со списком записей.
"""

import wx
from . import item_selector_dialog_proto

from ic.engine import form_manager
from ic.log import log

__version__ = (0, 1, 1, 2)

# Не определенная надпись
NONE_LABEL = u'Не определено'

ON_ITEMS_KEY = '__on__'
OFF_ITEMS_KEY = '__off__'


class icItemSelectorDialog(item_selector_dialog_proto.icItemSelectorDialogProto,
                           form_manager.icFormManager):
    """
    Диалоговое окно выбора элементов связанных со списком записей.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        item_selector_dialog_proto.icItemSelectorDialogProto.__init__(self, *args, **kwargs)

        self.records = ()
        self.items = ()
        self.label = None
        self.is_default_on = False

        self.record_sort = None
        self.item_sort = None

        # Востановление связей с обработчиками событий
        self.browse_panel.record_listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onRecordListItemSelected)
        self.browse_panel.off_all_button.Bind(wx.EVT_BUTTON, self.onOffAllButtonClick)
        self.browse_panel.off_button.Bind(wx.EVT_BUTTON, self.onOffButtonClick)
        self.browse_panel.on_button.Bind(wx.EVT_BUTTON, self.onOnButtonClick)
        self.browse_panel.on_all_button.Bind(wx.EVT_BUTTON, self.onOnAllButtonClick)

    def init_record_list_ctrl(self, records=(), columns=(), record_sort=None):
        """
        Инициализировать список записей.

        :param records: Список записей. Каждая запись - словарь.
        :param columns: Список отображаемых колонок. Каждая колонка - словарь:
            {'label': Заголовок колонки,
            'width': Ширина колонки,
            'align': Выравнивание,
            'field': Поле записи для отображения в колонке}
        :param record_sort: Функция сортировки записей. Если не указана, то сортировки нет.
            Сортировка lambda функция:
                lambda record: ...
            Например:
                lambda record: record['name']
        :return: True/False.
        """
        # Сортировка
        if record_sort:
            records.sort(key=record_sort)

        # Заполнение колонок
        cols = [dict(label=col.get('label', NONE_LABEL),
                     width=col.get('width', None),
                     align=col.get('align', None)) for col in columns]
        self.setColumns_list_ctrl(ctrl=self.browse_panel.record_listCtrl,
                                  cols=cols)
        # Заполнение строк
        rows = [tuple([rec.get(col.get('field', None), NONE_LABEL) for col in columns]) for rec in records]
        self.setRows_list_ctrl(ctrl=self.browse_panel.record_listCtrl,
                               rows=rows)
        return True

    def init_items_check_list(self, on_items=(), off_items=(), label=u'', item_sort=None):
        """
        Инициализировать списки выбора элементов.

        :param on_items: Список словарей записей включенных элементов.
        :param off_items: Список словарей записей отключенных элементов.
        :param label: Поле словаря элемента для надписи отображения в списке элементов.
            Либо lambda функция для получения надписи формата:
            lambda idx, item: ..., где
            idx - индекс записи
            item - словарь записи элемента выбора.
            lambda функция должна возвращать надпись, соответствующую элементу выбора.
        :param item_sort: Функция сортировки элементов выбора. Если не указана, то сортировки нет.
            Сортировка lambda функция:
                lambda item: ...
            Например:
                lambda item: item['name']
        :return: True/False
        """
        if item_sort is None:
            item_sort = self.item_sort
        # Предварительно отсортируем если необходимо
        if item_sort:
            on_items.sort(key=item_sort)
        if item_sort:
            off_items.sort(key=item_sort)

        on_items_labels = [(label(i, item) if callable(label) else item.get(label, NONE_LABEL)) for i, item in enumerate(on_items)]
        self.browse_panel.on_checkList.Clear()
        self.browse_panel.on_checkList.Append(on_items_labels)

        off_items_labels = [(label(i, item) if callable(label) else item.get(label, NONE_LABEL)) for i, item in enumerate(off_items)]
        self.browse_panel.off_checkList.Clear()
        self.browse_panel.off_checkList.Append(off_items_labels)
        return True

    def init(self, title=u'', records=(), columns=(), items=(), label=u'', is_default_on=False,
             record_sort=None, item_sort=None):
        """
        Инициализация диалоговой формы и всех ее объектов.

        :param title: Заголовок диалогового окна.
        :param records: Список записей. Каждая запись - словарь.
        :param columns: Список отображаемых колонок. Каждая колонка - словарь:
            {'label': Заголовок колонки,
            'width': Ширина колонки,
            'align': Выравнивание,
            'field': Поле записи для отображения в колонке}
        :param items: Список записей элементов для выбора. Каждый элемент - словарь.
        :param label: Поле словаря элемента для надписи отображения в списке элементов.
            Либо lambda функция для получения надписи формата:
            lambda idx, item: ..., где
            idx - индекс записи
            item - словарь записи элемента выбора.
            lambda функция должна возвращать надпись, соответствующую элементу выбора.
        :param is_default_on: Считаются все элементы по умолчанию выбранными?
        :param record_sort: Функция сортировки записей. Если не указана, то сортировки нет.
            Сортировка lambda функция:
                lambda record: ...
            Например:
                lambda record: record['name']
        :param item_sort: Функция сортировки элементов выбора. Если не указана, то сортировки нет.
            Сортировка lambda функция:
                lambda item: ...
            Например:
                lambda item: item['name']
        :return: True/False.
        """
        # Установить заголовок диалогового окна
        self.SetTitle(title)

        self.init_ctrl()

        # Запомнить параметры выбора элементов
        self.items = items
        self.label = label
        self.is_default_on = is_default_on
        self.record_sort = record_sort
        self.item_sort = item_sort

        # Инициализация списка записей
        self.records = list(records)
        if self.record_sort:
            self.records.sort(key=self.record_sort)
        self.init_record_list_ctrl(records, columns)

    def init_ctrl(self):
        """
        Инициализация контролов.
        """
        if self.isDarkSysTheme():
            self.browse_panel.on_label_staticText.SetForegroundColour(wx.GREEN)
            self.browse_panel.off_label_staticText.SetForegroundColour(wx.RED)
            self.browse_panel.on_all_button.SetForegroundColour(wx.GREEN)
            self.browse_panel.off_all_button.SetForegroundColour(wx.RED)
            self.browse_panel.on_button.SetForegroundColour(wx.GREEN)
            self.browse_panel.off_button.SetForegroundColour(wx.RED)
            self.browse_panel.on_checkList.SetForegroundColour(wx.GREEN)
            self.browse_panel.off_checkList.SetForegroundColour(wx.RED)
        else:
            self.browse_panel.on_label_staticText.SetForegroundColour(wx.Colour('DARK GREEN'))
            self.browse_panel.off_label_staticText.SetForegroundColour(wx.Colour('FIREBRICK'))
            self.browse_panel.on_all_button.SetForegroundColour(wx.Colour('DARK GREEN'))
            self.browse_panel.off_all_button.SetForegroundColour(wx.Colour('FIREBRICK'))
            self.browse_panel.on_button.SetForegroundColour(wx.Colour('DARK GREEN'))
            self.browse_panel.off_button.SetForegroundColour(wx.Colour('FIREBRICK'))
            self.browse_panel.on_checkList.SetForegroundColour(wx.Colour('DARK GREEN'))
            self.browse_panel.off_checkList.SetForegroundColour(wx.Colour('FIREBRICK'))

    def get_records(self):
        """
        Получить измененные записи.

        :return: Список измененных записей.
        """
        return self.records

    def refreshItems(self, record_idx, record, item_sort=None):
        """
        Обновить списки выбранных элементов для записи.

        :param record_idx: Индекс записи.
        :param record: Словарь записи.
        :param item_sort: Функция сортировки элементов выбора. Если не указана, то берется ранее установленная.
            Сортировка lambda функция:
                lambda item: ...
            Например:
                lambda item: item['name']
        :return: True/Falseю
        """
        if item_sort is None:
            item_sort = self.item_sort

        try:
            on_items = record.get(ON_ITEMS_KEY, self.items if self.is_default_on else list())
            if item_sort:
                on_items.sort(key=item_sort)
            off_items = record.get(OFF_ITEMS_KEY, list() if self.is_default_on else self.items)
            if item_sort:
                off_items.sort(key=item_sort)

            self.records[record_idx][ON_ITEMS_KEY] = on_items
            self.records[record_idx][OFF_ITEMS_KEY] = off_items

            return self.init_items_check_list(on_items, off_items, self.label)
        except:
            log.fatal(u'Ошибка обновления списков выбранных элементов для записи')
        return False

    # Обработчики событий
    def onCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRecordListItemSelected(self, event):
        """
        Обработчик выбора записи.
        """
        record_idx = event.GetIndex()
        record = self.records[record_idx]
        self.refreshItems(record_idx, record)

        event.Skip()

    def onOffAllButtonClick(self, event):
        """
        Обработчик отключения всех элментов.
        """
        log.debug(u'Отключение всех элементов')
        record_idx = self.getItemSelectedIdx(self.browse_panel.record_listCtrl)
        self.records[record_idx][OFF_ITEMS_KEY] = self.records[record_idx].get(ON_ITEMS_KEY, list())
        self.records[record_idx][ON_ITEMS_KEY] = list()
        self.refreshItems(record_idx, self.records[record_idx])

        event.Skip()

    def onOffButtonClick(self, event):
        """
        Обработчик отключения выбранных элементов.
        """
        record_idx = self.getItemSelectedIdx(self.browse_panel.record_listCtrl)
        log.debug(u'Выключение <%s> элемента' % record_idx)
        record = self.records[record_idx]
        check_indexes = self.getCheckedItems_list_ctrl(self.browse_panel.on_checkList, check_selected=True)
        on_items = [item for i, item in enumerate(record.get(ON_ITEMS_KEY, list())) if i not in check_indexes]
        off_items = record.get(OFF_ITEMS_KEY, list()) + [item for i, item in enumerate(record.get(ON_ITEMS_KEY, list())) if i in check_indexes]

        record[ON_ITEMS_KEY] = on_items
        record[OFF_ITEMS_KEY] = off_items
        self.refreshItems(record_idx, record)

        event.Skip()

    def onOnButtonClick(self, event):
        """
        Обработчик включения выбранных элементов.
        """
        record_idx = self.getItemSelectedIdx(self.browse_panel.record_listCtrl)
        log.debug(u'Включение <%s> элемента' % record_idx)
        record = self.records[record_idx]
        check_indexes = self.getCheckedItems_list_ctrl(self.browse_panel.off_checkList, check_selected=True)
        off_items = [item for i, item in enumerate(record.get(OFF_ITEMS_KEY, list())) if i not in check_indexes]
        on_items = record.get(ON_ITEMS_KEY, list()) + [item for i, item in enumerate(record.get(OFF_ITEMS_KEY, list())) if i in check_indexes]

        record[ON_ITEMS_KEY] = on_items
        record[OFF_ITEMS_KEY] = off_items
        self.refreshItems(record_idx, record)

        event.Skip()

    def onOnAllButtonClick(self, event):
        """
        Обработчик включения всех элементов.
        """
        log.debug(u'Включение всех элементов')
        record_idx = self.getItemSelectedIdx(self.browse_panel.record_listCtrl)
        self.records[record_idx][ON_ITEMS_KEY] = self.records[record_idx].get(OFF_ITEMS_KEY, list())
        self.records[record_idx][OFF_ITEMS_KEY] = list()
        self.refreshItems(record_idx, self.records[record_idx])

        event.Skip()


def get_item_selector_dlg(parent=None, title=u'', records=(), columns=(), items=(), label=None, is_default_on=False,
                          record_sort=None, item_sort=None):
    """
    Вызов диалоговой формы выбора элементов связанных со списком записей.

    :param parent: Родительское окно.
    :param title: Заголовок диалогового окна.
    :param records: Список записей. Каждая запись - словарь.
    :param columns: Список отображаемых колонок. Каждая колонка - словарь:
        {'label': Заголовок колонки,
        'width': Ширина колонки,
        'align': Выравнивание,
        'field': Поле записи для отображения в колонке}
    :param items: Список записей элементов для выбора. Каждый элемент - словарь.
    :param label: Поле словаря элемента для надписи отображения в списке элементов.
        Либо lambda функция для получения надписи формата:
        lambda idx, item: ..., где
        idx - индекс записи
        item - словарь записи элемента выбора.
        lambda функция должна возвращать надпись, соответствующую элементу выбора.
    :param is_default_on: Считаются все элементы по умолчанию выбранными?
    :param record_sort: Функция сортировки записей. Если не указана, то сортировки нет.
        Сортировка lambda функция:
            lambda record: ...
        Например:
            lambda record: record['name']
    :param item_sort: Функция сортировки элементов выбора. Если не указана, то сортировки нет.
        Сортировка lambda функция:
            lambda item: ...
        Например:
            lambda item: item['name']
    :return: Дополненный список записей выбранными и не выбранными элементами:
        {Словарь записи,
        '__on__': Список записей выбранных элементов,
        '__off__': Список записей не выбранных элементов}
        Либо None, если нажата <Отмена>.
    """
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()
        dlg = icItemSelectorDialog(parent=parent)
        dlg.init(title, records, columns, items, label, is_default_on,
                 record_sort=record_sort, item_sort=item_sort)
        result = dlg.ShowModal()
        new_records = dlg.get_records() if result == wx.ID_OK else None
        return new_records
    except:
        log.fatal(u'Ошибка вызова диалоговой формы выбора элементов связанных со списком записей')
    return None


def test():
    """
    Тестирование.
    """
    from ic.components import ictestapp
    app = ictestapp.TestApp(0)

    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    dlg = icItemSelectorDialog(frame, -1)

    dlg.ShowModal()

    dlg.Destroy()
    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test()
