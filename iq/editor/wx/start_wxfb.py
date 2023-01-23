#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start wxFormBuilder project editor dialog.
"""

import sys
import wx
import os.path

try:
    from . import start_wxfb_dlg
except ImportError:
    import start_wxfb_dlg

from ...util import log_func
from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from . import wxfb_manager

from ...engine.wx import stored_wx_form_manager

__version__ = (0, 0, 1, 1)


class iqStartWXFormBuilderEditorDialog(start_wxfb_dlg.iqStartWXFormBuilderEditorDialogProto,
                                       stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start wxFormBuilder project editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_wxfb_dlg.iqStartWXFormBuilderEditorDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('wxformbuilder')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.fbp_filename = None

        self.wxformbuilder_manager = wxfb_manager.iqWXFormBuilderManager()

        self.loadCustomProperties()

    def init(self):
        """
        Init form.
        """
        self.initImages()

    def initImages(self):
        """
        Init images of controls on form.
        """
        bmp = wxbitmap_func.createIconBitmap('fatcow/script_go')
        self.migrate_bitmap.SetBitmap(bmp)

    def onExitButtonClick(self, event):
        """
        Button click handler <Exit>.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onNewButtonClick(self, event):
        """
        Button click handler <New>.
        """
        self.wxformbuilder_manager.createProject()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onOpenButtonClick(self, event):
        """
        Button click handler <Open>.
        """
        if os.path.exists(self.fbp_filename):
            self.wxformbuilder_manager.openProject(prj_filename=self.fbp_filename)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=u'WARNING',
                                    prompt_text=u'wxFormBuilder project file <%s> not found' % self.fbp_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onMigrateButtonClick(self, event):
        """
        Button click handler <Migrate>.
        """
        result = wxfb_manager.migrateWXFormBuilderProject(self.fbp_filename)
        if result:
            dlg_func.openMsgBox(title=u'EDITOR',
                                prompt_text=u'Migration wxFormBuilder project file <%s> was successful' % self.fbp_filename)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=u'EDITOR',
                                    prompt_text=u'Migration wxFormBuilder project file <%s> ended unsuccessfully' % self.fbp_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()


def openStartWXFormBuilderEditorDlg(parent=None, fbp_filename=None):
    """
    Open start wxFormBuilder project editor dialog.

    :param parent: Parent form.
    :param fbp_filename: wxFormBuilder progect file name.
    :return: True/False
    """
    dlg = None
    try:
        dlg = iqStartWXFormBuilderEditorDialog(parent=parent)
        dlg.fbp_filename = fbp_filename
        new_title = u'wxFormBuilder project <%s>' % os.path.basename(fbp_filename)
        dlg.SetTitle(new_title)
        dlg.init()
        result = dlg.ShowModal() == wx.ID_OK
        dlg.saveCustomProperties()
        dlg.Destroy()
        return result
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error open start wxFormBuilder project editor dialog')
    return False


def startWXFormBuilderEditor(fbp_filename, *args, **kwargs):
    """
    Start wxFormBuilder project editor.

    :return:
    """
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)

    app = wx.App()
    result = openStartWXFormBuilderEditorDlg(parent=None, fbp_filename=fbp_filename)
    if result:
        app.MainLoop()
    return result


if __name__ == '__main__':
    startWXFormBuilderEditor(*sys.argv[1:])
