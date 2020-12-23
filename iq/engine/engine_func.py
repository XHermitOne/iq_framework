#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Engine functions module.
"""

from ..util import log_func
from ..util import global_func


__version__ = (0, 0, 0, 1)


def closeForceApp():
    """
    Force closing an application.

    :return: True/False.
    """
    log_func.info(u'Force closing an application.')

    if global_func.isWXEngine():
        from .wx import wxapp_func
        return wxapp_func.closeForceWxApplication()
    else:
        log_func.warning(u'Unsupported engine for force closing application')
    return False
