#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report generator launch function module.
"""

import os
import os.path

from iq.util import log_func
from iq.util import res_func
from iq.util import str_func
from iq.util import file_func

from . import report_browser
from . import report_gen_func
from . import style_library


__version__ = (0, 0, 0, 1)

DEFAULT_REPORT_FILE_EXT = '.rprt'


def getReportResourceFilename(report_filename='', report_dir=''):
    """
    Get the full file name of the report template.

    :param report_filename:The name of the report file in short form.
    :param report_dir: Report folder.
    :return: The full name of the report file.
    """
    # Check extension
    rprt_filename = report_filename
    if not rprt_filename.endswith(DEFAULT_REPORT_FILE_EXT):
        rprt_filename = os.path.splitext(rprt_filename)[0]+DEFAULT_REPORT_FILE_EXT

    # Check the relevance of the template
    full_src_filename = getPathFilename(report_filename, report_dir)
    full_rprt_filename = getPathFilename(rprt_filename, report_dir)
    if isNewReportTemplateFile(full_src_filename, full_rprt_filename):
        # If the original template is changed later than the working
        # template file <rprt> then you need to make changes
        updateReportTemplateFile(full_src_filename, full_rprt_filename)

    if os.path.exists(rprt_filename):
        # Check can be given an absolute file name
        filename = rprt_filename
    else:
        # The relative file name relative to the report
        # folder is most likely set
        filename = full_rprt_filename
        if not os.path.exists(filename):
            log_func.error(u'Report template file <%s> not found' % str(filename))
            filename = createReportResourceFile(filename)
    log_func.debug(u'Report te,plate filename <%s>' % str(filename))
    return filename


def getPathFilename(filename='', report_dir=''):
    """
    Get absolute report template filename.

    :param filename: Short report file name.
    :param report_dir: Report folder.
    :return: Absolute report template filename.
    """
    return file_func.getAbsolutePath(os.path.join(report_dir, filename))


def isNewReportTemplateFile(src_filename, rprt_filename):
    """
    Check the relevance of the template.
    If the original template is changed later than the working * .rprt
    template file, then you need to make changes.

    :return: True-changes to the original template/False-no changes.
    """
    src_modify_dt = file_func.getFileModifyDatetime(src_filename)
    rprt_modify_dt = file_func.getFileModifyDatetime(rprt_filename)
    if src_modify_dt and rprt_modify_dt:
        return src_modify_dt > rprt_modify_dt
    return False


def updateReportTemplateFile(src_filename, rprt_filename):
    """
    Update the report template.

    :param src_filename: The name of the source template file.
    :param rprt_filename: The name of the resulting template file is * .rprt.
    :return: Corrected name of the created template file or None in case of error.
    """
    # Delete destination file
    file_func.removeFile(rprt_filename)
    # Delete all intermediate files
    for ext in report_gen_func.SRC_REPORT_EXT:
        src_ext = os.path.splitext(src_filename)[1].lower()
        if src_ext != ext:
            filename = os.path.splitext(src_filename)[0] + ext
            if os.path.exists(filename):
                file_func.removeFile(filename)
    # Пересоздаем шаблон
    return createReportResourceFile(rprt_filename)


def createReportResourceFile(template_filename):
    """
    Создать ресурсный файл шаблона по имени запрашиваемого.

    :param template_filename: Имя запрашиваемого файла шаблона.
    :return: Скорректированное имя созданного файла шаблона или None в случае ошибки.
    """
    # Коррекция имени файла с учетом русских букв в имени файла
    dir_name = os.path.dirname(template_filename)
    base_filename = os.path.basename(template_filename).replace(' ', '_')
    base_filename = textfunc.rus2lat(base_filename) if textfunc.isRUSText(base_filename) else base_filename
    norm_tmpl_filename = os.path.join(dir_name, base_filename)

    log_func.info(u'Создание нового файла шаблона <%s>' % norm_tmpl_filename)
    # Последовательно проверяем какой файл можно взять за основу для шаблона
    for ext in report_generator.SRC_REPORT_EXT:
        src_filename = os.path.splitext(template_filename)[0] + ext
        unicode_src_filename = textfunc.toUnicode(src_filename)
        if os.path.exists(src_filename):
            # Да такой файл есть и он может выступать
            # в качестве источника для шаблона
            log_func.info(u'Найден источник шаблона отчета <%s>' % unicode_src_filename)
            try:
                rep_generator = report_generator.createReportGeneratorSystem(ext)
                return rep_generator.update(src_filename)
            except:
                log_func.fatal(u'Ошибка конвертации шаблона отчета <%s> -> <%s>' % (unicode_src_filename, norm_tmpl_filename))
            return None

    log_func.warning(u'Не найдены источники шаблонов отчета в папке <%s> для <%s>' % (dir_name,
                                                                                 textfunc.toUnicode(os.path.basename(template_filename))))
    return None


def loadStyleLib(stylelib_filename=None):
    """
    Загрузить библиотеку стилей из файла.

    :param stylelib_filename: Файл библиотеки стилей.
    :return: Библиотека стилей.
    """
    # Загрузить библлиотеку стилей из файла
    stylelib = None
    if stylelib_filename:
        stylelib_filename = os.path.abspath(stylelib_filename)
        if os.path.exists(stylelib_filename):
            xml_stylelib = icstylelib.icXMLRepStyleLib()
            stylelib = xml_stylelib.convert(stylelib_filename)
    return stylelib


def openReportBrowser(parent_form=None, report_dir='', mode=icreportbrowser.IC_REPORT_EDITOR_MODE):
    """
    Запуск браузера отчетов.

    :param parent_form: Родительская форма, если не указана, 
        то создается новое приложение.
    :param report_dir: Директорий, где хранятся отчеты.
    :return: Возвращает результат выполнения операции True/False.
    """
    dlg = None
    try:
        # Иначе вывести окно выбора отчета
        dlg = icreportbrowser.icReportBrowserDialog(parent=parent_form, mode=mode,
                                                    report_dir=report_dir)
        dlg.ShowModal()

        dlg.Destroy()
        return True
    except:
        log_func.fatal(u'Ошибка запуска браузера отчетов')
        if dlg:
            dlg.Destroy()
    return False


def openReportEditor(parent_form=None, report_dir=''):
    """
    Запуск редактора отчетов. Редактор - режим работы браузера.

    :param parent_form: Родительская форма, если не указана, 
        то создается новое приложение.
    :param report_dir: Директорий, где хранятся отчеты.
    :return: Возвращает результат выполнения операции True/False.
    """
    return openReportBrowser(parent_form, report_dir, icreportbrowser.IC_REPORT_EDITOR_MODE)


def openReportViewer(parent_form=None, report_dir=''):
    """
    Запуск просмотрщика отчетов. Просмотрщик - режим работы браузера.

    :param parent_form: Родительская форма, если не указана, 
        то создается новое приложение.
    :param report_dir: Директорий, где хранятся отчеты.
    :return: Возвращает результат выполнения операции True/False.
    """
    return openReportBrowser(parent_form, report_dir, icreportbrowser.IC_REPORT_VIEWER_MODE)


def printReport(parent_form=None, report_filename='', report_dir='',
                db_url=None, sql=None, command=None,
                stylelib_filename=None, variables=None):
    """
    Функция запускает генератор отчетов и вывод на печать.

    :param parent_form: Родительская форма, если не указана,
        то создается новое приложение.
    :param report_filename: Файл отчета.
    :param report_dir: Директорий, где хранятся отчеты.
    :param db_url: Connection string в виде url. Например
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: Запрос SQL.
    :param command: Комманда после генерации. print/preview/export.
    :param stylelib_filename: Файл библиотеки стилей.
    :param variables: Словарь переменных для заполнения отчета.
    :return: Возвращает результат выполнения операции True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            # Если определен отчет, то запустить на выполнение
            repgen_system = report_generator.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.Print(resfunc.loadResourceFile(report_filename),
                                       stylelib=stylelib,
                                       variables=variables)
    except:
        log_func.fatal(u'Ошибка печати отчета <%s>' % report_filename)
    return False


