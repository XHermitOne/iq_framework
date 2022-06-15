#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image file functions module.
"""

import os.path

from . import log_func


__version__ = (0, 0, 1, 2)


ICON_FILENAME_EXT = '.png'

ICON_NAME_SEPARATOR = '/'


def getIconPath():
    """
    Get icon image directory path.
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons')


def getIconFilename(icon_filename):
    """
    Get library icon file name.

    :param icon_filename: Icon filename as 'library/img_filename.png'
    :return: Full library icon file name or None if error.
    """
    library = None

    if icon_filename is None:
        icon_filename = 'fatcow/picture_error'
    elif not isinstance(icon_filename, str):
        log_func.warning(u'Error type icon filename <%s>' % icon_filename)
        return None

    icon_filename = icon_filename.replace(ICON_NAME_SEPARATOR, os.path.sep)

    if os.path.sep in icon_filename:
        if icon_filename.count(os.path.sep) == 1:
            library, icon_filename = icon_filename.split(os.path.sep)
        else:
            log_func.warning(u'Error format icon filename <%s>' % icon_filename)
            return None
    icon_filename = getLibraryIconFilename(icon_filename=icon_filename, library=library)
    return icon_filename


def getLibraryIconFilename(icon_filename, library=None):
    """
    Get library icon file name.

    :param icon_filename: Icon filename as 'img_filename.png'
    :param library: Icon library name.
    :return: Full library icon file name or None if error.
    """
    if not icon_filename.endswith(ICON_FILENAME_EXT):
        icon_filename += ICON_FILENAME_EXT

    icon_path = getIconPath()
    return os.path.join(icon_path, library, icon_filename) if library else os.path.join(icon_path, icon_filename)