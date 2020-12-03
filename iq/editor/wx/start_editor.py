#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start editor dialog.
"""

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
from ...engine.wx import stored_wx_form_manager

__version__ = (0, 0, 0, 1)


class iqStartEditorDialog(start_editor_dlg.iqStartEditorDialogProto,
                          stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_editor_dlg.iqStartEditorDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('python')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self._project_manager = prj.iqProjectManager()

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
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onNewPrjButtonClick(self, event):
        """
        Button click handler <New project>.
        """
        self._project_manager.create(parent=self)
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onRunPrjButtonClick(self, event):
        """
        Button click handler <Run project>.
        """
        prj_descriptions = prj_func.getProjectDescriptions()

        prj_data = list(prj_descriptions.items())
        prj_data.sort()
        prj_names = [name for name, description in prj_data]
        prj_items = [u'%s\t:\t%s' % (name, description) for name, description in prj_data]
        selected_prj_idx = dlg_func.getSingleChoiceIdxDlg(parent=self, title='PROJECTS',
                                                          prompt_text=u'Select a project to run:',
                                                          choices=prj_items)
        if selected_prj_idx >= 0:
            selected_prj_name = prj_names[selected_prj_idx]
            self._project_manager.run(selected_prj_name)

        self.EndModal(wx.ID_OK)
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

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onToolsButtonClick(self, event):
        """
        Button click handler <Tools>.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onHelpButtonClick(self, event):
        """
        Button click handler <Help>.
        """
        self.EndModal(wx.ID_OK)
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
        result = dlg.ShowModal() == wx.ID_OK
        dlg.saveCustomProperties()
        dlg.Destroy()
        return result
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error open start editor dialog')
    return False


def startEditor():
    """
    Start editor.

    :return:
    """
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)
    app = wx.App()
    result = openStartEditorDlg()
    app.MainLoop()
    return result


if __name__ == '__main__':
    startEditor()
