#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль генератора отчетов.

В ячейках шаблона отчета можон ставить следующие теги:
["..."] - Обращение к полю таблицы запроса.

[&...&] - Обращение к переменной отчета.
Переменные отчета могут задаваться в таблице запроса
в виде словаря по ключу '__variables__'.

[@package.module.function()@] - Вызов функции прикладного программиста.

[=...=] - Исполнение блока кода.
Системные переменные блока кода:
    value - Значение записываемое в ячейку
    record - Словарь текущей записи таблицы запроса
Например:
    [=value=record['dt'].strftime('%B')=]
    [=new_cell['color']=dict(background=(128, 0 , 0)) if record['is_alarm'] else None; value=record['field_name']=]

[^...^] - Системные функции генератора.
Например: 
    [^N^] - Номер строки табличной части.
    [^SUM(record['...'])^] или [^SUM({имя поля})^] - Суммирование по полю.
    [^AVG(record['...'])^] или [^AVG({имя поля})^] - Вычисление среднего значения по полю.

[*...*] - Установка стиля генерации.
"""

# Подключение библиотек
import time
import re
import copy

from ic.std.log import log
from ic.std.utils import textfunc
from ic.std.utils import execfunc

__version__ = (0, 1, 2, 2)

# Константы
# Ключевые теги для обозначения:
# значения поля таблицы запроса
REP_FIELD_PATT = r'(\[\'.*?\'\])'
# функционала
REP_FUNC_PATT = r'(\[@.*?@\])'
# выражения
REP_EXP_PATT = r'(\[#.*?#\])'
# ламбда-выражения
REP_LAMBDA_PATT = r'(\[~.*?~\])'
# переменной
REP_VAR_PATT = r'(\[&.*?&\])'
# Блок кода
REP_EXEC_PATT = r'(\[=.*?=\])'
# Системные функции
REP_SYS_PATT = r'(\[\^.*?\^\])'
REP_SUM_FIELD_START = '{'   # Теги используются в системной функции
REP_SUM_FIELD_STOP = '}'    # суммирования SUM для обозначения значений полей
# Указание стиля из библиотеки стилей
REP_STYLE_PATT = r'(\[\*.*?\*\])'
# Указание родительского отчета
REP_SUBREPORT_PATT = r'(\[$.*?$\])'

# Список всех патернов используемых при разборе значений ячеек
ALL_PATTERNS = [REP_FIELD_PATT,
                REP_FUNC_PATT,
                REP_EXP_PATT,
                REP_LAMBDA_PATT,
                REP_VAR_PATT,
                REP_EXEC_PATT,
                REP_SYS_PATT,
                REP_STYLE_PATT,
                REP_SUBREPORT_PATT,
                ]
    
# Спецификации и структуры
# Структура шаблона отчета
# Следующие ключи необходимы только для ICReportGenerator'a
IC_REP_TMPL = {'name': '',              # Имя отчета
               'description': '',       # Описание шаблона
               'variables': {},         # Переменные отчета
               'generator': None,       # Генератор
               'data_source': None,     # Указание источника данных/БД
               'query': None,           # Запрос отчета
               'style_lib': None,       # Библиотека стилей
               'header': {},            # Бэнд заголовка отчета (Координаты и размер)
               'footer': {},            # Бэнд подвала/примечания отчета (Координаты и размер)
               'detail': {},            # Бэнд области данных (Координаты и размер)
               'groups': [],            # Список бэндов групп (Координаты и размер)
               'upper': {},             # Бэнд верхнего колонтитула (Координаты и размер)
               'under': {},             # Бэнд нижнего колонтитула (Координаты и размер)
               'sheet': [],             # Лист ячеек отчета (Список строк описаний ячеек)
               'args': {},              # Аргументы для вывода отчета в акцесс
               'page_setup': None,      # Параметры страницы
               }

# Ориентация страницы
IC_REP_ORIENTATION_PORTRAIT = 0     # Книжная
IC_REP_ORIENTATION_LANDSCAPE = 1    # Альбомная

# Параметры страницы
IC_REP_PAGESETUP = {'orientation': IC_REP_ORIENTATION_PORTRAIT,     # Ориентация страницы
                    'start_num': 1,                                 # Начинать нумеровать со страницы...
                    'page_margins': (0, 0, 0, 0),                   # Поля
                    'scale': 100,                                   # Масштаб печати (в %)
                    'paper_size': 9,                                # Размер страницы - 9-A4
                    'resolution': (600, 600),                       # Плотность/качество печати
                    'fit': (1, 1),                                  # Параметры заполнения отчета на листах
                    }

# Структура данных бэнда
IC_REP_BAND = {'row': -1,       # Строка бэнда
               'col': -1,       # Колонка бэнда
               'row_size': -1,  # Размер бэнда по строкам
               'col_size': -1,  # Размер бэнда по колонкам
               }

# Форматы ячеек
REP_FMT_NONE = None     # Не устанавливать формат
REP_FMT_STR = 'S'       # Строковый/текстовый
REP_FMT_TIME = 'T'      # Время
REP_FMT_DATE = 'D'      # Дата
REP_FMT_NUM = 'N'       # Числовой
REP_FMT_FLOAT = 'F'     # Числовой с плавающей точкой
REP_FMT_MISC = 'M'      # Просто какойто формат
REP_FMT_EXCEL = 'X'     # Формат заданный Excel

# Структура ячейки отчета
IC_REP_CELL = {'merge_row': 0,      # Кол-во строк для объединеных ячеек
               'merge_col': 0,      # Кол-во волонок для объединеных ячеек
               'left': 0,           # Координата X
               'top': 0,            # Координата Y
               'width': 10,         # Ширина ячейки
               'height': 10,        # Высота ячейки
               'value': None,       # Текст ячейки
               'font': None,        # Шрифт Структура типа ic.components.icfont.SPC_IC_FONT
               'color': None,       # Цвет
               'border': None,      # Обрамление
               'align': None,       # Расположение текста
               'sum': None,         # Список сумм
               'visible': True,     # Видимость ячейки
               'num_format': None,      # Формат ячейки
               }

# Данные сумм
# ВНИМАНИЕ!!! На каждой итерации текущее значение суммы вычисляется, как value=value+eval(formul)
IC_REP_SUM = {'value': 0,       # Текущее значение суммы
              'formul': '0',    # Формула вычисления сумм
              }

# Цвет
IC_REP_COLOR = {'text': (0, 0, 0),      # Цвет текста
                'background': None,     # Цвет фона
                }

# Обрамление - кортеж из 4-х элементов
IC_REP_BORDER_LEFT = 0
IC_REP_BORDER_TOP = 1
IC_REP_BORDER_BOTTOM = 2
IC_REP_BORDER_RIGHT = 3
IC_REP_BORDER_LINE = {'color': (0, 0, 0),   # Цвет
                      'style': None,        # Стиль
                      'weight': 0,          # Толщина
                      }

# Стили линий обрамления отчета
IC_REP_LINE_SOLID = 0
IC_REP_LINE_SHORT_DASH = 1
IC_REP_LINE_DOT_DASH = 2
IC_REP_LINE_DOT = 3
IC_REP_LINE_TRANSPARENT = None

# Размещение
IC_REP_ALIGN = {'align_txt': (0, 0),    # кортеж из 2-х элементов
                'wrap_txt': False,      # Перенос текста по словам
                }
IC_REP_ALIGN_HORIZ = 0
IC_REP_ALIGN_VERT = 1

# Выравнивание текста
IC_HORIZ_ALIGN_LEFT = 0
IC_HORIZ_ALIGN_CENTRE = 1
IC_HORIZ_ALIGN_RIGHT = 2

IC_VERT_ALIGN_TOP = 3
IC_VERT_ALIGN_CENTRE = 4
IC_VERT_ALIGN_BOTTOM = 5

# Структура группы
IC_REP_GRP = {'header': {},         # Заголовок группы.
              'footer': {},         # Примечание группы.
              'field': None,        # Имя поля группы
              'old_rec': None,      # Старое значение записи таблицы запроса.
              }

DEFAULT_ENCODING = 'utf-8'


class icReportGenerator:
    """
    Класс генератора отчета.
    """
    def __init__(self):
        """
        Конструктор класса.
        """
        # Имя отчета
        self._RepName = None
        # Таблица запроса
        self._QueryTbl = None
        # Количество записей таблицы запроса
        self._QueryTblRecCount = -1
        # Текущая запись таблицы запроса
        self._CurRec = {}
        # Шаблон отчета
        self._Template = None
        # Описание листа шаблона отчета
        self._TemplateSheet = None
        # Выходной отчет
        self._Rep = None

        # Список групп
        self._RepGrp = []

        # Текущая координата Y для перераспределения координат ячеек
        self._cur_top = 0

        # Пространство имен отчета
        self._NameSpace = {}

        # Атрибуты ячейки по умолчанию
        # если None, то атрибуты не устанавливаются
        self.AttrDefault = None

        # Библиотека стилей
        self._StyleLib = None
        
        # Покоординатная замена значений ячеек
        self._CoordFill = None

        # Словарь форматов ячеек
        self._cellFmt = {}

    def generate(self, rep_template, query_table, name_space=None, coord_fill=None):
        """
        Генерация отчета.

        :param rep_template: Структура шаблона отчета (см. спецификации).
        :param query_table: Таблица запроса.
            Словарь следующей структуры:
                {
                    '__name__':имя таблицы запроса,
                    '__fields__':[имена полей],
                    '__data__':[список списков значений],
                    '__sub__':{словарь данных подотчетов},
                }.
        :param name_space: Пространство имен шаблона.
            Обычный словарь:
                {
                    'имя переменной': значение переменной, 
                }.
            ВНИМАНИЕ! Этот словарь может передаваться в таблице запроса
                ключ __variables__.
        :param coord_fill: Координатное заполнение значений ячеек.
            Формат:
                {
                    (Row,Col): 'Значение',
                }.
            ВНИМАНИЕ! Этот словарь может передаваться в таблице запроса
                ключ __coord_fill__.
        :return: Заполненную структуру отчета.
        """
        try:
            # Покоординатная замена значений ячеек
            self._CoordFill = coord_fill
            if query_table and '__coord_fill__' in query_table:
                if self._CoordFill is None:
                    self._CoordFill = dict()
                self._CoordFill.update(query_table['__coord_fill__'])

            # Инициализация списка групп
            self._RepGrp = list()

            # I. Определить все бэнды в шаблоне и ячейки сумм
            if isinstance(rep_template, dict):
                self._Template = rep_template
            else:
                # Вывести сообщение об ошибке в лог
                log.warning(u'Ошибка типа шаблона отчета <%s>.' % type(rep_template))
                return None

            # Инициализация имени отчета
            if 'name' in query_table and query_table['name']:
                # Если таблица запроса именована, то значит это имя готового отчета
                self._RepName = str(query_table['name'])
            elif 'name' in self._Template:
                self._RepName = self._Template['name']
            
            # Заполнить пространство имен
            self._NameSpace = name_space
            if self._NameSpace is None:
                self._NameSpace = dict()
            self._NameSpace.update(self._Template['variables'])
            if query_table and '__variables__' in query_table:
                self._NameSpace.update(query_table['__variables__'])
            if self._NameSpace:
                log.debug(u'Переменные отчета: %s' % str(list(self._NameSpace.keys())))

            # Библиотека стилей
            self._StyleLib = None
            if 'style_lib' in self._Template:
                self._StyleLib = self._Template['style_lib']
            
            self._TemplateSheet = self._Template['sheet']
            self._TemplateSheet = self._initSumCells(self._TemplateSheet)

            # II. Инициализация таблицы запроса
            self._QueryTbl = query_table
            # Определить количество записей в таблице запроса
            self._QueryTblRecCount = 0
            if self._QueryTbl and '__data__' in self._QueryTbl:
                self._QueryTblRecCount = len(self._QueryTbl['__data__'])

            # Проинициализировать бенды групп
            for grp in self._Template['groups']:
                grp['old_rec'] = None

            time_start = time.time()
            log.info(u'Отчет <%s>. Запуск генерации' % textfunc.toUnicode(self._RepName))

            # III. Вывод данных в отчет
            # Создать отчет
            self._Rep = copy.deepcopy(IC_REP_TMPL)
            self._Rep['name'] = self._RepName

            # Инициализация необходимых переменных
            field_idx = {}      # Индексы полей
            i = 0
            i_rec = 0
            # Перебор полей таблицы запроса
            if self._QueryTbl and '__fields__' in self._QueryTbl:
                for cur_field in self._QueryTbl['__fields__']:
                    field_idx[cur_field] = i
                    i += 1

            # Если записи в таблице запроса есть, то ...
            if self._QueryTblRecCount:
                # Проинициализировать текущую строку для использования
                # ее в заголовке отчета
                rec = self._QueryTbl['__data__'][i_rec]
                # Заполнить словарь текущей записи
                for field_name in field_idx.keys():
                    val = rec[field_idx[field_name]]
                    # Предгенерация значения данных ячейки
                    self._CurRec[field_name] = val
                # Прописать индекс текущей записи
                self._CurRec['ic_sys_num_rec'] = i_rec

            # Верхний колонтитул
            if self._Template['upper']:
                self._genUpper(self._Template['upper'])
            
            # Вывести в отчет заголовок
            self._genHeader(self._Template['header'])

            # Главный цикл
            # Перебор записей таблицы запроса
            while i_rec < self._QueryTblRecCount:
                # Обработка групп
                # Проверка смены группы в описании всех групп
                # и найти индекс самой общей смененной группы
                i_grp_out = -1      # индекс самой общей смененной группы
                # Флаг начала генерации (примечания групп не выводяться)
                start_gen = False
                for i_grp in range(len(self._Template['groups'])):
                    grp = self._Template['groups'][i_grp]
                    if grp['old_rec']:
                        # Проверить условие вывода примечания группы
                        if self._CurRec[grp['field']] != grp['old_rec'][grp['field']]:
                            i_grp_out = i_grp
                            break
                    else:
                        i_grp_out = 0
                        start_gen = True
                        break
                if i_grp_out != -1:
                    # Вывести примечания
                    if start_gen is False:
                        for i_grp in range(len(self._Template['groups'])-1, i_grp_out-1, -1):
                            grp = self._Template['groups'][i_grp]
                            self._genGrpFooter(grp)
                    # Вывести заголовки
                    for i_grp in range(i_grp_out, len(self._Template['groups'])):
                        grp = self._Template['groups'][i_grp]
                        grp['old_rec'] = copy.deepcopy(self._CurRec)
                        self._genGrpHeader(grp)
                    
                # Область данных
                self._genDetail(self._Template['detail'])

                # Увеличить суммы суммирующих ячеек
                self._sumIterate(self._TemplateSheet, self._CurRec)

                # Перейти на следующую запись
                i_rec += 1
                # Заполнить словарь текущей записи
                if i_rec < self._QueryTblRecCount:
                    rec = self._QueryTbl['__data__'][i_rec]
                    # Заполнить словарь текущей записи
                    for field_name in field_idx.keys():
                        val = rec[field_idx[field_name]]
                        # Предгенерация значения данных ячейки
                        self._CurRec[field_name] = val
                    # Прописать индекс текущей записи
                    self._CurRec['ic_sys_num_rec'] = i_rec

            # Вывести примечания после области данных
            for i_grp in range(len(self._Template['groups'])-1, -1, -1):
                grp = self._Template['groups'][i_grp]
                if grp['old_rec']:
                    self._genGrpFooter(grp)
                else:
                    break
            # Вывести в отчет примечание отчета
            self._genFooter(self._Template['footer'])
            # Нижний колонтитул
            if self._Template['under']:
                self._genUnder(self._Template['under'])

            # Параметры страницы
            self._Rep['page_setup'] = self._Template['page_setup']

            # Прогресс бар
            log.info(u'Отчет <%s>. Окончание генерации. Время: %d сек.' % (textfunc.toUnicode(self._RepName),
                                                                           time.time()-time_start))

            return self._Rep
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации отчета.')
            return None

    def _genHeader(self, header):
        """
        Сгенерировать заголовок отчета и перенести ее в выходной отчет.

        :param header: Бэнд заголовка.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            # log.debug(u'Генерация заголовка')
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(header['row'], header['row'] + header['row_size']):
                for col in range(header['col'], header['col'] + header['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Прописать область
            self._Rep['header'] = {'row': max_row,
                                   'col': header['col'],
                                   'row_size': i_row,
                                   'col_size': header['col_size'],
                                   }
            # Очистить сумы суммирующих ячеек
            self._TemplateSheet = self._clearSum(self._TemplateSheet, 0, len(self._TemplateSheet))
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации заголовка отчета <%s>.' % textfunc.toUnicode(self._RepName))
            return False
            
    def _genFooter(self, footer):
        """
        Сгенерировать примечание отчета и перенести ее в выходной отчет.

        :param footer: Бэнд примечания.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            # Подвала отчета просто нет
            if not footer:
                return True

            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0       # Счетчик строк бэнда
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(footer['row'], footer['row'] + footer['row_size']):
                for col in range(footer['col'], footer['col'] + footer['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Прописать область
            self._Rep['footer'] = {'row': max_row,
                                   'col': footer['col'],
                                   'row_size': i_row,
                                   'col_size': footer['col_size'],
                                   }
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации примечания отчета <%s>.' % self._RepName)
            return False

    def _genDetail(self, detail):
        """
        Сгенерировать область данных отчета и перенести ее в выходной отчет.

        :param detail: Бэнд области данных.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0   # Счетчик строк бэнда
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(detail['row'], detail['row'] + detail['row_size']):
                for col in range(detail['col'], detail['col'] + detail['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Прописать область
            if self._Rep['detail'] == {}:
                self._Rep['detail'] = {'row': max_row,
                                       'col': detail['col'],
                                       'row_size': i_row,
                                       'col_size': detail['col_size'],
                                       }
            else:
                self._Rep['detail']['row_size'] += i_row

            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации области данных отчета <%s>.' % self._RepName)
            return False

    def _genGrpHeader(self, rep_group):
        """
        Генерация заголовка группы.

        :param rep_group: Словарь IC_REP_GRP, описывающий группу.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            band = rep_group['header']
            if not band:
                return False
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0   # Счетчик строк бэнда
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(band['row'], band['row']+band['row_size']):
                for col in range(band['col'], band['col']+band['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Очистить сумы суммирующих ячеек
            # ВНИМАНИЕ!!! Итоговых ячеек не бывает в заголовках. Поэтому я не обработываю их
            band = rep_group['footer']
            if band:
                self._TemplateSheet = self._clearSum(self._TemplateSheet, band['row'], band['row']+band['row_size'])
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации заголовка группы <%s> отчета <%s>.' % (rep_group['field'], self._RepName))
            return False

    def _genGrpFooter(self, rep_group):
        """
        Генерация примечания группы.

        :param rep_group: Словарь IC_REP_GRP, описывающий группу.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            band = rep_group['footer']
            if not band:
                return False
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0   # Счетчик строк бэнда
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(band['row'], band['row']+band['row_size']):
                for col in range(band['col'], band['col']+band['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row + i_row, col, rep_group['old_rec'])
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации примечания группы <%s> отчета <%s>.' % (rep_group['field'], self._RepName))
            return False

    def _genUpper(self, upper):
        """
        Сгенерировать верхний колонтитул/заголовок страницы отчета и
        перенести ее в выходной отчет.

        :param upper: Бэнд верхнего колонтитула.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            if 'row' not in upper or 'col' not in upper or \
               'row_size' not in upper or 'col_size' not in upper:
                # Не надо обрабатывать строки
                self._Rep['upper'] = upper
                return True
                
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(upper['row'], upper['row'] + upper['row_size']):
                for col in range(upper['col'], upper['col'] + upper['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Прописать область
            self._Rep['upper'] = copy.deepcopy(upper)
            self._Rep['upper']['row'] = max_row
            self._Rep['upper']['row_size'] = i_row
            
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации верхнего колонтитула отчета <%s>.' % self._RepName)
            return False

    def _genUnder(self, under):
        """
        Сгенерировать нижний колонтитул отчета и перенести ее в выходной отчет.

        :param under: Бэнд нижнего колонтитула.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            if 'row' not in under or 'col' not in under or \
               'row_size' not in under or 'col_size' not in under:
                # Не надо обрабатывать строки
                self._Rep['under'] = under
                return True
                
            # Добавлять будем в конец отчета,
            # поэтому опреелить максимальную строчку
            max_row = len(self._Rep['sheet'])
            i_row = 0
            cur_height = 0
            # Перебрать все ячейки бэнда
            for row in range(under['row'], under['row'] + under['row_size']):
                for col in range(under['col'], under['col'] + under['col_size']):
                    if self._TemplateSheet[row][col]:
                        self._genCell(self._TemplateSheet, row, col,
                                      self._Rep, max_row+i_row, col, self._CurRec)
                        cur_height = self._TemplateSheet[row][col]['height']
                i_row += 1
                # Увеличить текущую координату Y
                self._cur_top += cur_height
            # Прописать область
            self._Rep['under'] = copy.deepcopy(under)
            self._Rep['under']['row'] = max_row
            self._Rep['under']['row_size'] = i_row
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации нижнего колонтитула отчета <%s>.' % self._RepName)
            return False
            
    def _genSubReport(self, sub_rep_name, row):
        """
        Генерация под-отчета.

        :param sub_rep_name: Имя под-отчета.
        :param row: Номер строки листа, после которой будет вставляться под-отчет.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            if '__sub__' in self._QueryTbl and self._QueryTbl['__sub__']:
                if sub_rep_name in self._QueryTbl['__sub__']:
                    # Если есть данные под-отчета, тогда запустить генерацию
                    report = self._QueryTbl['__sub__'][sub_rep_name]['report']
                    if isinstance(report, str):
                        # Импорт для генерации под-отчетов
                        from ic.report import icreptemplate
                        # Под-отчет задан именем файла.
                        template = icreptemplate.icExcelXMLReportTemplate()

                        self._QueryTbl['__sub__'][sub_rep_name]['report'] = template.read(report)
                    # Запуск генерации подотчета
                    rep_gen = icReportGenerator()
                    rep_result = rep_gen.generate(self._QueryTbl['__sub__'][sub_rep_name]['report'],
                                                  self._QueryTbl['__sub__'][sub_rep_name],
                                                  self._QueryTbl['__sub__'][sub_rep_name]['__variables__'],
                                                  self._QueryTbl['__sub__'][sub_rep_name]['__coord_fill__'])
                    # Вставить результат под-отчета после строки
                    self._Rep['sheet'] = self._Rep['sheet'][:row]+rep_result['sheet']+self._Rep['sheet'][row:]
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации под-отчета <%s> отчета <%s>.' % (sub_rep_name, self._RepName))
            return False

    def _genCell(self, from_sheet, from_row, from_col, to_report, to_row, to_col, record):
        """
        Генерация ячейки из шаблона в выходной отчет.

        :param from_sheet: Из листа шаблона.
        :param from_row: Координаты ячейки шаблона. Строка.
        :param from_col: Координаты ячейки шаблона. Столбец.
        :param to_report: В отчет.
        :param to_row: Координаты ячейки отчета. Строка.
        :param to_col: Координаты ячейки отчета. Столбец.
        :param record: Запись.
        :return: Возвращает результат выполнения операции True/False.
        """
        try:
            cell = copy.deepcopy(from_sheet[from_row][from_col])

            # Коррекция координат ячейки
            cell['top'] = self._cur_top
            # Генерация текста ячейки
            if self._CoordFill and (to_row, to_col) in self._CoordFill:
                # Координатные замены
                fill_val = str(self._CoordFill[(to_row, to_col)])
                cell['value'] = self._genTxt({'value': fill_val}, record, to_row, to_col)
            else:
                # Перенести все ячейки из шаблона в выходной отчет
                cell['value'] = self._genTxt(cell, record, to_row, to_col)

            # log.debug(u'Значение <%s>' % text(new_cell['value']))

            # Установка атирибутов ячейки по умолчанию
            # Заполнение некоторых атрибутов ячейки по умолчанию
            if self.AttrDefault and isinstance(self.AttrDefault, dict):
                cell.update(self.AttrDefault)
                
            # Установить описание ячейки отчета.
            if len(to_report['sheet']) <= to_row:
                # Расширить строки
                for i_row in range(len(to_report['sheet']), to_row + 1):
                    to_report['sheet'].append([])
            if len(to_report['sheet'][to_row]) <= to_col:
                # Расширить колонки
                for i_col in range(len(to_report['sheet'][to_row]), to_col + 1):
                    to_report['sheet'][to_row].append(None)
            # Установить описание колонки
            if cell['visible']:
                to_report['sheet'][to_row][to_col] = cell
            return True
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации ячейки шаблона <%s>.' % self._RepName)
            return False
        
    def _genTxt(self, cell, record=None, cell_row=None, cell_col=None):
        """
        Генерация текста.

        :param cell: Ячейка.
        :param record: Словарь, описывающий текущую запись таблицы запроса.
            Формат: { <имя поля> : <значение поля>, ...}
        :param cell_row: Номер строки ячейки в результирующем отчете.
        :param cell_col: Номер колонки ячейки в результирующем отчете.
        :return: Возвращает сгенерированное значение.
        """
        value = u''
        try:
            # Проверка на преобразование типов
            cell_val = cell['value']
            if cell_val is not None and not isinstance(cell_val, str):
                cell_val = str(cell_val)
            if cell_val not in self._cellFmt:
                parsed_fmt = self.funcTextParse(cell_val)
                self._cellFmt[cell_val] = parsed_fmt
            else:
                parsed_fmt = self._cellFmt[cell_val]

            func_str = []   # Выходной список значений
            i_sum = 0
            # Перебрать строки функционала
            for cur_func in parsed_fmt['func']:

                # Функция
                if re.search(REP_FUNC_PATT, cur_func):
                    value = self._exec_function(cur_func, locals(), globals())

                # Исполняемое выражение
                elif re.search(REP_EXP_PATT, cur_func):
                    value = self._exec_expression(cur_func, locals(), globals())

                # Ламбда-выражение
                elif re.search(REP_LAMBDA_PATT, cur_func):
                    value = self._exec_lambda(cur_func, locals(), globals())

                # Переменная
                elif re.search(REP_VAR_PATT, cur_func):
                    value = self._get_variable(cur_func, locals(), globals())

                # Блок кода
                elif re.search(REP_EXEC_PATT, cur_func):
                    value = self._exec_code(cur_func, locals(), globals())

                # Системная функция
                elif re.search(REP_SYS_PATT, cur_func):
                    # Функция суммирования
                    if cur_func[2:6].lower() == 'sum(':
                        value = str(cell['sum'][i_sum]['value'])
                        i_sum += 1  # Перейти к следующей сумме
                    # Функция вычисления среднего значения
                    elif cur_func[2:6].lower() == 'avg(':
                        if 'ic_sys_num_rec' not in record:
                            record['ic_sys_num_rec'] = 0
                        value = str(cell['sum'][i_sum]['value'] / (record['ic_sys_num_rec'] + 1))
                        i_sum += 1  # Перейти к следующей сумме
                    elif cur_func[2:-2].lower() == 'n':
                        if 'ic_sys_num_rec' not in record:
                            record['ic_sys_num_rec'] = 0
                        sys_num_rec = record['ic_sys_num_rec']
                        value = str(sys_num_rec + 1)
                    else:
                        # Вывести сообщение об ошибке в лог
                        log.warning(u'Неизвестная системная функция <%s> шаблона <%s>.' % (textfunc.toUnicode(cur_func),
                                                                                           self._RepName))
                        value = ''
                        
                # Стиль
                elif re.search(REP_STYLE_PATT, cur_func):
                    value = self._set_style(cur_func, locals(), globals())

                # Поле
                elif re.search(REP_FIELD_PATT, cur_func):
                    value = self._get_field_value(cur_func, locals(), globals())

                # Под-отчеты
                elif re.search(REP_SUBREPORT_PATT, cur_func):
                    value = self._gen_subreport(cur_func, locals(), globals())

                else:
                    log.warning(u'Не обрабатываемая функция <%s>' % str(cur_func))

                # ВНИМАНИЕ! В значении ячейки тоже могут быть управляющие коды
                value = self._genTxt({'value': value}, record)
                func_str.append(value)

            # Заполнение формата
            return self._valueFormat(parsed_fmt['fmt'], func_str)
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка генерации текста ячейки <%s> шаблона <%s>.' % (textfunc.toUnicode(cell['value']),
                                                                              self._RepName))
            return None

    def _exec_function(self, cur_func, locals, globals):
        """
        Выполнить вызов внешней функции.
        ВНИМАНИЕ: Функция в шаблоне может иметь 1 аргумент это словарь записи.
            Например:
                [@package_name.module_name.function_name(record)@]

        :param cur_func: Текст вызова функции с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Вычисленное значение в виде строки или пустая строка в случае ошибки.
        """
        value = u''
        func_body = cur_func[2:-2]
        try:
            value = str(self._execFuncGen(func_body, locals))
        except:
            log.fatal(u'Ошибка выполнения функции <%s>' % func_body)
        return value

    def _exec_expression(self, cur_func, locals, globals):
        """
        Выполнить исполняемое выражение.
        ВНИМАНИЕ: Исполняемое выражение в шаблоне должно иметь
            вид получения значения value.
            Например:
                [#record["dt"].strftime("%B")#]

        :param cur_func: Текст исполняемого выражения с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Вычисленное значение в виде строки или пустая строка в случае ошибки.
        """
        value = u''
        exp_body = cur_func[2:-2]
        try:
            value = eval(exp_body, globals, locals)
        except:
            log.fatal(u'Ошибка выполнения исполняемого выражения <%s>' % exp_body)
        log.debug(u'Выполнение исполняемого выражения <%s>. Значение <%s>' % (exp_body, str(value)))
        return value

    def _exec_lambda(self, cur_func, locals, globals):
        """
        Выполнение lambda выражения.
            ВНИМАНИЕ: Лямбда-выражение в шаблоне должно иметь 1 аргумент это словарь записи.
                Например:
                    [~rec: rec['name']=='Петров'~]

        :param cur_func: Вызов lambda выражения с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Вычисленное значение в виде строки или пустая строка в случае ошибки.
        """
        value = u''
        lambda_body = cur_func[2:-2]
        lambda_func = None
        try:
            lambda_func = eval('lambda ' + cur_func[2:-2])
        except:
            log.fatal(u'Ошибка определения lambda выражения <%s>' % lambda_body)

        if lambda_func:
            try:
                record = locals['record'] if 'record' in locals else globals.get('record', dict())
                value = str(lambda_func(record))
            except:
                log.fatal(u'Ошибка выполнения lambda выражения <%s>' % lambda_body)

        return value

    def _exec_code(self, cur_func, locals, globals):
        """
        Выполнить блок кода.
        ВНИМАНИЕ: В блоке кода доступны объекты new_cell и record.
            Если надо вывести информацию, то ее надо выводить в
            переменную value.
            Например:
            [=value = '-' if record['name']=='Петров' else ''=]

        :param cur_func: Текст блока кода с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Вычисленное значение в виде строки или пустая строка в случае ошибки.
        """
        value = u''
        exec_func = cur_func[2:-2].strip()
        try:
            exec(exec_func, globals, locals)
            # ВНИМАНИЕ! При выполнении блока кода значение переменной располагается
            # в пространстве имен locals.
            # Поэтому необходимо после выполнения блока кода вернуть переменную обратно в
            # текущую функцию
            value = locals.get('value', u'')
        except:
            log.fatal(u'Ошибка выполнения блока кода <%s>' % textfunc.toUnicode(exec_func))
        # log.debug(u'Выполнение блока кода <%s>. Значение <%s>' % (exec_func, str(value)))
        return str(value)

    def _get_variable(self, cur_func, locals, globals):
        """
        Получить переменную из пространства имен отчета.

        :param cur_func: Текст блока обращения к переменной с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Переменная в строковом виде.
        """
        var_name = cur_func[2:-2]
        if var_name in self._NameSpace:
            log.debug(u'Обработка переменной <%s>' % var_name)
        else:
            log.warning(u'Переменная <%s> не найдена в пространстве имен' % var_name)
        value = str(self._NameSpace.setdefault(var_name, u''))
        return value

    def _set_style(self, cur_func, locals, globals):
        """
        Установить стиль.

        :param cur_func: Текст блока указания имени стиля с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Переменная в строковом виде.
        """
        value = u''
        style_name = cur_func[2:-2]
        self._setStyleAttr(style_name)
        return value

    def _get_field_value(self, cur_func, locals, globals):
        """
        Получить значение поля текущей записи.

        :param cur_func: Текст блока обращения к полю с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Переменная в строковом виде.
        """
        value = u''
        field_name = str((cur_func[2:-2]))
        record = locals['record'] if 'record' in locals else globals.get('record', dict())
        try:
            value = record[field_name]
        except KeyError:
            log.warning(u'В строке (%s) поле <%s> не найдено' % (textfunc.toUnicode(record),
                                                                 textfunc.toUnicode(field_name)))
        return value

    def _gen_subreport(self, cur_func, locals, globals):
        """
        Запуск генерации подъотчета.

        :param cur_func: Текст ссылки на подъотчет с тегами.
        :param locals: Словарь локального пространства имен.
        :param globals: Словарь глобального пространства имен.
        :return: Переменная в строковом виде.
        """
        value = u''
        subreport_name = cur_func[2:-2]
        cell_row = locals['cell_row'] if 'cell_row' in locals else globals.get('cell_row', dict())
        self._genSubReport(subreport_name, cell_row)
        return value

    def _valueFormat(self, fmt, data_list):
        """
        Заполнение формата значения ячейки.

        :param fmt: Формат.
        :param data_list: Данные, которые нужно поместить в формат.
        :return: Возвращает строку, соответствующую формату.
        """
        # Заполнение формата
        if data_list is []:
            if fmt:
                value = fmt
            else:
                return None
        elif data_list == [None] and fmt == '%s':
            return None
        # Обработка значения None
        elif bool(None in data_list):
            data_lst = [{None: ''}.setdefault(val, val) for val in data_list]
            value = fmt % tuple(data_lst)
        else:
            value = fmt % tuple(data_list)
        return value
        
    def _setStyleAttr(self, style_name):
        """
        Установить атрибуты по умолчанию ячеек по имени стиля из библиотеки стилей.

        :param style_name: Имя стиля из библиотеки стилей.
        """
        if self._StyleLib and style_name in self._StyleLib:
            self.AttrDefault = self._StyleLib[style_name]
        else:
            self.AttrDefault = None
        
    def _getSum(self, formula):
        """
        Получить сумму по формуле.

        :param formula: Формула.
        :return: Возвращает строковое значение суммы.
        """
        return '0'

    def _initSumCells(self, sheet):
        """
        Выявление и инициализация ячеек с суммами.

        :param sheet: Описание листа отчета.
        :return: Возвращает описание листа с корректным описанием ячеек с суммами.
            В результате ошибки возвращает старое описание листа.
        """
        try:
            new_sheet = sheet
            # Просмотр и коррекция каждой ячейки листа
            for row in range(len(new_sheet)):
                for col in range(len(new_sheet[row])):
                    if new_sheet[row][col]:
                        new_sheet[row][col] = self._initSumCell(new_sheet[row][col])
            return new_sheet
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка инициализации суммирующих ячеек шаблона <%s>.' % self._RepName)
        return sheet

    def _initSumCell(self, cell):
        """
        Инициализация суммарной ячейки.

        :param cell: Описание ячейки.
        :return: Возвращает скоррекстированное описание ячейки.
            В случае ошибки возвращает старое описание ячейки.
        """
        try:
            new_cell = cell
            # Проверка на преобразование типов
            cell_val = new_cell['value']
            if cell_val is not None and not isinstance(cell_val, str):
                cell_val = str(cell_val)
            parsed_fmt = self.funcTextParse(cell_val, [REP_SYS_PATT])
            # Перебрать строки функционала
            for cur_func in parsed_fmt['func']:
                # Системная функция
                if re.search(REP_SYS_PATT, cur_func):
                    # Функция суммирования
                    if cur_func[2:6].lower() in ('sum(', 'avg('):
                        # Если данные суммирующей ячейки не инициализированы, то
                        if new_cell['sum'] is None:
                            new_cell['sum'] = []
                        # Проинициализировать данные суммарной ячейки
                        new_cell['sum'].append(copy.deepcopy(IC_REP_SUM))
                        new_cell['sum'][-1]['formul'] = cur_func[6:-3].replace(REP_SUM_FIELD_START, 'record[\'').replace(REP_SUM_FIELD_STOP, '\']')
            return new_cell
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка инициализации ячейки <%s>.' % cell)
        return cell

    def _sumIterate(self, sheet, record):
        """
        Итерация суммирования.

        :param sheet: Описание листа отчета.
        :param record: Запись, на которой вызывается итерация.
        :return: Возвращает описание листа с корректным описанием ячеек с суммами.
            В результате ошибки возвращает старое описание листа.
        """
        try:
            new_sheet = sheet
            # Просмотр и коррекция каждой ячейки листа
            for row in range(len(new_sheet)):
                for col in range(len(new_sheet[row])):
                    # Если ячейка определена, то ...
                    if new_sheet[row][col]:
                        # Если ячейка суммирующая,
                        # то выполнить операцию суммирования
                        if new_sheet[row][col]['sum'] is not None and new_sheet[row][col]['sum'] is not []:
                            for cur_sum in new_sheet[row][col]['sum']:
                                try:
                                    value = eval(cur_sum['formul'], globals(), locals())
                                except:
                                    log.warning(u'Ошибка выполнения формулы для подсчета сумм <%s>.' % cur_sum)
                                    value = 0.0
                                try:
                                    if value is None:
                                        value = 0.0
                                    else:
                                        value = float(value)
                                    cur_sum['value'] += value
                                except:
                                    log.warning(u'Ошибка итерации сумм <%s>+<%s>' % (cur_sum['value'], value))

            return new_sheet
        except:
            # Вывести сообщение об ошибке в лог
            log.fatal(u'Ошибка итерации сумм суммирующих ячеек шаблона <%s>.' % self._RepName)
        return sheet

    def _clearSum(self, sheet, start_row, stop_row):
        """
        Обнуление сумм.

        :param sheet: Описание листа отчета.
        :param start_row: Начало бэнда обнуления.
        :param stop_row: Конец бэнда обнуления.
        :return: Возвращает описание листа с корректным описанием ячеек с суммами.
            В результате ошибки возвращает старое описание листа.
        """
        try:
            new_sheet = sheet
            # Просмотр и коррекция каждой ячейки листа
            for row in range(start_row, stop_row):
                for col in range(len(new_sheet[row])):
                    # Если ячейка определена, то ...
                    if new_sheet[row][col]:
                        # Если ячейка суммирующая, то выполнить операцию обнуления
                        if new_sheet[row][col]['sum'] is not None and new_sheet[row][col]['sum'] is not []:
                            for cur_sum in new_sheet[row][col]['sum']:
                                cur_sum['value'] = 0
            return new_sheet
        except:
            # Вывести сообщение об ошибке в лог
            log.error(u'Ошибка обнуления сумм суммирующих ячеек шаблона <%s>.' % self._RepName)
        return sheet
        
    # Функции-свойства
    def getCurRec(self):
        return self._CurRec

    def funcTextParse(self, text, patterns=ALL_PATTERNS):
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
            ret = {'fmt': '', 'func': []}

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
                if func_find is False:
                    ret['fmt'] += parsed_str[i_parse]
            return ret
        except:
            log.fatal(u'Ошибка формата <%s> ячейки шаблона <%s>.' % (text, self._RepName))
        return None

    def _execFuncGen(self, function, locals):
        """
        Выполнить функцию при генерации.
        """
        # re_import = not ic_mode.isRuntimeMode()
        return execfunc.exec_code(function, bReImport=True)
