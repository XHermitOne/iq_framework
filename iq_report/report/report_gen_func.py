#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций общего интерфейса к системе генерации.
"""

# Подключение библиотек
from ic.std.log import log
from ic.std.utils import resfunc

from ic.report import icxmlreportgenerator
from ic.report import icodsreportgenerator
from ic.report import icxlsreportgenerator
# from ic.report import icreportmangenerator
from ic.report import icrtfreportgenerator

__version__ = (0, 1, 1, 2)

# Константы подсистемы
REP_GEN_SYS = None

# Спецификации
_ReportGeneratorSystemTypes = {'.xml': icxmlreportgenerator.icXMLReportGeneratorSystem,         # Мой XMLSS генератор
                               '.ods': icodsreportgenerator.icODSReportGeneratorSystem,         # Мой ODS генератор
                               '.xls': icxlsreportgenerator.icXLSReportGeneratorSystem,         # Мой XLS генератор
                               # '.rep': icreportmangenerator.icReportManagerGeneratorSystem,     # Report Manager
                               '.rtf': icrtfreportgenerator.icRTFReportGeneratorSystem,         # RTF генератор
                               }

# Список расширений источников шаблонов
SRC_REPORT_EXT = _ReportGeneratorSystemTypes.keys()


# Функции управления
def getReportGeneratorSystem(rep_filename, parent=None, bRefresh=True):
    """
    Получить объект системы генерации отчетов.

    :param rep_filename: Имя файла шаблона отчета.
    :param parent: Родительская форма, необходима для вывода сообщений.
    :param bRefresh: Указание обновления данных шаблона отчета в генераторе.
    :return: Функция возвращает объект-наследник класса icReportGeneratorSystem.
        None - в случае ошибки.
    """
    try:
        # Прочитать шаблон отчета
        rep = resfunc.loadResourceFile(rep_filename, bRefresh=True)
        
        global REP_GEN_SYS

        # Создание системы ренерации отчетов
        if REP_GEN_SYS is None:
            REP_GEN_SYS = createReportGeneratorSystem(rep['generator'], rep, parent)
            REP_GEN_SYS.RepTmplFileName = rep_filename
        elif not REP_GEN_SYS.sameGeneratorType(rep['generator']):
            REP_GEN_SYS = createReportGeneratorSystem(rep['generator'], rep, parent)
            REP_GEN_SYS.RepTmplFileName = rep_filename
        else:
            if bRefresh:
                # Просто установить обновление
                REP_GEN_SYS.setRepData(rep)
                REP_GEN_SYS.RepTmplFileName = rep_filename

        # Если родительская форма не определена у системы генерации,
        # то установить ее
        if REP_GEN_SYS and REP_GEN_SYS.getParentForm() is None:
            REP_GEN_SYS.setParentForm(parent)
            
        return REP_GEN_SYS
    except:
        log.error(u'Ошибка определения объекта системы генерации отчетов. Отчет <%s>.' % rep_filename)
        raise
    return None


def createReportGeneratorSystem(repgen_sys_type, report=None, parent=None):
    """
    Создать объект системы генерации отчетов.

    :param repgen_sys_type: Указание типа системы генерации отчетов.
        Тип задается расширением файла источника шаблона.
        В нашем случае один из SRC_REPORT_EXT.
    :param report: Словарь отчета.
    :param parent: Родительская форма, необходима для вывода сообщений.
    :return: Функция возвращает объект-наследник класса icReportGeneratorSystem.
        None - в случае ошибки.
    """
    rep_gen_sys_type = repgen_sys_type[-4:].lower() if isinstance(repgen_sys_type, str) else None
    rep_gen_sys = None
    if rep_gen_sys_type:
        rep_gen_sys_class = _ReportGeneratorSystemTypes.setdefault(rep_gen_sys_type, None)
        if rep_gen_sys_class is not None:
            rep_gen_sys = rep_gen_sys_class(report, parent)
        else:
            log.warning(u'Не известный тип генератора <%s>' % rep_gen_sys_type)
    else:
        log.warning(u'Не корректный тип генератора <%s>' % repgen_sys_type)
    return rep_gen_sys


def getCurReportGeneratorSystem(report_browser_dialog=None):
    """
    Возвратить текущую систему генерации.
    """
    global REP_GEN_SYS
    if REP_GEN_SYS is None:
        REP_GEN_SYS = icodsreportgenerator.icODSReportGeneratorSystem(parent=report_browser_dialog)
    return REP_GEN_SYS
