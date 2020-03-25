#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

try:
    from . import v_prototype
except ImportError:
    # Для запуска тестов
    import icprototype

__version__ = (0, 1, 2, 1)

COLOR_ENUM = ('#000000',)


class iqVStyles(v_prototype.iqVPrototype):
    """
    Стили ячеек.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Styles', 'children': []}
        self._style_dict = {}
        
        # Словарь контрольная сумма содержания стиля:словарь атрибутов стиля
        self._md5_styles_dict = {}
        
        # Максимальный идентификатор стиля (введен для оптимизации)
        self.max_style_id = None
        
    def getMaxStyleID(self):
        if self.max_style_id is None:
            styles_id = self.getStylesID()
            if styles_id:
                self.max_style_id = max(styles_id)
            else:
                self.max_style_id = 's0'
        return self.max_style_id

    def get_style_dict(self):
        """
        Словарь стилей по их идентификаторам.
        """
        return self._style_dict

    def init_style_dict(self):
        """
        Инициализация словаря стилей.
        """
        self._style_dict = dict([(style['ID'], style) for style in self._attributes['children']])
        return self._style_dict

    style_dict = property(get_style_dict)

    def createStyle(self):
        """
        Создать стиль.
        """
        style = iqVStyle(self)
        attrs = style.create()

        if self._style_dict is None:
            self.init_style_dict()
        else:
            # Просто добавить стиль с словарь стилей (для увеличения производительности)
            self._style_dict[attrs['ID']] = attrs
        return style

    def getStyle(self, style_id):
        """
        Поиск стиля по идентификатору.
        """
        style = None
        if style_id in self._style_dict:
            style = iqVStyle(self)
            style.setAttributes(self._style_dict[style_id])
        else:
            # Попробовать поискать в списке
            find_style = [style_attr for style_attr in self._attributes['children']
                          if style_attr['name'] == 'Style' and style_attr['ID'] == style_id]
            if find_style:
                style = iqVStyle(self)
                style.setAttributes(find_style[0])
                # Блин рассинхронизация произошла со словарем
                self.init_style_dict()

        # Если такой стиль не найден, тогда вернуть стиль по умолчанию
        if style is None and style_id != 'Default':
            return self.getStyle('Default')
        return style

    def _equalStyleElement(self, style_element_attr1, style_element_attr2):
        """
        Сравнение элементов стилей.

        :return: True - элементы равны, False - не равны.
        """
        if ((style_element_attr1 is None) and (style_element_attr2 is not None)) or \
           ((style_element_attr1 is not None) and (style_element_attr2 is None)):
            return False
            
        attrs1 = dict([item for item in style_element_attr1.items() if item[0] not in v_prototype.PROTOTYPE_ATTR_NAMES])
        attrs2 = dict([item for item in style_element_attr2.items() if item[0] not in v_prototype.PROTOTYPE_ATTR_NAMES])
        equal = True
        for item in attrs1.items():
            try:
                if item[1] == attrs2[item[0]]:
                    pass
                elif type(item[1]) != type(attrs2[item[0]]):
                    value1 = item[1]
                    if isinstance(value1, bool):
                        value1 = int(value1)
                    value2 = attrs2[item[0]]
                    if isinstance(value2, bool):
                        value2 = int(value2)
                    equal = equal and (str(value1) == str(value2))
                else:
                    equal = False
            except KeyError:
                return False

            if equal is False:
                break

        # Если определены дочерние елементы, то рекурсивно проверить и их
        if equal:
            if ('children' in style_element_attr1 and style_element_attr1['children']) or \
               ('children' in style_element_attr2 and style_element_attr2['children']):

                children1 = style_element_attr1['children']
                children2 = style_element_attr2['children']

                if len(children1) != len(children2):
                    return False

                for i, child1 in enumerate(children1):
                    child2 = children2[i]
                    equal = equal and self._equalStyleElement(child1, child2)

                    if equal is False:
                        break
                
        return equal

    def _compare_style_element(self, element, element_name, style):
        """
        Сравнение елемента стиля.
        """
        if element:
            elements = [el for el in style['children'] if el['name'] == element_name]
            if elements:
                equal = self._equalStyleElement(elements[0], element)
            else:
                equal = False
        else:
            equal = True
        return equal

    def _compare_style_elements(self, style,
                                alignment=None,
                                borders=None, font=None, interior=None,
                                number_format=None):
        """
        Сравнение элементов стиля.
        """
        equal_align = self._compare_style_element(alignment, 'Alignment', style)
        equal_border = self._compare_style_element(borders, 'Borders', style)
        equal_font = self._compare_style_element(font, 'Font', style)
        equal_interior = self._compare_style_element(interior, 'Interior', style)
        equal_n_fmt = self._compare_style_element(number_format, 'NumberFormat', style)
        return equal_align and equal_border and equal_font and equal_interior and equal_n_fmt

    def findStyle(self, alignment=None,
                  borders=None, font=None, interior=None,
                  number_format=None):
        """
        Поиск стиля по его содержанию.
        """
        find_style = None

        md5_style = self._calcCrcStyleAttr(alignment, borders, font, interior, number_format)

        find_result = md5_style in self._md5_styles_dict
        if not find_result:
            # Надо поискать стиль
            for i in range(len(self._attributes['children'])):
                style = self._attributes['children'][-i]
                # Если количество элементов стиля не совпадает с количеством
                # искомых элементов, то эти стили не равны
                if len(style['children']) != len([element for element in [alignment, borders, font, interior,
                                                                          number_format] if element is not None]):
                    find_result = False
                    continue
            
                find_result = self._compare_style_elements(style, alignment, borders, font, interior, number_format)

                if find_result:
                    find_style = style
                    break
        else:
            # Искомый стиль есть в хеше
            find_style = self._md5_styles_dict[md5_style]

        if find_result:
            style = iqVStyle(self)
            if find_style:
                style.setAttributes(find_style)
                # Прописать в хэшэ
                self._md5_styles_dict[md5_style] = find_style
            return style
        return None

    def _getCrcElementStr(self, element):
        """
        Представить в строковом виде элемент без дополнительных полей.
        """
        return str(dict([(key, element[key]) for key in element.keys() \
                         if key not in v_prototype.PROTOTYPE_ATTR_NAMES]))
        
    def _getCrcAlignmentStr(self, style):
        """
        Выравнивание в строковом представлении (для вычисления контрольной суммы).
        """
        align = [element for element in style['children'] if element['name'] == 'Alignment']
        if align:
            return self._getCrcElementStr(align[0])
        return ''        
        
    def _getCrcBordersStr(self, style):
        """
        Обрамление в строковом представлении (для вычисления контрольной суммы).
        """
        borders = [element for element in style['children'] if element['name'] == 'Borders']
        if borders:
            borders_str = ''
            for border in borders[0]['children']:
                borders_str += self._getCrcElementStr(border)
            return borders_str
        return ''        

    def _getCrcFontStr(self, style):
        """
        Шрифт в строковом представлении (для вычисления контрольной суммы).
        """
        font = [element for element in style['children'] if element['name'] == 'Font']
        if font:
            return self._getCrcElementStr(font[0])
        return ''        
        
    def _getCrcInteriorStr(self, style):
        """
        Интерьер в строковом представлении (для вычисления контрольной суммы).
        """
        interior = [element for element in style['children'] if element['name'] == 'Interior']
        if interior:
            return self._getCrcElementStr(interior[0])
        return ''        
        
    def _getCrcNumberFormatStr(self, style):
        """
        Формат чисел в строковом представлении (для вычисления контрольной суммы).
        """
        num_fmt = [element for element in style['children'] if element['name'] == 'NumberFormat']
        if num_fmt:
            return self._getCrcElementStr(num_fmt[0])
        return ''        
    
    def _calcCrcStyleAttr(self, alignment=None,
                          borders=None, font=None, interior=None,
                          number_format=None):
        """
        Вычислить контрольную сумму по атрибутам.
        """
        new_style_attr = {'children': []}
        if alignment:
            alignment['name'] = 'Alignment'
            new_style_attr['children'].append(alignment)
        if borders:
            borders['name'] = 'Borders'
            new_style_attr['children'].append(borders)
        if font:
            font['name'] = 'Font'
            new_style_attr['children'].append(font)
        if interior:
            interior['name'] = 'Interior'
            new_style_attr['children'].append(interior)
        if number_format:
            number_format['name'] = 'NumberFormat'
            new_style_attr['children'].append(number_format)
        return self._getCrcStyle(new_style_attr)
        
    def _getCrcStyle(self, style):
        """
        Контрольная сумма содержания стиля.
        """
        style_str = ''
        # Alignment
        style_str += self._getCrcAlignmentStr(style)
        # Borders
        style_str += self._getCrcBordersStr(style)
        # Font
        style_str += self._getCrcFontStr(style)
        # Interior
        style_str += self._getCrcInteriorStr(style)
        # NumberFormat
        style_str += self._getCrcNumberFormatStr(style)
        return hashlib.md5(style_str).hexdigest()

    def _delCrcStyle(self, crc_style):
        """
        Удалить стиль из кеша.
        """
        if crc_style in self._md5_styles_dict:
            del self._md5_styles_dict[crc_style]
            
    def _isCrcStyleID(self, style_id):
        """
        Есть ли в кеше стиль с таким идентификатором?

        :return: Возвращает контрольную сумму стиля в кеше или None,
            если стиль не найден.
        """
        result = [i_style for i_style in self._md5_styles_dict.items() if i_style[1]['ID'] == style_id]
        if result:
            return result[0][0]
        return None
        
    def getStylesID(self):
        """
        Список идентификаторов стилей.
        """
        return [style['ID'] for style in self._attributes['children']]

    def _createDefaultStyle(self):
        """
        Создать стиль по умолчанию, если его нет.

        :return: Возвращает True-если стиль Default создан,
        и False-если нет.
        """
        styles_id = [style_element['ID'] for style_element in self._attributes['children']]
        if 'Default' not in styles_id:
            default_style = self.createStyle()
            default_style.setID('Default')
            default_style.setAttrs(alignment={'Vertical': 'Bottom'},
                                   font={'FontName': 'Arial Cyr', 'CharSet': 204})
            return True
        return False
    
    def clearUnUsedStyles(self):
        """
        Удаление не используемых стилей.

        :return: Возвращает список идентификаторов удаленных стилей.
        """
        # Создать стиль по умолчанию если он создан
        self._createDefaultStyle()
        
        del_styles_id = []
        styles_id = self.getStylesID()
        # Определение идентификаторов используемых стилей
        used_styles_id = ['Default']
        work_sheets = [element for element in self._parent._attributes['children'] if element['name'] == 'Worksheet']
        for work_sheet in work_sheets:
            tables = [element for element in work_sheet['children'] if element['name'] == 'Table']
            for table in tables:
                if 'StyleID' in table:
                    style_id = table['StyleID']
                    if style_id not in used_styles_id:
                        used_styles_id.append(style_id)
                for tab_element in table['children']:
                    if 'StyleID' in tab_element:
                        style_id = tab_element['StyleID']
                        if style_id not in used_styles_id:
                            used_styles_id.append(style_id)
                    if tab_element['name'] == 'Row':
                        for cell in tab_element['children']:
                            if 'StyleID' in cell:
                                style_id = cell['StyleID']
                                if style_id not in used_styles_id:
                                    used_styles_id.append(style_id)
                                    
        for style_id in styles_id:
            if style_id not in used_styles_id:
                result = self.delStyleByID(style_id)
                if result:
                    del_styles_id.append(style_id)
                
        return del_styles_id
                
    def delStyleByID(self, style_id):
        """
        Удалить стиль по идентификатору.
        """
        try:
            style_idx = self.getStylesID().index(style_id)
        except ValueError:
            return False
        
        if style_idx >= 0:
            del self._attributes['children'][style_idx]
            return True
        return False


class iqVStyle(v_prototype.iqVPrototype):
    """
    Стиль ячеек.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        # self._attributes = dict(DEFAULT_STYLE_ATTR.items()+[('ID', self.newID())])
        self._attributes = {'ID': self.newID(), 'name': 'Style', 'children': []}

    def getID(self):
        """
        Идентификатор стиля.
        """
        return self._attributes['ID']
    
    def setID(self, id_name):
        """
        Идентификатор стиля.

        :param id_name: Имя идентификатора.
        """
        self._attributes['ID'] = str(id_name)
    
    def newID(self):
        """
        Генерация нового идетификатора стиля.
        """
        max_style_id = self._parent.getMaxStyleID()
        max_str_i = ''.join([symb for symb in max_style_id if symb.isdigit()])
        i = int(max_str_i)+1 if max_str_i else 0
        new_id = 'text' + str(i)

        # Запомнить максимальный идентификатор стиля
        self._parent.max_style_id = new_id
        return new_id

    def newID_depricated(self):
        """
        Генерация нового идетификатора стиля.
        """
        styles_id = self._parent.getStylesID()
        i = 1
        while ('text'+str(i)) in styles_id:
            i += 1
        
        return 'text'+str(i)

    def _delAttr(self, name):
        """
        Удалить из содержания стиля атрибут по имени.
        """
        try:
            idx = [attr['name'] for attr in self._attributes['children']].index(name)
        except ValueError:
            idx = -1
        if idx >= 0:
            del self._attributes['children'][idx]
        return self._attributes
    
    def setAttrs(self, alignment=None,
                 borders=None, font=None, interior=None,
                 number_format=None):
        """
        Заполнение содержания стиля.
        """
        self._attributes['children'] = []
        return self.updateAttrs(alignment, borders, font, interior, number_format)
        
    def updateAttrs(self, alignment=None,
                    borders=None, font=None, interior=None,
                    number_format=None, update_attrs=None):
        """
        Заполнение содержания стиля.
        """
        if update_attrs is None:
            style_attrs = self._attributes['children']
        else:
            style_attrs = update_attrs
            
        if alignment:
            self._delAttr('Alignment')
            alignment['name'] = 'Alignment'
            style_attrs.append(alignment)
        if borders:
            self._delAttr('Borders')
            borders['name'] = 'Borders'
            style_attrs.append(borders)
        if font:
            self._delAttr('Font')
            font['name'] = 'Font'
            style_attrs.append(font)
        if interior:
            self._delAttr('Interior')
            interior['name'] = 'Interior'
            style_attrs.append(interior)
        if number_format:
            self._delAttr('NumberFormat')
            number_format['name'] = 'NumberFormat'
            style_attrs.append(number_format)
        self._attributes['children'] = style_attrs
        
        if self._parent:
            md5_attrs = self._parent._isCrcStyleID(self.getID())
            if md5_attrs:
                self._parent._delCrcStyle(md5_attrs)
        return self._attributes

    def getAttrs(self):
        """
        Содержание стиля.

        :return: Словарь внутреннего содержания стиля.
        """
        attrs = {}
        for element in self._attributes['children']:
            if element['name'] == 'Alignment':
                attrs['alignment'] = element
            elif element['name'] == 'Borders':
                attrs['borders'] = element
            elif element['name'] == 'Font':
                attrs['font'] = element
            elif element['name'] == 'Interior':
                attrs['interior'] = element
            elif element['name'] == 'NumberFormat':
                attrs['number_format'] = element
        return attrs
        
    def createAlignment(self):
        """
        Создать выравнивание.
        """
        align = iqVAlignment(self)
        attrs = align.create()
        return align

    def createBorders(self):
        """
        Создать обрамление.
        """
        borders = iqVBorders(self)
        attrs = borders.create()
        return borders

    def createFont(self):
        """
        Создать шрифт.
        """
        font = iqVFont(self)
        attrs = font.create()
        return font

    def createInterior(self):
        """
        Создать заливку.
        """
        interior = iqVInterior(self)
        attrs = interior.create()
        return interior

    def createNumberFormat(self):
        """
        Создать формат.
        """
        fmt = iqVNumberFormat(self)
        attrs = fmt.create()
        return fmt


