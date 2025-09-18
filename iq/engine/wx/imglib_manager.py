#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image library manager class module.
"""

import wx
from ...util import log_func

from . import wxbitmap_func

from . import base_manager

__version__ = (0, 1, 1, 1)


class iqImageLibManager(base_manager.iqBaseManager):
    """
    Image library manager class.
    """
    def initImageLib(self, img_width=None, img_height=None, assign_ctrl=None):
        """
        Initialization component icon image list object.

        :param img_width: Image width.
        :param img_height: Image height.
        :param assign_ctrl: Sets the image list associated with the control and takes ownership of it.
        :return: Image list.
        """
        self.__img_idx = dict()

        if img_width is None:
            img_width = wxbitmap_func.DEFAULT_ICON_WIDTH
        if img_height is None:
            img_height = wxbitmap_func.DEFAULT_ICON_HEIGHT

        self._imagelist = wx.ImageList(img_width, img_height)

        if img_width == wxbitmap_func.DEFAULT_ICON_WIDTH and img_height == wxbitmap_func.DEFAULT_ICON_HEIGHT:
            img_size = wx.DefaultSize
        else:
            img_size = wx.Size(img_width, img_height)

        empty_bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_MENU, size=img_size)
        # log_func.debug(u'Bitmap size %s' % str(empty_bmp.GetSize()))
        empty_icon_idx = self._imagelist.Add(empty_bmp)
        self.__img_idx[None] = empty_icon_idx

        if assign_ctrl:
            try:
                assign_ctrl.AssignImageList(self._imagelist, wx.IMAGE_LIST_NORMAL)
                log_func.info('Image library manager initialized')
            except:
                log_func.fatal(u'Error assign image list to <%s>' % str(assign_ctrl))
        else:
            log_func.warning(u'Not define assign control for image list')

        return self._imagelist

    def getImageLibImageList(self):
        """
        Get image list object.

        :return:
        """
        if not self.isInitImageLib():
            self.initImageLib()
        return self._imagelist

    def addImageLibImage(self, img_name=None):
        """
        Add image to library.

        :param img_name: Image as icon name.
        :return: wx.Bitmap object or None if error.
        """
        if not isinstance(img_name, str):
            log_func.warning(u'Not supported image name type <%s>' % type(img_name))
            return None

        bmp = wxbitmap_func.createIconBitmap(icon_filename=img_name)
        if bmp:
            return self.addImageLibBitmap(img_name, bmp)
        return None

    def addImageLibBitmap(self, img_name, bmp):
        """
        Add image to library.

        :param img_name: Image as icon name.
        :param bmp: wx.Bitmap object.
        :return: wx.Bitmap object or None if error.
        """
        if not self.isInitImageLib():
            self.initImageLib()

        # log_func.debug(u'Bitmap size %s' % str(bmp.GetSize()))
        img_idx = self._imagelist.Add(bmp)
        self.__img_idx[img_name] = img_idx
        return bmp

    def getImageLibImageIdx(self, img_name):
        """
        Get image index in imagelist.

        :param img_name: Image as icon name.
        :return: Image index or None if error.
        """
        if not self.isInitImageLib():
            self.initImageLib()

        if img_name not in self.__img_idx:
            self.addImageLibImage(img_name)

        if img_name in self.__img_idx:
            return self.__img_idx[img_name]
        return None

    def isInitImageLib(self):
        """
        Check if image library is initialized.

        :return: True/False.
        """
        return hasattr(self, '_imagelist')

    def getImageLibImageBmp(self, img_name):
        """
        Get image bitmap in imagelist.

        :param img_name: Image as icon name.
        :return: Image bitmap or None if error.
        """
        if not self.isInitImageLib():
            self.initImageLib()

        if img_name not in self.__img_idx:
            bmp = self.addImageLibImage(img_name)
            return bmp

        if img_name in self.__img_idx:
            img_idx = self.__img_idx[img_name]
            return self._imagelist.GetBitmap(img_idx)
        return None
