#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get marker icons functions.

Used free icons from https://mapicons.mapsmarker.com
"""

import os.path

from ...util import log_func

__version__ = (0, 0, 0, 1)

ICON_FILENAME_EXT = '.png'

# Default marker color sequence
DEFAULT_COLOR_NAMES_SEQUENCE = ('blue', 'green', 'yellow', 'red', 'cyan', 'magenta', 'gray')


def getMarkerIconFilename(icon_name):
    """
    Get the full filename of the marker icon.

    :param icon_name: Icon name.
        May be given as a name (for example marker) or base filename (for example marker.png).
    :return: Full icon filename or None if error.
    """
    if not isinstance(icon_name, str):
        log_func.warning(u'Incorrect icon name type <%s>' % icon_name.__class__.__name__)
        return None

    if not icon_name.endswith(ICON_FILENAME_EXT):
        icon_name += ICON_FILENAME_EXT

    filename = os.path.join(os.path.dirname(__file__), 'img', icon_name)
    return filename

