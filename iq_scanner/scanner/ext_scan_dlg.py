#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional scan management dialogs.
"""

import os
import os.path
import wx

from iq.util import log_func
from iq.util import file_ext_func
from iq.util import pdf_func
from iq.dialog import dlg_func
# from ic.std.utils import execfunc
# from ic.std.utils import pdffunc
from . import scanner_dlg_proto


__version__ = (0, 0, 0, 1)


class iqLoadSheetsDialog(scanner_dlg_proto.iqLoadSheetsDlgProto):
    """
    Dialog box for loading sheets into the scanner tray.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        scanner_dlg_proto.iqLoadSheetsDlgProto.__init__(self, *args, **kwargs)

        self.real_sheet = 60

    def setMaxSheets(self, max_sheets=60):
        """
        Set the maximum number of sheets to scan.

        :param max_sheets: The maximum number of sheets to scan.
        """
        self.sheets_spinCtrl.SetRange(1, max_sheets)
        self.sheets_spinCtrl.SetValue(max_sheets)

    def getSheets(self):
        """
        The number of sheets selected by the user for scanning.

        :return: The number of sheets selected by the user for scanning.
        """
        return self.real_sheet

    def onNextButtonClick(self, event):
        """
        The handler for the <Next> button.
        """
        self.real_sheet = self.sheets_spinCtrl.GetValue()
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        The handler for the <Cancel> button.
        """
        self.real_sheet = -1
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


class iqVerifyScanDialog(scanner_dlg_proto.iqVerifyScanDlgProto):
    """
    Dialog box for checking scan results.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        scanner_dlg_proto.iqVerifyScanDlgProto.__init__(self, *args, **kwargs)

        self.verify_filename = None

    def setVerifyFilename(self, filename):
        """
        Remember the file being checked.

        :param filename: The full name of the file to be scanned.
        """
        self.verify_filename = filename

    def onPreviewButtonClick(self, event):
        """
        Button handler <Preview ...>.
        """
        # execfunc.view_file_ext(self.verify_filename)
        file_ext_func.openFileAppDefault(self.verify_filename)
        event.Skip()

    def onReScanButtonClick(self, event):
        """
        The handler for the <Rescan> button.
        """
        self.EndModal(wx.ID_BACKWARD)
        event.Skip()

    def onNextButtonClick(self, event):
        """
        The handler for the <Next> button.
        """
        self.EndModal(wx.ID_OK)
        event.Skip()

    def onCancelButtonClick(self, event):
        """
        The handler for the <Cancel> button.
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()


def scan_glue_load_sheets(parent=None, max_sheets=60):
    """
    Determine the number of sheets to scan parts.

    :param parent: Parent window.
    :param max_sheets: The maximum number of sheets in the tray for scanning.
    :return: The number of sheets selected by the user for scanning.
         Or -1, if nothing is just selected or <Cancel> is pressed.
    """
    dlg = iqLoadSheetsDialog(parent=parent)
    dlg.setMaxSheets(max_sheets)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return dlg.getSheets()
    return -1


def scan_glue_verify(parent=None, verify_filename=None):
    """
    Procedure for checking part scan results.

    :param parent: Parent form.
    :param verify_filename: The full name of the file to be scanned.
    :return: True - the scan was successful. User Confirmed.
         False - Scan is canceled.
         None - Required to scan part. User Defined.
    """
    dlg = iqVerifyScanDialog(parent=parent)
    dlg.setVerifyFilename(verify_filename)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return True
    elif result == wx.ID_BACKWARD:
        return None
    return False


def scan_glue_mode(scan_manager, scan_filename, n_sheets, is_duplex=False, max_tray_sheets=60):
    """
    Starting the document gluing mode in parts.

    :param scan_manager: Scan manager.
    :param scan_filename: The name of the resulting scan file.
    :param n_sheets: Number of sheets.
    :param is_duplex: Duplex scanning?
    :param max_tray_sheets: The maximum number of sheets in the scanner tray.
    :return: True/False.
    """
    # The main cycle of scanning a document in parts and subsequent gluing
    n_part = 1
    scan_file_path, scan_file_ext = os.path.splitext(scan_filename)
    part_suffix = '_part%03d' % n_part
    new_scan_filename = scan_file_path + part_suffix + scan_file_ext
    sheets = scan_glue_load_sheets(None, min(max_tray_sheets, n_sheets))
    scan_sheet_count = sheets
    is_cancel = scan_sheet_count <= 0

    while (0 < scan_sheet_count <= n_sheets) or is_cancel:
        log_func.debug(u'Scan File <%s> Scan Sheets [%d]' % (new_scan_filename, sheets))
        # If duplex is used, then it is necessary to increase the number of pages
        scan_n_pages = sheets * 2 if is_duplex else sheets
        # Starting the scanning process
        scan_result = scan_manager.scanMulti(new_scan_filename, scan_n_pages)
        if scan_result and os.path.exists(new_scan_filename):
            verify_result = scan_glue_verify(None, new_scan_filename)
            if verify_result:
                n_part += 1
                part_suffix = '_part%03d' % n_part
                new_scan_filename = scan_file_path + part_suffix + scan_file_ext
                do_scan_sheet_count = min(max_tray_sheets, n_sheets-scan_sheet_count)
                if do_scan_sheet_count <= 0:
                    # All sheets are scanned.
                    break
                sheets = scan_glue_load_sheets(None, do_scan_sheet_count)
                if sheets <= 0:
                    # Clicked <Cancel>
                    is_cancel = True
                    break
                scan_sheet_count += sheets
            elif verify_result is None:
                scan_sheet_count -= sheets
                sheets = scan_glue_load_sheets(None, min(max_tray_sheets, n_sheets))
                if sheets <= 0:
                    # Clicked <Cancel>
                    is_cancel = True
                    break
                scan_sheet_count += sheets
            else:
                is_cancel = True
                log_func.warning(u'Scan to parts of file <%s> canceled' % new_scan_filename)
                break
        else:
            is_cancel = True
            log_func.warning(u'Error scanning file <%s>' % new_scan_filename)

    # Glue the scanned parts of the document
    if not is_cancel:
        part_pdf_filenames = [scan_file_path + ('_part%03d' % i_part) + scan_file_ext for i_part in range(1, n_part)]
        log_func.debug(u'Merge %d parts of scan %s to PDF file% s' % (n_part-1, part_pdf_filenames, scan_filename))
        # glue_result = pdf_func.glue_pdf_files(scan_filename, *part_pdf_filenames)
        glue_result = pdf_func.joinPDF(part_pdf_filenames, scan_filename)

        dlg_func.openMsgBox(u'SCAN',
                            u'Load documents in the scanner tray for later scanning')
        return glue_result
    else:
        log_func.warning(u'The mode of combining a scanned document in parts is canceled')

    return False
