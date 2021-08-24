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
from ...util import sys_func

from ...engine.wx import wxbitmap_func

import iq

__version__ = (0, 0, 0, 1)

# Conversion start command format SVG -> PNG
UNIX_SVG2PNG_CONVERT_CMD_FMT = 'convert -background %s -resize %dx%d -extent %dx%d -gravity center %s %s'
WIN_SVG2PNG_CONVERT_CMD_FMT = '\"\"%s\\SVG2PNG\\convert.exe\" -background %s -resize %dx%d -extent %dx%d -gravity center %s %s\"'


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

        self._svg_bitmap = None
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
            # dst_svg_filename = os.path.join(file_func.getProjectProfilePath(),
            #                                 '%s.svg' % self.getGUID())
            # if svg_filename and os.path.exists(svg_filename):
            #     file_func.copyFile(svg_filename, dst_svg_filename, True)

            if os.path.exists(svg_filename):
                self.loadSVG(svg_filename)
                self._image = wx.svg.SVGimage.CreateFromFile(svg_filename)
                self._svg_filename = svg_filename
                return self.drawSVG(auto_rewrite=True)
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

    def drawSVG(self, auto_rewrite=True):
        """
        Draw the background of the mnemonic on the device context.
        ATTENTION! To extract an image from an SVG file
        The external SVG -> PNG conversion utility is used.
        And PNG is already displayed on the device context.

        :param auto_rewrite: Automatically overwrite the intermediate PNG file.
        :return: True/False.
        """
        if self._svg_filename is None:
            log_func.warning(u'Not define SVG file in <%s : %s>' % (self.getName(), self.__class__.__name__))
            return False

        try:
            # Mimic panel size
            width, height = self.GetSize()

            png_filename = os.path.join(file_func.getProjectProfilePath(),
                                        '%s_background_%dx%d.png' % (self.getName(), width, height))
            svg_filename = os.path.join(file_func.getProjectProfilePath(),
                                        os.path.basename(self._svg_filename))
            # Save SVG file to HOME folder
            # This is done so that you can replace the mnemonic diagram on
            # the fly
            if not os.path.exists(svg_filename) or not file_func.isSameFile(svg_filename, self._svg_filename):
                # If the file has changed, then overwrite it in the HOME folder
                file_func.copyFile(self._svg_filename, svg_filename)
                # and delete all PNG files
                file_func.delFilesByMask(file_func.getProjectProfilePath(),
                                         '%s_background_*.png' % self.getName())

            background_colour = self.getBackgroundColour()
            if not os.path.exists(png_filename) or auto_rewrite:
                # Define background colour
                if isinstance(background_colour, str):
                    bg_colour = background_colour.lower()
                elif isinstance(background_colour, (list, tuple)):
                    if sys_func.isWindowsPlatform():
                        bg_colour = '\"rgb(%s)\"' % str(background_colour[:3]).replace(' ', '').strip('()[]')
                    else:
                        bg_colour = '\'rgb(%s)\'' % str(background_colour[:3]).strip('()[]')
                else:
                    bg_colour = 'none'

                # Launch file conversion
                if sys_func.isLinuxPlatform():
                    cmd = UNIX_SVG2PNG_CONVERT_CMD_FMT % (bg_colour, width, height, width, height,
                                                          svg_filename, png_filename)
                elif sys_func.isWindowsPlatform():
                    win_svg2png_convert_cmd_fmt = iq.KERNEL.settings.THIS.SETTINGS.win_svg2png_convert_cmd_fmt.get()
                    if not win_svg2png_convert_cmd_fmt:
                        win_svg2png_convert_cmd_fmt = WIN_SVG2PNG_CONVERT_CMD_FMT
                    cmd = win_svg2png_convert_cmd_fmt % (os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                                                         bg_colour, width, height, width, height,
                                                         svg_filename, png_filename)
                else:
                    log_func.warning(u'Unsupported <%s> platform' % sys_func.getPlatform())
                    return False

                log_func.info(u'Start SVG -> PNG covert command: <%s> ' % cmd)
                os.system(cmd)
                if not os.path.exists(png_filename):
                    log_func.warning(u'Conversion error SVG -> PNG (<%s> -> <%s>)' % (svg_filename, png_filename))
                    return False

            self._svg_bitmap = wxbitmap_func.createBitmap(png_filename, background_colour)
            return True
        except:
            log_func.fatal(u'SVG Render image background rendering error')
        return False

    def getSVGBitmap(self):
        """
        A picture object to display the background.

        :return: The wx.Bitmap object corresponding to the current background of the mnemonic.
        """
        return self._svg_bitmap
