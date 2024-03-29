#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report browser.

Module <report_browser_win.py>. 
Generated by the iqFramework module the Glade prototype.
"""

import os
import os.path
import signal
import gi

gi.require_version('Gtk', '3.0')
import gi.repository.Gtk

from iq.util import log_func
from iq.util import ini_func
from iq.util import file_func
from iq.util import global_func
from iq.util import lang_func
from iq.util import sys_func

from iq.engine.gtk import gtk_handler
from iq.engine.gtk import gtktreeview_manager
# from iq.engine.gtk import gtkwindow_manager

from iq.dialog import dlg_func

from iq_report.report import report_gen_func

from .. import report_folder_func

__version__ = (0, 0, 1, 1)

_ = lang_func.getTranslation().gettext

# Browser modes
REPORT_VIEWER_MODE = 0
REPORT_EDITOR_MODE = 1


class iqReportBrowserWin(gtk_handler.iqGtkHandler,
                         gtktreeview_manager.iqGtkTreeViewManager):
    """
    Report browser class.
    """
    def __init__(self, parent=None, mode=REPORT_VIEWER_MODE, report_dir='', *args, **kwargs):
        self.glade_filename = os.path.join(os.path.dirname(__file__), 'report_browser_win.glade')
        gtk_handler.iqGtkHandler.__init__(self, glade_filename=self.glade_filename,
                                          top_object_name='report_browser_win',  
                                          *args, **kwargs)

        self._report_dirname = report_dir

        if not self._report_dirname or not os.path.exists(self._report_dirname):
            self._report_dirname = ini_func.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
            if not self._report_dirname or not os.path.exists(self._report_dirname):
                self._report_dirname = dlg_func.getDirDlg(self,
                                                          u'Report directory <%s> not found. Select report directory.' % self._report_dirname)

                if self._report_dirname:
                    self._report_dirname = os.path.normpath(self._report_dirname)
                    ini_func.saveParamINI(self.getReportSettingsINIFile(),
                                          'REPORTS', 'report_dir', self._report_dirname)
        self.getGtkObject('report_folder_label').set_text(self._report_dirname)

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
        self.buildReportTree(self._report_dirname)

    def getReportSettingsINIFile(self):
        """
        Get the name of the configuration file in which the path
        to the report folder is stored.
        """
        if global_func.getProjectName():
            prj_settings_filename = file_func.getProjectSettingsFilename()
            return prj_settings_filename
        return os.path.join(report_folder_func.getRootDirname(), 'settings.ini')

    def onPreviewButtonClicked(self, widget):
        """
        Preview button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]

        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            log_func.debug(u'Preview <%s>' % str(rep_filename))
            report_gen_func.getReportGeneratorSystem(rep_filename,
                                                     parent=self,
                                                     refresh=True).preview()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)

    def onPrintButtonClicked(self, widget):
        """
        Print button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]
        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            log_func.debug(u'Print <%s>' % rep_filename)
            report_gen_func.getReportGeneratorSystem(rep_filename,
                                                     parent=self,
                                                     refresh=True).print()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)

    def onPageSetupButtonClicked(self, widget):
        """
        Page setup button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]
        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            report_gen_func.getReportGeneratorSystem(rep_filename,
                                                     parent=self).setPageSetup()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)

    def onExportButtonClicked(self, widget):
        """
        Convert button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]
        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            log_func.debug(u'Convert <%s>' % rep_filename)
            report_gen_func.getReportGeneratorSystem(rep_filename,
                                                     parent=self,
                                                     refresh=True).convert()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)

    def onReportFolderButtonClicked(self, widget):
        """
        Report folder button click handler.
        """
        self._report_dirname = ini_func.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
        report_dirname = dlg_func.getDirDlg(parent=self, title=_(u'Select report folder path:'),
                                            default_path=self._report_dirname)
        if report_dirname:
            self._report_dirname = report_dirname
            ini_func.saveParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir', self._report_dirname)

            self.getGtkObject('report_folder_label').set_text(self._report_dirname)
            self.buildReportTree(self._report_dirname)

    def onCreateButtonClicked(self, widget):
        """
        Create report button click handler.
        """
        report_gen_func.getCurReportGeneratorSystem().createNew(self._report_dirname)

    def onEditButtonClicked(self, widget):
        """
        Edit button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]
        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            rep_generator = report_gen_func.getReportGeneratorSystem(rep_filename, parent=self)
            if rep_generator is not None:
                rep_generator.edit(rep_filename)
            else:
                log_func.warning(u'Report generator not defined. Type <%s>' % item_data[report_folder_func.REP_FILE_IDX])

    def onUpdateButtonClicked(self, widget):
        """
        Update button click handler.
        """
        item_data = self.getGtkTreeViewSelectedItemData(treeview=self.getGtkObject('report_treeview'))
        has_children = isinstance(item_data, dict) and 'data' in item_data and item_data['data'][report_folder_func.REP_ITEMS_IDX]
        if not has_children:
            rep_filename = item_data['data'][report_folder_func.REP_FILE_IDX]
            log_func.debug(u'Update report <%s>' % rep_filename)
            report_gen_func.getReportGeneratorSystem(rep_filename,
                                                     parent=self).update(rep_filename)
        else:
            report_gen_func.getCurReportGeneratorSystem(self).update()

        self.buildReportTree(self._report_dirname)

    def onExitButtonClicked(self, widget):
        """
        Exit button click handler.
        """
        self.getGtkTopObject().close()
        gi.repository.Gtk.main_quit()

    def buildReportTree(self, report_dir):
        """
        Build the report tree by report data.

        :param report_dir: Report directory.
        :return: True/False.
        """
        rep_data = report_folder_func.getReportList(report_dir)
        if rep_data is None:
            log_func.warning(u'Error data. Report directory <%s>' % report_dir)
            return False

        treeview = self.getGtkObject('report_treeview')
        self.clearGtkTreeView(treeview=treeview)
        root = self.addGtkTreeViewRootItem(treeview=treeview,
                                           node=dict(img='fatcow/report_stack', description=_(u'Reports'), data=None),
                                           columns=('img', 'description'))
        self._appendItemsReportTree(parent_item=root, data=rep_data)
        self.expandGtkTreeViewItem(treeview=treeview, item=root)
        return True

    def _appendItemsReportTree(self, parent_item, data):
        """
        Add tree items based on the received report description.

        :param parent_item: Parent item.
        :param data: Report data branch.
        """
        if not data:
            log_func.warning(u'An empty list of report descriptions when building a report tree')

        treeview = self.getGtkObject('report_treeview')
        for item_data in data:
            label = '%s / %s' % (item_data[report_folder_func.REP_DESCRIPTION_IDX],
                                 os.path.basename(item_data[report_folder_func.REP_FILE_IDX]))
            img_name = 'fatcow/report_stack' if item_data[report_folder_func.REP_ITEMS_IDX] is not None else 'fatcow/report'
            item = self.appendGtkTreeViewChildItem(treeview=treeview,
                                                   parent_item=parent_item,
                                                   columns=[img_name, label],
                                                   data=dict(label=label, data=item_data))

            if item_data[report_folder_func.REP_ITEMS_IDX] is not None:
                self._appendItemsReportTree(item, item_data[report_folder_func.REP_ITEMS_IDX])

    def setReportDir(self, rep_dir):
        """
        Set report directory.

        :param rep_dir: Report directory.
        """
        self._report_dirname = rep_dir

    def getReportDir(self):
        """
        Get report folder.
        """
        return self._report_dirname


