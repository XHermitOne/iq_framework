#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start LimeReport project editor dialog.
"""

import sys
import os.path
import wx

try:
    from . import start_limereport_dlg
except ImportError:
    import start_limereport_dlg

import iq
from iq.util import log_func
from iq.util import global_func
from iq.util import lang_func
from iq.util import file_func
from iq.util import pdf_func

from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from iq.engine.wx import form_manager
from ...engine.wx import stored_wx_form_manager

from ..lime_report import limereport_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqStartLimeReportEditorDialog(start_limereport_dlg.iqStartLimeReportEditorDialogProto,
                                    stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start LimeReport project editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_limereport_dlg.iqStartLimeReportEditorDialogProto.__init__(self, *args, **kwargs)

        bmp = wxbitmap_func.createIconBitmap('fatcow/fruit_lime')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.lrxml_filename = None

        self.limereport_manager = limereport_manager.iqLimeReportManager()

        # self.loadCustomProperties()

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
        bmp = wxbitmap_func.createIconBitmap('fatcow/report_add')
        self.new_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/report_design')
        self.open_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/page_white_magnify')
        self.preview_bitmap.SetBitmap(bmp)

        bmp = wxbitmap_func.createIconBitmap('fatcow/document_copies')
        self.convert_bitmap.SetBitmap(bmp)

    def initControls(self):
        """
        Init controls method.
        """
        pass

    def onConvertButtonClick(self, event):
        event.Skip()

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
        new_lrxml_basename = dlg_func.getTextEntryDlg(parent=self, title=_(u'NEW'),
                                                      prompt_text=_(u'Entry new LRXML filename'))
        if new_lrxml_basename:
            new_dirname = dlg_func.getDirDlg(parent=self, title=_(u'NEW'),
                                             default_path=os.path.dirname(self.lrxml_filename))
            if new_dirname:
                new_lrxml_filename = os.path.join(new_dirname,
                                                  new_lrxml_basename + limereport_manager.LIME_REPORT_PROJECT_FILE_EXT)
                self.limereport_manager.createProject(new_prj_filename=new_lrxml_filename)

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onOpenButtonClick(self, event):
        """
        Button click handler <Open>.
        """
        if os.path.exists(self.lrxml_filename):
            self.limereport_manager.openProject(prj_filename=self.lrxml_filename)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.lrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onPreviewButtonClick(self, event):
        """
        Button click handler <Preview>.
        """
        if os.path.exists(self.lrxml_filename):
            if self.limereport_manager.preview(prj_filename=self.lrxml_filename):
                self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.lrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onPrintButtonClick(self, event):
        """
        Button click handler <Preview>.
        """
        if os.path.exists(self.lrxml_filename):
            if self.limereport_manager.print(prj_filename=self.lrxml_filename):
                self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.jrxml_filename)
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def openStartLimeReportEditorDialog(parent=None, lrxml_filename=None):
    """
    Open dialog.

    :param parent: Parent window.
    :param lrxml_filename: LRXML jasperReport project filename.
    :return: True/False.
    """
    dialog = None
    try:
        if parent is None:
            parent = global_func.getMainWin()

        dialog = iqStartLimeReportEditorDialog(parent)
        dialog.lrxml_filename = lrxml_filename
        new_title = u'LimeReport project <%s>' % os.path.basename(lrxml_filename)
        dialog.SetTitle(new_title)
        dialog.init()
        result = dialog.ShowModal()
        dialog.Destroy()
        return result == wx.ID_OK
    except:
        if dialog:
            dialog.Destroy()
        log_func.fatal(u'Error open dialog <iqStartLimeReportEditorDialog>')
    return False


def startLimeReportEditor(lrxml_filename, *args, **kwargs):
    """
    Start LimeReport project designer/editor.

    :param lrxml_filename: LRXML jasperReport project filename.
    :return:
    """
    app = wx.App()
    result = openStartLimeReportEditorDialog(parent=None, lrxml_filename=lrxml_filename)
    if result:
        app.MainLoop()
    return result


if __name__ == '__main__':
    startLimeReportEditor(*sys.argv[1:])
