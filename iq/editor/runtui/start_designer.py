#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI. Start RAD designer.
"""

from iq.util import log_func
from iq.util import lang_func

from . import form_json_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


def startRunTUIRadDesigner(json_filename=None):
    """
    Start RUNTUI RAD designer.

    :param json_filename: JSON form filename.
    :return: True/False.
    """
    return form_json_manager.runRunTUIRadDesigner(filename=json_filename)