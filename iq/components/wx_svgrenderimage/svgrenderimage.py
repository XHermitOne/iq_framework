#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderImage prototype class.
"""

import os.path
import six
import wx.svg
from . import svg_file

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)


class iqSVGRenderImage(svg_file.iqSVGFile):
    """
    Wx SVGRenderImage prototype class.
    """
    def __init__(self, parent, svg_filename=None):
        """
        Constructor.
        """
        self.parent = parent
        svg_file.iqSVGFile.__init__(self)

        self._image = None

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
            self.loadSVG(dst_svg_filename)
            self._image = wx.svg.SVGimage.CreateFromFile(dst_svg_filename)
            return True
        except:
            log_func.fatal(u'Error set SVG File <%s>' % svg_filename)
        return False

    def getImage(self):
        """
        Get SVG image object.

        :return: SVG image object.
        """
        return self._image

    def getRenderer(self):
        """
        Get renderer object.

        :return: Get renderer object.
        """
        return self.parent.getRenderer() if self.parent else None
