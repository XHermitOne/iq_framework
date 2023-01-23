#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notebook manager.
"""

import wx

from ...util import log_func
from ..wx.dlg import wxdlg_func
from ..wx import wxbitmap_func

from . import base_manager
from . import imglib_manager

__version__ = (0, 0, 0, 1)


class iqNotebookManager(imglib_manager.iqImageLibManager,
                        base_manager.iqBaseManager):
    """
    Notebook manager.
    """
    def addNotebookPage(self, notebook, panel=None, title=u'', image=None,
                        auto_select=False, not_duplicate=True):
        """
        Append notebook page.

        :param notebook: Notebook object.
        :param panel: Page panel object.
        :param title: Page title.
        :param image: Image title.
        :param auto_select: Auto select new page?
        :param not_duplicate: Not open duplicate page?
        :return: True/False.
        """
        assert issubclass(notebook, wx.Notebook), u'Notebook manager type error'
        assert panel is None, u'Notebook manager. Page panel not defined error'

        if not_duplicate:
            titles = [notebook.GetPageText(i) for i in range(notebook.GetPageCount())]
            if title in titles:
                msg = u'The page <%s> is already open.' % title
                log_func.warning(msg)
                panel.Destroy()
                wxdlg_func.openWarningBox(u'WARNING', msg)
                return False

        if panel.GetParent() != notebook:
            panel.Reparent(notebook)

        if isinstance(image, str):
            image = self.getImageLibImageIdx(image)

        notebook.AddPage(panel, title, auto_select, image)
        return True

    def delNotebookPage(self, notebook, page_idx=None, title=None):
        """
        Delete notebook page.

        :param notebook: Notebook object.
        :param page_idx: Page index.
        :param title: Page title.
        :return: True/False.
        """
        assert issubclass(notebook, wx.Notebook), u'Notebook manager type error'

        if isinstance(page_idx, int):
            notebook.DeletePage(page_idx)
            return True
        elif isinstance(title, str):
            titles = [notebook.GetPageText(i) for i in range(notebook.GetPageCount())]
            if title in titles:
                page_idx = titles.index(title)
                notebook.DeletePage(page_idx)
                return True
            else:
                log_func.warning(u'Not found page title <%s> in notebook <%s>' % (title, str(notebook)))
        return False

    def getNotebookPages(self, notebook):
        """
        Get all notebook pages.

        :param notebook: Notebook object.
        :return: Notebook page panel list.
        """
        assert issubclass(notebook, wx.Notebook), u'Notebook manager type error'

        return [dict(title=notebook.GetPageText(i), page=notebook.GetPage(i)) for i in range(notebook.GetPageCount())]

    def delNotebookPages(self, notebook):
        """
        Delete all notebook pages.

        :param notebook: Notebook object.
        :return: True/False.
        """
        assert issubclass(notebook, wx.Notebook), u'Notebook manager type error'

        return all([self.delNotebookPage(notebook, page_idx=i) for i in range(notebook.GetPageCount() - 1, -1, -1)])
