#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wx SVGRenderImage component.
"""

import os.path
import wx

from ... import object

from . import spc
from . import svgrenderimage

from .. import wx_panel

from ...util import log_func
from ...util import file_func

__version__ = (0, 0, 0, 1)


class iqWxSVGRenderImage(svgrenderimage.iqSVGRenderImage, wx_panel.COMPONENT):
    """
    Wx SVGRenderImage component.
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

        svgrenderimage.iqSVGRenderImage.__init__(self, parent=parent,
                                                 svg_filename=self.getSVGFilename())

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onPanelSize)

    def onEraseBackground(self, event):
        """
        Adding a picture to the panel background through the device context.
        """
        self.drawDCBitmap(dc=event.GetDC(), bmp=self.getSVGBitmap())

    def onPanelSize(self, event):
        """
        Overriding the mnemoscheme panel resize handler.
        """
        self.drawSVG()
        # self.layoutAll(False)

        self.Refresh()
        event.Skip()

    def getSVGFilename(self):
        """
        Get SVG filename.
        """
        svg_filename = self.getAttribute('svg_filename')
        if not svg_filename:
            log_func.warning(u'Not define SVG file in <%s>' % self.getName())
            return None

        if svg_filename.startswith(os.path.sep):
            return svg_filename
        return os.path.join(file_func.getFrameworkPath(), svg_filename)

    def design(self):
        """
        Design component.

        :return: True/False.
        """
        return self.editSVG(svg_filename=self.getSVGFilename())


COMPONENT = iqWxSVGRenderImage
