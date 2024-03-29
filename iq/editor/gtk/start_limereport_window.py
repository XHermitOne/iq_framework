#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module <start_limereport_window.py>. 
Generated by the iqFramework module the Glade prototype.
"""

import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func
from iq.util import global_func
from iq.util import lang_func

from ...dialog import dlg_func

from iq.engine.gtk import gtk_handler
# from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

from ...engine.gtk import stored_gtk_form_manager

from ..lime_report import limereport_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqStartLimereportWindow(gtk_handler.iqGtkHandler,
                              stored_gtk_form_manager.iqStoredGtkFormsManager):
    """
    Start LimeReport project editor dialog.
    """
    def __init__(self, *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'start_limereport_win.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='start_limereport_window',  
                                          *args, **kwargs)

        self.lrxml_filename = None

        self.limereport_manager = limereport_manager.iqLimeReportManager()

        self.loadCustomProperties()

    def init(self):
        """
        Init form.
        """
        self.initImages()
        self.initControls()

    def initImages(self):
        """
        Init images of controls on form.
        """
        pass

    def initControls(self):
        """
        Init controls method.
        """
        pass

    def onDestroy(self, widget):
        """
        Destroy window handler.
        """
        self.saveCustomProperties()
        gi.repository.Gtk.main_quit()

    def onOpenLimeReportProjectButtonClicked(self, widget):
        """
        Button click handler <Open>.
        """
        if os.path.exists(self.lrxml_filename):
            self.limereport_manager.openProject(prj_filename=self.lrxml_filename)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.lrxml_filename)
        self.getGtkTopObject().close()

    def onPreviewButtonClicked(self, widget):
        """
        Button click handler <Preview>.
        """
        if os.path.exists(self.lrxml_filename):
            self.limereport_manager.preview(prj_filename=self.lrxml_filename)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.lrxml_filename)
        self.getGtkTopObject().close()

    def onPrintButtonClicked(self, widget):
        """
        Button click handler <Print>.
        """
        if os.path.exists(self.lrxml_filename):
            self.limereport_manager.print(prj_filename=self.lrxml_filename)
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    prompt_text=u'LimeReport project file <%s> not found' % self.lrxml_filename)
        self.getGtkTopObject().close()

    def onNewLimeReportProjectButtonClicked(self, widget):
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

        self.getGtkTopObject().close()

    def onExitButtonClicked(self, widget):
        """
        Button click handler <Exit>.
        """
        self.getGtkTopObject().close()

    def onHelpButtonClicked(self, widget):
        """
        Button click handler <Help>.
        """
        self.getGtkTopObject().close()

    def onConvertButtonClicked(self, widget):
        """
        Button click handler <Convert>.
        """
        self.getGtkTopObject().close()


def openStartLimereportWindow(parent=None, lrxml_filename=None):
    """
    Open start_limereport_window.

    :param parent: Parent window.
    :param lrxml_filename: LRXML jasperReport project filename.
    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iqStartLimereportWindow()
        obj.lrxml_filename = lrxml_filename
        new_title = _(u'LimeReport project') + ' <%s>' % os.path.basename(lrxml_filename)
        obj.getGtkTopObject().set_title(new_title)
        obj.init()
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <start_limereport_window>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    


def startLimeReportEditor(lrxml_filename, *args, **kwargs):
    """
    Start LimeReport project designer/editor.

    :param lrxml_filename: LRXML jasperReport project filename.
    :return:
    """
    log_func.info(u'GTK library version: %s' % gi.__version__)

    result = False
    win = None
    try:
        win = iqStartLimereportWindow()
        win.lrxml_filename = lrxml_filename
        new_title = _(u'LimeReport project') + ' <%s>' % os.path.basename(lrxml_filename)
        win.getGtkTopObject().set_title(new_title)
        win.init()
        win.getGtkTopObject().show_all()
        result = True
    except:
        log_func.fatal(u'Error open window <start_limereport_window>')

    gi.repository.Gtk.main()

    if win and win.getGtkTopObject() is not None:
        win.getGtkTopObject().destroy()
    return result
