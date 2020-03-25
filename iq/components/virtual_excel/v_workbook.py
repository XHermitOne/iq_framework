#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

try:
    from . import v_prototype
    from . import v_worksheet
    from . import v_style
except ImportError:
    # Для запуска тестов
    import icprototype
    import icworksheet
    import icstyle


__version__ = (0, 1, 2, 1)


class iqVWorkbook(v_prototype.iqVPrototype):
    """
    Книга.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Workbook', 'children': []}
        # Словарь листов по именам
        self._worksheet_dict = {}

        self.Name = None
        
        # Управление стилями
        self.styles = None

    def load(self, name):
        """
        Загрузить.
        """
        self.Name=os.path.abspath(name.strip())
        return self._parent.load(name)

    def save(self):
        """
        Сохранить книгу.
        """
        return self._parent.save()

    def saveAs(self, name):
        """
        Сохранить как...
        """
        self.Name = os.path.abspath(name.strip())
        return self._parent.saveAs(self.Name)
    
    def get_worksheet_dict(self):
        """
        Словарь листов по именам.
        """
        return self._worksheet_dict

    def init_worksheet_dict(self):
        """
        Инициализация словаря листов.
        """
        self._worksheet_dict = dict([(worksheet['Name'], worksheet) for worksheet in \
                                    [element for element in self._attributes['children'] if element['name'] == 'Worksheet']])
        return self._worksheet_dict
        
    worksheet_dict = property(get_worksheet_dict)

    def create(self):
        """
        Создать.
        """
        attrs = self._parent.getAttributes()
        # Т.к. в XML файле м.б. только одна книга, то здесь нельзя добавять
        # а только заменять описание книги
        attrs['children'] = [self._attributes]
        return self._attributes

    def createWorksheet(self):
        """
        Создать лист.
        """
        work_sheet = v_worksheet.iqVWorksheet(self)
        attrs = work_sheet.create()
        self.init_worksheet_dict()
        return work_sheet

    def _find_worksheet_attr_name(self, worksheets, name):
        """
        Найти лист в списке по имени.
        """
        work_sheet_attr = None

        if not isinstance(name, str):
            name = str(name)  # 'utf-8')
            
        for sheet in worksheets:
            if not isinstance(sheet['Name'], str):
                sheet_name = str(sheet['Name'])   #  'utf-8')
            else:
                sheet_name = sheet['Name']
            if sheet_name == name:
                work_sheet_attr = sheet
                break
        return work_sheet_attr
            
    def findWorksheet(self, name):
        """
        Поиск листа по имени.
        """
        work_sheet = None
        if name in self._worksheet_dict:
            work_sheet = v_worksheet.iqVWorksheet(self)
            work_sheet.setAttributes(self._worksheet_dict[name])
        else:
            # Попробовать поискать в списке
            find_worksheet = self._find_worksheet_attr_name([element for element in self._attributes['children'] \
                                                             if element['name'] == 'Worksheet'], name)
            if find_worksheet:
                work_sheet = v_worksheet.iqVWorksheet(self)
                work_sheet.setAttributes(find_worksheet)
                # Блин рассинхронизация произошла со словарем
                self.init_worksheet_dict()
        return work_sheet

    def getWorksheetIdx(self, idx=0):
        """
        Лист по индексу.
        """    
        work_sheets = [element for element in self._attributes['children'] if element['name'] == 'Worksheet']
        try:
            worksheet_attr = work_sheets[idx]
            work_sheet = v_worksheet.iqVWorksheet(self)
            work_sheet.setAttributes(worksheet_attr)
            return work_sheet
        except:
            print('Error getWorksheetIdx')
            raise
    
    def createStyles(self):
        """
        Создать стили.
        """
        styles = v_style.iqVStyles(self)
        attrs = styles.create()
        return styles

    def getStylesAttrs(self):
        """
        Стили.
        """
        styles = [element for element in self._attributes['children'] if element['name'] == 'Styles']
        if styles:
            return styles[0]
        return None

    def getStyles(self):
        """
        Объект стилей.
        """
        if self.styles:
            return self.styles
        
        styles_data = self.getStylesAttrs()
        if styles_data is None:
            self.styles = self.createStyles()
        else:
            self.styles = v_style.iqVStyles(self)
            self.styles.setAttributes(styles_data)
        return self.styles

    def getWorksheetNames(self):
        """
        Список имен листов книги.
        """
        return [work_sheet['Name'] for work_sheet in self._attributes['children'] if work_sheet['name'] == 'Worksheet']
