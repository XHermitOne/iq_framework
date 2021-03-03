#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderPanel component.
"""

import os.path
import wx

from . import spc
from . import svgrenderpanel

from .. import wx_panel

from ...util import file_func
from ...util import log_func

__version__ = (0, 0, 0, 1)

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 100


class iqWxSVGRenderPanel(svgrenderpanel.iqSVGRenderPanel, wx_panel.COMPONENT):
    """
    Wx SVGRenderPanel component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        svgrenderpanel.iqSVGRenderPanel.__init__(self, parent=parent,
                                                 svg_filename=self.getSVGFilename())

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def getSVGFilename(self):
        """
        Get SVG filename.
        """
        svg_filename = self.getAttribute('svg_background')
        if not svg_filename:
            log_func.warning(u'Not define SVG file as background in <%s>' % self.getName())
            return None

        if svg_filename.startswith(os.path.sep):
            return svg_filename
        return os.path.join(file_func.getFrameworkPath(), svg_filename)

    def isCenter(self):
        """
        Center background image?

        :return: True/False.
        """
        return self.getAttribute('center')

    def getImages(self):
        """
        Get SVG image list.

        :return: SVG image list.
        """
        svg_images = [child.getImage() for child in self.getChildren()]
        return svg_images

    def onPaint(self, event):
        """
        Paint handler.
        """
        dc = wx.PaintDC(self)
        dc.Clear()

        image_width = self._background_image.width if self._background_image else DEFAULT_WIDTH
        image_height = self._background_image.height if self._background_image else DEFAULT_HEIGHT
        dc_dim = min(self.Size.width, self.Size.height)
        img_dim = min(image_width, image_height)
        scale = dc_dim / img_dim
        width = int(image_width * scale)
        height = int(image_height * scale)

        # dc.SetBrush(wx.Brush('white'))
        # dc.DrawRectangle(0, 0, width, height)

        # Center
        if self.isCenter():
            panel_width, panel_height = self.GetSize()
            dc.SetLogicalOrigin(-((panel_width - width)/2), -((panel_height - height)/2))

        renderer = self.getRenderer()
        background_img = self.getBackgroundImage()
        if renderer and background_img:
            context = renderer.CreateContext(dc)
            background_img.RenderToGC(context, scale)

            images = self.getImages()
            for image in images:
                image_context = renderer.CreateContext(dc)
                # matrix = new_context.CreateMatrix()
                # matrix.Invert()
                # matrix.Translate(100, 100)
                # matrix.Rotate(math.pi * 2.0 * 60.0 / 360.0)
                # new_context.SetTransform(matrix)
                image.RenderToGC(image_context, scale)


COMPONENT = iqWxSVGRenderPanel
