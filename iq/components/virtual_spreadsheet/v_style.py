#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

from . import v_prototype

__version__ = (0, 0, 0, 1)

COLOR_ENUM = ('#000000',)


class iqVStyles(v_prototype.iqVPrototype):
    """
    Cell styles.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Styles', '__children__': []}
        self._style_dict = {}
        
        # Vocabulary checksum style content: vocabulary style attributes
        self._md5_styles_dict = {}
        
        # Maximum style ID (entered for optimization)
        self.max_style_id = None
        
    def getMaxStyleID(self):
        if self.max_style_id is None:
            styles_id = self.getStylesID()
            if styles_id:
                self.max_style_id = max(styles_id)
            else:
                self.max_style_id = 's0'
        return self.max_style_id

    def getStyleDict(self):
        """
        Dictionary of styles by their identifiers.
        """
        return self._style_dict

    def initStyleDict(self):
        """
        Initialization of the style dictionary.
        """
        self._style_dict = dict([(style['ID'], style) for style in self._attributes['__children__']])
        return self._style_dict

    style_dict = property(getStyleDict)

    def createStyle(self):
        """
        Create style.
        """
        style = iqVStyle(self)
        attrs = style.create()

        if self._style_dict is None:
            self.initStyleDict()
        else:
            # Just add a style with the style dictionary (for increased performance)
            self._style_dict[attrs['ID']] = attrs
        return style

    def getStyle(self, style_id):
        """
        Searching for a style by ID.
        """
        style = None
        if style_id in self._style_dict:
            style = iqVStyle(self)
            style.setAttributes(self._style_dict[style_id])
        else:
            # Try searching in the list
            find_style = [style_attr for style_attr in self._attributes['__children__']
                          if style_attr['name'] == 'Style' and style_attr['ID'] == style_id]
            if find_style:
                style = iqVStyle(self)
                style.setAttributes(find_style[0])
                # The dictionary was out of sync
                self.initStyleDict()

        # If this style is not found, then return the default style
        if style is None and style_id != 'Default':
            return self.getStyle('Default')
        return style

    def _equalStyleElement(self, style_element_attr1, style_element_attr2):
        """
        Comparison of style elements.

        :return: True - elements are equal, False - not equal.
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
                elif not isinstance(item[1], type(attrs2[item[0]])):
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

        # If child elements are defined, then recursively check them as well
        if equal:
            if ('__children__' in style_element_attr1 and style_element_attr1['__children__']) or \
               ('__children__' in style_element_attr2 and style_element_attr2['__children__']):

                children1 = style_element_attr1['__children__']
                children2 = style_element_attr2['__children__']

                if len(children1) != len(children2):
                    return False

                for i, child1 in enumerate(children1):
                    child2 = children2[i]
                    equal = equal and self._equalStyleElement(child1, child2)

                    if equal is False:
                        break
                
        return equal

    def _compareStyleElement(self, element, element_name, style):
        """
        Comparison of the style element.
        """
        if element:
            elements = [el for el in style['__children__'] if el['name'] == element_name]
            if elements:
                equal = self._equalStyleElement(elements[0], element)
            else:
                equal = False
        else:
            equal = True
        return equal

    def _compareStyleElements(self, style,
                              alignment=None,
                              borders=None, font=None, interior=None,
                              number_format=None):
        """
        Comparison of style elements.
        """
        equal_align = self._compareStyleElement(alignment, 'Alignment', style)
        equal_border = self._compareStyleElement(borders, 'Borders', style)
        equal_font = self._compareStyleElement(font, 'Font', style)
        equal_interior = self._compareStyleElement(interior, 'Interior', style)
        equal_n_fmt = self._compareStyleElement(number_format, 'NumberFormat', style)
        return equal_align and equal_border and equal_font and equal_interior and equal_n_fmt

    def findStyle(self, alignment=None,
                  borders=None, font=None, interior=None,
                  number_format=None):
        """
        Search for a style by its content.
        """
        find_style = None

        md5_style = self._calcCrcStyleAttr(alignment, borders, font, interior, number_format)

        find_result = md5_style in self._md5_styles_dict
        if not find_result:
            # Find style
            for i in range(len(self._attributes['__children__'])):
                style = self._attributes['__children__'][-i]
                # If the number of style elements does not match
                # the number of elements you are looking for,
                # then these styles are not equal
                if len(style['__children__']) != len([element for element in [alignment, borders, font, interior,
                                                                          number_format] if element is not None]):
                    find_result = False
                    continue
            
                find_result = self._compareStyleElements(style, alignment, borders, font, interior, number_format)

                if find_result:
                    find_style = style
                    break
        else:
            # The desired style is in the hash
            find_style = self._md5_styles_dict[md5_style]

        if find_result:
            style = iqVStyle(self)
            if find_style:
                style.setAttributes(find_style)
                # Register in hash
                self._md5_styles_dict[md5_style] = find_style
            return style
        return None

    def _getCrcElementStr(self, element):
        """
        Present an element in string form without additional fields.
        """
        return str(dict([(key, element[key]) for key in element.keys() \
                         if key not in v_prototype.PROTOTYPE_ATTR_NAMES]))
        
    def _getCrcAlignmentStr(self, style):
        """
        Alignment in the string view (for calculating the checksum).
        """
        align = [element for element in style['__children__'] if element['name'] == 'Alignment']
        if align:
            return self._getCrcElementStr(align[0])
        return ''        
        
    def _getCrcBordersStr(self, style):
        """
        Framing in a string view (for calculating the checksum).
        """
        borders = [element for element in style['__children__'] if element['name'] == 'Borders']
        if borders:
            borders_str = ''
            for border in borders[0]['__children__']:
                borders_str += self._getCrcElementStr(border)
            return borders_str
        return ''        

    def _getCrcFontStr(self, style):
        """
        Font in the string view (for calculating the checksum).
        """
        font = [element for element in style['__children__'] if element['name'] == 'Font']
        if font:
            return self._getCrcElementStr(font[0])
        return ''        
        
    def _getCrcInteriorStr(self, style):
        """
        Interior in a string view (for calculating the checksum).
        """
        interior = [element for element in style['__children__'] if element['name'] == 'Interior']
        if interior:
            return self._getCrcElementStr(interior[0])
        return ''        
        
    def _getCrcNumberFormatStr(self, style):
        """
        Format of numbers in a string representation (for calculating the checksum).
        """
        num_fmt = [element for element in style['__children__'] if element['name'] == 'NumberFormat']
        if num_fmt:
            return self._getCrcElementStr(num_fmt[0])
        return ''        
    
    def _calcCrcStyleAttr(self, alignment=None,
                          borders=None, font=None, interior=None,
                          number_format=None):
        """
        To calculate the checksum for the attributes.
        """
        new_style_attr = {'__children__': []}
        if alignment:
            alignment['name'] = 'Alignment'
            new_style_attr['__children__'].append(alignment)
        if borders:
            borders['name'] = 'Borders'
            new_style_attr['__children__'].append(borders)
        if font:
            font['name'] = 'Font'
            new_style_attr['__children__'].append(font)
        if interior:
            interior['name'] = 'Interior'
            new_style_attr['__children__'].append(interior)
        if number_format:
            number_format['name'] = 'NumberFormat'
            new_style_attr['__children__'].append(number_format)
        return self._getCrcStyle(new_style_attr)
        
    def _getCrcStyle(self, style):
        """
        The checksum of the contents of the style.
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
        Delete a style from the cache.
        """
        if crc_style in self._md5_styles_dict:
            del self._md5_styles_dict[crc_style]
            
    def _isCrcStyleID(self, style_id):
        """
        Is there a style with this ID in the cache?

        :return: Returns the checksum of the style in the cache,
            or None if the style is not found.
        """
        result = [i_style for i_style in self._md5_styles_dict.items() if i_style[1]['ID'] == style_id]
        if result:
            return result[0][0]
        return None
        
    def getStylesID(self):
        """
        A list of the IDs of the styles.
        """
        return [style['ID'] for style in self._attributes['__children__']]

    def _createDefaultStyle(self):
        """
        Create the default style if there is none.

        :return: Returns True if the Default style was created, and False if not.
        """
        styles_id = [style_element['ID'] for style_element in self._attributes['__children__']]
        if 'Default' not in styles_id:
            default_style = self.createStyle()
            default_style.setID('Default')
            default_style.setAttrs(alignment={'Vertical': 'Bottom'},
                                   font={'FontName': 'Arial Cyr', 'CharSet': 204})
            return True
        return False
    
    def clearUnUsedStyles(self):
        """
        Deleting unused styles.

        :return: Returns a list of IDs of deleted styles.
        """
        # Create the default style if it is created
        self._createDefaultStyle()
        
        del_styles_id = []
        styles_id = self.getStylesID()
        # Defining the IDs of the styles used
        used_styles_id = ['Default']
        work_sheets = [element for element in self._parent._attributes['__children__'] if element['name'] == 'Worksheet']
        for work_sheet in work_sheets:
            tables = [element for element in work_sheet['__children__'] if element['name'] == 'Table']
            for table in tables:
                if 'StyleID' in table:
                    style_id = table['StyleID']
                    if style_id not in used_styles_id:
                        used_styles_id.append(style_id)
                for tab_element in table['__children__']:
                    if 'StyleID' in tab_element:
                        style_id = tab_element['StyleID']
                        if style_id not in used_styles_id:
                            used_styles_id.append(style_id)
                    if tab_element['name'] == 'Row':
                        for cell in tab_element['__children__']:
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
        Delete a style by ID.
        """
        try:
            style_idx = self.getStylesID().index(style_id)
        except ValueError:
            return False
        
        if style_idx >= 0:
            del self._attributes['__children__'][style_idx]
            return True
        return False


class iqVStyle(v_prototype.iqVPrototype):
    """
    Cell style.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        # self._attributes = dict(DEFAULT_STYLE_ATTR.items()+[('ID', self.newID())])
        self._attributes = {'ID': self.newID(), 'name': 'Style', '__children__': []}

    def getID(self):
        """
        Style id.
        """
        return self._attributes['ID']
    
    def setID(self, id_name):
        """
        Set style id.

        :param id_name: Id name.
        """
        self._attributes['ID'] = str(id_name)
    
    def newID(self):
        """
        The generation of a new ID style.
        """
        max_style_id = self._parent.getMaxStyleID()
        max_str_i = ''.join([symb for symb in max_style_id if symb.isdigit()])
        i = int(max_str_i)+1 if max_str_i else 0
        new_id = 'text' + str(i)

        # Remember the maximum style ID
        self._parent.max_style_id = new_id
        return new_id

    def newID_depricated(self):
        """
        The generation of a new ID style.
        """
        styles_id = self._parent.getStylesID()
        i = 1
        while ('text'+str(i)) in styles_id:
            i += 1
        
        return 'text'+str(i)

    def _delAttr(self, name):
        """
        Delete an attribute by name from the style content.
        """
        try:
            idx = [attr['name'] for attr in self._attributes['__children__']].index(name)
        except ValueError:
            idx = -1
        if idx >= 0:
            del self._attributes['__children__'][idx]
        return self._attributes
    
    def setAttrs(self, alignment=None,
                 borders=None, font=None, interior=None,
                 number_format=None):
        """
        Filling in the style content.
        """
        self._attributes['__children__'] = []
        return self.updateAttrs(alignment, borders, font, interior, number_format)
        
    def updateAttrs(self, alignment=None,
                    borders=None, font=None, interior=None,
                    number_format=None, update_attrs=None):
        """
        Filling in the style content.
        """
        if update_attrs is None:
            style_attrs = self._attributes['__children__']
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
        self._attributes['__children__'] = style_attrs
        
        if self._parent:
            md5_attrs = self._parent._isCrcStyleID(self.getID())
            if md5_attrs:
                self._parent._delCrcStyle(md5_attrs)
        return self._attributes

    def getAttrs(self):
        """
        Style attributes.

        :return: Dictionary of internal style content.
        """
        attrs = {}
        for element in self._attributes['__children__']:
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
        Create alignment.
        """
        align = iqVAlignment(self)
        attrs = align.create()
        return align

    def createBorders(self):
        """
        Create borders.
        """
        borders = iqVBorders(self)
        attrs = borders.create()
        return borders

    def createFont(self):
        """
        Create font.
        """
        font = iqVFont(self)
        attrs = font.create()
        return font

    def createInterior(self):
        """
        Create interior.
        """
        interior = iqVInterior(self)
        attrs = interior.create()
        return interior

    def createNumberFormat(self):
        """
        Create number format.
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
    Alignment.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Alignment'}


class iqVBorders(v_prototype.iqVPrototype):
    """
    Borders.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'Borders', '__children__': []}


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
    Border.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
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
    Font.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
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
    Interior.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
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
    Number num_format.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.
        """
        v_prototype.iqVPrototype.__init__(self, parent, *args, **kwargs)
        self._attributes = {'name': 'NumberFormat'}
