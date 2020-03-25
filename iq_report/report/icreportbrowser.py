#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль приложения генератора отчетов.
"""

# Подключение библиотек
import os
import os.path

import wx
import wx.lib.buttons

from ic.std.utils import inifunc
from ic.std.dlg import dlg
from ic.std.img import bmp
from ic.std.log import log
from ic.std.utils import filefunc
from ic.std.utils import resfunc

import ic.report
from ic.report import report_generator
from ic import config

__version__ = (0, 1, 1, 2)

# Константы
# Индексы полей списка кортежей

REP_FILE_IDX = 0        # полное имя файла/директория отчета
REP_NAME_IDX = 1        # имя отчета/директория
REP_DESCRIPT_IDX = 2    # описание отчета/директория
REP_ITEMS_IDX = 3       # вложенные объекты
REP_IMG_IDX = 4         # Образ отчета в дереве отчетов

# Режимы работы браузера
IC_REPORT_VIEWER_MODE = 0
IC_REPORT_EDITOR_MODE = 1

# Позиции и размеры кнопок управления
REP_BROWSER_BUTTONS_POS_X = 780
REP_BROWSER_BUTTONS_WIDTH = 200
REP_BROWSER_BUTTONS_HEIGHT = 30

# Не обрабатываемые имена папок
NOT_WORK_DIRNAMES = ('__pycache__',)

# Размер диалогового окна
REP_BROWSER_DLG_WIDTH = 1000
REP_BROWSER_DLG_HEIGHT = 460

# Заголовок
TITLE = 'icReport'


def getReportList(report_dir, is_sort=True):
    """
    Получить список отчетов.

    :param report_dir: Директорий, в котором лежат файлы отчетов.
    :type is_sort: bool.
    :param is_sort: Сортировать список по именам?
    :return: Возвращает список списков следующего формата:
        [
        [полное имя файла/директория отчета, имя отчета/директория,
            описание отчета/директория, None/вложенные объекты, индекс образа],
        .
        .
        .
        ]
        Описание директория берется из файла descript.ion,
        который должен находится в этой же директории.
        Если такой файл не найден, то описание директория - пустое.
        Вложенные объекты список, элементы которого имеют такую же структуру.
    """
    try:
        # Коррекция аргументов
        report_dir = os.path.abspath(os.path.normpath(report_dir))
        log.debug(u'Сканирование папки отчетов <%s>' % report_dir)

        # Выходой список
        dir_list = list()
        rep_list = list()

        # Сначала обработать под-папки
        sub_dirs = filefunc.getSubDirsFilter(report_dir)

        # то записать информацию в выходной список о директории
        img_idx = 0
        for sub_dir in sub_dirs:

            # Исключить не обрабатываемые папки
            if os.path.basename(sub_dir) in NOT_WORK_DIRNAMES:
                continue

            description_file = None
            try:
                description_file = open(os.path.join(sub_dir, 'descript.ion'), 'rt')
                dir_description = description_file.read()
                description_file.close()
            except:
                if description_file:
                    description_file.close()
                dir_description = sub_dir

            # Для поддиректориев рекурсивно вызвать эту же функцию
            data = [sub_dir, os.path.basename(sub_dir), dir_description,
                    getReportList(sub_dir, is_sort), img_idx]
            dir_list.append(data)
        if is_sort:
            # ВНИМАНИЕ! Сортировка по 3-й колонке
            dir_list.sort(key=lambda i: i[2])

        # Получить список всех файлов
        file_rep_list = [filename for filename in filefunc.getFilesByExt(report_dir, '.rprt')
                         if not filename.lower().endswith('_pkl.rprt')]
        # log.debug(u'Список файлов отчетов %s' % filefunc.getFilesByExt(report_dir, '.rprt'))

        for rep_file_name in file_rep_list:
            # записать данные о этом файле в выходной список
            rep_struct = resfunc.loadResourceFile(rep_file_name, bRefresh=True)
            # Определение образа
            img_idx = 2
            try:
                if rep_struct['generator'][-3:].lower() == 'xml':
                    img_idx = 1
            except:
                log.warning('Ошибка определения типа отчета')
            # Данные
            try:
                data = [rep_file_name, rep_struct['name'],
                        rep_struct['description'], None, img_idx]
                rep_list.append(data)
            except:
                log.fatal(u'Ошибка чтения шаблона отчета <%s>' % rep_file_name)
        if is_sort:
            # ВНИМАНИЕ! Сортировка по 3-й колонке
            rep_list.sort(key=lambda i: i[2])

        return dir_list + rep_list
    except:
        # Вывести сообщение об ошибке в лог
        log.fatal(u'Ошибка заполнения информации о файлах отчетов <%s>.' % report_dir)
    return list()


def get_root_dirname():
    """
    Путь к корневой папке.
    """
    cur_dirname = os.path.dirname(__file__)
    if not cur_dirname:
        cur_dirname = os.getcwd()
    return os.path.dirname(os.path.dirname(cur_dirname))


def get_img_dirname():
    """
    Путь к папке образов.
    """
    cur_dirname = os.path.dirname(__file__)
    if not cur_dirname:
        cur_dirname = os.getcwd()
    return os.path.join(cur_dirname, 'img')


class icReportBrowserDialog(wx.Dialog):
    """
    Форма браузера отчетов.
    """
    def __init__(self, parent=None, mode=IC_REPORT_VIEWER_MODE, report_dir=''):
        """
        Конструктор.

        :param parent: Родительская форма.
        :param mode: Режим работы.
        :param report_dir: Папка отчетов.
        """
        # Версия в строковом виде
        ver = '.'.join([str(ident) for ident in config.__version__])
        # Создать экземпляр главного окна
        wx.Dialog.__init__(self, parent, wx.NewId(),
                           title=u'%s. Система управления отчетами. v. %s' % (TITLE, ver),
                           pos=wx.DefaultPosition, size=wx.Size(REP_BROWSER_DLG_WIDTH, REP_BROWSER_DLG_HEIGHT),
                           style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        # Папка отчетов
        self._ReportDir = report_dir

        self.icon = None
        self.SetIcon(self.get_icon_obj())

        # Строка папки отчетов
        self.dir_txt = wx.StaticText(self, id=wx.NewId(),
                                     label='',
                                     pos=wx.Point(10, 10), size=wx.DefaultSize,
                                     style=0)

        # Если папки отчетов не определена или не существует, то ...
        if not self._ReportDir or not os.path.exists(self._ReportDir):
            # ... считать путь к папке отчетов из файла настройки
            self._ReportDir = inifunc.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
            if not self._ReportDir or not os.path.exists(self._ReportDir):
                self._ReportDir = dlg.getDirDlg(self,
                                                u'Папка отчетов <%s> не найдена. Выберите папку отчетов.' %  self._ReportDir)
                # Сохранить сразу в конфигурационном файле
                if self._ReportDir:
                    self._ReportDir = os.path.normpath(self._ReportDir)
                    inifunc.saveParamINI(self.getReportSettingsINIFile(),
                                         'REPORTS', 'report_dir', self._ReportDir)
        # Отобразить новый путь в окне
        self.dir_txt.SetLabel(self._ReportDir)

        # Список отчетов
        self.rep_tree = wx.TreeCtrl(self, wx.NewId(),
                                    pos=wx.Point(10, 30), size=wx.Size(750, 390), style=wx.TR_HAS_BUTTONS,
                                    validator=wx.DefaultValidator, name='ReportTree')

        self.img_list = wx.ImageList(16, 16)
        self.img_list.Add(bmp.createBitmap(os.path.join(get_img_dirname(), 'reports.png')))
        self.img_list.Add(bmp.createBitmap(os.path.join(get_img_dirname(), 'page_excel.png')))
        self.img_list.Add(bmp.createBitmap(os.path.join(get_img_dirname(), 'report.png')))
        self.rep_tree.AssignImageList(self.img_list)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged, id=self.rep_tree.GetId())

        # Кнопки управления

        # Кнопка вывода отчета/предварительного просмотра/печати
        self.rep_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                             bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                           'report_magnify.png')),
                                                             u'Предв. просмотр',
                                                             size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                   REP_BROWSER_BUTTONS_HEIGHT),
                                                             pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 30))
        self.Bind(wx.EVT_BUTTON, self.onPreviewRepButton, id=self.rep_button.GetId())

        # Кнопка /печати
        self.print_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                               bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                             'printer.png')),
                                                               u'Печать',
                                                               size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                     REP_BROWSER_BUTTONS_HEIGHT),
                                                               pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 70))
        self.Bind(wx.EVT_BUTTON, self.onPrintRepButton, id=self.print_button.GetId())

        # Кнопка установки параметров страницы
        self.page_setup_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                    bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                                  'page_orientation.png')),
                                                                    u'Параметры страницы',
                                                                    size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                          REP_BROWSER_BUTTONS_HEIGHT),
                                                                    pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 110))
        self.Bind(wx.EVT_BUTTON, self.onPageSetupButton, id=self.page_setup_button.GetId())

        # Кнопка конвертирования отчета
        self.convert_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                 bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                               'excel_exports.png')),
                                                                 u'Конвертация',
                                                                 size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                       REP_BROWSER_BUTTONS_HEIGHT),
                                                                 pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 150))
        self.Bind(wx.EVT_BUTTON, self.onConvertRepButton, id=self.convert_button.GetId())

        if mode == IC_REPORT_EDITOR_MODE:
            # Кнопка настройки
            self.set_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                 bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                               'folder_vertical_document.png')),
                                                                 u'Папка отчетов',
                                                                 size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                       REP_BROWSER_BUTTONS_HEIGHT),
                                                                 pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 190))
            self.Bind(wx.EVT_BUTTON, self.onSetRepDirButton, id=self.set_button.GetId())

            # Кнопка создания нового отчета
            self.new_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                 bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                               'report_add.png')),
                                                                 u'Создание',
                                                                 size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                       REP_BROWSER_BUTTONS_HEIGHT),
                                                                 pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 230))
            self.Bind(wx.EVT_BUTTON, self.onNewRepButton, id=self.new_button.GetId())

            # Кнопка редактирования отчета
            self.edit_button=wx.lib.buttons.GenBitmapTextButton(self,wx.NewId(),
                                                                bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                              'report_design.png')),
                                                                u'Редактирование',
                                                                size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                      REP_BROWSER_BUTTONS_HEIGHT),
                                                                pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 270))
            self.Bind(wx.EVT_BUTTON, self.onEditRepButton, id=self.edit_button.GetId())

            # Кнопка Обновления отчета
            self.convert_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                     bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                                   'arrow_refresh.png')),
                                                                     u'Обновление',
                                                                     size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                           REP_BROWSER_BUTTONS_HEIGHT),
                                                                     pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 310))
            self.Bind(wx.EVT_BUTTON, self.onUpdateRepButton, id=self.convert_button.GetId())

            # Кнопка модуля отчета
            self.module_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                                    bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                                  'script_lightning.png')),
                                                                    u'Модуль отчета',
                                                                    size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                          REP_BROWSER_BUTTONS_HEIGHT),
                                                                    pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 350))
            self.Bind(wx.EVT_BUTTON, self.onModuleRepButton, id=self.module_button.GetId())
                
        # Кнопка выхода
        self.exit_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(),
                                                              bmp.createBitmap(os.path.join(get_img_dirname(),
                                                                                            'door_in.png')),
                                                              u'Выход',
                                                              size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                    REP_BROWSER_BUTTONS_HEIGHT),
                                                              pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 390),
                                                              style=wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.onExitButton, id=self.exit_button.GetId())

        # Заполнить дерево отчетов
        self._fillReportTree(self._ReportDir)

    def get_icon_obj(self):
        """
        Функция получения иконки формы браузера.
        """
        if self.icon is None:
            icon_filename = os.path.join(get_img_dirname(), 'report_stack.png')
            self.icon = wx.Icon(icon_filename, wx.BITMAP_TYPE_PNG)
        return self.icon

    def getReportSettingsINIFile(self):
        """
        Определить имя конфигурационного файла, 
            в котором хранится путь к папке отчетов.
        """
        return os.path.join(get_root_dirname(), 'settings.ini')
        
    def onPreviewRepButton(self, event):
        """
        Обработчик нажатия кнопки 'Предварительный просмотр/Печать'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        log.debug(u'Предварительный просмотр <%s>' % str(item_data[REP_FILE_IDX] if item_data else u'-'))
        # Если это файл отчета, то получить его
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Получение отчета
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX],
                                                      parent=self,
                                                      bRefresh=True).preview()
        # Если это папка, то вывести сообщение
        else:
            dlg.getWarningBox(title=u'ВНИМАНИЕ', message=u'Необходимо выбрать отчет!', parent=self)
        event.Skip()
            
    def onPrintRepButton(self, event):
        """
        Обработчик нажатия кнопки 'Печать отчета'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        log.debug(u'Печать <%s>' % item_data[REP_FILE_IDX] if item_data else u'-')
        # Если это файл отчета, то получить его
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Получение отчета
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX],
                                                      parent=self,
                                                      bRefresh=True).Print()
        # Если это папка, то вывести сообщение
        else:
            dlg.getWarningBox(title=u'ВНИМАНИЕ', message=u'Необходимо выбрать отчет!', parent=self)
        event.Skip()

    def onPageSetupButton(self, event):
        """
        Обработчик нажатия кнопки 'Параметры страницы'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        # Если это файл отчета, то получить его
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Получение отчета
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX], parent=self).setPageSetup()
        # Если это папка, то вывести сообщение
        else:
            dlg.getWarningBox(title=u'ВНИМАНИЕ', message=u'Необходимо выбрать отчет!', parent=self)
        event.Skip()

    def onSetRepDirButton(self, event):
        """
        Обработчик нажатия кнопки 'Папка отчетов'.
        """
        # Считать путь к папке отчетов из файла настройки
        self._ReportDir = inifunc.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
        # Выбрать папку отчетов
        dir_dlg = wx.DirDialog(self, u'Выберите путь к папке отчетов:',
                               style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        # Установка пути по умолчанию
        if self._ReportDir:
            dir_dlg.SetPath(self._ReportDir)
        if dir_dlg.ShowModal() == wx.ID_OK:
            self._ReportDir = dir_dlg.GetPath()
        
        dir_dlg.Destroy()        

        # Сохранить новую выбранную папку
        ok = inifunc.saveParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir', self._ReportDir)
            
        if ok is True:
            # Отобразить новый путь в окне
            self.dir_txt.SetLabel(self._ReportDir)
            # и обновить дерево отчетов
            self._fillReportTree(self._ReportDir)
        event.Skip()

    def onExitButton(self, event):
        """
        Обработчик нажатия кнопки 'Выход'.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onNewRepButton(self, event):
        """
        Обработчик нажатия ккнопки 'Новый отчет'.
        """
        # Запустить редакторы
        report_generator.getCurReportGeneratorSystem().createNew(self._ReportDir)
        event.Skip()

    def onEditRepButton(self, event):
        """
        Обработчик нажатия ккнопки 'Редактирование отчета'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        # Если это файл отчета, то запустить на редактирование
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Запустить на редактирование
            rep_generator = report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX], parent=self)
            if rep_generator is not None:
                rep_generator.edit(item_data[0])
            else:
                log.warning(u'Не определен генератор отчета. Тип <%s>' % item_data[REP_FILE_IDX])

        event.Skip()

    def onUpdateRepButton(self, event):
        """
        Обработчик нажатия кнопки 'Обновление отчета'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        # Если это файл отчета, то запустить обновление шаблона
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Запустить обновление шаблона отчета
            log.debug(u'Обновление отчета <%s>' % item_data[0])
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX], parent=self).update(item_data[0])
        else:
            report_generator.getCurReportGeneratorSystem(self).update()
                
        # Заполнить дерево отчетов
        self._fillReportTree(self._ReportDir)

        event.Skip()

    def onConvertRepButton(self, event):
        """
        Обработчик нажатия кнопки 'Конвертация'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        log.debug(u'Конвертация <%s>' % item_data[REP_FILE_IDX] if item_data else u'-')
        # Если это файл отчета, то получить его
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            # Получение отчета
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX],
                                                      parent=self,
                                                      bRefresh=True).convert()
        else:
            dlg.getWarningBox(title=u'ВНИМАНИЕ', message=u'Необходимо выбрать отчет!', parent=self)

        event.Skip()

    def onModuleRepButton(self, event):
        """
        Обработчик нажатия кнопки 'Модуль отчета'.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        # Если это файл отчета, то запустить открытие модуля отчета
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            report_generator.getReportGeneratorSystem(item_data[REP_FILE_IDX],
                                                      parent=self).openModule(item_data[REP_FILE_IDX])
        else:
            dlg.getWarningBox(title=u'ВНИМАНИЕ', message=u'Необходимо выбрать отчет!', parent=self)

        event.Skip()

    def onRightMouseClick(self, event):
        """
        Нажаитие правой кнопки мыши на дереве.
        """
        # Создать всплывающее меню
        popup_menu = wx.Menu()
        id_rename = wx.NewId()
        popup_menu.Append(id_rename, u'Переименовать отчет')
        self.Bind(wx.EVT_MENU, self.onRenameReport, id=id_rename)
        self.rep_tree.PopupMenu(popup_menu,event.GetPosition())
        event.Skip()

    def onRenameReport(self, event):
        """
        Переименовать отчет.
        """
        # Определить выбранный пункт дерева
        item = self.rep_tree.GetSelection()
        item_data = self.rep_tree.GetItemData(item)
        # Если это файл отчета, то переименовать его
        if item_data is not None and item_data[REP_ITEMS_IDX] is None:
            old_rep_name = os.path.splitext(os.path.split(item_data[REP_FILE_IDX])[1])[0]
            new_rep_name = dlg.getTextInputDlg(self, u'Переименование отчета',
                                               u'Введите новое имя отчета', old_rep_name)
            # Если имя введено и имя не старое, то переименовать
            if new_rep_name and new_rep_name != old_rep_name:
                new_rep_file_name = os.path.join(os.path.split(item_data[REP_FILE_IDX])[0],
                                                 new_rep_name+'.rprt')
                # Если новый файл не существует, то переименовать старый
                if not os.path.isfile(new_rep_file_name):
                    self.renameReport(item_data[REP_FILE_IDX], new_rep_name)
                else:
                    dlg.getWarningBox(title=u'ВНИМАНИЕ',
                                      message=u'Невозможно поменять имя отчета. Отчет с таким именем уже существует.',
                                      parent=self)

        event.Skip()

    def renameReport(self, rep_filename, new_name):
        """
        Переименовать отчет.
        """
        old_name = os.path.splitext(os.path.split(rep_filename)[1])[0]
        old_rep_file_name = rep_filename
        old_rep_pkl_file_name = os.path.splitext(old_rep_file_name)[0] + '_pkl.rprt'
        old_xls_file_name = os.path.splitext(old_rep_file_name)[0] + '.xls'
        new_rep_file_name = os.path.join(os.path.split(old_rep_file_name)[0],
                                         new_name + '.rprt')
        if os.path.isfile(old_rep_file_name):
            try:
                os.rename(old_rep_file_name, new_rep_file_name)
            except:
                log.fatal(u'Ошибка переименования файла <%s>' % old_rep_file_name)
            # Убить пикловский файл
            if os.path.isfile(old_rep_pkl_file_name):
                os.remove(old_rep_pkl_file_name)
            # Поменять имя в файле отчета.
            report = resfunc.loadResource(new_rep_file_name)
            report['name'] = new_name

            rep_file = None
            try:
                rep_file = open(new_rep_file_name, 'wt')
                rep_file.write(str(report))
                rep_file.close()
            except:
                rep_file.close()

        new_xls_file_name = os.path.join(os.path.split(old_rep_file_name)[0],
                                         new_name + '.xls')
        if os.path.isfile(old_xls_file_name):
            os.rename(old_xls_file_name, new_xls_file_name)
            # Поменять имя листа отчета.
            try:
                # Установить связь с Excel
                excel_app = win32com.client.Dispatch('Excel.Application')
                # Сделать приложение невидимым
                excel_app.Visible = 0
                # Открыть
                rep_tmpl = new_xls_file_name.replace('./', os.getcwd()+'/')
                rep_tmpl_book = excel_app.Workbooks.Open(rep_tmpl)
                rep_tmpl_sheet = rep_tmpl_book.Worksheets(old_name)
                # Переименовать лист
                rep_tmpl_sheet.Name = new_name
                # Сохранить и закрыть
                rep_tmpl_book.save()
                excel_app.Quit()
            except pythoncom.com_error:
                # Вывести сообщение об ошибке в лог
                log.fatal(u'Ошибка переименования файла')

    def onSelectChanged(self, event):
        """
        Изменение выделенного компонента.
        """
        event.Skip()

    def _fillReportTree(self, report_dir):
        """
        Наполнить дерево отчетов данными об отчетах.

        :param report_dir: Директория отчетов.
        """
        # Получить описание всех отчетов
        rep_data = getReportList(report_dir)
        if rep_data is None:
            log.warning(u'Данные не прочитались. Папка отчетов <%s>' % report_dir)
            return
        # Удалить все пункты
        self.rep_tree.DeleteAllItems()
        # Корень
        root = self.rep_tree.AddRoot(u'Отчеты', image=0)
        self.rep_tree.SetItemData(root, None)
        # Добавить пункты дерева по полученному описанию отчетов
        self._appendItemsReportTree(root, rep_data)
        # Развернуть дерево
        self.rep_tree.Expand(root)

    def _appendItemsReportTree(self, parent_id, items):
        """
        Добавить пункты дерева по полученному описанию отчетов.

        :param parent_id: Идентификатор родительского узла.
        :param items: Ветка описаний отчетов.
        """
        if not items:
            log.warning(u'Пустой список описаний отчетов при построении дерева отчетов')

        # Перебрать описания отчетов в описании.
        for item_data in items:
            item = self.rep_tree.AppendItem(parent_id, item_data[REP_DESCRIPT_IDX], -1, -1, data=None)
            # Если описание папки отчетов, то доавить рекурсивно ветку
            if item_data[REP_ITEMS_IDX] is not None:
                self._appendItemsReportTree(item, item_data[REP_ITEMS_IDX])
                # Добавить изображение папки
                self.rep_tree.SetItemImage(item, 0, wx.TreeItemIcon_Normal)
                self.rep_tree.SetItemImage(item, 0, wx.TreeItemIcon_Selected)
            else:
                # Добавить изображение отчета
                self.rep_tree.SetItemImage(item, item_data[REP_IMG_IDX], wx.TreeItemIcon_Normal)
                self.rep_tree.SetItemImage(item, item_data[REP_IMG_IDX], wx.TreeItemIcon_Selected)
            # Добавить связь с данными
            self.rep_tree.SetItemData(item, item_data)

    def setReportDir(self, rep_dir):
        """
        Установить директорий/папку отчетов.

        :param rep_dir: Папка отчетов.
        """
        self._ReportDir = rep_dir

    def getReportDir(self):
        """
        Папка отчетов.
        """
        return self._ReportDir
