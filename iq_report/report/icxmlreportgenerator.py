#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль системы генератора отчетов, основанные на генерации XML файлов.
"""

# Подключение библиотек
import os 
import os.path

from ic.std.log import log
from ic.std.dlg import dlg

from ic.report import icrepgensystem
from ic.report import icreptemplate
from ic.report import icrepgen
from ic.report import icrepfile

from ic import config

__version__ = (0, 1, 1, 2)


class icXMLReportGeneratorSystem(icrepgensystem.icReportGeneratorSystem):
    """
    Класс системы генерации отчетов, основанные на генерации XML файлов.
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
                dlg.getMsgBox(u'Ошибка', u'Не определена папка отчетов!')
                                
        return self._report_dir

    def _genXMLReport(self, report):
        """
        Генерация отчета и сохранение его в XML файл.

        :param report: Полное описание шаблона отчета.
        :return: Возвращает имя xml файла или None в случае ошибки.
        """
        if report is None:
            report = self._Rep
        data_rep = self.generateReport(report)
        if data_rep:
            rep_file = icrepfile.icExcelXMLReportFile()
            rep_file_name = os.path.join(self.getReportDir(),
                                         '%s_report_result.xml' % str(data_rep['name']))
            rep_file.write(rep_file_name, data_rep)
            log.info(u'Сохранение отчета в файл <%s>' % rep_file_name)
            return rep_file_name
        return None
        
    def preview(self, report=None):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            # Открыть excel в режиме просмотра
            self.previewExcel(xml_rep_file_name)
            
    def previewExcel(self, xml_filename):
        """
        Открыть excel  в режиме предварительного просмотра.

        :param xml_filename: Имя xml файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Скрыть Excel
            excel_app.Visible = 0
            # Закрыть все книги
            excel_app.Workbooks.Close()
            # Открыть
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Показать Excel
            excel_app.Visible = 1
            
            excel_app.ActiveWindow.ActiveSheet.PrintPreview()
            return True
        except pythoncom.com_error:
            # Вывести сообщение об ошибке в лог
            log.fatal()
            return False

    def print(self, report=None):
        """
        Печать.

        :param report: Полное описание шаблона отчета.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            # Открыть печать в excel
            self.printExcel(xml_rep_file_name)

    def printExcel(self, xml_filename):
        """
        Печать отчета с помощью excel.

        :param xml_filename: Имя xml файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Скрыть Excel
            excel_app.Visible = 0
            # Закрыть все книги
            excel_app.Workbooks.Close()
            # Открыть
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Показать Excel
            excel_app.Visible = 1
            return True
        except pythoncom.com_error:
            # Вывести сообщение об ошибке в лог
            log.fatal()
            return False
            
    def setPageSetup(self):
        """
        Установка параметров страницы.
        """
        pass

    def convert(self, report=None, to_xls_filename=None, *args, **kwargs):
        """
        Вывод результатов отчета в Excel.

        :param report: Полное описание шаблона отчета.
        :param to_xls_filename: Имя файла, куда необходимо сохранить отчет.
        """
        xml_rep_file_name = self._genXMLReport(report)
        if xml_rep_file_name:
            # Excel
            self.openExcel(xml_rep_file_name)

    def openExcel(self, xml_filename):
        """
        Открыть excel.

        :param xml_filename: Имя xml файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Excel
            excel_app = win32com.client.Dispatch('Excel.Application')
            # Скрыть Excel
            excel_app.Visible = 0
            # Закрыть все книги
            excel_app.Workbooks.Close()
            # Открыть
            rep_tmpl_book = excel_app.Workbooks.Open(xml_filename)
            # Показать Excel
            excel_app.Visible = 1
            return True
        except pythoncom.com_error:
            # Вывести сообщение об ошибке в лог
            log.fatal()
            return False

    def edit(self, rep_filename=None):
        """
        Редактирование отчета.

        :param rep_filename: Полное имя файла шаблона отчета.
        """
        # Определить файл *.xml
        xml_file = os.path.abspath(os.path.splitext(rep_filename)[0]+'.xml')
        cmd = 'start excel.exe \"%s\"' % xml_file
        # и запустить MSExcel
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

            query_tbl = self.getQueryTbl(self._Rep)
            if not query_tbl or not query_tbl['__data__']:
                if not config.get_glob_var('NO_GUI_MODE'):
                    if dlg.getAskBox(u'Внимание',
                                     u'Нет данных, соответствующих запросу: %s. Продолжить генерацию отчета?' % self._Rep['query']):
                        return None
                else:
                    log.warning(u'Пустая таблица запроса. Продолжение генерации.')
                query_tbl = self.createEmptyQueryTbl()

            # 2. Запустить генерацию
            rep = icrepgen.icReportGenerator()
            data_rep = rep.generate(self._Rep, query_tbl)

            return data_rep
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета <%s>.' % self._Rep['name'])
        return None
