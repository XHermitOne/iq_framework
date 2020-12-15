#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image functions module.
"""

from ..util import global_func
from ..util import log_func


__version__ = (0, 0, 0, 1)


def createImage(img_filename, *args, **kwargs):
    """
    Create image object from image filename.

    :param img_filename: Image filename.
    :return: Image object or None if error.
    """
    if global_func.isWXEngine():
        from .wx import wxbitmap_func
        return wxbitmap_func.createBitmap(img_filename, *args, **kwargs)
    else:
        log_func.warning(u'Unsupported image objects')
    return None


def createIconImage(icon_filename=None, *args, **kwargs):
    """
    Create image object from library icon image filename.

    :param icon_filename: Icon filename as 'library/img_filename.png'
        If None then create missing image bitmap.
    :return: Image object or None if error.
    """
    if global_func.isWXEngine():
        from .wx import wxbitmap_func
        return wxbitmap_func.createIconBitmap(icon_filename, *args, **kwargs)
    else:
        log_func.warning(u'Unsupported image objects')
    return None

