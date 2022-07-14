#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main form module <iqMainFormProto>. 
Generated by the iqFramework module the wxFormBuider prototype form.
"""

import wx
from . import main_form_proto

import iq
from iq.util import log_func
from iq.util import global_func

from iq.engine.wx import mainform_manager

from ..menubars import main_menubar

__version__ = (0, 0, 0, 1)


class iqMainForm(main_form_proto.iqMainFormProto, 
        mainform_manager.iqMainFormManager):

    """
    Main form class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        main_form_proto.iqMainFormProto.__init__(self, *args, **kwargs)

        self.main_menubar = main_menubar.iqMainMenubar()
        self.SetMenuBar(self.main_menubar)

    def init(self):
        """
        Init frame.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images method.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass



def showMainForm(parent=None):
    """
    Open main form.

    :param parent: Parent window.
    :return: True/False.
    """
    try:
        if parent is None:
            parent = global_func.getMainWin()

        frame = iqMainForm(parent)
        frame.init()
        frame.Show()
        return True
    except:
        log_func.fatal(u'Error show main form <iqMainForm>')
    return False


def runMainForm():
    """
    Start application.
    """
    app = global_func.getApplication()
    if app is None:
        app = global_func.createApplication()
    if mainform_manager.showMainForm(iqMainForm):
        app.MainLoop()


if __name__ == '__main__':
    runMainForm()

