#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Функции стандартных диалогов прикладного уровня.
"""

import wx
import wx.lib.calendar

from . import dlgfunc

try:
    from . import iccalendardlg
except ImportError:
    pass

from . import icyeardlg
from . import icmonthdlg
from . import icquarterdlg
from . import icmonthrangedlg
try:
    from . import icdaterangedlg
except ImportError:
    pass

from . import icnsilistdlg
from . import icintegerdlg
from . import icradiochoicedlg
from . import icintrangedlg
from . import iccheckboxdlg
from . import icradiochoicemaxidlg
from . import iccheckboxmaxidlg

try:
    from ic.log import log
except ImportError:
    pass

try:
    from ic.utils import datefunc
except ImportError:
    pass


__version__ = (0, 1, 9, 1)


def getIntegerDlg(parent=None, title=None, label=None, min_value=0, max_value=100):
    """
    Ввод целого числа в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label: Текст приглашения ввода.
    :param min_value: Минимально-допустимое значение.
    :param max_value: Максимально-допустимое значение.
    :return: Введенное значение или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icintegerdlg.icIntegerDialog(parent)
    dlg.init(title=title, label=label, min_value=min_value, max_value=max_value)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getDateDlg(parent=None):
    """
    Выбор даты в диалоговом окне календаря.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :return: Выбранную дату(datetime) или None если нажата <отмена>.
    """
    selected_date = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = iccalendardlg.icCalendarDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_date = dlg.getSelectedDateAsDatetime()
    dlg.Destroy()

    return selected_date


def getYearDlg(parent=None, title=None, default_year=None):
    """
    Выбор года в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заоголовок диалогового окна.
    :param default_year: Устанавлемое здачение по умолчанию.
    :return: Выбранный год (datetime) или None если нажата <отмена>.
    """
    selected_year = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icyeardlg.icYearDialog(parent)
    dlg.Centre()

    if title:
        # Если определен заголовок, то установить в диалоговом окне
        dlg.SetTitle(title)

    if default_year:
        # Выбран год по умолчанию
        dlg.setSelectedYear(default_year)
    dlg.init_year_choice()

    if dlg.ShowModal() == wx.ID_OK:
        selected_year = dlg.getSelectedYearAsDatetime()
    dlg.Destroy()

    return selected_year


def getMonthDlg(parent=None):
    """
    Выбор месяца в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :return: Первый день выбранного месяца (datetime) или None если нажата <отмена>.
    """
    selected_month = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthdlg.icMonthDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_month = dlg.getSelectedMonthAsDatetime()
    dlg.Destroy()

    return selected_month


