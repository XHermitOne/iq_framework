#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx OGL diagram class module.
"""

import wx
import wx.lib.ogl

from . import divided_shape

from ...util import id_func

__version__ = (0, 1, 1, 1)

DEFAULT_MAX_WIDTH = 1500
DEFAULT_MAX_HEIGHT = 1500

# Default shape size
DEFAULT_OGL_SHAPE_WIDTH = 150
DEFAULT_OGL_SHAPE_HEIGHT = 70

# Auto-placement spacer
DEFAULT_AUTOLAYOUT_SPACER_X = 50
DEFAULT_AUTOLAYOUT_SPACER_Y = 50

# Pens
BLACK_DASHED_PEN = wx.BLACK_DASHED_PEN
BLACK_PEN = wx.BLACK_PEN
CYAN_PEN = wx.CYAN_PEN
GREY_PEN = wx.GREY_PEN
LIGHT_GREY_PEN = wx.LIGHT_GREY_PEN
MEDIUM_GREY_PEN = wx.MEDIUM_GREY_PEN
RED_PEN = wx.RED_PEN
TRANSPARENT_PEN = wx.TRANSPARENT_PEN
WHITE_PEN = wx.WHITE_PEN
PEN_LIST = [BLACK_DASHED_PEN, BLACK_PEN, CYAN_PEN, GREY_PEN, LIGHT_GREY_PEN,
            MEDIUM_GREY_PEN, RED_PEN, TRANSPARENT_PEN, WHITE_PEN]
PEN_STR_LIST = ['BLACK_DASHED_PEN', 'BLACK_PEN', 'CYAN_PEN', 'GREY_PEN', 'LIGHT_GREY_PEN',
                'MEDIUM_GREY_PEN', 'RED_PEN', 'TRANSPARENT_PEN', 'WHITE_PEN']

# Brushes
BLACK_BRUSH = wx.BLACK_BRUSH
BLUE_BRUSH = wx.BLUE_BRUSH
CYAN_BRUSH = wx.CYAN_BRUSH
GREY_BRUSH = wx.GREY_BRUSH
LIGHT_GREY_BRUSH = wx.LIGHT_GREY_BRUSH
MEDIUM_GREY_BRUSH = wx.MEDIUM_GREY_BRUSH
RED_BRUSH = wx.RED_BRUSH
TRANSPARENT_BRUSH = wx.TRANSPARENT_BRUSH
WHITE_BRUSH = wx.WHITE_BRUSH
BRUSH_LIST = [BLACK_BRUSH, BLUE_BRUSH, CYAN_BRUSH, GREY_BRUSH, LIGHT_GREY_BRUSH,
              MEDIUM_GREY_BRUSH, RED_BRUSH, TRANSPARENT_BRUSH, WHITE_BRUSH]
BRUSH_STR_LIST = ['BLACK_BRUSH', 'BLUE_BRUSH', 'CYAN_BRUSH', 'GREY_BRUSH', 'LIGHT_GREY_BRUSH',
                  'MEDIUM_GREY_BRUSH', 'RED_BRUSH', 'TRANSPARENT_BRUSH', 'WHITE_BRUSH']

# Arrows
ARROW_HOLLOW_CIRCLE = wx.lib.ogl.ARROW_HOLLOW_CIRCLE
ARROW_FILLED_CIRCLE = wx.lib.ogl.ARROW_FILLED_CIRCLE
ARROW_ARROW = wx.lib.ogl.ARROW_ARROW
ARROW_SINGLE_OBLIQUE = wx.lib.ogl.ARROW_SINGLE_OBLIQUE
ARROW_DOUBLE_OBLIQUE = wx.lib.ogl.ARROW_DOUBLE_OBLIQUE
ARROW_LIST = [ARROW_HOLLOW_CIRCLE, ARROW_FILLED_CIRCLE, ARROW_ARROW,
              ARROW_SINGLE_OBLIQUE, ARROW_DOUBLE_OBLIQUE]
ARROW_STR_LIST = ['ARROW_HOLLOW_CIRCLE', 'ARROW_FILLED_CIRCLE', 'ARROW_ARROW',
                  'ARROW_SINGLE_OBLIQUE', 'ARROW_DOUBLE_OBLIQUE']


class iqOGLDiagramViewerProto(wx.lib.ogl.ShapeCanvas):
    """
    Wx OGL diagram viewer class.
    """
    is_ogl_initialized = False

    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window.
        """
        # Init OGL
        if not self.is_ogl_initialized:
            wx.lib.ogl.OGLInitialize()
            self.is_ogl_initialized = True

        wx.lib.ogl.ShapeCanvas.__init__(self, parent, id=wx.NewId(), style=wx.NO_BORDER)

        self.SetScrollbars(20, 20, round(DEFAULT_MAX_WIDTH / 20), round(DEFAULT_MAX_HEIGHT / 20))

        self.diagram = None
        # Shapes
        self.shapes = dict()
        # Lines
        self.lines = dict()

        # Diagramm data
        self.diagram_res = None

        # Init
        self.init()

        self._default_parameters = dict()

        # Current selected shape
        self.selected_shape = None

    def init(self):
        """
        Initialization.
        """
        # Diagram
        self.diagram = wx.lib.ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)

    def createShape(self, **attrs):
        """
        Create shape.

        :param attrs: Attributes.
        """
        shape = None
        if 'type' in attrs and 'name' in attrs:
            type = attrs['type']
            name = attrs['name']
            if 'size' in attrs:
                width, height = tuple(attrs['size'])
            else:
                width, height = (DEFAULT_OGL_SHAPE_WIDTH, DEFAULT_OGL_SHAPE_HEIGHT)

            if type in (divided_shape.DIVIDED_SHAPE_TYPE, ):
                shape = divided_shape.iqDividedShape(name=name, width=width, height=height, canvas=self)
                shape.cod = attrs.get('cod', None)

        return shape

    def _isPointInArea(self, x, y, left, top, width, height):
        """
        Is the specified point in the area?
        """
        return left <= x <= (left + width) and top <= y <= (top + height)

    def _getShapeIntersectionArea(self, left, top, width, height):
        """
        Find the shape intersecting the specified area.
        """
        for shape in self.shapes.values():
            x = shape.GetX()
            y = shape.GetY()
            width = shape.GetWidth() if not width else width
            height = shape.GetHeight() if not height else height
            if self._isPointInArea(x, y, left, top, width, height) or \
               self._isPointInArea(x + width, y, left, top, width, height) or \
               self._isPointInArea(x, y + height, left, top, width, height) or \
               self._isPointInArea(x + width, y + height, left, top, width, height):
                return shape
        return None

    def genAutoLayoutPosXY(self, shape_attributes):
        """
        Generating the next shape location.

        :param shape_attributes: Shape attributes.
        :return: eturns the tuple of coordinates of the shape on the canvas.
        """
        try:
            x = DEFAULT_AUTOLAYOUT_SPACER_X + 50
            y = DEFAULT_AUTOLAYOUT_SPACER_Y
            if 'size' in shape_attributes:
                width, height = tuple(shape_attributes['size'])
            else:
                width, height = (DEFAULT_OGL_SHAPE_WIDTH, DEFAULT_OGL_SHAPE_HEIGHT)

            # Generate Y
            to_lines = [line for line in self.diagram_res['lines'] if line['to'] == shape_attributes['name']]
            for line in to_lines:
                from_shape = self.findShape(line['from'])
                if from_shape:
                    max_y = from_shape.GetY() + from_shape.GetHeight() + DEFAULT_AUTOLAYOUT_SPACER_Y
                    if max_y > y:
                        y = max_y
            from_lines = [line for line in self.diagram_res['lines'] if line['from'] == shape_attributes['name']]
            for line in from_lines:
                to_shape = self.findShape(line['to'])
                if to_shape:
                    max_y = to_shape.GetY() + to_shape.GetHeight() + DEFAULT_AUTOLAYOUT_SPACER_Y
                    if max_y > y:
                        y = max_y

            # Generate X
            intersection_shape = self._getShapeIntersectionArea(x, y, width, height)
            while intersection_shape is not None:
                x = intersection_shape.GetX() + intersection_shape.GetWidth() + DEFAULT_AUTOLAYOUT_SPACER_X
                intersection_shape = self._getShapeIntersectionArea(x, y, width, height)

            return x, y
        except:
            return DEFAULT_AUTOLAYOUT_SPACER_X + 50, DEFAULT_AUTOLAYOUT_SPACER_Y

    def setDefaultParameters(self, parameters):
        """
        Устанавливает позиции по умолчанию.
        """
        self._default_parameters = parameters

    def getDefaultParameters(self):
        """
        Возвращает позиции по умолчанию.
        """
        return self._default_parameters

    def setShapeProperties(self, shape, **shape_attributes):
        """
        Set shape properties.

        :param shape: Shape object.
        :param shape_attributes: Shape attributes.
        """
        if shape:
            is_draggable = self.isDraggable()
            shape.SetDraggable(is_draggable, is_draggable)
            shape.SetCanvas(self)

            # Set the coordinates, if they are defined
            if self._default_parameters.get(shape.name, None):
                x, y, width, height = self._default_parameters[shape.name]
                shape.SetWidth(width)
                shape.SetHeight(height)
                shape.SetX(x)
                shape.SetY(y)
            else:
                if 'pos' in shape_attributes:
                    x, y = tuple(shape_attributes['pos'])
                else:
                    x, y = self.genAutoLayoutPosXY(shape_attributes)
                shape.SetX(x)
                shape.SetY(y)

                # Set the size, if it is defined
                if 'size' in shape_attributes:
                    width, height = tuple(shape_attributes['size'])
                else:
                    width, height = (150, 100)
                shape.SetWidth(width)
                shape.SetHeight(height)

            # Pen
            if 'pen' in shape_attributes:
                pen = shape_attributes['pen']
                if isinstance(pen, str):
                    # The pen is set to a string value
                    pen = eval(pen, globals(), locals())
                shape.SetPen(pen)

            # Brush
            if 'brush' in shape_attributes:
                brush = shape_attributes['brush']
                if isinstance(brush, str):
                    # The brush is set to a string value
                    brush = eval(brush, globals(), locals())
                shape.SetBrush(brush)

            is_divided_shape = isinstance(shape, wx.lib.ogl.DividedShape)
            # Title
            if 'title' in shape_attributes:
                title = shape_attributes['title']
                if title:
                    if is_divided_shape:
                        region_title = wx.lib.ogl.ShapeRegion()
                        region_title.SetName('title')
                        region_title.SetText(title)
                        region_title.SetProportions(0.0, 0.3)   # Leave a third under the heading
                        region_title.SetFormatMode(wx.lib.ogl.FORMAT_CENTRE_HORIZ)
                        region_title.SetFont(shape.titleFont)
                        shape.AddRegion(region_title)
                    else:
                        for line_txt in title.split('\n'):
                            shape.AddText(line_txt)
            # Text
            if 'text' in shape_attributes:
                text = shape_attributes['text']
                if text:
                    if is_divided_shape:
                        region_text = wx.lib.ogl.ShapeRegion()
                        region_text.SetName('text')
                        region_text.SetText(text)
                        if shape_attributes.get('text2', None):
                            region_text.SetProportions(0.0, 0.4)    # Leave the rest under the text
                        else:
                            region_text.SetProportions(0.0, 0.7)
                        region_text.SetFormatMode(wx.lib.ogl.FORMAT_NONE)
                        region_text.SetFont(shape.textFont)
                        shape.AddRegion(region_text)
                    else:
                        for line_txt in text.split('\n'):
                            shape.AddText(line_txt)
            # Description
            if 'text2' in shape_attributes:
                text2 = shape_attributes['text2']
                if text2:
                    if is_divided_shape:
                        region_descr = wx.lib.ogl.ShapeRegion()
                        region_descr.SetName('text2')
                        region_descr.SetText(text2)
                        region_descr.SetProportions(0.0, 0.3)
                        region_descr.SetFormatMode(wx.lib.ogl.FORMAT_NONE)
                        font = region_descr.GetFont()
                        region_descr.SetFont(shape.text2Font)
                        shape.AddRegion(region_descr)

            if is_divided_shape:
                shape.SetRegionSizes()
                shape.reformatRegions(self)

        return shape

    def addShape(self, **shape_attributes):
        """
        Add new shape into canvas.
        """
        shape = self.createShape(**shape_attributes)
        if shape:
            # Set shape properties
            self.setShapeProperties(shape, **shape_attributes)

            # Add shape into diagram
            self.diagram.AddShape(shape)
            shape.Show(True)

            event_handler = divided_shape.iqShapeEvtHandler()
            event_handler.SetShape(shape)
            event_handler.SetPreviousHandler(shape.GetEventHandler())
            shape.SetEventHandler(event_handler)

            # Register a shape in the chart shape list
            shape_name = None
            if 'name' in shape_attributes:
                shape_name = str(shape_attributes['name'])
            self.shapes[shape_name] = shape
        return shape

    def createLine(self, **line_attributes):
        """
        Create new line.
        """
        line = wx.lib.ogl.LineShape()
        return line

    def findShape(self, shape_name):
        """
        Find the shape object by its unique name.
        """
        return self.shapes.get(shape_name, None)

    def setLineProperties(self, line, **line_attributes):
        """
        Set line properties.
        """
        if line:
            # First, identify the shapes that the line connects
            # If there are no shapes, then there is no need for a line.
            from_shape = None
            if 'from' in line_attributes:
                from_shape_name = line_attributes['from']
                from_shape = self.findShape(from_shape_name)

            to_shape = None
            if 'to' in line_attributes:
                to_shape_name = line_attributes['to']
                to_shape = self.findShape(to_shape_name)

            if from_shape and to_shape:
                line.SetCanvas(self)

                # Pen
                if 'pen' in line_attributes:
                    pen = line_attributes['pen']
                    if isinstance(pen, str):
                        # Pen as string
                        pen = eval(pen, globals(), locals())
                    line.SetPen(pen)

                # Brush
                if 'brush' in line_attributes:
                    brush = line_attributes['brush']
                    if isinstance(brush, str):
                        # Brush as string
                        brush = eval(brush, globals(), locals())
                    line.SetBrush(brush)

                # Arrow
                if 'arrow' in line_attributes:
                    arrow = line_attributes['arrow']
                    if isinstance(arrow, str):
                        # Arrow as string
                        arrow = eval(arrow, globals(), locals())
                    line.AddArrow(arrow)

                line.MakeLineControlPoints(2)
                from_shape.AddLine(line, to_shape)
        return line

    def addLine(self, **line_attributes):
        """
        Add new line.
        """
        line = self.createLine(**line_attributes)
        if line:
            # Set line properties
            self.setLineProperties(line, **line_attributes)

            # Add line intodiagram
            self.diagram.AddShape(line)
            line.Show(True)

            # Register
            line_name = None
            if 'name' in line_attributes:
                line_name = str(line_attributes['name'])
            self.lines[line_name] = line
        return line

    def setDiagram(self, diagram):
        """
        Set diagram.

        :param diagram: Diagram data.
        """
        # Clear diagram
        self.diagram.DeleteAllShapes()
        self.shapes = dict()
        self.lines = dict()

        # Diagram data
        self.diagram_res = diagram

        if self.diagram_res:
            return self.addDiagram(self.diagram_res)
        return None

    def _genLineName(self, line):
        """
        Generate line name.

        :param line: Line data.
        """
        if 'name' in line:
            return line['name']
        elif ('name' not in line) and \
             ('from' in line and 'to' in line):
            return line['from'] + '->' + line['to']

        return id_func.genGUID()

    def addDiagram(self, diagram, recreate=False):
        """
        Add diagram.

        :param diagram: Diagram data.
        :param recreate: Should I recreate the elements if they already exist?
        """
        shapes = list()
        if 'shapes' in diagram:
            shapes = diagram['shapes']

        lines = list()
        if 'lines' in diagram:
            lines = diagram['lines']

        # Add shapes
        for shape in shapes:
            if shape['name'] not in self.shapes or recreate:
                self.addShape(**shape)

        # Add lines
        for line in lines:
            if 'name' not in line:
                line['name'] = self._genLineName(line)
            if line['name'] not in self.lines or recreate:
                self.addLine(**line)

    def _asString(self, obj, obj_list, obj_str_list):
        """
        Object as string.
        """
        if obj in obj_list:
            i = obj_list.index(obj)
            return obj_str_list[i]
        # If you still can't convert the object, then return it.
        return obj

    def _getLineRes(self, line):
        """
        Get line resource data.

        :param line: Line object.
        :return: Resource format
            {
                'type': Line type,
                'from': From shape name,
                'to': To shape name,
                'pen': Pen,
                'brush': Brush,
                'arrow': Arrow,
            }
        """
        type = line.GetClassName()
        pen = self._asString(line.GetPen(), PEN_LIST, PEN_STR_LIST)
        brush = self._asString(line.GetBrush(), BRUSH_LIST, BRUSH_STR_LIST)
        arrow = self._asString(line.GetArrows()[0]._GetType(), ARROW_LIST, ARROW_STR_LIST)
        from_shape = line.GetFrom()
        to_shape = line.GetTo()
        line_res = {'type': type,
                    'from': from_shape.id,
                    'to': to_shape.id,
                    'pen': pen,
                    'brush': brush,
                    'arrow': arrow}
        return line_res

    def _getDividedShapeRes(self, shape):
        """
        Get shape resource data.

        :param shape: Shape object.
        :return: Resource format
            {
                'type': Shape type,
                'name': Shape name,
                'pos': Shape position (x, y),
                'size': Shape size (width, height),
                'pen': Pen,
                'brush': Brush,
                'title': Title,
                'text': Text,
            }
        """
        type = shape.GetClassName()
        name = shape.name
        x = shape.GetX()
        y = shape.GetY()
        width = shape.GetWidth()
        height = shape.GetHeight()
        pen = self._asString(shape.GetPen(), PEN_LIST, PEN_STR_LIST)
        brush = self._asString(shape.GetBrush(), BRUSH_LIST, BRUSH_STR_LIST)

        title_id = shape.FindRegion('title')[1]
        title = ''
        if title_id >= 0:
            region = shape._regions[title_id]
            title = region.GetText()

        text_id = shape.FindRegion('text')[1]
        text = ''
        if text_id >= 0:
            region = shape._regions[text_id]
            text = region.GetText()

        shape_res = {'type': type,
                     'name': name,
                     'pos': (x, y),
                     'size': (width, height),
                     'pen': pen,
                     'brush': brush,
                     'title': title,
                     'text': text}
        return shape_res

    def getDiagram(self):
        """
        Get diagram resource data

        :return: Resource format
            {'shapes': [shape data list],
             'lines': [line data list]}
        """
        diagram_res = {'shapes': [], 'lines': []}
        diagram = self.GetDiagram()

        shapes = diagram.GetShapeList()
        for shape in shapes:
            if issubclass(shape.__class__, wx.lib.ogl.LineShape):
                # Lines
                shape_res = self._getLineRes(shape)
                diagram_res['lines'].append(shape_res)
            elif issubclass(shape.__class__, divided_shape.iqDividedShape):
                # Shapes
                shape_res = self._getDividedShapeRes(shape)
                diagram_res['shapes'].append(shape_res)

        return diagram_res

    def getSelectedShape(self):
        """
        Get current selected shape.
        """
        return self.selected_shape

    def isDraggable(self):
        """
        Can drag and drop shapes?
        """
        return False

    def onShapeDblClick(self, event):
        """
        Handler for double-clicking on a shape.
        """
        pass
