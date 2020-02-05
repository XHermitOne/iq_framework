#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project functions.
"""

import os
import os.path

from ..util import file_func

__version__ = (0, 0, 0, 1)


def getProjectNames():
    """
    Get all project names in framework.

    :return: Project names list.
    """
    framework_path = file_func.getFrameworkPath()

    prj_names = [dirname for dirname in os.listdir(framework_path) if not dirname.startswith(file_func.HIDDEN_DIRNAME_SIGN) and dirname != 'iq']
    return prj_names
