#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wxBitmap functions module.
"""

import os.path
import wx

from ...util import log_func
from ...util import icon_func

__version__ = (0, 1, 2, 1)

DEFAULT_ICON_WIDTH = 16
DEFAULT_ICON_HEIGHT = 16


def createBitmap(img_filename, mask_colour=None):
    """
    Create wx.Bitmap from image filename.

    :param img_filename: Image filename.
    :param mask_colour: Colour for create image mask. If None then mask not create.
    :return: wx.Bitmap object or None if error.
    """
    try:
        img_filename = os.path.abspath(img_filename)
        if (not img_filename) or (not os.path.exists(img_filename)):
            log_func.warning(u'Image file <%s> not found' % img_filename)
            return None

        bmp = wx.Bitmap(img_filename, getImageFileType(img_filename))
        if mask_colour is not None:
            mask = wx.Mask(bmp, mask_colour)
            bmp.SetMask(mask)
        return bmp
    except:
        log_func.fatal(u'Error create wx.Bitmap object from <%s>' % img_filename)
    return None


def getImageFileType(img_filename):
    """
    Get img file type as (.jpg, .png and etc.)
    """
    if not img_filename:
        log_func.warning(u'Not define image filename')
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
        log_func.fatal(u'Error get image file type')

    return None


def createIconBitmap(icon_filename=None, mask_colour=None):
    """
    Create wx.Bitmap from library icon image filename.

    :param icon_filename: Icon filename as 'library/img_filename.png'
        If None then create missing image bitmap.
    :param mask_colour: Colour for create image mask. If None then mask not create.
    :return: wx.Bitmap object or None if error.
    """
    if icon_filename is None:
        return wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU)
    img_filename = icon_func.getIconFilename(icon_filename=icon_filename)
    if img_filename:
        # log_func.debug(u'Create bitmap <%s>' % img_filename)
        return createBitmap(img_filename, mask_colour=mask_colour)
    return None


def createEmptyBitmap(width, height, background_colour=None):
    """
    Create empyty wx.Bitmap object.

    :param width: Bitmap width.
    :param height: Bitmap height.
    :param background_colour: Background colour.
        Default use white.
    :return: Empty wx.Bitmap given size.
    """
    try:
        if background_colour is None:
            background_colour = wx.WHITE

        #
        bmp = wx.Bitmap(width, height)
        # Create device context object
        dc = wx.MemoryDC()
        # Select an object for context
        dc.SelectObject(bmp)
        # Change background
        dc.SetBackground(wx.Brush(background_colour))
        dc.Clear()
        # Free object
        dc.SelectObject(wx.NullBitmap)
        return bmp
    except:
        log_func.fatal(u'Error create empty wx.Bitmap. Size <%s x %s>' % (width, height))
    return None


def findBitmap(*img_filenames):
    """
    Search and create a Bitmap object by the list of image file names.

    :param img_filenames: The names of the files to be found.
    :return: Returns the created Bitmap object or
        None if none of the suggested files exists.
    """
    for img_filename in img_filenames:
        if os.path.exists(img_filename):
            return createBitmap(img_filename)
    return None


def createArtProviderBitmap(image_id=None, image_client_id=None, img_size=None):
    """
    Create bitmap object by wx art provider.

    :param image_id: Unique identifier of the bitmap.
    :param image_client_id:  ArtClient identifier of the client (i.e. who is asking for the bitmap).
    :param img_size: Size of the returned bitmap or DefaultSize if size doesn’t matter.
    """
    if image_id is None:
        image_id = wx.ART_MISSING_IMAGE
    if image_client_id is None:
        image_client_id = wx.ART_MENU
    if img_size is None:
        img_size = wx.DefaultSize
    try:
        if not isinstance(img_size, wx.Size):
            img_size = wx.Size(*img_size)
        return wx.ArtProvider.GetBitmap(image_id, client=image_client_id, size=img_size)
    except:
        log_func.fatal(u'Error create bitmap object by wx art provider')
    return wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU)


def scaleBitmap(bitmap, width, height):
    """
    Scale bitmap.

    :param bitmap: wx.Bitmap object or image file name.
    :param width: New bitmap width.
    :param height: New bitmap height.
    :return: New scaled wx.Bitmap object.
    """
    if not isinstance(bitmap, wx.Bitmap):
        bitmap = createBitmap(bitmap)
    try:
        img = wx.ImageFromBitmap(bitmap)
        img = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        new_bmp = wx.BitmapFromImage(img)
        return new_bmp
    except:
        log_func.fatal(u'Error scale bitmap')
    return bitmap