def openReportBrowserWin():
    """
    Open report_browser_win.

    :return: True/False.
    """
    result = False
    obj = None
    try:
        obj = iqReportBrowserWin()
        obj.init()
        obj.getGtkTopObject().run()
        result = True
    except:
        log_func.fatal(u'Error open window <report_browser_win>')

    if obj and obj.getGtkTopObject() is not None:
        obj.getGtkTopObject().destroy()
    return result                    


def openReportBrowser(parent_form=None, report_dir='', mode=REPORT_EDITOR_MODE, lock_run_copy=False):
    """
    Launch report browser.

    :param parent_form: The parent form, if not specified, creates a new application.
    :param report_dir: Directory where reports are stored.
    :param mode: Report browser mode.
    :param lock_run_copy: Lock run copy browser.
    :return: True/False.
    """
    if lock_run_copy:
        find_report_dir_process = sys_func.getActiveProcessCount(report_dir)
        if sys_func.isActiveProcess('iq_report --edit') or sys_func.isActiveProcess('iq_report --view') or (find_report_dir_process > 2):
            log_func.warning(u'GTK. Report browser already open [%d]' % find_report_dir_process)
            return False

    log_func.info(u'GTK library version: %s' % gi.__version__)

    result = False
    win = None
    try:
        win = iqReportBrowserWin(parent=parent_form, mode=mode,
                                 report_dir=report_dir)
        win.init()
        win.getGtkTopObject().show_all()
        result = True
    except:
        log_func.fatal(u'Error starting report browser')

    gi.repository.Gtk.main()

    if win and win.getGtkTopObject() is not None:
        win.getGtkTopObject().destroy()
    return result


if __name__ == '__main__':
    openReportBrowser()
