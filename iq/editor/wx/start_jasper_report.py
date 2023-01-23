#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start JasperReport project editor dialog.
"""

import sys
import os.path
import wx

try:
    from . import start_jasperreport_dlg
except ImportError:
    import start_jasperreport_dlg

import iq
from iq.util import log_func
from iq.util import global_func
from iq.util import lang_func

from ...engine.wx import wxbitmap_func
from ...dialog import dlg_func

from iq.engine.wx import form_manager
from ...engine.wx import stored_wx_form_manager

from ..jasper_report import jasperreport_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqStartJasperReportEditorDialog(start_jasperreport_dlg.iqStartJasperReportEditorDialogProto,
                                      stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Start JasperReport project editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        start_jasperreport_dlg.iqStartJasperReportEditorDialogProto.__init__(self, *args, **kwargs)

        bmp = wxbitmap_func.createIconBitmap('fatcow/report_green')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.jrxml_filename = None

        self.jasperreport_manager = jasperreport_manager.iqJasperReportManager()

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
        new_jrxml_basename = dlg_func.getTextEntryDlg(parent=self, title=_(u'NEW'),
                                                      prompt_text=_(u'Entry new JRXML filename'))
        if new_jrxml_basename:
            new_dirname = dlg_func.getDirDlg(parent=self, title=_(u'NEW'),
                                             default_path=os.path.dirname(self.jrxml_filename))
            if new_dirname:
                new_jrxml_filename = os.path.join(new_dirname,
                                                  new_jrxml_basename + jasperreport_manager.JASPER_REPORT_PROJECT_FILE_EXT)
                self.jasperreport_manager.createProject(new_prj_filename=new_jrxml_filename)

        self.EndModal(wx.ID_OK)
        event.Skip()

    def onOpenButtonClick(self, event):
        """
        Button click handler <Open>.
        """
        if os.path.exists(self.jrxml_filename):
            self.jasperreport_manager.openProject(prj_filename=self.jrxml_filename)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'JasperReport project file <%s> not found' % self.jrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onPreviewButtonClick(self, event):
        """
        Button click handler <Preview>.
        """
        if os.path.exists(self.jrxml_filename):
            self.jasperreport_manager.generate(prj_filename=self.jrxml_filename,
                                               command='process',
                                               fmt='view')
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'JasperReport project file <%s> not found' % self.jrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onPrintButtonClick(self, event):
        """
        Button click handler <Preview>.
        """
        if os.path.exists(self.jrxml_filename):
            self.jasperreport_manager.generate(prj_filename=self.jrxml_filename,
                                               command='process',
                                               fmt='print')
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'JasperReport project file <%s> not found' % self.jrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def onConvertButtonClick(self, event):
        """
        Button click handler <Convert to>.
        """
        if os.path.exists(self.jrxml_filename):
            selected_fmt = self.convert_choice.GetSelection().lower()
            self.jasperreport_manager.generate(prj_filename=self.jrxml_filename,
                                               command='process',
                                               fmt=selected_fmt)
            self.EndModal(wx.ID_OK)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'JasperReport project file <%s> not found' % self.jrxml_filename)
            self.EndModal(wx.ID_CANCEL)
        event.Skip()


def openStartJasperReportEditorDialog(parent=None, jrxml_filename=None):
    """
    Open dialog.

    :param parent: Parent window.
    :param jrxml_filename: JRXML jasperReport project filename.
    :return: True/False.
    """
    dialog = None
    try:
        if parent is None:
            parent = global_func.getMainWin()

        dialog = iqStartJasperReportEditorDialog(parent)
        dialog.jrxml_filename = jrxml_filename
        new_title = u'JasperReport project <%s>' % os.path.basename(jrxml_filename)
        dialog.SetTitle(new_title)
        dialog.init()
        result = dialog.ShowModal()
        dialog.Destroy()
        return result == wx.ID_OK
    except:
        if dialog:
            dialog.Destroy()
        log_func.fatal(u'Error open dialog <iqStartJasperReportEditorDialog>')
    return False


def startJasperReportEditor(jrxml_filename, *args, **kwargs):
    """
    Start JasperReport project editor.

    :param jrxml_filename: JRXML jasperReport project filename.
    :return:
    """
    app = wx.App()
    result = openStartJasperReportEditorDialog(parent=None, jrxml_filename=jrxml_filename)
    if result:
        app.MainLoop()
    return result


if __name__ == '__main__':
    startJasperReportEditor(*sys.argv[1:])
