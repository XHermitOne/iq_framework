#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run function module.
"""

import wx

from ...util import log_func

__version__ = (0, 0, 0, 1)


def runApplication(main_form_class=None):
    """
    Run wx application function.

    :param main_form_class: Main form class Frame or Dialog.
    :return: True/False.
    """
    if main_form_class is None:
        log_func.warning(u'Not define main form class in wx application')
        return False

    app = wx.App()
    main_form = None
    if issubclass(main_form_class, wx.Frame):
        main_form = main_form_class(parent=None)
        main_form.Show()
    elif issubclass(main_form_class, wx.Dialog):
        main_form = main_form_class(parent=None)
        main_form.ShowModal()
    else:
        log_func.warning(u'Not supported main form class <%s>' % main_form_class.__name__)

    if main_form:
        app.MainLoop()

    if main_form:
        main_form.Destroy()
    return True
