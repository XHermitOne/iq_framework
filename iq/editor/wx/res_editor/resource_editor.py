#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource editor class module:
"""

import sys
import wx

try:
    from . import resource_editor_frm
except:
    import resource_editor_frm

__version__ = (0, 0, 0, 1)


class iqResourceEditor(resource_editor_frm.iqResourceEditorFrameProto):
    """
    Resource editor class.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window object.
        """
        resource_editor_frm.iqResourceEditorFrameProto.__init__(self, parent=parent)


def openResourceEditor(parent=None, res_filename=None):
    """
    Open resource editor frame.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    frame = iqResourceEditor(parent=parent)
    frame.Show()


def runResourceEditor(res_filename=None):
    """
    Run resource editor.

    :param res_filename: Resource file name.
    :return: True/False.
    """
    app = wx.App()
    openResourceEditor(res_filename=res_filename)
    app.MainLoop()


if __name__ == '__main__':
    runResourceEditor(res_filename=sys.argv[1] if len(sys.argv) > 1 else None)