HORIZONTAL_ENUM = ('Automatic', 'Left', 'Center', 'Right', 'Fill', 'Justify',
                   'CenterAcrossSelection', 'Distributed', 'JustifyDistributed')
VERTICAL_ENUM = ('Automatic', 'Top', 'Center', 'Bottom', 'Justify',
                 'Distributed', 'JustifyDistributed')
READINGORDER_ENUM = ('RightToLeft', 'LeftToRight', 'Context')

ALIGNMENT_SPC = {'Horizontal': HORIZONTAL_ENUM[0],
                 'Indent': 0,
                 'ReadingOrder': READINGORDER_ENUM[-1],
                 'Rotate': 0,
                 'ShrinkToFit': False,
                 'Vertical': VERTICAL_ENUM[0],
                 'VerticalText': False,
                 'WrapText': False}


class iqVAlignment(v_prototype.iqVPrototype):
    """
    Выравнивание.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Alignment'}


class iqVBorders(v_prototype.iqVPrototype):
    """
    Обрамление.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Borders', 'children': []}


POSITION_ENUM = ('Left', 'Top', 'Right', 'Bottom', 'DiagonalLeft', 'DiagonalRight')
LINESTYLE_ENUM = ('None', 'Continuous', 'Dash', 'Dot', 'DashDot', 'DashDotDot',
                  'SlantDashDot', 'Double')