def getQuarterDlg(parent=None):
    """
    Выбор квартала в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :return: Кортеж (год, номер картала) или None если нажата <отмена>.
    """
    selected_quarter = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icquarterdlg.icQuarterDialog(parent=parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_quarter = dlg.getSelectedQuarter()
    dlg.Destroy()

    return selected_quarter


MONTH_CHOICES = datefunc.MONTHS


def getMonthNumDlg(parent=None, title=None, text=None):
    """
    Выбор номера месяца в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заоголовок диалогового окна.
    :param text: Приглашение ввода.
    :return: Номер месяца 1-январь ... 12-декабрь или None, если нажата <Отмена>.
    """
    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    title = u'МЕСЯЦ' if title is None else title
    text = u'Выберите месяц' if text is None else text
    selected_idx = dlgfunc.getSingleChoiceIdxDlg(parent, title=title, prompt_text=text, choices=MONTH_CHOICES)
    if selected_idx >= 0:
        return selected_idx + 1
    # Нажата ОТМЕНА
    return None


def getMonthRangeDlg(parent=None):
    """
    Выбор периода по месяцам в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :return: Кортеж периода по месяцам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icmonthrangedlg.icMonthRangeDialog(parent)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedMonthRangeAsDatetime()
    dlg.Destroy()

    return selected_range


def getDateRangeDlg(parent=None, is_concrete_date=False):
    """
    Выбор периода по датам в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param is_concrete_date: Вкл. режим ввода конкретной даты?
    :return: Кортеж периода по датам (datetime) или None если нажата <отмена>.
    """
    selected_range = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icdaterangedlg.icDateRangeDialog(parent)
    dlg.setConcreteDateCheck(is_concrete_date)

    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        selected_range = dlg.getSelectedDateRangeAsDatetime()
    dlg.Destroy()

    if selected_range:
        try:
            log.debug(u'Выбранный диапазон дат: <%s> - <%s>' % selected_range)
        except:
            pass
    return selected_range


def getNSIListDlg(parent=None,
                  db_url=None, nsi_sprav_tabname=None,
                  code_fieldname='cod', name_fieldname='name',
                  ext_filter=''):
    """
    Выбор значения из простого спискового справочника.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param db_url: URL подключения к БД.
    :param nsi_sprav_tabname: Имя таблицы справочника.
    :param code_fieldname: Имя поля кода в таблице справочника.
    :param name_fieldname: Имя поля наименования в таблице справочника.
    :param ext_filter: Дополнительный фильтр записей.
    :return: Выбранный код справочника или None если нажата <отмена>.
    """
    selected_code = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icnsilistdlg.icNSIListDialog(parent)
    dlg.Centre()
    dlg.setDbURL(db_url)
    dlg.initChoice(nsi_sprav_tabname, code_fieldname, name_fieldname, ext_filter)

    if dlg.ShowModal() == wx.ID_OK:
        selected_code = dlg.getSelectedCode()

    try:
        dlg.Destroy()
    except wx.PyDeadObjectError:
        print(u'wx.PyDeadObjectError. Ошибка удаления диалогового окна')
    return selected_code


def getStdDlgQueue(*dlgs):
    """
    Определить очередность вызова диалоговых окон для
    определения параметров запроса отчета.

    :param dlgs: Список словарей описания вызова диалоговых окон.
        Вызов диалогового окна - это словарь формата:
        {'key': Ключ результата,
         'function': Функция вызова диалога,
         'args': Список аргументов функции вызова диалога,
         'kwargs': Словарь именованных аргументов вункции вызова диалога}.
    :return: Словарь заполненных значений с помощью диалоговых функций.
    """
    # ВНИМАНИЕ! Для корректного отображения окон необходимо указать
    # frame в явном виде
    frame = wx.Frame(None, -1)
    frame.Center()

    result = dict()

    for dlg in dlgs:
        dlg_func = dlg.get('function', None)
        args = dlg.get('args', tuple())
        kwargs = dlg.get('kwargs', dict())
        if dlg_func:
            result_key = dlg['key'] if 'key' in dlg else dlg_func.__name__
            result[result_key] = dlg_func(parent=frame, *args, **kwargs)

    frame.Destroy()
    return result


def getRadioChoiceDlg(parent=None, title=None, label=None, choices=()):
    """
    Выбор элемента wxRadioBox.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label: Текст приглашения ввода.
    :param choices: Список выбора.
        Максимальное количество элементов выбора 5.
        При большем количестве элементов необходимо использовать 
        другую диалоговую форму выбора.    
    :return: Индекс выбранного эдемента или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icradiochoicedlg.icRadioChoiceDialog(parent)
    dlg.init(title=title, label=label, choices=choices)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getIntRangeDlg(parent=None, title=None, label_begin=None, label_end=None, min_value=0, max_value=100):
    """
    Ввод целого числа в диалоговом окне.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label_begin: Текст приглашения ввода первого номера диапазона.
    :param label_end: Текст приглашения ввода последнего номера диапазона.
    :param min_value: Минимально-допустимое значение.
    :param max_value: Максимально-допустимое значение.
    :return: Введенное значение или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icintrangedlg.icIntRangeDialog(parent)
    dlg.init(title=title, label_begin=label_begin, label_end=label_end,
             min_value=min_value, max_value=max_value)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getCheckBoxDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Выбор элементов wxCheckBox.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label: Текст приглашения ввода.
    :param choices: Список выбора.
        Максимальное количество элементов выбора 7.
        При большем количестве элементов необходимо использовать
        другую диалоговую форму выбора.
    :param defaults: Список отметок по умолчанию.
    :return: Признак выбранного элемента True-выбран/False-нет или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = iccheckboxdlg.icCheckBoxDialog(parent)
    dlg.init(title=title, label=label, choices=choices, defaults=defaults)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getRadioChoiceMaxiDlg(parent=None, title=None, label=None,
                          choices=(), default=None):
    """
    Выбор элемента wxRadioBox.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label: Текст приглашения ввода.
    :param choices: Список выбора.
        Максимальное количество элементов выбора 5.
        При большем количестве элементов необходимо использовать
        другую диалоговую форму выбора.
    :param default: Индекс выбранного элемента по умолчанию.
    :return: Индекс выбранного эдемента или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = icradiochoicemaxidlg.icRadioChoiceMaxiDialog(parent)
    dlg.init(title=title, label=label, choices=choices, default=default)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def getCheckBoxMaxiDlg(parent=None, title=None, label=None, choices=(), defaults=()):
    """
    Выбор элементов wxCheckBox.

    :param parent: Родительское окно. Если не определено, то
        береться wx.GetApp().GetTopWindow()
    :param title: Заголовок окна.
    :param label: Текст приглашения ввода.
    :param choices: Список выбора.
        Максимальное количество элементов выбора 7.
        При большем количестве элементов необходимо использовать
        другую диалоговую форму выбора.
    :param defaults: Список отметок по умолчанию.
    :return: Признак выбранного элемента True-выбран/False-нет или None если нажата <отмена>.
    """
    value = None

    if parent is None:
        parent = wx.GetApp().GetTopWindow()

    dlg = iccheckboxmaxidlg.icCheckBoxMaxiDialog(parent)
    dlg.init(title=title, label=label, choices=choices, defaults=defaults)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:
        value = dlg.getValue()
    dlg.Destroy()

    return value


def test():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()
    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    print((getDateDlg(frame)))

    frame.Destroy()

    app.MainLoop()


def test_nsi_1():
    """
    Тестирование.
    """
    app = wx.PySimpleApp()
    # ВНИМАНИЕ! Выставить русскую локаль
    # Это необходимо для корректного отображения календарей,
    # форматов дат, времени, данных и т.п.
    locale = wx.Locale()
    locale.Init(wx.LANGUAGE_RUSSIAN)

    frame = wx.Frame(None, -1)

    # Параметры подключения к БД
    DB_HOST = '10.0.0.3'
    DB_PORT = 5432
    DB_USER = 'xhermit'
    DB_PASSWORD = 'xhermit'
    DB_NAME = 'testing'

    DB_URL = 'postgres://%s:%s@%s:%d/%s' % (DB_USER, DB_PASSWORD,
                                            DB_HOST, DB_PORT, DB_NAME)

    print((getNSIListDlg(frame, db_url=DB_URL,
                        nsi_sprav_tabname='nsi_tags')))

    frame.Destroy()

    app.MainLoop()


if __name__ == '__main__':
    test_nsi_1()
