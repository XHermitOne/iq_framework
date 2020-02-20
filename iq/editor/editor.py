#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor functions.
"""

from ..util import log_func
from ..util import global_func
from ..util import res_func
from ..util import py_func

from ..dialog import dlg_func

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
            import wx
            from .wx import wxfb_manager

            app = wx.App()
            if wxfb_manager.isWXFormBuilderFormPy(res_filename):
                result = wxfb_manager.adaptWXWFormBuilderPy(res_filename)
                if result:
                    msg = u'Python adaptation of wxFormBuilder module <%s> was successful' % res_filename
                    dlg_func.openMsgBox(title=u'EDITOR', prompt_text=msg)
                else:
                    msg = u'Python adaptation of wxFormBuilder module <%s> ended unsuccessfully' % res_filename
                    dlg_func.openErrBox(title=u'EDITOR', prompt_text=msg)
                return result
            else:
                msg = u'Python module <%s> maintenance not supported' % res_filename
                log_func.warning(msg)
                dlg_func.openWarningBox(title=u'EDITOR', prompt_text=msg)
            app.MainLoop()
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
