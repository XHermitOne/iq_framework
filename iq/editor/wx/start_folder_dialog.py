#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dialog module <iqStartFolderDialogProto>. 
Generated by the iqFramework modulo the wxFormBuider prototype dialog.
"""

import os.path
import wx
from . import start_folder_dlg

import iq
from ...util import log_func
from ...util import global_func
from ...util import res_func
from ...engine.wx import wxbitmap_func

from ...engine.wx import form_manager

from . import wxfb_manager
from .res_editor import new_resource_dialog
from .res_editor import resource_editor

from ...engine.wx import stored_wx_form_manager

from ...project import prj

__version__ = (0, 0, 0, 1)


class iqStartFolderDialog(start_folder_dlg.iqStartFolderDialogProto,
                          form_manager.iqFormManager,
                          stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_folder_dlg.iqStartFolderDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('fatcow/application_add')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.folder_path = None

        self.loadCustomProperties()

    def init(self):
        """
        Init dialog.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images method.
        """
        bmp = wxbitmap_func.createIconBitmap('fatcow/plugin_add')
        self.res_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/application_form_edit')
        self.wxfb_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/resultset_next')
        self.run_bitmap.SetBitmap(bmp)

    def initControls(self):
        """
        Init controls method.
        """
        if self.folder_path:
            folder_basename = os.path.basename(self.folder_path)
            prj_basename = folder_basename + res_func.RESOURCE_FILE_EXT
            prj_filename = os.path.join(self.folder_path, prj_basename)
            self.run_button.Enable(os.path.exists(prj_filename))

    def onExitButtonClick(self, event):
        """
        Button click handler <Exit>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onResButtonClick(self, event):
        """
        Button click handler <New resource>.
        """
        new_res_filename = os.path.join(self.folder_path,
                                        'default%d%s' % (wx.NewId(),
                                                         res_func.RESOURCE_FILE_EXT)) if self.folder_path else None
        res_filename = new_resource_dialog.createNewResource(parent=self, res_filename=new_res_filename)

        self.EndModal(wx.ID_OK)

        if res_filename is not None:
            resource_editor.openResourceEditor(res_filename=res_filename)

        event.Skip()

    def onWXFBButtonClick(self, event):
        """
        Button click handler <New wxFormBuilder project>.
        """
        wxfb_manager.runWXFormBuilder()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRunButtonClick(self, event):
        """
        Button click handler <Run project>.
        """
        project_manager = prj.iqProjectManager()
        selected_prj_name = os.path.basename(self.folder_path) if self.folder_path else None
        project_manager.run(selected_prj_name)

        self.EndModal(wx.ID_OK)
        event.Skip()


def openStartFolderDialog(parent=None, folder_path=None):
    """
    Open dialog.

    :param parent: Parent window.
    :param folder_path: Folder path.
    :return: True/False.
    """
    if parent is None:
        parent = global_func.getMainWin()

    dialog = None
    try:
        dialog = iqStartFolderDialog(parent)
        dialog.folder_path = folder_path
        dialog.init()
        result = dialog.ShowModal() == wx.ID_OK
        dialog.saveCustomProperties()
        dialog.Destroy()
        return result
    except:
        if dialog:
            dialog.Destroy()
        log_func.fatal(u'Error open dialog <iqStartFolderDialog>')
    return False


def startFolderEditor(folder_path=None):
    """
    Start folder editor.

    :param folder_path: Folder path.
    :return: True/False.
    """
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)

    app = wx.App()
    result = openStartFolderDialog(folder_path=folder_path)
    app.MainLoop()
    return result
