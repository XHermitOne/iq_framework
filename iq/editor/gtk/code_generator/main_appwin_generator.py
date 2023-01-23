#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python main ApplicationWindow generate functions.
"""

import os
import os.path

from ....util import log_func
from ....util import str_func
from ....util import py_func
from ....util import txtfile_func
from ....util import file_func

__version__ = (0, 0, 0, 1)


DEFAULT_SRC_GLADE_APPWIN_FILENAME = 'main_application_window.glade'


def genDefaultMainAppWindowGlade(prj_filename=None, rewrite=False):
    """
    Generate default main ApplicationWindow form Glade project file.

    :param prj_filename: Glade project filename.
    :param rewrite: Rewrite it if exists?
    :return: True/False.
    """
    if not prj_filename:
        log_func.warning(u'Not define Glade project filename')
        return False

    package_dirname = os.path.dirname(prj_filename)
    py_func.createInitModule(package_path=package_dirname, rewrite=rewrite)

    src_filename = os.path.join(os.path.dirname(__file__), DEFAULT_SRC_GLADE_APPWIN_FILENAME)

    save_ok = file_func.copyFile(src_filename=src_filename, dst_filename=prj_filename)

    return save_ok
