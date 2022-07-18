#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль приложения генератора отчетов.
"""

import os
import os.path

import wx
import wx.lib.buttons

from iq.util import ini_func
from iq.util import file_func
from iq.util import res_func
from iq.util import log_func
from iq.util import global_func
from iq.util import lang_func
from iq.util import sys_func

from iq.dialog import dlg_func
from iq.engine import img_func

from iq_report.report import report_gen_func
from iq_report.report import report_glob_data

from .. import report_folder_func

__version__ = (0, 0, 3, 1)

_ = lang_func.getTranslation().gettext

# Browser modes
REPORT_VIEWER_MODE = 0
REPORT_EDITOR_MODE = 1

# Positions and sizes of control buttons
REP_BROWSER_BUTTONS_POS_X = 980
REP_BROWSER_BUTTONS_WIDTH = 200
REP_BROWSER_BUTTONS_HEIGHT = 30

# Dialog box size
REP_BROWSER_DLG_WIDTH = 1200
REP_BROWSER_DLG_HEIGHT = 460

# Dialog title
TITLE = 'iqReport'


class iqReportBrowserDialog(wx.Dialog):
    """
    Report browser form.
    """
    def __init__(self, parent=None, mode=REPORT_VIEWER_MODE, report_dir=''):
        """
        Constructor.

        :param parent: Parent window.
        :param mode: Browser mode.
        :param report_dir: Report directory.
        """
        ver = '.'.join([str(ident) for ident in __version__])
        wx.Dialog.__init__(self, parent, wx.NewId(),
                           title=u'%s. Report management system. v. %s' % (TITLE, ver),
                           pos=wx.DefaultPosition,
                           size=wx.Size(REP_BROWSER_DLG_WIDTH, REP_BROWSER_DLG_HEIGHT),
                           style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION)

        self._report_dirname = report_dir

        img = img_func.createIconImage('fatcow/report_stack')
        if img:
            self.SetIcon(icon=wx.Icon(img))
        else:
            log_func.warning(u'Error set report browser icon')

        self.dir_statictext = wx.StaticText(self, id=wx.NewId(),
                                            label='',
                                            pos=wx.Point(10, 10), size=wx.DefaultSize,
                                            style=0)

        if not self._report_dirname or not os.path.exists(self._report_dirname):
            self._report_dirname = ini_func.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
            if not self._report_dirname or not os.path.exists(self._report_dirname):
                self._report_dirname = dlg_func.getDirDlg(self,
                                                          u'Report directory <%s> not found. Select report directory.' % self._report_dirname)

                if self._report_dirname:
                    self._report_dirname = os.path.normpath(self._report_dirname)
                    ini_func.saveParamINI(self.getReportSettingsINIFile(),
                                          'REPORTS', 'report_dir', self._report_dirname)
        self.dir_statictext.SetLabel(self._report_dirname)

        self.report_treectrl = wx.TreeCtrl(self, wx.NewId(),
                                           pos=wx.Point(10, 30), size=wx.Size(950, 390), style=wx.TR_HAS_BUTTONS,
                                           validator=wx.DefaultValidator, name='ReportTree')

        self.img_list = wx.ImageList(16, 16)
        img = img_func.createIconImage('fatcow/report_stack')
        self.img_list.Add(img)
        img = img_func.createIconImage('fatcow/report_green')
        self.img_list.Add(img)
        img = img_func.createIconImage('fatcow/report')
        self.img_list.Add(img)
        self.report_treectrl.AssignImageList(self.img_list)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged, id=self.report_treectrl.GetId())

        img = img_func.createIconImage('fatcow/report_magnify')
        self.rep_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Preview'),
                                                             size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                   REP_BROWSER_BUTTONS_HEIGHT),
                                                             pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 30))
        self.Bind(wx.EVT_BUTTON, self.onPreviewReportButton, id=self.rep_button.GetId())

        img = img_func.createIconImage('fatcow/printer')
        self.print_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Print'),
                                                               size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                     REP_BROWSER_BUTTONS_HEIGHT),
                                                               pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 70))
        self.Bind(wx.EVT_BUTTON, self.onPrintReportButton, id=self.print_button.GetId())

        img = img_func.createIconImage('fatcow/page_orientation')
        self.page_setup_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Page setup'),
                                                                    size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                          REP_BROWSER_BUTTONS_HEIGHT),
                                                                    pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 110))
        self.Bind(wx.EVT_BUTTON, self.onPageSetupButton, id=self.page_setup_button.GetId())

        img = img_func.createIconImage('fatcow/excel_exports')
        self.export_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Export'),
                                                                size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                      REP_BROWSER_BUTTONS_HEIGHT),
                                                                pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 150))
        self.Bind(wx.EVT_BUTTON, self.onConvertReportButton, id=self.export_button.GetId())

        if mode == REPORT_EDITOR_MODE:
            img = img_func.createIconImage('fatcow/folder_vertical_document')
            self.set_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Report folder'),
                                                                 size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                       REP_BROWSER_BUTTONS_HEIGHT),
                                                                 pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 190))
            self.Bind(wx.EVT_BUTTON, self.onSetReportDirButton, id=self.set_button.GetId())

            img = img_func.createIconImage('fatcow/report_add')
            self.new_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Create'),
                                                                 size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                       REP_BROWSER_BUTTONS_HEIGHT),
                                                                 pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 230))
            self.Bind(wx.EVT_BUTTON, self.onNewReportButton, id=self.new_button.GetId())

            img = img_func.createIconImage('fatcow/report_design')
            self.edit_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Edit'),
                                                                size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                      REP_BROWSER_BUTTONS_HEIGHT),
                                                                pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 270))
            self.Bind(wx.EVT_BUTTON, self.onEditReportButton, id=self.edit_button.GetId())

            img = img_func.createIconImage('fatcow/arrow_refresh')
            self.convert_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Update'),
                                                                     size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                           REP_BROWSER_BUTTONS_HEIGHT),
                                                                     pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 310))
            self.Bind(wx.EVT_BUTTON, self.onUpdateReportButton, id=self.convert_button.GetId())

        img = img_func.createIconImage('fatcow/door_in')
        self.exit_button = wx.lib.buttons.GenBitmapTextButton(self, wx.NewId(), img, _(u'Exit'),
                                                              size=(REP_BROWSER_BUTTONS_WIDTH,
                                                                    REP_BROWSER_BUTTONS_HEIGHT),
                                                              pos=wx.Point(REP_BROWSER_BUTTONS_POS_X, 390),
                                                              style=wx.ALIGN_LEFT)
        self.Bind(wx.EVT_BUTTON, self.onExitButton, id=self.exit_button.GetId())

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
        
    def onPreviewReportButton(self, event):
        """
        Preview button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        log_func.debug(u'Preview <%s>' % str(item_data[report_folder_func.REP_FILE_IDX] if item_data else u'-'))

        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX],
                                                     parent=self,
                                                     refresh=True).preview()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)
        event.Skip()
            
    def onPrintReportButton(self, event):
        """
        Print button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        log_func.debug(u'Print <%s>' % item_data[report_folder_func.REP_FILE_IDX] if item_data else u'-')
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX],
                                                     parent=self,
                                                     refresh=True).print()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)
        event.Skip()

    def onPageSetupButton(self, event):
        """
        Page setup button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX], parent=self).setPageSetup()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)
        event.Skip()

    def onSetReportDirButton(self, event):
        """
        Report folder button click handler.
        """
        self._report_dirname = ini_func.loadParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir')
        dir_dlg = wx.DirDialog(self, _(u'Select report folder path:'),
                               style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if self._report_dirname:
            dir_dlg.SetPath(self._report_dirname)
        if dir_dlg.ShowModal() == wx.ID_OK:
            self._report_dirname = dir_dlg.GetPath()
        
        dir_dlg.Destroy()        

        ok = ini_func.saveParamINI(self.getReportSettingsINIFile(), 'REPORTS', 'report_dir', self._report_dirname)
            
        if ok is True:
            self.dir_statictext.SetLabel(self._report_dirname)
            self.buildReportTree(self._report_dirname)
        event.Skip()

    def onExitButton(self, event):
        """
        Exit button click handler.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onNewReportButton(self, event):
        """
        Create report button click handler.
        """
        report_gen_func.getCurReportGeneratorSystem().createNew(self._report_dirname)
        event.Skip()

    def onEditReportButton(self, event):
        """
        Edit button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            rep_generator = report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX], parent=self)
            if rep_generator is not None:
                rep_generator.edit(item_data[0])
            else:
                log_func.warning(u'Report generator not defined. Type <%s>' % item_data[report_folder_func.REP_FILE_IDX])

        event.Skip()

    def onUpdateReportButton(self, event):
        """
        Update button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            log_func.debug(u'Update report <%s>' % item_data[0])
            report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX], parent=self).update(item_data[0])
        else:
            report_gen_func.getCurReportGeneratorSystem(self).update()
                
        self.buildReportTree(self._report_dirname)

        event.Skip()

    def onConvertReportButton(self, event):
        """
        Convert button click handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        log_func.debug(u'Convert <%s>' % item_data[report_folder_func.REP_FILE_IDX] if item_data else u'-')
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            report_gen_func.getReportGeneratorSystem(item_data[report_folder_func.REP_FILE_IDX],
                                                     parent=self,
                                                     refresh=True).convert()
        else:
            dlg_func.openWarningBox(title=_(u'WARNING'),
                                    message=_(u'You must select a report'), parent=self)

        event.Skip()

    def onRightMouseClick(self, event):
        """
        Tree item right mouse button clcik handler.
        """
        popup_menu = wx.Menu()
        id_rename = wx.NewId()
        popup_menu.Append(id_rename, _(u'Rename'))
        self.Bind(wx.EVT_MENU, self.onRenameReport, id=id_rename)
        self.report_treectrl.PopupMenu(popup_menu, event.GetPosition())
        event.Skip()

    def onRenameReport(self, event):
        """
        Rename report menu item handler.
        """
        item = self.report_treectrl.GetSelection()
        item_data = self.report_treectrl.GetItemData(item)
        if item_data is not None and item_data[report_folder_func.REP_ITEMS_IDX] is None:
            old_rep_name = os.path.splitext(os.path.split(item_data[report_folder_func.REP_FILE_IDX])[1])[0]
            new_rep_name = dlg_func.getTextEntryDlg(self, _(u'Rename report'),
                                                    _(u'Entry new report name'), old_rep_name)
            if new_rep_name and new_rep_name != old_rep_name:
                new_rep_file_name = os.path.join(os.path.split(item_data[report_folder_func.REP_FILE_IDX])[0],
                                                 new_rep_name + report_folder_func.REPORT_FILENAME_EXT)

                if not os.path.isfile(new_rep_file_name):
                    self.renameReport(item_data[report_folder_func.REP_FILE_IDX], new_rep_name)
                else:
                    dlg_func.openWarningBox(title=_(u'WARNING'),
                                            prompt_text=_(u'A report with the same name already exists'),
                                            parent=self)

        event.Skip()

    def renameReport(self, rep_filename, new_name):
        """
        Rename report.
        """
        old_name = os.path.splitext(os.path.split(rep_filename)[1])[0]
        old_rep_file_name = rep_filename
        old_rep_pkl_file_name = os.path.splitext(old_rep_file_name)[0] + res_func.PICKLE_RESOURCE_FILE_EXT
        old_xls_file_name = os.path.splitext(old_rep_file_name)[0] + report_folder_func.XLS_FILENAME_EXT
        new_rep_file_name = os.path.join(os.path.split(old_rep_file_name)[0],
                                         new_name + report_folder_func.REPORT_FILENAME_EXT)
        if os.path.isfile(old_rep_file_name):
            try:
                os.rename(old_rep_file_name, new_rep_file_name)
            except:
                log_func.fatal(u'Error rename file <%s>' % old_rep_file_name)

            if os.path.isfile(old_rep_pkl_file_name):
                os.remove(old_rep_pkl_file_name)

            report = res_func.loadResource(new_rep_file_name)
            report['name'] = new_name

            rep_file = None
            try:
                rep_file = open(new_rep_file_name, 'wt', encoding=report_glob_data.DEFAULT_REPORT_ENCODING)
                rep_file.write(str(report))
                rep_file.close()
            except:
                rep_file.close()

        new_xls_file_name = os.path.join(os.path.split(old_rep_file_name)[0],
                                         new_name + report_folder_func.XLS_FILENAME_EXT)
        if os.path.isfile(old_xls_file_name):
            os.rename(old_xls_file_name, new_xls_file_name)
            try:
                excel_app = win32com.client.Dispatch('Excel.Application')
                excel_app.Visible = 0
                rep_tmpl = new_xls_file_name.replace('./', os.getcwd()+'/')
                rep_tmpl_book = excel_app.Workbooks.Open(rep_tmpl)
                rep_tmpl_sheet = rep_tmpl_book.Worksheets(old_name)
                rep_tmpl_sheet.Name = new_name
                rep_tmpl_book.save()
                excel_app.Quit()
            except pythoncom.com_error:
                log_func.fatal(u'Error rename file')

    def onSelectChanged(self, event):
        """
        Tree item select changed handler.
        """
        event.Skip()

    def buildReportTree(self, report_dir):
        """
        Build the report tree by report data.

        :param report_dir: Report directory.
        """
        rep_data = report_folder_func.getReportList(report_dir)
        if rep_data is None:
            log_func.warning(u'Error data. Report directory <%s>' % report_dir)
            return

        self.report_treectrl.DeleteAllItems()
        root = self.report_treectrl.AddRoot(_(u'Reports'), image=0)
        self.report_treectrl.SetItemData(root, None)
        self._appendItemsReportTree(root, rep_data)
        self.report_treectrl.Expand(root)

    def _appendItemsReportTree(self, parent_id, items):
        """
        Add tree items based on the received report description.

        :param parent_id: Parent item id.
        :param items: Report data branch.
        """
        if not items:
            log_func.warning(u'An empty list of report descriptions when building a report tree')

        for item_data in items:
            label = '%s / %s' % (item_data[report_folder_func.REP_DESCRIPTION_IDX], os.path.basename(item_data[report_folder_func.REP_FILE_IDX]))
            item = self.report_treectrl.AppendItem(parent_id, label, -1, -1, data=None)

            if item_data[report_folder_func.REP_ITEMS_IDX] is not None:
                self._appendItemsReportTree(item, item_data[report_folder_func.REP_ITEMS_IDX])

                self.report_treectrl.SetItemImage(item, 0, wx.TreeItemIcon_Normal)
                self.report_treectrl.SetItemImage(item, 0, wx.TreeItemIcon_Selected)
            else:

                self.report_treectrl.SetItemImage(item, item_data[report_folder_func.REP_IMG_IDX], wx.TreeItemIcon_Normal)
                self.report_treectrl.SetItemImage(item, item_data[report_folder_func.REP_IMG_IDX], wx.TreeItemIcon_Selected)

            self.report_treectrl.SetItemData(item, item_data)

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
            log_func.warning(u'Report browser already open [%d]' % find_report_dir_process)
            return False

    app = wx.GetApp()
    if app is None:
        app = wx.App()
    log_func.info(u'wxPython version: %s' % wx.VERSION_STRING)

    dlg = None
    try:
        dlg = iqReportBrowserDialog(parent=parent_form, mode=mode,
                                    report_dir=report_dir)
        dlg.ShowModal()
        dlg.Destroy()
        return True
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error starting report browser')
    return False
