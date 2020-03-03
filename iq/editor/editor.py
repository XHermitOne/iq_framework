#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor functions.
"""

import os.path

from ..util import log_func
from ..util import global_func
from ..util import res_func
from ..util import py_func

from ..dialog import dlg_func
from ..editor.wx import wxfb_manager

__version__ = (0, 0, 0, 1)


def openEditor():
    """
    Open main editor form.

    :return: True/False.
    """
    if global_func.isWXEngine():
        from .wx import start_editor
        start_editor.startEditor()
        return True
    else:
        log_func.error(u'Not supported engine as editor')
    return False


def _openResourceEditor(res_filename):
    """
    Open resource editor form.

    :param res_filename: Resource filename.
        Resource file may be *.res or *.py file.
    :return: True/False.
    """
    if global_func.isWXEngine():
        if res_func.isResourceFile(res_filename):
            from .wx.res_editor import resource_editor
            resource_editor.runResourceEditor(res_filename=res_filename)
            return True

        elif py_func.isPythonFile(res_filename):
            from .wx import start_py
            return start_py.startPythonEditor(py_filename=res_filename)

        elif wxfb_manager.isWXFormBuilderProjectFile(res_filename):
            from .wx import start_wxfb
            return start_wxfb.startWXFormBuilderEditor(fbp_filename=res_filename)

        elif os.path.isdir(res_filename):
            from .wx import start_folder_dialog
            return start_folder_dialog.startFolderEditor(folder_path=res_filename)

        elif not os.path.exists(res_filename):
            # PyCharm
            res_filename = os.path.dirname(res_filename)
            if os.path.isdir(res_filename):
                from .wx import start_folder_dialog
                return start_folder_dialog.startFolderEditor(folder_path=res_filename)

        else:
            log_func.error(u'Not support editing file <%s>' % res_filename)
    else:
        log_func.error(u'Not supported engine as editor')
    return False


def openResourceEditor(res_filename):
    """
    Open resource editor form.

    :param res_filename: Resource filename.
        Resource file may be *.res or *.py file.
    :return: True/False.
    """
    try:
        return _openResourceEditor(res_filename)
    except:
        log_func.fatal(u'Error open resource editor form')
    return False
