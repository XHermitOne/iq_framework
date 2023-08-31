#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image function.
"""

import os.path

from . import log_func
from . import sys_func
from . import exec_func

__version__ = (0, 0, 1, 1)

IMG_FILENAME_EXT = ('.png', '.jpg', '.jpeg', '.gif')

OPEN_IMAGE_LINUX_EXEC_FMT = 'eog %s &'
OPEN_IMAGE_WINDOWS_EXEC_FMT = 'rundll32 \"%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll\", ImageView_Fullscreen \"%s\"'


def viewImage(img_filename):
    """
    View image file.

    :param img_filename: Image filename path.
    :return: True/False.
    """
    if not os.path.exists(img_filename):
        log_func.warning(u'Image file <%s> not found' % img_filename)
        return False

    filename_ext = os.path.splitext(img_filename)[1]
    if filename_ext:
        filename_ext = filename_ext.lower()
        if filename_ext in IMG_FILENAME_EXT:
            if sys_func.isLinuxPlatform():
                cmd = OPEN_IMAGE_LINUX_EXEC_FMT % img_filename
                return exec_func.execSystemCommand(cmd)
            elif sys_func.isWindowsPlatform():
                cmd = OPEN_IMAGE_WINDOWS_EXEC_FMT % img_filename
                return exec_func.execSystemCommand(cmd)
            else:
                log_func.warning(u'Unsupported platform for view image <%s>' % img_filename)
        else:
            log_func.warning(u'Not supported file type <%s>' % filename_ext)
    else:
        log_func.warning(u'Not defined ext of filename <%s>' % img_filename)
    return False
