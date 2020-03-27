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
from ic.std.utils import textfunc

from ic.virtual_excel import icexcel

from ic.report import icrepgensystem
from ic.report import icrepgen
from ic.report import icrepfile

from ic import config


__version__ = (0, 1, 1, 1)


class icODSReportGeneratorSystem(icrepgensystem.icReportGeneratorSystem):
    """
    Класс системы генерации отчетов, основанные на генерации ODS файлов.
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

    def _genODSReport(self, report, *args, **kwargs):
        """
        Генерация отчета и сохранение его в ODS файл.

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
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            return self.doSelectAction(ods_rep_file_name)
        else:
            log.warning(u'Файл отчета <%s> не существует' % ods_rep_file_name)

    def doSelectAction(self, data):
        """
        Запуск выбора действия над отчетом.

        :param data: Данные об отчете.
        """
        action = report_action_dlg.getReportActionDlg(title=self.getReportDescription())
        if action == report_action_dlg.PRINT_ACTION_ID:
            return self.PrintOffice(data)
        elif action == report_action_dlg.PREVIEW_ACTION_ID:
            return self.PreviewOffice(data)
        elif action == report_action_dlg.EXPORT_ACTION_ID:
            return self.OpenOffice(data)
        else:
            log.warning(u'Не определено действие над отчетом')
        return None

    def preview(self, report=None, *args, **kwargs):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            # Открыть в режиме просмотра
            self.PreviewOffice(ods_rep_file_name)
            
    def PreviewOffice(self, ods_filename):
        """
        Открыть отчет в режиме предварительного просмотра.

        :param ods_filename: Имя ods файла, содержащего сгенерированный отчет.
        """
        if not os.path.exists(ods_filename):
            log.warning(u'Предварительный просмотр. Файл <%s> не найден' % ods_filename)
            return

        pdf_filename = os.path.splitext(ods_filename)[0]+'.pdf'
        if os.path.exists(pdf_filename):
            try:
                os.remove(pdf_filename)
            except:
                log.error(u'Delete file <%s>' % pdf_filename)

        cmd = 'unoconv --format=pdf %s' % ods_filename
        log.info(u'UNOCONV. Выполнение комманды <%s>' % cmd)
        os.system(cmd)

        cmd = 'evince %s&' % pdf_filename
        log.info(u'EVINCE. Выполнение комманды <%s>' % cmd)
        os.system(cmd)

    def print(self, report=None, *args, **kwargs):
        """
        Печать.

        :param report: Полное описание шаблона отчета.
        """
        ods_rep_file_name = self._genODSReport(report, *args, **kwargs)
        if ods_rep_file_name and os.path.exists(ods_rep_file_name):
            # Открыть печать в CALC
            self.PrintOffice(ods_rep_file_name)

    def PrintOffice(self, ods_filename):
        """
        Печать отчета с помощью CALC.

        :param ods_filename: Имя ods файла, содержащего сгенерированный отчет.
        """
        if ods_filename and os.path.exists(ods_filename):
            cmd = 'libreoffice -p %s&' % ods_filename
            log.info(u'Выполнение комманды ОС <%s>' % cmd)
            os.system(cmd)
        else:
            log.warning(u'Печать. Файл <%s> не найден.' % ods_filename)

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
        rep_file_name = self._genODSReport(report, *args, **kwargs)
        if rep_file_name:
            # Открыть CALC в режиме
            self.OpenOffice(rep_file_name)

    def OpenOffice(self, ods_filename):
        """
        Открыть.

        :param ods_filename: Имя ods файла, содержащего сгенерированный отчет.
        """
        if ods_filename and os.path.exists(ods_filename):
            cmd = 'libreoffice %s&' % ods_filename
            log.info('Выполнение комманды ОС <%s>' % cmd)
            os.system(cmd)
        else:
            log.warning(u'Открытие. Файл <%s> не найден' % ods_filename)

    def edit(self, rep_filename=None):
        """
        Редактирование отчета.

        :param rep_filename: Полное имя файла шаблона отчета.
        """
        # Определить файл *.ods
        ods_file = os.path.abspath(os.path.splitext(rep_filename)[0]+'.ods')
        cmd = 'libreoffice \"%s\"&' % ods_file
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
                    log.warning(u'')
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
                dlg.getMsgBox(u'Внимание',
                              u'Нет данных, соответствующих запросу: %s' % self._Rep['query'],
                              self._ParentForm)
                return None

            # 2. Запустить генерацию
            rep = icrepgen.icReportGenerator()
            data_rep = rep.generate(self._Rep, query_tbl,
                                    name_space=vars, *args, **kwargs)

            return data_rep
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета <%s>.' % textfunc.toUnicode(self._Rep['name']))
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
                log.info(u'Конвертация отчета <%s> в файл <%s>' % (textfunc.toUnicode(xml_rep_file_name),
                                                                   textfunc.toUnicode(rep_file_name)))
                v_excel = icexcel.icVExcel()
                v_excel.load(xml_rep_file_name)
                v_excel.saveAs(rep_file_name)
            else:
                # ВНИМАНИЕ! UNOCONV транслирует не все стили и атрибуты ячеек
                # Поэтому сначала используется Virtual Excel
                cmd = 'unoconv --format=ods %s' % xml_rep_file_name
                log.info(u'UNOCONV. Конвертация отчета <%s> в файл <%s>. (%s)' % (textfunc.toUnicode(xml_rep_file_name),
                                                                                  textfunc.toUnicode(rep_file_name),
                                                                                  textfunc.toUnicode(cmd)))
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
            return self.PreviewOffice(report_filename)

    def printResult(self, report_data=None):
        """
        Печать.

        :param report_data: Сгенерированный отчет.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.PrintOffice(report_filename)

    def convertResult(self, report_data=None, to_filename=None):
        """
        Конвертирование результатов отчета.

        :param report_data: Сгенерированный отчет.
        :param to_filename: Имя результирующего файла.
        """
        report_filename = self.save(report_data)
        if report_filename:
            return self.OpenOffice(report_filename)
