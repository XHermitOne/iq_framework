#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start Glade project editor dialog.
"""

import sys
import wx
import os.path

try:
    from . import start_glade_dlg
except ImportError:
    import start_glade_dlg

from ...util import log_func
from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from . import glade_manager

from ...engine.wx import stored_wx_form_manager

__version__ = (0, 0, 1, 1)


class iqStartGladeEditorDialog(start_glade_dlg.iqStartGladeEditorDialogProto,
                               stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start Glade project editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_glade_dlg.iqStartGladeEditorDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('glade')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.glade_filename = None

        self.glade_manager = glade_manager.iqGladeManager()

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
        # bmp = wxbitmap_func.createIconBitmap('fatcow/script_go')
        # self.migrate_bitmap.SetBitmap(bmp)
        pass

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
        self.glade_manager.createProject()

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onOpenButtonClick(self, event):
        """
        Button click handler <Open>.
        """
        if os.path.exists(self.glade_filename):
            self.glade_manager.openProject(prj_filename=self.glade_filename)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=u'WARNING',
                                    prompt_text=u'Glade project file <%s> not found' % self.glade_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    # def onMigrateButtonClick(self, event):
    #     """
    #     Button click handler <Migrate>.
    #     """
    #     result = wxfb_manager.migrateWXFormBuilderProject(self.glade_filename)
    #     if result:
    #         dlg_func.openMsgBox(title=u'EDITOR',
    #                             prompt_text=u'Migration wxFormBuilder project file <%s> was successful' % self.glade_filename)
    #         self.EndModal(wx.ID_OK)
    #     else:
    #         dlg_func.openWarningBox(title=u'EDITOR',
    #                                 prompt_text=u'Migration wxFormBuilder project file <%s> ended unsuccessfully' % self.glade_filename)
    #         self.EndModal(wx.ID_CANCEL)
    #     event.Skip()


def openStartGladeEditorDlg(parent=None, glade_filename=None):
    """
    Open start Glade project editor dialog.

    :param parent: Parent form.
    :param glade_filename: Glade project file name.
    :return: True/False
    """
    dlg = None
    try:
        dlg = iqStartGladeEditorDialog(parent=parent)
        dlg.glade_filename = glade_filename
        new_title = u'Glade project <%s>' % os.path.basename(glade_filename)
        dlg.SetTitle(new_title)
        dlg.init()
        result = dlg.ShowModal() == wx.ID_OK
        dlg.saveCustomProperties()
        dlg.Destroy()
        return result
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error open start Glade project editor dialog')
    return False


def startGladeEditor(glade_filename, *args, **kwargs):
    """
    Start Glade project editor.

    :return:
    """
    try:
        import gi
        log_func.info(u'PyGObject version: %s' % str(gi.version_info))
    except ImportError:
        log_func.warning(u'Not installed PyGObject library')
        log_func.warning(u'For install: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1')

    app = wx.App()
    result = openStartGladeEditorDlg(parent=None, glade_filename=glade_filename)
    if result:
        app.MainLoop()
    return result


if __name__ == '__main__':
    startGladeEditor(*sys.argv[1:])
