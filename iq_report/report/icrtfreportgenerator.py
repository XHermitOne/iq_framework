#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль системы генератора отчетов, основанные на генерации RTF файлов.
"""

# --- Подключение библиотек ---
import os 
import os.path
import copy
import re

from ic.report import rtf_report
from ic.report import icrepgensystem
from ic.std.dlg import dlg

from ic.std.log import log

__version__ = (0, 1, 1, 2)

# --- Константы ---
RTF_VAR_PATTERN = r'(#.*?#)'
# Список всех патернов используемых при разборе значений ячеек
ALL_PATERNS = [RTF_VAR_PATTERN]


class icRTFReportGeneratorSystem(icrepgensystem.icReportGeneratorSystem):
    """
    Класс системы генерации отчетов, основанные на генерации RTF файлов.
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
        return self._report_dir

    def _genRTFReport(self, report):
        """
        Генерация отчета и сохранение его в RTF файл.

        :param report: Полное описание шаблона отчета.
        :return: Возвращает имя rtf файла или None в случае ошибки.
        """
        if report is None:
            report = self._Rep
        data_rep = self.generateReport(report)
        if data_rep:
            rep_file_name = os.path.join(self.getReportDir(), '%s_report_result.rtf' % data_rep['name'])
            template_file_name = os.path.abspath(data_rep['generator'], self.getReportDir())
            log.info(u'Сохранение отчета %s в файл %s' % (template_file_name, rep_file_name))
            
            data = self._predGenerateAllVar(data_rep['__data__'])
            rtf_report.genRTFReport(data, rep_file_name, template_file_name)
            return rep_file_name
        return None
        
    def preview(self, report=None):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        rtf_rep_file_name = self._genRTFReport(report)
        if rtf_rep_file_name:
            # Открыть в режиме просмотра
            self.previewWord(rtf_rep_file_name)
            
    def previewWord(self, rtf_filename):
        """
        Открыть word  в режиме предварительного просмотра.

        :param rtf_filename: Имя rtf файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Скрыть
            word_app.Visible = 0
            # Открыть
            rep_tmpl_book = word_app.Documents.Open(rtf_filename)
            # Показать
            word_app.Visible = 1
            
            rep_tmpl_book.PrintPreview()
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
        rtf_rep_file_name = self._genRTFReport(report)
        if rtf_rep_file_name:
            # Открыть печать
            self.printWord(rtf_rep_file_name)

    def printWord(self, rtf_filename):
        """
        Печать отчета с помощью word.

        :param rtf_filename: Имя rtf файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Скрыть
            word_app.Visible = 0
            # Открыть
            rep_tmpl_book = word_app.Documents.Open(rtf_filename)
            # Показать
            word_app.Visible = 1
            
            rep_tmpl_book.PrintOut()
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
        pass

    def openWord(self, rtf_filename):
        """
        Открыть word.

        :param rtf_filename: Имя rtf файла, содержащего сгенерированный отчет.
        """
        try:
            # Установить связь с Word
            word_app = win32com.client.Dispatch('Word.Application')
            # Скрыть
            word_app.Visible = 0
            # Открыть
            rep_tmpl_book = word_app.Open(rtf_filename)
            # Показать
            word_app.Visible = 1
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
        # Определить файл *.rtf
        rtf_file = os.path.abspath(os.path.splitext(rep_filename)[0]+'.rtf')
        cmd = 'start word.exe \'%s\'' % rtf_file
        log.info(u'Выполнение комманды ОС <%s>' % cmd)
        # и запустить MSWord
        os.system(cmd)

    def generateReport(self, report=None):
        """
        Запустить генератор отчета.

        :param report: Шаблон отчета.
        :return: Возвращает сгенерированный отчет или None в случае ошибки.
        """
        try:
            if report is not None:
                self._Rep = report

            # 1. Получить таблицу запроса
            # Данные отчета.
            # Формат:
            # {
            #    #Переменные
            #    '__variables__':{'имя переменной1':значение переменной1,...}, #Переменные
            #    #Список таблиц
            #    '__tables__':[
            #        {
            #        '__fields__':(('имя поля1'),...), #Поля
            #        '__data__':[(значение поля1,...)], #Данные
            #        },...
            #        ],
            #    #Циклы генерации
            #    '__loop__':{
            #        'имя цикла1':[{переменные и таблицы, используемые в цикле},...],
            #        ...
            #        },
            # }.

            query_data = self.GetQueryTbl(self._Rep)
            if not query_data:
                dlg.getWarningBox(u'Внимание',
                                  u'Нет данных, соответствующих запросу: %s' % self._Rep['query'],
                                  parent=self._ParentForm)
                return None

            # 2. Запустить генерацию
            rep_data = copy.deepcopy(self._Rep)
            rep_data['__data__'] = query_data
            return rep_data
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета %s.' % self._Rep['name'])
            return None

    def _predGenerateAllVar(self, data):
        """
        Предобработка всех переменных. Выполняется рекурсивно.

        :return: Возвращает структуры с заполненными переменными.
        """
        if '__variables__' in data:
            # Сделать предобработку
            data['__variables__'] = self._predGenerateVar(data['__variables__'])
        if '__loop__' in data:
            for loop_name, loop_body in data['__loop__'].items():
                if loop_body:
                    for i_loop in range(len(loop_body)):
                        loop_body[i_loop] = self._predGenerateAllVar(loop_body[i_loop])
                    data['__loop__'][loop_name] = loop_body
        return data

    def _predGenerateVar(self, variables, value=None):
        """
        Предобработка словаря переменных.

        :param variables: Словарь переменных.
        :param value: Текущее обработываемое значение.
        """
        if value is None:
            for name, value in variables.items():
                variables[name] = self._predGenerateVar(variables, str(value))
            return variables
        else:
            # Сначала заменить перевод каретки
            value = value.replace('\r\n', '\n').strip()
            # Затем распарсить
            parsed = self._funcTextParse(value)
            values = []
            for cur_var in parsed['func']:
                if re.search(RTF_VAR_PATTERN, cur_var):
                    if cur_var[1:-1] in variables:
                        values.append(self._predGenerateVar(variables,
                                                            variables[cur_var[1:-1]]))
                    else:
                        values.append('')
                else:
                    log.warning(u'Не известный тег <%s>' % cur_var)
            # Заполнить формат
            val_str = self._valueFormat(parsed['fmt'], values)
            return val_str

    def _funcTextParse(self, text, patterns=ALL_PATERNS):
        """
        Разобрать строку на формат и исполняемый код.

        :param text: Разбираемая строка.
        :param patterns: Cписок строк патернов тегов обозначения
            начала и конца функционала.
        :return: Возвращает словарь следующей структуры:
            {
            'fmt': Формат строки без строк исполняемого кода вместо него стоит %s;
            'func': Список строк исполняемого кода.
            }
            В случае ошибки возвращает None.
        """
        try:
            # Инициализация структуры
            ret = {}
            ret['fmt'] = ''
            ret['func'] = []
    
            # Проверка аргументов
            if not text:
                return ret
    
            # Заполнение патерна
            pattern = r''
            for cur_sep in patterns:
                pattern += cur_sep
                if cur_sep != patterns[-1]:
                    pattern += r'|'
                    
            # Разбор строки на обычные строки и строки функционала
            parsed_str = [x for x in re.split(pattern, text) if x is not None]
            # Перебор тегов
            for i_parse in range(len(parsed_str)):
                # Перебор патернов функционала
                func_find = False
                for cur_patt in patterns:
                    # Какой-то функционал
                    if re.search(cur_patt, parsed_str[i_parse]):
                        ret['func'].append(parsed_str[i_parse])
                        # И добавить в формат %s
                        ret['fmt'] += '%s'
                        func_find = True
                        break
                # Обычная строка
                if not func_find:
                    ret['fmt'] += parsed_str[i_parse]
            return ret
        except:
            # win32api.MessageBox(0, '%s' % (sys.exc_info()[1].args[1]))
            log.fatal()
        return None

    def _valueFormat(self, fmt, data_list):
        """
        Заполнение формата значения ячейки.
        
        :param fmt: Формат.
        :param data_list: Данные, которые нужно поместить в формат.
        :return: Возвращает строку, соответствующую формату.
        """
        # Заполнение формата
        if data_list == list():
            value = fmt
        # Обработка значения None
        elif bool(None in data_list):
            data_lst = [{None: ''}.setdefault(val, val) for val in data_list]
            value = fmt % tuple(data_lst)
        else:
            value = fmt % tuple(data_list)
        return value
