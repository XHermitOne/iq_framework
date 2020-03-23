#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme component.
"""

import os.path
import wx

from . import spc
from . import mnemoscheme

from .. import mnemo_anchor

from .. import wx_panel

from ...util import file_func
from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqMnemoScheme(mnemoscheme.iqMnemoSchemeManager, wx_panel.COMPONENT):
    """
    Mnemoscheme component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        wx_panel.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        mnemoscheme.iqMnemoSchemeManager.__init__(self, *args, **kwargs)

        self.setSVGBackground(self.getSVGFilename(), auto_draw=True)
        self.setSVGSize(self.getSVGWidth(), self.getSVGHeight())

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.Bind(wx.EVT_SIZE, self.onPanelSize)

    def onEraseBackground(self, event):
        """
        Adding a picture to the panel background through the device context.
        """
        self.drawDCBitmap(dc=event.GetDC(), bmp=self.getBackgroundBitmap())

    def onPanelSize(self, event):
        """
        Overriding the mnemoscheme panel resize handler.
        """
        self.drawBackground()
        self.layoutAll(False)

        self.Refresh()
        event.Skip()

    def getAnchors(self):
        """
        List of mnemonic anchors.
        """
        children = self.getChildren()
        return [child for child in children if isinstance(child, mnemo_anchor.COMPONENT)]

    def getControls(self):
        """
        List of active mnemonic controls.
        """
        children = self.getChildren()
        return [child for child in children if not isinstance(child, mnemo_anchor.COMPONENT)]

    def layoutAll(self, auto_refresh=True):
        """
        The method of arranging and dimensioning controls mnemonic diagrams according to the anchors.

        :param auto_refresh: Automatically refresh the mnemoscheme object.
        :return: True/False.
        """
        anchors = self.getAnchors()
        result = all([anchor.layoutControl() for anchor in anchors])

        if auto_refresh:
            self.Refresh()

        return result

    def getSVGFilename(self):
        """
        Get SVG filename.
        """
        svg_filename = self.getAttribute('svg_background')
        if not svg_filename:
            log_func.error(u'Not define SVG file as background in <%s>' % self.getName())
            return None

        if svg_filename.startswith(os.path.sep):
            return svg_filename
        return os.path.join(file_func.getFrameworkPath(), svg_filename)

    def getSVGWidth(self):
        """
        Get SVG width in original units.
        """
        return self.getAttribute('svg_width')

    def getSVGHeight(self):
        """
        Get SVG height in original units.
        """
        return self.getAttribute('svg_height')


COMPONENT = iqMnemoScheme
