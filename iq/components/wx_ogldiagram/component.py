#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx OGL diagram component.
"""

import wx

from ..wx_widget import component
from . import spc

from . import ogl_diagram

from ...util import log_func
from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqWxOglDiagram(ogl_diagram.iqOGLDiagramViewerProto,
                     component.iqWxWidget):
    """
    Wx OGL diagram component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        component.iqWxWidget.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        ogl_diagram.iqOGLDiagramViewerProto.__init__(self, parent=parent, id=wx.NewId())

        foreground_colour = self.getForegroundColour()
        if foreground_colour is not None:
            self.SetForegroundColour(wx.Colour(foreground_colour[0], foreground_colour[1], foreground_colour[2]))

        background_colour = self.getBackgroundColour()
        if background_colour is not None:
            self.SetBackgroundColour(wx.Colour(background_colour[0], background_colour[1], background_colour[2]))

    def isDraggable(self):
        """
        Can drag and drop shapes?
        """
        return self.getAttribute('is_draggable')

    def onShapeDblClick(self, event):
        """
        Handler for double-clicking on a shape.
        """
        context = self.getContext()
        context['self'] = self
        context['event'] = event
        context['SHAPE'] = self.getSelectedShape()

        function_body = self.getAttribute('on_shape_dbl_click')
        if function_body:
            exec_func.execTxtFunction(function=function_body,
                                      context=context)
        if event is not None:
            event.Skip()


COMPONENT = iqWxOglDiagram

