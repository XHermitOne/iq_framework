#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wxBitmap functions module.
"""

import os.path
import wx

from ...util import file_func
from ...util import log_func
from ...util import icon_func

__version__ = (0, 0, 0, 1)


def createBitmap(img_filename, mask_colour=None):
    """
    Create wx.Bitmap from image filename.

    :param img_filename: Image filename.
    :param mask_colour: Colour for create image mask. If None then mask not create.
    :return: wx.Bitmap object or None if error.
    """
    try:
        img_filename = file_func.getAbsolutePath(img_filename)
        if (not img_filename) or (not os.path.exists(img_filename)):
            log_func.warning(u'Image file <%s> not found' % img_filename)
            return None

        bmp = wx.Bitmap(img_filename, getImageFileType(img_filename))
        if mask_colour is not None:
            bmp.SetMask(wx.Colour(bmp, mask_colour))
        return bmp
    except:
        log_func.fatal(u'Create wx.Bitmap object from <%s> error' % img_filename)
    return None


def getImageFileType(img_filename):
    """
    Get img file type as (.jpg, .png and etc.)
    """
    if not img_filename:
        log_func.error(u'Not define image filename')
        return None

    try:
        name, ext = os.path.splitext(img_filename)
        ext = ext[1:].upper()
        if ext == 'BMP':
            return wx.BITMAP_TYPE_BMP
        elif ext == 'GIF':
            return wx.BITMAP_TYPE_GIF
        elif ext == 'JPG' or ext == 'JPEG':
            return wx.BITMAP_TYPE_JPEG
        elif ext == 'PCX':
            return wx.BITMAP_TYPE_PCX
        elif ext == 'PNG':
            return wx.BITMAP_TYPE_PNG
        elif ext == 'PNM':
            return wx.BITMAP_TYPE_PNM
        elif ext == 'TIF' or ext == 'TIFF':
            return wx.BITMAP_TYPE_TIF
        elif ext == 'XBM':
            return wx.BITMAP_TYPE_XBM
        elif ext == 'XPM':
            return wx.BITMAP_TYPE_XPM
        elif ext == 'ICO':
            return wx.BITMAP_TYPE_ICO
        return None
    except:
        log_func.fatal(u'Get image file type error')

    return None


def createIconBitmap(icon_filename, mask_colour=None):
    """
    Create wx.Bitmap from library icon image filename.

    :param icon_filename: Icon filename as 'library/img_filename.png'
    :param mask_colour: Colour for create image mask. If None then mask not create.
    :return: wx.Bitmap object or None if error.
    """
    img_filename =  icon_func.getIconFilename(icon_filename=icon_filename)
    if img_filename:
        return createBitmap(img_filename, mask_colour=mask_colour)
    return None