#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль функций системы генератора отчетов.

В качестве ключей таблицы запроса могут быть:
    '__variables__': Словарь переменных отчета,
    '__coord_fill__': Словарь координатных замен,
    '__sql__': SQL выражения указания таблицы запроса,
        ВНИМАНИЕ! SQL выражение задается без сигнатуры SQL_SIGNATURE.
            Просто в виде SQL выражения типа <SELECT>,
    '__fields__': Список описаний полей таблицы запроса.
    '__data__': Список записей таблицы запроса,

Все эти ключи обрабатываются в процессе генерации отчета.
"""

# Подключение библиотек
import os
import os.path
import re
import shutil
import sqlalchemy

from ic.std.utils import execfunc
from ic.std.log import log
from ic.std.utils import filefunc
from ic.std.utils import resfunc
from ic.std.dlg import dlg
from ic.std.utils import textfunc
from ic.std.utils import txtgen

from ic.report import icreptemplate

__version__ = (0, 1, 1, 2)

# Константы подсистемы
DEFAULT_REP_TMPL_FILE = os.path.join(os.path.dirname(__file__), 'new_report_template.ods')

OFFICE_OPEN_CMD_FORMAT = 'libreoffice %s'

ODS_TEMPLATE_EXT = '.ods'
XLS_TEMPLATE_EXT = '.xls'
XML_TEMPLATE_EXT = '.xml'
DEFAULT_TEMPLATE_EXT = ODS_TEMPLATE_EXT
DEFAULT_REPORT_TEMPLATE_EXT = '.rprt'

DEFAULT_REPORT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/reports/')

# Сигнатуры значений бендов отчета (Длина сигнатуры д.б. 4 символа)
DB_URL_SIGNATURE = 'URL:'
SQL_SIGNATURE = 'SQL:'
CODE_SIGNATURE = 'PRG:'
PY_SIGNATURE = 'PY:'


class icReportGeneratorSystem(object):
    """
    Класс системы генерации отчетов. Абстрактный класс.
    """

    def __init__(self, report=None, parent=None):
        """
        Конструктор класса.

        :param report: Шаблон отчета.
        :param parent: Родительская форма, необходима для вывода сообщений.
        """
        # Шаблон отчета
        self._Rep = report
        # Таблица запроса
        self._QueryTab = None

        # Родительская форма, необходима для вывода сообщений.
        self._ParentForm = parent

        # Предварительный просмотр
        self.PrintPreview = None

    def getReportDir(self):
        """
        Папка отчетов.
        """
        return DEFAULT_REPORT_DIR

    def getProfileDir(self):
        """
        Папка профиля программы.
        """
        return filefunc.getProfilePath()

    def getGeneratorType(self):
        """
        Тип системы генерации отчетов.
        """
        my_generator_type = self._Rep.get('generator', None) if self._Rep else None
        if my_generator_type is None:
            log.warning(u'Не удалось определить тип системы генерации отчетов в <%s>' % self.__class__.__name__)
        elif isinstance(my_generator_type, str):
            my_generator_type = my_generator_type.lower()
        return my_generator_type

    def sameGeneratorType(self, generator_type):
        """
        Проверка на тот же тип системы генерации отчетов что и указанный.

        :param generator_type: Тип системы генерации отчетов.
            Тип задается расширением файла источника шаблона.
            Обычно '.ods', '.xml', 'xls' и т.п.
        :return: True/False
        """
        my_generator_type = self.getGeneratorType()
        return my_generator_type == generator_type.lower()

    def getReportDescription(self):
        """
        Описание отчета.

        :return: Строку описание отчета или его имя если описание не
            определено.
        """
        description = u''
        if self._Rep:
            description = self._Rep.get('description', self._Rep.get('name', u''))
        return description

    def setParentForm(self, parent):
        """
        Установить родительскую форму для определения папки отчетов.
        """
        self._ParentForm = parent
        
    def getParentForm(self):
        """
        Родительская форма.
        """
        return self._ParentForm
        
    def reloadRepData(self, tmpl_filename=None):
        """
        Перегрузить данные отчета.

        :param tmpl_filename: Имя файла шаблона отчета.
        """
        self._Rep = resfunc.loadResourceFile(tmpl_filename, bRefresh=True)
        
    def setRepData(self, report):
        """
        Установить данные отчета.
        """
        self._Rep = report

    def selectAction(self, report=None, *args, **kwargs):
        """
        Запуск генерации отчета с последующим выбором действия.

        :param report: Полное описание шаблона отчета.
        """
        return

    def preview(self, report=None, *args, **kwargs):
        """
        Предварительный просмотр.

        :param report: Полное описание шаблона отчета.
        """
        return

    def print(self, report=None, *args, **kwargs):
        """
        Печать.

        :param report: Полное описание шаблона отчета.
        """
        return 

    def setPageSetup(self):
        """
        Установка параметров страницы.
        """
        return

    def convert(self, report=None, to_filename=None, *args, **kwargs):
        """
        Конвертирование результатов отчета.

        :param report: Полное описание шаблона отчета.
        :param to_filename: Имя файла, куда необходимо сохранить отчет.
        """
        return

    def export(self, report=None, to_filename=None, *args, **kwargs):
        """
        Вывод результатов отчета во внешнюю программу.

        :param report: Полное описание шаблона отчета.
        :param to_filename: Имя файла, куда необходимо сохранить отчет.
        """
        return self.convert(report, to_filename)

    def createNew(self, dst_path=None):
        """
        Создание нового отчета.

        :param dst_path: Результирующая папка, в которую будет помещен новый файл.
        """
        return self.createNewByOffice(dst_path)
        
    def createNewByOffice(self, dst_path=None):
        """
        Создание нового отчета средствами LibreOffice Calc.

        :param dst_path: Результирующая папка, в которую будет помещен новый файл.
        """
        try:
            src_filename = DEFAULT_REP_TMPL_FILE
            new_filename = dlg.getTextInputDlg(self._ParentForm,
                                               u'Создание нового файла',
                                               u'Введите имя файла шаблона отчета')
            if os.path.splitext(new_filename)[1] != '.ods':
                new_filename += '.ods'

            if dst_path is None:
                # Необходимо определить результирующий путь
                dst_path = dlg.getDirDlg(self._ParentForm,
                                         u'Папка хранения')
                if not dst_path:
                    dst_path = os.getcwd()

            dst_filename = os.path.join(dst_path, new_filename)
            if os.path.exists(dst_filename):
                if dlg.getAskBox(u'Заменить существующий файл?'):
                    shutil.copyfile(src_filename, dst_filename)
            else:
                shutil.copyfile(src_filename, dst_filename)

            cmd = OFFICE_OPEN_CMD_FORMAT % dst_filename
            log.debug(u'Command <%s>' % textfunc.toUnicode(cmd))
            os.system(cmd)

            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'createNew report template by LibreOffice Calc')

    def edit(self, report=None):
        """
        Редактирование отчета.

        :param report: Полное описание шаблона отчета.
        """
        return

    def update(self, tmpl_filename=None):
        """
        Обновить шаблон отчета в системе генератора отчетов.

        :param tmpl_filename: Имя файла шаблона отчета.
            Если None, то должен производиться запрос на выбор этого файла.
        :return: Имя файла файла шаблона или None в случае ошибки.
        """
        try:
            return self._update(tmpl_filename)
        except:
            log.fatal(u'Ошибка обновления шаблона <%s>' % tmpl_filename)
        return None

    def _update(self, tmpl_filename=None):
        """
        Обновить шаблон отчета в системе генератора отчетов.

        :param tmpl_filename: Имя файла шаблона отчета.
            Если None, то должен производиться запрос на выбор этого файла.
        :return: Имя файла файла шаблона или None в случае ошибки.
        """
        if tmpl_filename is None:
            filename = dlg.getFileDlg(parent=self._ParentForm,
                                      title=u'Выберите шаблон отчета:',
                                      wildcard=u'Электронные таблицы ODF (*.ods)|*.ods|Microsoft Excel 2003 XML (*.xml)|*.xml',
                                      default_path=self.getReportDir())
        else:
            filename = os.path.abspath(os.path.normpath(tmpl_filename))

        if os.path.isfile(filename):
            # Конвертация
            log.debug(u'Начало конвертации <%s>' % filename)
            tmpl_filename = None
            template = None
            if os.path.exists(os.path.splitext(filename)[0] + DEFAULT_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + DEFAULT_TEMPLATE_EXT
                template = icreptemplate.icODSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + ODS_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + ODS_TEMPLATE_EXT
                template = icreptemplate.icODSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + XLS_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + XLS_TEMPLATE_EXT
                template = icreptemplate.icXLSReportTemplate()
            elif os.path.exists(os.path.splitext(filename)[0] + XML_TEMPLATE_EXT):
                tmpl_filename = os.path.splitext(filename)[0] + XML_TEMPLATE_EXT
                template = icreptemplate.icExcelXMLReportTemplate()
            else:
                log.warning(u'Не найден шаблон отчета <%s>' % filename)

            new_filename = None
            if template:
                rep_template = template.read(tmpl_filename)
                new_filename = os.path.splitext(filename)[0]+DEFAULT_REPORT_TEMPLATE_EXT
                resfunc.saveResourcePickle(new_filename, rep_template)
            log.info(u'Конец конвертации')
            return new_filename
        else:
            log.warning(u'Не найден файл источника шаблона <%s>' % filename)
        return None
   
    def openModule(self, tmpl_filename=None):
        """
        Открыть модуль отчета в редакторе.
        """
        if tmpl_filename is None:
            log.warning(u'Не определен файл модуля отчета')
        # Определить файл *.xml
        module_file = os.path.abspath(os.path.splitext(tmpl_filename)[0]+'.py')
        if os.path.exists(module_file):
            try:
                self._ParentForm.GetParent().ide.OpenFile(module_file)
            except:
                log.fatal(u'Ошибка открытия модуля <%s>' % module_file)
        else:
            dlg.getMsgBox(u'Файл модуля отчета <%s> не найден.' % module_file)
        
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
        return None

    def generateReport(self, report=None, *args, **kwargs):
        """
        Запустить генератор отчета.

        :param report: Шаблон отчета.
        :return: Возвращает сгенерированный отчет или None в случае ошибки.
        """
        return None

    def initRepTemplate(self, report, QueryTab_=None):
        """
        Прочитать данные о шаблоне отчета.

        :param report: Полное описание шаблона отчета.
        :param QueryTab_: Таблица запроса.
        """
        # 1. Прочитать структру отчета
        self._Rep = report
        # 2. Таблица запроса
        self._QueryTab = QueryTab_

        # 3. Скорректировать шаблон для нормальной обработки генератором
        self._Rep = self.RepSQLObj2SQLite(self._Rep, resfunc.loadResourceFile(resfunc.icGetTabResFileName()))

        # 5. Коррекция параметров БД и запроса
        # self._Rep['data_source'] = ic_exec.ExecuteMethod(self._Rep['data_source'], self)
        # self._Rep['query'] = ic_exec.ExecuteMethod(self._Rep['query'], self)

        # !!! ВНИМАНИЕ!!!
        # --- Проверка случая когда функция  запроса возвращает SQL запрос ---
        # if type(self._Rep['query'])==type(''):
        #     self._Rep['query']=ic.db.tabrestr.icQueryTxtSQLObj2SQLite(self._Rep['query'],\
        #         ic.utils.util.readAndEvalFile(ic.utils.resource.icGetTabResFileName()))

    def _getSQLQueryTable(self, report, db_url=None, sql=None):
        """
        Получить таблицу запроса.

        :param report: Шаблон отчета.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Текст SQL запроса.
        :return: Функция возвращает словарь -
            ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ 
            {'__fields__':имена полей таблицы,'__data__':данные таблицы}
        """
        result = None
        # Инициализация
        db_connection = None
        try:
            if not db_url:
                data_source = report['data_source']

                if not data_source:
                    # Учет случая когда источник данных не определен
                    log.warning(u'Не определен источник данных в отчете')
                    return {'__fields__': list(), '__data__': list()}

                signature = data_source[:4].upper()
                if signature != DB_URL_SIGNATURE:
                    log.warning('Not support DB type <%s>' % signature)
                    return result
                # БД задается с помощью стандартного DB URL
                db_url = data_source[4:].lower().strip()

            log.info(u'Связь с БД <%s>' % db_url)
            # Установить связь с БД
            db_connection = sqlalchemy.create_engine(db_url)
            # Освободить БД
            # db_connection.dispose()
            log.info(u'SQL <%s>' % textfunc.toUnicode(sql, 'utf-8'))
            sql_result = db_connection.execute(sql)
            rows = sql_result.fetchall()
            cols = rows[0].keys() if rows else []

            # Закрыть связь
            db_connection.dispose()
            db_connection = None

            # ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ
            # {'__fields__':имена полей таблицы,'__data__':данные таблицы} !!!
            result = {'__fields__': cols, '__data__': list(rows)}
            return result
        except:
            if db_connection:
                # Закрыть связь
                db_connection.dispose()

            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения таблицы SQL запроса <%s>.' % sql)
            log.error(u'''ВНИМАНИЕ! Если возникает ошибка в модуле:
        ----------------------------------------------------------------------------------------------
        File "/usr/lib/python2.7/dist-packages/sqlalchemy/engine/default.py", line 324, in do_execute
            cursor.execute(statement, parameters)
        TypeError: 'dict' object does not support indexing
        ----------------------------------------------------------------------------------------------        
        Это означает что SQLAlchemy не может распарсить SQL выражение. 
        Необходимо вместо <%> использовать <%%> в SQL выражении. 
                    ''')

        return None

    def _isQueryFunc(self, query):
        """
        Определить представлен запрос в виде функции?

        :param query: Текст запроса.
        :return: True/False.
        """
        return query and isinstance(query, str) and query.startswith(PY_SIGNATURE)

    def _execQueryFunc(self, query, vars=None):
        """
        Получить запрос из функции.

        :param query: Текст запроса.
        :param vars: Внешние переменные.
        :return: Возвращает запрос в разрешенном формате.
        """
        # Убрать сигнатуру определения функции
        func = query.replace(PY_SIGNATURE, '').strip()
        var_names = vars.keys() if vars else None
        log.debug(u'Выполнение функции: <%s>. Дополнительные переменные %s' % (func, var_names))
        return execfunc.exec_code(func, name_space=locals(), kwargs=vars)

    def _isEmptyQueryTbl(self, query_tbl):
        """
        Проверка пустой таблицы запроса.

        :param query_tbl: Словарь таблицы запроса.
        :return: True - пустая таблица запроса.
            False - есть данные.
        """
        if not query_tbl:
            return True
        # Есть переменные?
        elif isinstance(query_tbl, dict) and '__variables__' in query_tbl and query_tbl['__variables__']:
            return False
        # Есть координатные замены?
        elif isinstance(query_tbl, dict) and '__coord_fill__' in query_tbl and query_tbl['__coord_fill__']:
            return False
        # Есть данные табличной части?
        elif isinstance(query_tbl, dict) and '__data__' in query_tbl and query_tbl['__data__']:
            return False
        return True

    def createEmptyQueryTbl(self):
        """
        Создать пустую таблицу запроса.
        В случае постой таблицы запроса генерация не должна прекращаться.

        :return: Функция возвращает словарь -
            ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ
            {'__fields__': (), '__data__': []}
        """
        return {'__fields__': (), '__data__': []}

    def getQueryTbl(self, report, db_url=None, sql=None, *args, **kwargs):
        """
        Получить таблицу запроса.

        :param report: Шаблон отчета.
        :param db_url: Connection string в виде url. Например
            postgresql+psycopg2://postgres:postgres@10.0.0.3:5432/realization.
        :param sql: Запрос SQL.
            ВНИМАНИЕ! В начале SQL запроса должна стоять сигнатура:
            <SQL:> - Текст SQL запроса
            <PY:> -  Запрос задается функцией Python
            <PRG:> - Запрос задается внешней функцией Python.
        :return: Функция возвращает словарь -
            ТАБЛИЦА ЗАПРОСА ПРЕДСТАВЛЯЕТСЯ В ВИДЕ СЛОВАРЯ 
            {'__fields__':описания полей таблицы,'__data__':данные таблицы}
        """
        query = None
        try:
            if sql:
                query = sql
            else:
                # !!! ВНИМАНИЕ!!!
                # Проверка случая когда функция  запроса возвращает таблицу
                if isinstance(report['query'], dict):
                    return report['query']
                elif self._isQueryFunc(report['query']):
                    variables = kwargs.get('variables', None)
                    query = self._execQueryFunc(report['query'], vars=variables)

                    # Если метод возвращает уже сгенерированную таблицу запроса,
                    # то просто вернуть ее
                    if isinstance(query, dict):
                        if '__sql__' in query:
                            dataset_dict = self._getSQLQueryTable(report=report,
                                                                  db_url=db_url,
                                                                  sql=query['__sql__'])
                            if isinstance(dataset_dict, dict):
                                query.update(dataset_dict)
                        return query
                else:
                    query = report['query']
                # Обработка когда запрос вообще не определен
                if query is None:
                    log.warning(u'Запрос отчета не определен')
                    return None

                if query.startswith(SQL_SIGNATURE):
                    # Запрос задается SQL выражением
                    query = query.replace(SQL_SIGNATURE, u'').strip()
                elif query.startswith(CODE_SIGNATURE):
                    # Запрос задается функцией Python
                    query = execfunc.exec_code(query.replace(CODE_SIGNATURE, u'').strip())
                elif query.startswith(PY_SIGNATURE):
                    # Запрос задается функцией Python
                    query = execfunc.exec_code(query.replace(PY_SIGNATURE, u'').strip())
                else:
                    log.warning(u'Не указана сигнатура в запросе <%s>' % query)
                    return None
                # ВНИМАНИЕ! Запрос может параметризироваться переменными передаваемыми
                # явным образом. Поэтому необходимо произвести генерацию
                if kwargs:
                    try:
                        # Для замен используем другой генератор
                        # необходимо только заменить открывающий и закрывающие сигнатуры тега
                        query_txt = query.replace(u'[&', u'{{ ').replace(u'&]', u' }}')
                        query = txtgen.gen(query_txt, kwargs)
                    except:
                        log.fatal(u'Ошибка преобразования запроса\n<%s>\nпри получении таблицы запроса для отчета' % str(query))

            query_tbl = None
            if not self._QueryTab:
                # Таблица запроса определена в виде SQL
                query_tbl = self._getSQLQueryTable(report, db_url=db_url, sql=query)
            else:
                # Если таблица запроса указана конкретно, то обработать ее
                # Указано имя таблицы запроса
                if isinstance(self._QueryTab, str):
                    if self._QueryTab[:4].upper() == SQL_SIGNATURE:
                        # Обработка обычного SQL запроса
                        query_tbl = self._getSQLQueryTable(report, sql=self._QueryTab[4:].strip())
                    else:
                        log.warning(u'Не поддерживаемый тип запроса <%s>' % self._QueryTab)
                # Таблица уже просто определена как DataSet
                elif isinstance(self._QueryTab, dict):
                    query_tbl = self._QueryTab
                else:
                    log.warning(u'Не поддерживаемый тип запроса <%s>' % type(self._QueryTab))
            return query_tbl
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка определения таблицы запроса <%s>.' % query)
        return None

    def RepSQLObj2SQLite(self, report, res_table):
        """
        Преобразование имен в шаблоне отчета в контексте SQLObject в имена в
            контексте sqlite.

        :param report: Щаблон отчета.
        :param res_table: Ресурсное описание таблиц.
        """
        try:
            rep = report
            # Для корректной обработки имен полей и таблиц они д.б.
            # отсортированны по убыванию длин имен классов данных
            data_class_names = res_table.keys()
            data_class_names.sort()
            data_class_names.reverse()

            # Обработка шаблона отчета
            # 1. Верхний и нижний колонтитулы
            # Перебор ячеек
            for row in rep['upper']:
                for cell in row:
                    if cell:
                        # Перебор классов
                        for data_class_name in data_class_names:
                            cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
                                                                                res_table[data_class_name]['scheme'])
            # Перебор ячеек
            for row in rep['under']:
                for cell in row:
                    if cell:
                        # Перебор классов
                        for data_class_name in data_class_names:
                            cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
                                                                                res_table[data_class_name]['scheme'])
            # 2. Лист шаблона
            # Перебор ячеек
            for row in rep['sheet']:
                for cell in row:
                    if cell:
                        # Перебор классов
                        for data_class_name in data_class_names:
                            cell['value'] = ic.db.tabrestr.icNamesSQLObj2SQLite(cell['value'], data_class_name,
                                                                                res_table[data_class_name]['scheme'])
            # 3. Описание групп
            for grp in rep['groups']:
                for data_class_name in data_class_names:
                    grp['field'] = ic.db.tabrestr.icNamesSQLObj2SQLite(grp['field'], data_class_name,
                                                                       res_table[data_class_name]['scheme'])

            return rep
        except:
            return report

    def previewResult(self, report_data=None):
        """
        Предварительный просмотр.

        :param report_data: Сгенерированный отчет.
        """
        return

    def printResult(self, report_data=None):
        """
        Печать.

        :param report_data: Сгенерированный отчет.
        """
        return

    def convertResult(self, report_data=None, to_filename=None):
        """
        Конвертирование результатов отчета.

        :param report_data: Сгенерированный отчет.
        :param to_filename: Имя результирующего файла.
        """
        return

    def save(self, report_data=None):
        """
        Сохранить результаты генерации в файл

        :param report_data: Сгенерированный отчет.
        :return: Имя сохраненного файла или None, если сохранения не произошло.
        """
        return None
