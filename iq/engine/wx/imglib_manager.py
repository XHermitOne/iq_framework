#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image library manager class module.
"""

import wx
from ...util import log_func

from . import wxbitmap_func

__version__ = (0, 0, 0, 1)


class iqImageLibraryManager(object):
    """
    Image library manager class.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._imagelist = None
        self._img_idx = dict()

    def initImageLibrary(self):
        """
        Initialization component icon image list object.

        :return: Image list.
        """
        self._imagelist = wx.ImageList(wxbitmap_func.DEFAULT_ICON_WIDTH,
                                       wxbitmap_func.DEFAULT_ICON_HEIGHT)

        empty_bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU)
        empty_icon_idx = self._imagelist.Add(empty_bmp)
        self._img_idx[None] = empty_icon_idx

        return self._imagelist

    def getImageList(self):
        """
        Get image list object.

        :return:
        """
        return self._imagelist

    def addImage(self, img_name=None):
        """
        Add image to library.

        :param img_name: Image as icon name.
        :return: wx.Bitmap object or None if error.
        """
        if not isinstance(img_name, str):
            log_func.error(u'Not supported image name type <%s>' % type(img_name))
            return None

        bmp = wxbitmap_func.createIconBitmap(icon_filename=img_name)
        if bmp:
            return self.addBitmap(img_name, bmp)
        return None

    def addBitmap(self, img_name, bmp):
        """
        Add image to library.

        :param img_name: Image as icon name.
        :param bmp: wx.Bitmap object.
        :return: wx.Bitmap object or None if error.
        """
        img_idx = self._imagelist.Add(bmp)
        self._img_idx[img_name] = img_idx
        return bmp

    def getImageIdx(self, img_name):
        """
        Get image index in imagelist.

        :param img_name: Image as icon name.
        :return: Image index or None if error.
        """
        if img_name not in self._img_idx:
            self.addImage(img_name)

        if img_name in self._img_idx:
            return self._img_idx[img_name]
        return None

    def getImageBmp(self, img_name):
        """
        Get image bitmap in imagelist.

        :param img_name: Image as icon name.
        :return: Image bitmap or None if error.
        """
        if img_name not in self._img_idx:
            bmp = self.addImage(img_name)
            return bmp

        if img_name in self._img_idx:
            img_idx = self._img_idx[img_name]
            return self._imagelist.GetBitmap(img_idx)
        return None
