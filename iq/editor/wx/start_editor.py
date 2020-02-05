#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start editor dialog.
"""

import sys
import wx

try:
    from . import start_editor_dlg
except:
    import start_editor_dlg

from ...util import log_func
from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from ...project import prj

from ...project import prj_func

__version__ = (0, 0, 0, 1)


class iqStartEditorDialog(start_editor_dlg.iqStartEditorDialogProto):
    """
    Start editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_editor_dlg.iqStartEditorDialogProto.__init__(self, *args, **kwargs)

        self._project_manager = prj.iqProjectManager()

    def init(self):
        """
        Init form.
        """
        self.init_images()

    def init_images(self):
        """
        Init images of controls on form.
        """
        bmp = wxbitmap_func.createIconBitmap('fatcow/application_add')
        self.new_prj_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/resultset_next')
        self.run_prj_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/bug_delete')
        self.dbg_prj_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/bug_delete')
        self.dbg_prj_bitmap.SetBitmap(bmp)

    def onExitButtonClick(self, event):
        """
        Button click handler <Exit>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onNewPrjButtonClick(self, event):
        """
        Button click handler <New project>.
        """
        self._project_manager.create(parent=self)
        event.Skip()

    def onRunPrjButtonClick(self, event):
        """
        Button click handler <Run project>.
        """
        prj_names = prj_func.getProjectNames()
        selected_prj_name = dlg_func.getSingleChoiceDlg(parent=self, title='PROJECTS',
                                                        prompt_text=u'Select a project to run:',
                                                        choices=prj_names)
        if selected_prj_name:
            self._project_manager.run(selected_prj_name)
        event.Skip()

    def onDbgPrjButtonClick(self, event):
        """
        Button click handler <Debug project>.
        """
        prj_names = prj_func.getProjectNames()
        selected_prj_name = dlg_func.getSingleChoiceDlg(parent=self, title='PROJECTS',
                                                        prompt_text=u'Select a project to debug:',
                                                        choices=prj_names)
        if selected_prj_name:
            self._project_manager.debug(selected_prj_name)

        event.Skip()

    def onToolsButtonClick(self, event):
        """
        Button click handler <Tools>.
        """
        event.Skip()

    def onHelpButtonClick(self, event):
        """
        Button click handler <Help>.
        """
        event.Skip()


def openStartEditorDlg(parent=None):
    """
    Open start editor dialog.

    :param parent: Parent form.
    :return: True/False
    """
    dlg = None
    try:
        dlg = iqStartEditorDialog(parent=parent)
        dlg.init()
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Open start editor dialog error')
    return False


def startEditor():
    """
    Start editor.

    :return:
    """
    app = wx.App()
    openStartEditorDlg()
    app.MainLoop()


if __name__ == '__main__':
    startEditor()