def previewReport(parent_form=None, report_filename='', report_dir='',
                  db_url=None, sql=None, command=None,
                  stylelib_filename=None, variables=None):
    """
    Функция запускает генератор отчетов и вывод на экран предварительного просмотра.

    :param parent_form: Родительская форма, если не указана,
        то создается новое приложение.
    :param report_filename: Файл отчета.
    :param report_dir: Директорий, где хранятся отчеты.
    :param db_url: Connection string в виде url. Например
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: Запрос SQL.
    :param command: Комманда после генерации. print/preview/export.
    :param stylelib_filename: Файл библиотеки стилей.
    :param variables: Словарь переменных для заполнения отчета.
    :return: Возвращает результат выполнения операции True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            # Если определен отчет, то запустить на выполнение
            repgen_system = report_generator.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.preview(resfunc.loadResourceFile(report_filename),
                                         stylelib=stylelib,
                                         variables=variables)
    except:
        log_func.fatal(u'Ошибка предварительного просмотра отчета <%s>' % report_filename)
    return False


def exportReport(parent_form=None, report_filename='', report_dir='',
                 db_url=None, sql=None, command=None,
                 stylelib_filename=None, variables=None):
    """
    Функция запускает генератор отчетов и вывод в Office.

    :param parent_form: Родительская форма, если не указана,
        то создается новое приложение.
    :param report_filename: Файл отчета.
    :param report_dir: Директорий, где хранятся отчеты.
    :param db_url: Connection string в виде url. Например
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: Запрос SQL.
    :param command: Комманда после генерации. print/preview/export.
    :param stylelib_filename: Файл библиотеки стилей.
    :param variables: Словарь переменных для заполнения отчета.
    :return: Возвращает результат выполнения операции True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            # Если определен отчет, то запустить на выполнение
            repgen_system = report_generator.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.convert(resfunc.loadResourceFile(report_filename),
                                         stylelib=stylelib,
                                         variables=variables)
    except:
        log_func.fatal(u'Ошибка экспорта отчета <%s>' % report_filename)
    return False