BORDER_SPC = {'Position': POSITION_ENUM[0],
              'Color': COLOR_ENUM[0],
              'LineStyle': LINESTYLE_ENUM[0],
              'Weight': 0
              }


class iqVBorder(v_prototype.iqVPrototype):
    """
    Обрамление.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Border'}


UNDERLINE_ENUM = ('None', 'Single', 'Double',
                  'SingleAccounting', 'DoubleAccounting')
VERTICALALIGN_ENUM = ('None', 'Subscript', 'Superscript')

FAMILY_ENUM = ('Automatic', 'Decorative', 'Modern', 'Roman', 'Script', 'Swiss')

FONT_SPC = {'Bold': False,
            'Color': COLOR_ENUM[0],
            'FontName': 'Arial',
            'Italic': False,
            'Outline': False,
            'Shadow': False,
            'Size': 10,
            'StrikeThrogh': False,
            'Underline': UNDERLINE_ENUM[0],
            'VerticalAlign': VERTICALALIGN_ENUM[0],
            'CharSet': 0,
            'Family': FAMILY_ENUM[0]
            }


class iqVFont(v_prototype.iqVPrototype):
    """
    Шрифт.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Font'}


PATTERN_ENUM = ('None', 'Solid',
                'Gray75', 'Gray50', 'Gray25', 'Gray125', 'Gray0625',
                'HorizStripe', 'VertStripe', 'ReverseDiagStripe', 'DiagStripe',
                'DiagCross', 'ThickDiagCross', 'ThinHorzStripe', 'ThinVertStripe',
                'ThinReverseDiagStripe', 'ThinDiagStripe',
                'ThinHorzCross', 'ThinDiagCross')

INTERIOR_SPC = {'Color': COLOR_ENUM[0],
                'Pattern': PATTERN_ENUM[1],
                'PatternColor': COLOR_ENUM[0]
                }


class iqVInterior(v_prototype.iqVPrototype):
    """
    Заливка.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Interior'}


FORMAT_ENUM = ('General', 'General Number', 'General Date',
               'Long Date', 'Medium Date', 'Short Date',
               'Long Time', 'Medium Time', 'Short Time',
               'Currency', 'Euro Currency', 'Fixed', 'Stadart',
               'Percent', 'Scientific', 'Yes/No', 'True/False', 'On/Off')

NUMBERFORMAT_SPC = {'Format': FORMAT_ENUM[0]}
    

class iqVNumberFormat(v_prototype.iqVPrototype):
    """
    Формат.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Конструктор.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'NumberFormat'}
