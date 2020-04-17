#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main form manager.
"""

import os.path
import wx
import wx.adv
import wx.lib.agw.aui

from ...util import log_func
from ...util import file_func
from ...util import global_func
from ..wx.dlg import wxdlg_func
from ..wx import wxbitmap_func

from . import base_manager
from . import imglib_manager

__version__ = (0, 0, 0, 1)

DEFAULT_SPLASH_DELAY = 3

DEFAULT_SPLASH_IMG_FILE_EXT = '.png'

MAINNOTEBOOK_ATTR_NAME = '__main_notebook'


def getMainWindow():
    """
    Main window object.
    """
    app = global_func.getApplication()
    if app:
        return app.GetTopWindow()
    return None


class iqMainNotebook(wx.lib.agw.aui.AuiNotebook,
                     imglib_manager.iqImageLibManager):
    """
    The class of the main manager of the panels of the main window of the system.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Constructor.

        :param parent: Main form object.
        """
        wx.lib.agw.aui.AuiNotebook.__init__(self, parent, *args, **kwargs)

        self.SetClientSize(parent.GetClientSize())
        # self.initImageLib()

    def addPage(self, page_panel, title, open_exists=False, default_page=-1,
                not_duplicate=True):
        """
        Append page in notebook.

        :param page_panel: Panel object.
        :param title: New page title.
        :param open_exists: Allow to open a page with the same title?
        :param default_page: The index of the page to open by default.
            If -1, the current page to add opens.
        :param not_duplicate: Not open duplicate page?
        :return: True/False.
        """
        try:
            if not_duplicate:
                titles = [self.GetPageText(i) for i in range(self.GetPageCount())]
                if title in titles:
                    msg = u'The page <%s> is already open.' % title
                    log_func.warning(msg)
                    page_panel.Destroy()
                    wxdlg_func.openWarningBox(u'WARNING', msg)
                    return False

            if open_exists:
                self.openPageByTitle(title)
                return True

            if page_panel.GetParent() != self:
                page_panel.Reparent(self)

            if not self.IsShown():
                self.Show()

            if default_page != -1:
                ret = self.AddPage(page_panel, title, False)
                self.SetSelection(default_page)
            else:
                ret = self.AddPage(page_panel, title, True)
            return ret
        except:
            log_func.fatal(u'Error add page main notebook')
        return None

    def delPage(self, page_idx):
        """
        Delete page notebook.

        :param page_idx: Page index.
        """
        try:
            self.AdvanceSelection()

            page_panel = self.GetPage(page_idx)
            page_panel.Destroy()

            result = self.DeletePage(page_idx)

            if self.GetPageCount() <= 0:
                self.Show(False)

            self.Refresh()
            return result
        except:
            log_func.fatal(u'Error delete page main notebook')
        return None

    def clear(self):
        """
        Delete all pages.
        """
        for i in range(self.GetPageCount()):
            page_panel = self.GetPage(i)
            page_panel.Destroy()

        result = wx.Notebook.DeleteAllPages(self)

        self.Show(False)
        return result

    def openPageByTitle(self, title):
        """
        Open page notebook by page title.

        :param title: Page title.
        """
        idx = None
        filter_page = [i for i in range(self.GetPageCount()) if title == self.GetPageText(i)]
        if filter_page:
            idx = filter_page[0]
            self.SetSelection(idx)
        else:
            log_func.warning(u'Page <%s> not found in main notebook' % title)
        return idx


class iqMainFormManager(base_manager.iqBaseManager):
    """
    Main form manager.
    """
    def showMainFormSplash(self, main_form=None, splash_filename=None, delay=DEFAULT_SPLASH_DELAY):
        """
        Show splash window.

        :param main_form: Main form object.
        :param splash_filename: Splash image filename.
        :param delay: Time delay in seconds.
        :return: True/False.
        """
        if main_form is None:
            main_form = self

        assert issubclass(main_form.__class__, wx.Frame) or issubclass(main_form.__class__, wx.Dialog), u'Main form manager type error'

        if not os.path.splitext(splash_filename)[1]:
            splash_filename += DEFAULT_SPLASH_IMG_FILE_EXT
        splash_filename = file_func.getAbsolutePath(splash_filename)

        if not splash_filename or not os.path.exists(splash_filename):
            log_func.error(u'Splash image filename <%s> not found' % splash_filename)
            return False

        bmp = wxbitmap_func.createBitmap(splash_filename)
        splash = wx.adv.SplashScreen(bitmap=bmp,
                                     splashStyle=wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                     milliseconds=delay * 1000,
                                     parent=None,
                                     pos=wx.DefaultPosition,
                                     size=wx.DefaultSize,
                                     style=wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        splash.Show()
        return True

    def getMainNotebook(self):
        """
        Main notebook object.
        """
        if not hasattr(self, MAINNOTEBOOK_ATTR_NAME):
            main_notebook = iqMainNotebook(parent=self)
            setattr(self, MAINNOTEBOOK_ATTR_NAME, main_notebook)
        return getattr(self, MAINNOTEBOOK_ATTR_NAME)

    def destroyMainNotebook(self):
        """
        Delete main notebook object.

        :return: True/False.
        """
        if not hasattr(self, MAINNOTEBOOK_ATTR_NAME):
            return True
        if getattr(self, MAINNOTEBOOK_ATTR_NAME) is None:
            return True

        try:
            main_notebook = self.getMainNotebook()
            main_notebook.clear()
            main_notebook.Close()
            self.RemoveChild(main_notebook)
            main_notebook.Destroy()
            setattr(self, MAINNOTEBOOK_ATTR_NAME, None)
            self.Refresh()
            return True
        except:
            log_func.fatal(u'Error delete main notebook object')
        return False

    def addPage(self, page_panel, title, open_exists=False, default_page=-1):
        """
        Append page in notebook.

        :param page_panel: Panel object.
        :param title: New page title.
        :param open_exists: Allow to open a page with the same title?
        :param default_page: The index of the page to open by default.
            If -1, the current page to add opens.
        :return: True/False.
        """
        return self.getMainNotebook().addPage(page_panel=page_panel, title=title,
                                              open_exists=open_exists, default_page=default_page)

    def delPage(self, page_idx):
        """
        Delete page notebook.

        :param page_idx: Page index.
        """
        main_notebook = self.getMainNotebook()
        result = main_notebook.delPage(page_idx=page_idx)
        if main_notebook.GetPageCount() == 0:
            self.destroyMainNotebook()
        return result

    def clearPages(self):
        """
        Delete all pages.
        """
        main_notebook = self.getMainNotebook()
        result = main_notebook.clear()
        if main_notebook.GetPageCount() == 0:
            self.destroyMainNotebook()
        return result

    def openPageByTitle(self, title):
        """
        Open page notebook by page title.

        :param title: Page title.
        """
        return self.getMainNotebook().openPageByTitle(title=title)


def showMainForm(main_form_class):
    """
    Open main form.

    :param main_form_class: Main form class.
    :return: True/False.
    """
    frame = None
    try:
        frame = main_form_class(parent=None)
        app = global_func.getApplication()
        if app:
            app.SetTopWindow(frame)
        frame.init()
        frame.Show()
        return True
    except:
        if frame:
            frame.Destroy()
        log_func.fatal(u'Error show frame <%s>' % main_form_class.__name__)
    return False