def selectReport(parent_form=None, report_filename='', report_dir='',
                 db_url=None, sql=None, command=None,
                 stylelib_filename=None, variables=None):
    """
    Функция запускает генератор отчетов с последующим выбором действия.

    :param parent_form: Родительская форма, если не указана,
        то создается новое приложение.
    :param report_filename: Файл отчета.
    :param report_dir: Директорий, где хранятся отчеты.
    :param db_url: Connection string в виде url. Например
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: Запрос SQL.
    :param command: Комманда после генерации. print/preview/export.
    :param stylelib_filename: Файл библиотеки стилей.
    :param variables: Словарь переменных для заполнения отчета.
    :return: Возвращает результат выполнения операции True/False.
    """
    report_filename = getReportResourceFilename(report_filename, report_dir)
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            stylelib = loadStyleLib(stylelib_filename)
            # Если определен отчет, то запустить на выполнение
            repgen_system = report_generator.getReportGeneratorSystem(report_filename, parent_form)
            return repgen_system.selectAction(resfunc.loadResourceFile(report_filename),
                                              stylelib=stylelib,
                                              variables=variables)
    except:
        log_func.fatal(u'Ошибка генерации отчета с выбором действия <%s>' % report_filename)
    return False


# Комманды пост обработки сгенерированног отчета
DO_COMMAND_PRINT = 'print'
DO_COMMAND_PREVIEW = 'preview'
DO_COMMAND_EXPORT = 'export'
DO_COMMAND_SELECT = 'select'


def doReport(parent_form=None, report_filename='', report_dir='', db_url='', sql='', command=None,
             stylelib_filename=None, variables=None):
    """
    Функция запускает генератор отчетов.

    :param parent_form: Родительская форма, если не указана,
        то создается новое приложение.
    :param report_filename: Файл отчета.
    :param report_dir: Директорий, где хранятся отчеты.
    :param db_url: Connection string в виде url. Например
        postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
    :param sql: Запрос SQL.
    :param command: Комманда после генерации. print/preview/export.
    :param stylelib_filename: Файл библиотеки стилей.
    :param variables: Словарь переменных для заполнения отчета.
    :return: Возвращает результат выполнения операции True/False.
    """
    try:
        if not report_filename:
            return openReportViewer(parent_form, report_dir)
        else:
            # Если определен отчет, то запустить на выполнение
            repgen_system = report_generator.getReportGeneratorSystem(report_filename, parent_form)
            stylelib = loadStyleLib(stylelib_filename)

            data = repgen_system.generate(resfunc.loadResourceFile(report_filename), db_url, sql,
                                          stylelib=stylelib, vars=variables)

            if command:
                command = command.lower()
                if command == DO_COMMAND_PRINT:
                    repgen_system.printResult(data)
                elif command == DO_COMMAND_PREVIEW:
                    repgen_system.previewResult(data)
                elif command == DO_COMMAND_EXPORT:
                    repgen_system.convertResult(data)
                elif command == DO_COMMAND_SELECT:
                    repgen_system.doSelectAction(data)
                else:
                    log_func.warning(u'Не обрабатываемая команда запуска <%s>' % command)
            else:
                repgen_system.save(data)
        return True
    except:
        log_func.fatal(u'Ошибка запуска генератора отчета <%s>' % report_filename)


if __name__ == '__main__':
    doReport()
