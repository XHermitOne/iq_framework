#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Dialog form for selecting a printer installed in the system.
"""

import sys
import wx

from . import printer_dlg_proto

from iq.util import log_func
from iq.util import printer_func

from .. import wxbitmap_func

__version__ = (0, 2, 2, 1)


class iqChoicePrinterDlg(printer_dlg_proto.iqChoicePrinterDlgProto):
    """
    Dialog form for selecting a printer installed in the system.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        printer_dlg_proto.iqChoicePrinterDlgProto.__init__(self, *args, **kwargs)
        self.SetIcon(icon=wx.Icon(wxbitmap_func.createIconBitmap('fatcow/printer')))

        self.image_list = None
        self.printer_idx = None
        self.default_printer_idx = None
        self.network_printer_idx = None
        self.printers_info = None

        self.selected_printer_info = None
        self.init()

    def init(self):
        """
        Initializing the dialog box.
        """
        self.initImages()
        self.initPrinters()

    def initImages(self):
        """
        Images initializing.
        """
        self.image_list = wx.ImageList(16, 16)
        bmp = wxbitmap_func.createIconBitmap('fatcow/printer')
        self.printer_idx = self.image_list.Add(bmp)
        bmp = wxbitmap_func.createIconBitmap('fatcow/printer_empty')
        self.default_printer_idx = self.image_list.Add(bmp)
        bmp = wxbitmap_func.createIconBitmap('fatcow/printer_network')
        self.network_printer_idx = self.image_list.Add(bmp)
        self.printer_listCtrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

    def initPrinters(self):
        """
        Initializing the printer list.
        """
        self.printers_info = printer_func.getPrintersInfo()

        self.printer_listCtrl.DeleteAllItems()
        default_idx = -1
        for i, info in enumerate(self.printers_info):
            is_default = info[0]
            printer_name = info[1]
            is_network = info[2]

            if is_default:
                default_idx = i

            if is_default:
                img_idx = self.default_printer_idx
            elif is_network:
                img_idx = self.network_printer_idx
            else:
                img_idx = self.printer_idx
            self.printer_listCtrl.InsertImageStringItem(sys.maxsize, printer_name, img_idx)

        # Select the default printer
        if default_idx >= 0:
            self.printer_listCtrl.Select(default_idx)

    def onOkButtonClick(self, event):
        """
        Handler of the <OK> button.
        """
        idx = self.printer_listCtrl.GetFirstSelected()
        if idx == -1:
            # If no printer is selected, then we assume that the default printer is selected
            find_default = [info for info in self.printers_info if info[0]]
            self.selected_printer_info = find_default[0] if find_default else None
        else:
            self.selected_printer_info = self.printers_info[idx]
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        Handler of the <Cancel> button
        """
        self.selected_printer_info = None
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def getSelectedPrinterInfo(self):
        """
        Information about the selected printer in the form of a dictionary format:
            {
                'name': 'Printer name',
                'default': True - The printer is the default printer.
                           False - A regular printer
                'network': True - The printer is a network printer.
                           False - Local printer
            }
        """
        if self.selected_printer_info:
            return dict(name=self.selected_printer_info[1],
                        default=self.selected_printer_info[0],
                        network=self.selected_printer_info[2])
        return None


def choicePrinterDlg(parent=None):
    """
    Select the printer installed in the system using the dialog box.

    :param parent: Parent window.
    :return: Information about the selected printer in the form of a dictionary format:
            {
                'name': 'Printer name',
                'default': True - The printer is the default printer.
                           False - A regular printer
                'network': True - The printer is a network printer.
                           False - Local printer
            }
        Or None if <Cancel> pressed.
    """
    ret = None
    dlg = None
    try:
        if parent is None:
            app = wx.GetApp()
            parent = app.GetTopWindow()

        dlg = iqChoicePrinterDlg(parent=parent)
        result = dlg.ShowModal()

        if result == wx.ID_OK:
            ret = dlg.getSelectedPrinterInfo()

        dlg.Destroy()
    except:
        if dlg:
            dlg.Destroy()
        log_func.fatal(u'Error choice printer dialog')

    return ret
