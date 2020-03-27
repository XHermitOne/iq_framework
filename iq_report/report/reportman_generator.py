#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль системы генератора отчетов ReportManager.
"""

# --- Подключение библиотек ---
import os
import os.path


from ic.report import icrepgensystem
from ic.std.utils import resfunc
from ic.std.utils import utilfunc
from ic.std.utils import execfunc
from ic.std.dlg import dlg
from ic.std.log import log

# PyReportManager - the ActiveX wrapper code
try:
    from ic.report import reportman
except ImportError:
    log.error(u'Ошибка импорта PyReportManager', bForcePrint=True)


__version__ = (0, 1, 1, 2)

# --- Константы подсистемы ---
DEFAULT_REP_FILE_NAME = 'c:/temp/new_report.rep'


# --- Описания классов ---
class icReportManagerGeneratorSystem(icrepgensystem.icReportGeneratorSystem):
    """
    Класс системы генерации отчетов ReportManager.
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
        
    def getReportDir(self):
        """
        Папка отчетов.
        """
        return self._report_dir

    def preview(self, report=None):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        if report is None:
            report = self._Rep
        # Создание связи с ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Параметры отчета
            params = self._getReportParameters(report)
            # Установка параметров
            self._setReportParameters(report_manager, params)
            # Вызов предварительного просмотра
            report_manager.preview(u'Предварительный просмотр: %s' % report_file)
        except:
            log.fatal(u'Ошибка передварительного просмотра отчета %s' % report_file)
            
    def print(self, report=None):
        """
        Печать.

        :param report: Полное описание шаблона отчета.
        """
        if report is None:
            report = self._Rep
        # Создание связи с ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Параметры отчета
            params = self._getReportParameters(report)
            # Установка параметров
            self._setReportParameters(report_manager, params)
            # Вызов предварительного просмотра
            report_manager.printout(u'Печать: %s' % report_file, True, True)
        except:
            log.fatal(u'Ошибка печати отчета %s' % report_file)

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
        if report is None:
            report = self._Rep
        # Создание связи с ActiveX
        report_dir = os.path.abspath(self.getReportDir())
        report_file = os.path.join(report_dir, report['generator'])
        try:
            report_manager = reportman.ReportMan(report_file)
            # Параметры отчета
            params = self._getReportParameters(report)
            # Установка параметров
            self._setReportParameters(report_manager, params)
            # Вызов предварительного просмотра
            report_manager.execute()
        except:
            log.fatal(u'Ошибка конвертирования отчета %s' % report_file)

    def edit(self, rep_filename=None):
        """
        Редактирование отчета.

        :param rep_filename: Полное имя файла шаблона отчета.
        """
        # Создание связи с ActiveX
        rprt_file_name = os.path.abspath(rep_filename)
        rep = resfunc.loadResource(rprt_file_name)
        report_dir = os.path.abspath(self.getReportDir())
        rep_file = os.path.join(report_dir, rep['generator'])
        
        reportman_designer_key = utilfunc.getRegValue('Software\\Classes\\Report Manager Designer\\shell\\open\\command',
                                                      None)
        if reportman_designer_key:
            reportman_designer_run = reportman_designer_key.replace('\'%1\'', '\'%s\'') % rep_file
            cmd = 'start %s' % reportman_designer_run
            log.debug(u'Запуск команды ОС: <%s>' % cmd)
            # и запустить Report Manager Designer
            os.system(cmd)
        else:
            msg = u'Не определен дизайнер отчетов Report Manager Designer %s' % reportman_designer_key
            log.warning(msg)
            dlg.getWarningBox(u'ВНИМАНИЕ!', msg)

        # Определить файл *.xml
        xml_file = os.path.normpath(os.path.abspath(os.path.splitext(rep_filename)[0]+'.xml'))
        cmd = 'start excel.exe \'%s\'' % xml_file
        log.debug(u'Запуск команды ОС: <%s>' % cmd)
        # и запустить MSExcel
        os.system(cmd)

    def _getReportParameters(self, report=None):
        """
        Запустить генератор отчета.

        :param report: Шаблон отчета.
        :return: Возвращает словарь параметров. {'Имя параметра отчета':Значение параметра отчета}.
        """
        try:
            if report is not None:
                self._Rep = report
            else:
                report = self._Rep

            # 1. Получить параметры запроса отчета
            query = report['query']
            if query is not None:
                if self._isQueryFunc(query):
                    query = self._execQueryFunc(query)
                else:
                    query = execfunc.exec_code(query)
                
            return query
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения параметров отчета %s.' % report['name'])
            return None

    def _setReportParameters(self, report_obj, parameters):
        """
        Установить параметры для отчета.

        :param report_obj: Объект отчета ReportManger.
        :param parameters: Словарь параметров. {'Имя параметра отчета':Значение параметра отчета}.
        :return: Возвращает результат выполнения операции.
        """
        try:
            if parameters:
                for param_name, param_value in parameters.items():
                    report_obj.set_param(param_name, param_value)
            return True
        except:
            log.fatal(u'Ошибка установки параметров %s в отчете %s' % (parameters, report_obj._report_filename))
            return False
