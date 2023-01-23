#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderPanel prototype class.
"""

import os.path
import six
import wx.svg
from ..wx_svgrenderimage import svg_file

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)


class iqSVGRenderPanel(svg_file.iqSVGFile):
    """
    Wx SVGRenderPanel prototype class.
    """
    def __init__(self, parent, svg_filename=None):
        """
        Constructor.
        """
        self.parent = parent
        svg_file.iqSVGFile.__init__(self)

        self._background_image = None

        if 'wxMSW' in wx.PlatformInfo:
            self._renderer = wx.GraphicsRenderer.GetDirect2DRenderer()
            # self._renderer = wx.GraphicsRenderer.GetCairoRenderer()
        else:
            self._renderer = wx.GraphicsRenderer.GetDefaultRenderer()

        if svg_filename:
            self.setSVGFile(svg_filename=svg_filename)

    def setSVGFile(self, svg_filename):
        """
        Set SVG file.

        :param svg_filename: Source SVG filename.
        :return: True/False.
        """
        try:
            dst_svg_filename = os.path.join(file_func.getProjectProfilePath(),
                                            '%s.svg' % self.getGUID())
            if svg_filename and os.path.exists(svg_filename):
                file_func.copyFile(svg_filename, dst_svg_filename, True)

            self.loadSVG(dst_svg_filename)
            self._background_image = wx.svg.SVGimage.CreateFromFile(dst_svg_filename)
            return True
        except:
            log_func.fatal(u'Error set SVG File <%s>' % svg_filename)
        return False

    def getBackgroundImage(self):
        """
        Get SVG background image object.

        :return: SVG image object.
        """
        return self._background_image

    def getRenderer(self):
        """
        Get renderer object.

        :return: Get renderer object.
        """
        return self._renderer

    def getImages(self):
        """
        Get SVG image list.

        :return: SVG image list.
        """
        log_func.warning(u'Not define method getImages in class <%s>' % self.__class__.__name__)
        return list()
