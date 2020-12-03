#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start python module editor dialog.
"""

import sys
import os.path
import wx

try:
    from . import start_py_dlg
except:
    import start_py_dlg

from ...util import log_func
from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from . import wxfb_manager
from ...script import migrate_py
from .code_generator import gui_generator

from ...engine.wx import stored_wx_form_manager

__version__ = (0, 0, 0, 1)


class iqStartPythonEditorDialog(start_py_dlg.iqStartPythonEditorDialogProto,
                                stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start python module editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_py_dlg.iqStartPythonEditorDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('python_script')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.py_filename = None

        self.loadCustomProperties()

    def init(self):
        """
        Init form.
        """
        self.initImages()

        is_wxfb_py = wxfb_manager.isWXFormBuilderFormPy(self.py_filename)
        self.wxfb_button.Enable(is_wxfb_py)
        self.gen_button.Enable(is_wxfb_py)

    def initImages(self):
        """
        Init images of controls on form.
        """
        bmp = wxbitmap_func.createIconBitmap('fatcow/plugin_go')
        self.wxfb_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/script_gear')
        self.gen_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/script_go')
        self.migrate_bitmap.SetBitmap(bmp)

    def onExitButtonClick(self, event):
        """
        Button click handler <Exit>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onWXFBButtonClick(self, event):
        """
        Button click handler <Adapt wxFormBuilder form python module>.
        """
        result = wxfb_manager.adaptWXWFormBuilderPy(self.py_filename)

        if result:
            msg = u'Python adaptation of wxFormBuilder module <%s> was successful' % self.py_filename
            dlg_func.openMsgBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_OK)
        else:
            msg = u'Python adaptation of wxFormBuilder module <%s> ended unsuccessfully' % self.py_filename
            dlg_func.openErrBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_CANCEL)

        event.Skip()

    def onMigrateButtonClick(self, event):
        """
        Button click handler <Migrate>.
        """
        result = migrate_py.migratePy(py_filename=self.py_filename)

        if result:
            msg = u'Python migrate <%s> was successful' % self.py_filename
            dlg_func.openMsgBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_OK)
        else:
            msg = u'Python migrate <%s> ended unsuccessfully' % self.py_filename
            dlg_func.openErrBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_CANCEL)

        event.Skip()

    def onGenButtonClick(self, event):
        """
        Button click handler <Generate GUI module>.
        """
        result = gui_generator.gen(src_filename=self.py_filename, parent=self)

        if result:
            msg = u'Python generate by <%s> was successful' % self.py_filename
            dlg_func.openMsgBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_OK)
        else:
            msg = u'Python migrate <%s> ended unsuccessfully' % self.py_filename
            dlg_func.openErrBox(title=u'EDITOR', prompt_text=msg)
            self.EndModal(wx.ID_CANCEL)

        event.Skip()


def openStartPythonEditorDlg(parent=None, py_filename=None):
    """
    Open start python module editor dialog.

    :param parent: Parent form.
    :return: True/False
    """
    dlg = None
    try:
        dlg = iqStartPythonEditorDialog(parent=parent)
        dlg.py_filename = py_filename
        new_title = u'Python module <%s>' % os.path.basename(py_filename)
        dlg.SetTitle(new_title)
        dlg.init()
        result = dlg.ShowModal() == wx.ID_OK
        dlg.saveCustomProperties()
        dlg.Destroy()
        return result
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error open start python module editor dialog')
    return False


def startPythonEditor(py_filename, *args, **kwargs):
    """
    Start python module editor.

    :return:
    """
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)

    app = wx.App()
    result = openStartPythonEditorDlg(parent=None, py_filename=py_filename)
    if result:
        app.MainLoop()
    return result


if __name__ == '__main__':
    startPythonEditor(*sys.argv[1:])


