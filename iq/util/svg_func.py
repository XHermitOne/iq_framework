#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SVG file functions..
"""

import os.path

from . import log_func
from . import sys_func
from . import exec_func

__version__ = (0, 0, 0, 1)

SVG_FILENAME_EXT = '.svg'

DEFAULT_SVG_VIEWER = 'eog'


def viewSVG(svg_filename):
    """
    View SVG file in viewer.

    :param svg_filename: SVG filename.
    :return: True/False.
    """
    if not os.path.exists(svg_filename):
        log_func.warning(u'SVG file <%s> not found' % svg_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            cmd = '%s %s &' % (DEFAULT_SVG_VIEWER, svg_filename)
            return exec_func.execSystemCommand(cmd)
        elif sys_func.isWindowsPlatform():
            log_func.warning(u'Not support view SVG file <%s> on Windows platform' % svg_filename)
    except:
        log_func.fatal(u'Error view SVG file <%s>' % svg_filename)
    return False

