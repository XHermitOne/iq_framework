#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль системы генератора отчетов, основанные на генерации XML файлов.
"""

# Подключение библиотек
import copy
import os 
import os.path

from .dlg import report_action_dlg
from ic.std.log import log
from ic.std.dlg import dlg

from ic.virtual_excel import icexcel

from ic.report import icrepgensystem
from ic.report import icrepgen
from ic.report import icrepfile

from ic import config

__version__ = (0, 1, 1, 2)


class icXLSReportGeneratorSystem(icrepgensystem.icReportGeneratorSystem):
    """
    Класс системы генерации отчетов, основанные на генерации XLS файлов.
    """

    def __init__(self, report=None, parent=None):
        """
        Конструктор класса.

        :param report: Шаблон отчета.
        :param parent: Родительская форма, необходима для вывода сообщений.
        """
        # вызов конструктора предка
        icrepgensystem.icReportGeneratorSystem.__init__(self, report, parent)

        # Имя файла шаблона отчета
        self.RepTmplFileName = None
        
        # Папка отчетов.
        self._report_dir = None
        if self._ParentForm:
            self._report_dir = os.path.abspath(self._ParentForm.getReportDir())
        
    def reloadRepData(self, tmpl_filename=None):
        """
        Перегрузить данные отчета.

        :param tmpl_filename: Имя файла шаблона отчета.
        """
        if tmpl_filename is None:
            tmpl_filename = self.RepTmplFileName
        icrepgensystem.icReportGeneratorSystem.reloadRepData(self, tmpl_filename)
        
    def getReportDir(self):
        """
        Папка отчетов.
        """
        if self._report_dir is None:
            if self._ParentForm:
                self._report_dir = os.path.abspath(self._ParentForm.getReportDir())
            else:
                log.warning(u'Не определена папка отчетов!')
                self._report_dir = ''
                                
        return self._report_dir

    def _genXLSReport(self, report, *args, **kwargs):
        """
        Генерация отчета и сохранение его в XLS файл.

        :param report: Полное описание шаблона отчета.
        :return: Возвращает имя xml файла или None в случае ошибки.
        """
        if report is None:
            report = self._Rep
        data_rep = self.generateReport(report, *args, **kwargs)
        return self.save(data_rep)

    def selectAction(self, report=None, *args, **kwargs):
        """
        Запуск генерации отчета с последующим выбором действия.

        :param report: Полное описание шаблона отчета.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            return self.doSelectAction(xls_rep_file_name)
        else:
            log.warning(u'Файл отчета <%s> не существует' % xls_rep_file_name)

    def doSelectAction(self, data):
        """
        Запуск выбора действия над отчетом.

        :param data: Данные об отчете.
        """
        action = report_action_dlg.getReportActionDlg(title=self.getReportDescription())
        if action == report_action_dlg.PRINT_ACTION_ID:
            return self.printOffice(data)
        elif action == report_action_dlg.PREVIEW_ACTION_ID:
            return self.previewOffice(data)
        elif action == report_action_dlg.EXPORT_ACTION_ID:
            return self.openOffice(data)
        else:
            log.warning(u'Не определено действие над отчетом')
        return None

    def preview(self, report=None, *args, **kwargs):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            # Открыть в режиме просмотра
            self.previewOffice(xls_rep_file_name)
            
    def previewOffice(self, xls_filename):
        """
        Открыть отчет в режиме предварительного просмотра.

        :param xls_filename: Имя xls файла, содержащего сгенерированный отчет.
        """
        if not os.path.exists(xls_filename):
            log.warning(u'Предварительный просмотр. Файл <%s> не найден' % xls_filename)
            return

        pdf_filename = os.path.splitext(xls_filename)[0] + '.pdf'
        if os.path.exists(pdf_filename):
            try:
                os.remove(pdf_filename)
            except:
                log.error(u'Ошибка удаления файла <%s>' % pdf_filename)

        cmd = 'unoconv --format=pdf %s' % xls_filename
        log.info(u'UNOCONV. Выполнения комманды ОС <%s>' % cmd)
        os.system(cmd)

        cmd = 'evince %s&' % pdf_filename
        log.info(u'EVINCE. Выполнения комманды ОС <%s>' % cmd)
        os.system(cmd)

    def print(self, report=None, *args, **kwargs):
        """
        Печать.

        :param report: Полное описание шаблона отчета.
        """
        xls_rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if xls_rep_file_name and os.path.exists(xls_rep_file_name):
            # Открыть печать в CALC
            self.printOffice(xls_rep_file_name)

    def printOffice(self, xls_filename):
        """
        Печать отчета с помощью CALC.

        :param xls_filename: Имя xls файла, содержащего сгенерированный отчет.
        """
        if xls_filename and os.path.exists(xls_filename):
            cmd = 'libreoffice -p %s&' % xls_filename
            log.info(u'Выполнения комманды ОС <%s>' % cmd)
            os.system(cmd)
        else:
            log.warning(u'Печать. Файл <%s> не найден.' % xls_filename)

    def setPageSetup(self):
        """
        Установка параметров страницы.
        """
        pass

    def convert(self, report=None, to_filename=None, *args, **kwargs):
        """
        Вывод результатов отчета в Excel.

        :param report: Полное описание шаблона отчета.
        :param to_filename: Имя файла, куда необходимо сохранить отчет.
        """
        rep_file_name = self._genXLSReport(report, *args, **kwargs)
        if rep_file_name:
            # Открыть CALC в режиме
            self.openOffice(rep_file_name)

    def openOffice(self, xls_filename):
        """
        Открыть.

        :param xls_filename: Имя xls файла, содержащего сгенерированный отчет.
        """
        if xls_filename and os.path.exists(xls_filename):
            cmd = 'libreoffice %s&' % xls_filename
            log.info('Выполнения комманды ОС <%s>' % cmd)
            os.system(cmd)
        else:
            log.warning(u'Открытие. Файл <%s> не найден' % xls_filename)

    def edit(self, rep_filename=None):
        """
        Редактирование отчета.

        :param rep_filename: Полное имя файла шаблона отчета.
        """
        # Определить файл *.xls
        xls_file = os.path.abspath(os.path.splitext(rep_filename)[0]+'.xls')
        cmd = 'libreoffice \"%s\"&' % xls_file
        # и запустить
        os.system(cmd)

    def generateReport(self, report=None, *args, **kwargs):
        """
        Запустить генератор отчета.

        :param report: Шаблон отчета.
        :return: Возвращает сгенерированный отчет или None в случае ошибки.
        """
        try:
            if report is not None:
                self._Rep = report

            # 1. Получить таблицу запроса
            # Переменные могут учавствовать в генерации текста запроса
            variables = kwargs.get('variables', None)
            if variables:
                kwargs.update(variables)

            query_tbl = self.getQueryTbl(self._Rep, *args, **kwargs)
            if self._isEmptyQueryTbl(query_tbl):
                if not config.get_glob_var('NO_GUI_MODE'):
                    if not dlg.getAskBox(u'Внимание',
                                         u'Нет данных, соответствующих запросу: %s. Продолжить генерацию отчета?' % self._Rep['query']):
                        return None
                else:
                    log.warning(u'Пустая таблица запроса. Продолжение генерации.')
                query_tbl = self.createEmptyQueryTbl()

            # 2. Запустить генерацию
            rep = icrepgen.icReportGenerator()
            coord_fill = kwargs.get('coord_fill', None)
            data_rep = rep.generate(self._Rep, query_tbl,
                                    name_space=variables, coord_fill=coord_fill)

            return data_rep
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета <%s>.' % self._Rep['name'])
        return None

    def generate(self, report=None, db_url=None, sql=None, stylelib=None, vars=None, *args, **kwargs):
        """
        Запустить генератор отчета.

        :param report: Шаблон отчета.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
        :param stylelib: Библиотека стилей.
        :param vars: Словарь переменных отчета.
        :return: Возвращает сгенерированный отчет или None в случае ошибки.
        """
        try:
            if report is not None:
                self._Rep = report

            if stylelib:
                self._Rep['style_lib'] = stylelib

            if vars:
                self._Rep['variables'] = vars

            # 1. Получить таблицу запроса
            _kwargs = copy.deepcopy(kwargs)
            _kwargs.update(dict(db_url=db_url, sql=sql, stylelib=stylelib, variables=vars))
            query_tbl = self.getQueryTbl(self._Rep, **_kwargs)
            if self._isEmptyQueryTbl(query_tbl):
                dlg.getMsgBox(u'Внимание', u'Нет данных, соответствующих запросу: %s' % self._Rep['query'],
                              parent=self._ParentForm)
                return None

            # 2. Запустить генерацию
            rep = icrepgen.icReportGenerator()
            data_rep = rep.generate(self._Rep, query_tbl,
                                    name_space=vars, *args, **kwargs)

            return data_rep
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета <%s>.' % self._Rep['name'])
        return None

    def save(self, report_data=None, is_virtual_excel=True):
        """
        Сохранить результаты генерации в файл

        :param report_data: Сгенерированный отчет.
        :param is_virtual_excel: Сохранение произвести с помощью VirtualExcel?
            True - да, False - Сохранение производится конвертацией с помощью UNOCONV.
            ВНИМАНИЕ! При конвертации с помощью UNOCONV ячейки не образмериваются.
                Размеры ячеек остаются по умолчанию.
                UNOCONV транслирует не все стили и атрибуты ячеек.
        :return: Имя сохраненного файла или None, если сохранения не произошло.
        """
        if report_data:
            rep_file = icrepfile.icExcelXMLReportFile()
            save_dir = self.getProfileDir()
            if not save_dir:
                save_dir = icrepgensystem.DEFAULT_REPORT_DIR
            # print(u'DBG:', save_dir, report_data, type(report_data))
            xml_rep_file_name = os.path.join(save_dir, '%s_report_result.xml' % report_data['name'])
            rep_file_name = os.path.join(save_dir, '%s_report_result.ods' % report_data['name'])

            rep_file.write(xml_rep_file_name, report_data)

            if is_virtual_excel:
                log.info(u'Конвертация отчета <%s> в файл <%s>' % (xml_rep_file_name, rep_file_name))
                v_excel = icexcel.icVExcel()
                v_excel.load(xml_rep_file_name)
                v_excel.saveAs(rep_file_name)
                # Здесь дописать переконвертацию
            else:
                # ВНИМАНИЕ! UNOCONV транслирует не все стили и атрибуты ячеек
                # Поэтому сначала используется Virtual Excel
                cmd = 'unoconv -f ods %s' % xml_rep_file_name
                log.info(u'UNOCONV. Конвертация отчета <%s> в файл <%s>. (%s)' % (xml_rep_file_name,
                                                                                  rep_file_name, cmd))
                os.system(cmd)

            return rep_file_name
        return None

    def previewResult(self, report_data=None):
        """
        Предварительный просмотр.

        :param report_data: Сгенерированный отчет.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.previewOffice(report_filename)

    def printResult(self, report_data=None):
        """
        Печать.

        :param report_data: Сгенерированный отчет.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.printOffice(report_filename)

    def convertResult(self, report_data=None, to_filename=None):
        """
        Конвертирование результатов отчета.

        :param report_data: Сгенерированный отчет.
        :param to_filename: Имя результирующего файла.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.openOffice(report_filename)
