#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Help editor dialog.
"""

import os.path
import wx

try:
    from . import help_editor_dlg
except:
    import help_editor_dlg

from ... import global_data
from ...util import file_func
from ...util import log_func
from ...util import file_ext_func
from ...util import pdf_func
from ...engine.wx import wxbitmap_func

from ...engine.wx import stored_wx_form_manager

__version__ = (0, 0, 0, 1)


class iqHelpEditorDialog(help_editor_dlg.iqHelpEditorDialogProto,
                         stored_wx_form_manager.iqStoredWxFormsManager):
    """
    Help editor dialog.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        help_editor_dlg.iqHelpEditorDialogProto.__init__(self, *args, **kwargs)
        bmp = wxbitmap_func.createIconBitmap('fatcow/help')
        if bmp:
            self.SetIcon(icon=wx.Icon(bmp))

        self.help_name2path = dict()

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
        Init controls on form.
        """
        str_version = 'iqFramework %s' % '.'.join([str(sign) for sign in global_data.VERSION])
        self.version_staticText.SetLabel(str_version)

        # Append help buttons
        help_path = file_func.getFrameworkHelpPath()
        help_list_paths = file_func.getDirectoryPaths(help_path) + file_func.getFilesByMask(os.path.join(help_path, '*.pdf'))
        for hlp_path in help_list_paths:
            label = os.path.basename(hlp_path)
            if os.path.isfile(hlp_path):
                self.help_name2path[label] = hlp_path
            elif os.path.isdir(hlp_path):
                self.help_name2path[label] = file_func.findPathByMask(find_mask='index.html', root_path=hlp_path)
            button = wx.Button(parent=self.button_scrolledWindow, label=label)
            if file_func.getFilenameExt(hlp_path) == pdf_func.PDF_FILENAME_EXT:
                bmp = wxbitmap_func.createIconBitmap('fatcow/file_extension_pdf')
            else:
                bmp = wxbitmap_func.createIconBitmap('fatcow/help')
            button.SetBitmap(bmp)
            self.button_scrolledWindow.GetSizer().Add(button, 0, wx.ALL | wx.EXPAND, 5)
            button.Bind(wx.EVT_BUTTON, self.onHelpButtonClick)

        self.Layout()

    def onHelpButtonClick(self, event):
        """
        Help button click handler.
        """
        help_name = event.GetEventObject().GetLabel()
        help_filename = self.help_name2path.get(help_name, None)
        if help_filename:
            log_func.info(u'Open help file name <%s : %s>' % (help_name, help_filename))
            file_ext_func.openFileAppDefault(filename=help_filename)
        self.EndModal(wx.ID_OK)
        event.Skip()


def openHelpEditorDlg(parent=None):
    """
    Open help editor dialog.

    :param parent: Parent form.
    :return: True/False
    """
    dlg = None
    try:
        dlg = iqHelpEditorDialog(parent=parent)
        dlg.init()
        result = dlg.ShowModal() == wx.ID_OK
        dlg.saveCustomProperties()
        dlg.Destroy()
        return result
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error open help editor dialog')
    return False


def helpEditor():
    """
    Help editor.

    :return:
    """
    app = wx.App()
    result = openHelpEditorDlg()
    app.MainLoop()
    return result


if __name__ == '__main__':
    helpEditor()
