#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx OGL diagram divided shape class module.
"""

import wx
import wx.lib.ogl

__version__ = (0, 0, 0, 1)

DIVIDED_SHAPE_TYPE = 'iqDividedShape'


class iqDividedShape(wx.lib.ogl.DividedShape):
    """
    A DividedShape is a rectangle with a number of vertical divisions.
    Each division may have its text formatted with independent characteristics,
    and the size of each division relative to the whole image may be specified.
    """
    def __init__(self, name, width, height, canvas=None):
        """
        Конструктор.
        """
        wx.lib.ogl.DividedShape.__init__(self, width, height)

        self.name = name
        self.titleFont = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.textFont = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text2Font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.SetRegionSizes()
        self.reformatRegions(canvas)

    def reformatRegions(self, canvas=None):
        """
        Reformatting regions.
        """
        rnum = 0

        if canvas is None:
            canvas = self.GetCanvas()

        dc = wx.ClientDC(canvas)  # used for measuring

        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1

    def OnSizingEndDragLeft(self, point, x, y, keys=0, attachment=0):
        """
        """
        wx.lib.ogl.DividedShape.OnSizingEndDragLeft(self, point, x, y, keys, attachment)
        self.SetRegionSizes()
        self.reformatRegions()
        self.GetCanvas().Refresh()


class iqShapeEvtHandler(wx.lib.ogl.ShapeEvtHandler):
    """
    The ShapeEvtHandler class.
    """
    def __init__(self, *args, **kwargs):
        wx.lib.ogl.ShapeEvtHandler.__init__(self)

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        """
        Left click handler.
        """
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Refresh(False)
            canvas.selected_shape = None
        else:
            redraw = False
            shape_list = canvas.GetDiagram().GetShapeList()
            to_unselect = list()

            for cur_shape in shape_list:
                if cur_shape.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    to_unselect.append(cur_shape)

            shape.Select(True, dc)
            canvas.selected_shape = shape

            if to_unselect:
                for cur_shape in to_unselect:
                    cur_shape.Select(False, dc)

                canvas.Refresh(False)

    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        """
        Left double click handler.
        """
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        canvas.onShapeDblClick(None)
        return wx.lib.ogl.ShapeEvtHandler.OnLeftDoubleClick(self, x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        """
        End drag handler.
        """
        shape = self.GetShape()
        wx.lib.ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

    def OnSizingEndDragLeft(self, pt, x, y, keys=0, attachment=0):
        """
        Sizing end drag handler.
        """
        wx.lib.ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attachment)

    def OnMovePost(self, dc, x, y, old_x, old_y, display=True):
        """
        Move post handler.
        """
        # shape = self.GetShape()
        wx.lib.ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, old_x, old_y, display)

    def OnRightClick(self, x, y, keys=0, attachment=0):
        """
        Right click handler.
        """
        pass
