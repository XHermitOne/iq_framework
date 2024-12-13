#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image function.
"""

import os.path

from . import log_func
from . import sys_func
from . import exec_func

import PIL.Image

__version__ = (0, 2, 1, 1)

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


def compressImage(img_filename, new_filename, new_size_ratio=1.0, quality=90, width=None, height=None):
    """
    Compress image.

    :param img_filename: Image file name.
    :param new_filename: Destination image file name.
    :param new_size_ratio: Size ratio.
    :param quality: Quality.
    :param width: New width.
    :param height: New height.
    :return: True/False.
    """
    try:
        # Load the image to memory
        img = PIL.Image.open(img_filename)
        # Get the original image size in bytes
        image_size = os.path.getsize(img_filename)
        if new_size_ratio < 1.0:
            # If resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
            img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), PIL.Image.LANCZOS)
        elif width and height:
            # If width and height are set, resize with them instead
            img = img.resize((width, height), PIL.Image.LANCZOS)

        if os.path.exists(new_filename):
            os.remove(new_filename)
        # Make new filename appending _compressed to the original file name
        try:
            # Save the image with the corresponding quality and optimize set to True
            img.save(new_filename, quality=quality, optimize=True)
        except OSError:
            # Convert the image to RGB mode first
            img = img.convert('RGB')
            # Save the image with the corresponding quality and optimize set to True
            img.save(new_filename, quality=quality, optimize=True)

        # Get the new image size in bytes
        new_image_size = os.path.getsize(new_filename)
        # Calculate the saving bytes
        saving_diff_percent = (new_image_size - image_size) / image_size * 100
        # Print the new size in a good format
        log_func.info('Compress image file <%s : %d> -> <%s : %d>. Compressed: %d%%' % (img_filename, image_size, new_filename, new_image_size, saving_diff_percent))
        return os.path.exists(new_filename)
    except:
        log_func.fatal(u'Error compress image file <%s> -> <%s>' % (img_filename, new_filename))
    return False
