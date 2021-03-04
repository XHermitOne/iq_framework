#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scan Management Manager.

Used libraries:

python-sane - Scanner Management Library.

Install:
************************************
sudo apt-get install python-sane
************************************

reportlab - Library for generating PDF files.
Used to scan immediately
multiple sheets in one document.

Install:
***************************************
sudo apt-get install python-reportlab
***************************************
"""

import traceback
import os
import os.path
import sane
import wx
from reportlab.pdfgen import canvas

from iq.util import log_func
from iq.util import file_func
from iq.util import global_func
from iq.dialog import dlg_func

from . import config

from . import ext_scan_dlg

__version__ = (0, 0, 0, 1)

# Scan modes
GREY_SCAN_MODE = 'Grey'
COLOR_SCAN_MODE = 'Color'
LINEART_SCAN_MODE = 'Lineart'
HALFTONE_SCAN_MODE = 'Halftone'
SCAN_MODES = (LINEART_SCAN_MODE, HALFTONE_SCAN_MODE,
              GREY_SCAN_MODE, COLOR_SCAN_MODE)

# Default PDF file name for multi-page scanning
DEFAULT_PDF_SCAN_FILENAME = os.path.join(file_func.getHomePath(),
                                         global_func.getProjectName(),
                                         'scan.pdf')

# Seurces
FLATBED_SOURCE = 'Flatbed'
FRONT_SOURCE = 'ADF Front'
BACK_SOURCE = 'ADF Back'
DUPLEX_SOURCE = 'ADF Duplex'
SCAN_SOURCES = (FLATBED_SOURCE, FRONT_SOURCE, BACK_SOURCE, DUPLEX_SOURCE)

# Page sizes
A4_PORTRAIT_PAGE_SIZE = (210.0, 297.0)
A4_LANDSCAPE_PAGE_SIZE = (297.0, 210.0)
A3_PORTRAIT_PAGE_SIZE = (297.0, 420.0)
A3_LANDSCAPE_PAGE_SIZE = (420.0, 297.0)
SCAN_PAGE_SIZES = (A4_PORTRAIT_PAGE_SIZE, A3_PORTRAIT_PAGE_SIZE)

# Supported Scan File Types
PDF_FILE_TYPE = 'pdf'
JPEG_FILE_TYPE = 'jpeg'
JPG_FILE_TYPE = 'jpg'
TIF_FILE_TYPE = 'tif'
BMP_FILE_TYPE = 'bmp'
SCAN_FILE_TYPES = (PDF_FILE_TYPE, JPEG_FILE_TYPE, JPG_FILE_TYPE,
                   TIF_FILE_TYPE, BMP_FILE_TYPE)

# Default depth
DEFAULT_DEPTH = 8

MULTISCAN_PAGE_FILENAME = os.path.join(file_func.getHomePath(),
                                       global_func.getProjectName(),
                                       'page%d.jpg')

# How to set scan options
# ATTENTION! This order is important because mutually controlled options
SCAN_OPTIONS_ORDER = ('source', 'mode', 'depth',
                      'page_width', 'page_height',
                      'tl_x', 'tl_y', 'br_x', 'br_y')


# Scanned page size in dots by default
# Values determined experimentally
DEFAULT_IMAGE_PAGE_SIZE = (4961, 7016)

# Error message when a document is jammed in the feed tray
DOC_FEEDER_JAMMED_ERR = 'error: Document feeder jammed'


class iqScanManager(object):
    """
    Scan Management Manager.
    """
    def init(self):
        """
        Initialization.
        """
        self.sane_ver = sane.init()
        self.devices = sane.get_devices()

        # Задублированные опции сканирования
        self.options = dict()

    def initOptionsOrder(self):
        """
        Initialization.
        How to set scan options.
        ATTENTION! This order is important because options mutually controlled

        :return: True/False
        """
        options = self.getScanOptions()
        if options is None:
            return False

        global SCAN_OPTIONS_ORDER
        SCAN_OPTIONS_ORDER = tuple([option[1].replace('-', '_') for option in options])
        return True

    def getSaneVersion(self):
        """
        Sane package version.
        It is determined after initialization.

        :return: Sane package version.
        """
        if hasattr(self, 'sane_ver'):
            return self.sane_ver
        return None

    def getDeviceNames(self):
        """
        List of names of available scanners.

        :return: List of names of available scanners.
        """
        if hasattr(self, 'devices'):
            return tuple([device[0] for device in self.devices])
        return tuple()

    def isDevices(self):
        """
        Are scanners available?

        :return: True/False.
        """
        if hasattr(self, 'devices'):
            return bool(self.devices)
        return False

    def open(self, device_name):
        """
        Open scan device.

        :param device_name: The name of the scan device.
        :return: Scan device object.
        """
        try:
            self.scan_device_obj = sane.open(device_name)
            self.initOptionsOrder()
        except:
            log_func.fatal(u'Error opening scan device <%s>' % device_name)
            self.scan_device_obj = None
        return self.scan_device_obj

    def close(self):
        """
        Close the scan device.

        :return: True/False
        """
        try:
            self.scan_device_obj.close()
            self.scan_device_obj = None
            return True
        except AttributeError:
            log_func.fatal(u'Scanning device is not open.')

        return False

    def getScanOptions(self):
        """
        Scan options.

        :return: Scan options.
        """
        try:
            return self.scan_device_obj.get_options()
        except AttributeError:
            log_func.fatal(u'Scanning device is not open.')
            return None

    def getScanOptionsDict(self):
        """
        Scan options in the form of a dictionary.

        :return: Scan options in the form of a dictionary.
        """
        options = self.getScanOptions()
        if options:
            return dict([(option[1], option) for option in options])
        return dict()

    def setScanOptions(self, **options):
        """
        Set Scan Options

        :param options: Options.
        :return: True/False.
        """
        try:
            global SCAN_OPTIONS_ORDER
            for option_name in SCAN_OPTIONS_ORDER:
                if option_name in options:
                    option_val = options[option_name]
                    try:
                        setattr(self.scan_device_obj, option_name, option_val)
                        log_func.info(u'Set scan option <%s>. Value <%s>' % (option_name, option_val))
                        # Remember the option values set.
                        # It may be that we install the options in the device,
                        # but for some reason they are not set :-(
                        self.options[option_name] = option_val
                    except:
                        log_func.warning(u'Error setting scan option <%s>. Value <%s>' % (option_name, option_val))
            return True
        except:
            log_func.fatal(u'Error setting scan options')
        return False

    def getScanParameters(self):
        """
        Scan Settings.

        :return: Scan Settings
        """
        try:
            return self.scan_device_obj.get_parameters()
        except AttributeError:
            log_func.fatal(u'Scanning device is not open')
            return None

    def getMaxSheets(self):
        """
        The maximum number of sheets placed in the scanner tray.

        :return: The maximum number of sheets placed in the scanner tray.
        """
        return config.get_glob_var('DEFAULT_SCANNER_MAX_SHEETS')

    def isDuplexOption(self):
        """
        Check if duplex option is enabled.

        :return: True/False.
        """
        options = self.options
        if options:
            try:
                if 'source' in options:
                    # Check on the exposed options
                    scan_source_opt = options['source']
                else:
                    # Check on device options
                    dev_options = self.getScanOptionsDict()
                    scan_source = dev_options['source']
                    scan_source_opt = scan_source[8][scan_source[4]]
                return 'Duplex' in scan_source_opt
            except:
                log_func.fatal(u'Definition error on duplex scan options')
        else:
            log_func.warning(u'No scan options defined. Duplex is disabled by default')
        return False

    def setDuplexOption(self, is_duplex=False):
        """
        On/off. duplex option.

        :param is_duplex: A sign of 2-sided scanning.
        """
        src = DUPLEX_SOURCE if is_duplex else FRONT_SOURCE
        return self.setScanOptions(source=src)

    def startScan(self):
        """
        Start scan.

        :return: True/False.
        """
        try:
            self.scan_device_obj.start()
            return True
        except:
            log_func.fatal(u'Scan Start Error')
        return False

    def scan(self, scan_filename=None):
        """
        Scan a document and save it to a file.

        :param scan_filename: The name of the scan file.
            If the file name is not specified, then scanning and
            returns the PIL.Image object.
        :return: Scan file name or PIL.Image object.
            None - in case of an error.
        """
        try:
            image = self.scan_device_obj.snap()

            if scan_filename:
                image.save(scan_filename)
                return scan_filename
            # Do not save to file. We need a scan image object.
            return image
        except:
            log_func.fatal(u'Scan error')

            # So we display scanning errors
            trace_txt = traceback.format_exc()
            if DOC_FEEDER_JAMMED_ERR in trace_txt:
                self.showScanErrorMsg(u'Document misfeed in the paper feed tray')

        return None

    def scanSingle(self, scan_filename=None):
        """
        Single Page Scan
        If incl. DUPLEX and off-page scanning,
        then you need to scan 1 sheet from 2 sides.

        :param scan_filename: The name of the scan file.
            If the file name is not specified, then scanning and
            returns the PIL.Image object.
        :return: True/False
        """
        if self.isDuplexOption():
            # If on DUPLEX and multi-page scanning is turned off,
            # then you need to scan 1 sheet from 2 sides
            log_func.debug(u'Duplex scan')
            return self.scanMulti(scan_filename, 2)

        log_func.debug(u'Single-sided scanning')
        self.startScan()
        scan_obj = self.scan(scan_filename)
        return scan_obj is not None

    def _imageDrawCanvas(self, image, canvas, n, page_size=DEFAULT_IMAGE_PAGE_SIZE):
        """
        Output the scanned page to a PDF canvas.

        :param image: Image object of the scanned page.
        :param canvas: PDF canvas object.
        :param n: Page number.
        :param page_size: Page size in dots,
             to which all scanned pages will be brought.
        :return: True/False.
        """
        if image:
            img_filename = os.path.join(file_func.getHomePath(),
                                        MULTISCAN_PAGE_FILENAME % n)
            width, height = page_size
            image = image.resize((int(width), int(height)))
            image.save(img_filename)
            canvas.drawImage(img_filename, 0, 0)
            canvas.showPage()
            return True
        else:
            log_func.warning(u'Error writing scanned page [%d] to PDF file' % n)
        return False

    def scanMulti(self, scan_filename=None, n_page=-1):
        """
        Multipage scanning.

        :param scan_filename: The name of the scan file.
            Multipage scanning is done in a PDF file.
            The function checks for the file name extension.
            If the file name is not specified, then the default file name is taken.
            ~ / .icscanner / scan.pdf
        :param n_page: The number of scanned pages.
            If -1, then all possible pages are scanned.
        :return: True/False.
        """
        if scan_filename is None:
            scan_filename = DEFAULT_PDF_SCAN_FILENAME

        file_ext = os.path.splitext(scan_filename)[1]
        if file_ext.lower() != '.pdf':
            log_func.warning(u'Incorrect file type for saving multi-page scan result')
            return False

        try:
            scan = self.scan_device_obj.multi_scan()

            scan_canvas = canvas.Canvas(scan_filename, pagesize=DEFAULT_IMAGE_PAGE_SIZE)

            if n_page < 0:
                # Scan all possible pages
                is_stop_scan = False
                i_page = 0
                while not is_stop_scan:
                    image = None
                    try:
                        image = scan.next()
                    except StopIteration:
                        is_stop_scan = True
                        continue

                    result = self._imageDrawCanvas(image, scan_canvas, i_page)
                    if not result:
                        continue

                    i_page += 1
            else:
                # Scan specific number of pages
                for i_page in range(n_page):
                    image = None
                    try:
                        image = scan.next()
                    except StopIteration:
                        continue
                    result = self._imageDrawCanvas(image, scan_canvas, i_page)
                    if not result:
                        continue
            # Save PDF Canvas
            scan_canvas.save()
            return True
        except:
            log_func.fatal(u'Multipage Scan Error')

            trace_txt = traceback.format_exc()
            if DOC_FEEDER_JAMMED_ERR in trace_txt:
                self.showScanErrorMsg(u'Document misfeed in the paper feed tray')

        return False

    def showScanErrorMsg(self, err_msg=u''):
        """
        Function for displaying scan errors.

        :param err_msg: The error message.
        """
        log_func.warning(u'SCAN ERROR. %s' % err_msg)

        try:
            app = wx.GetApp()
            if not app:
                app = wx.PySimpleApp()
                dlg_func.openErrBox(u'SCAN ERROR', err_msg, parent=None)
                app.MainLoop()
            else:
                dlg_func.openErrBox(u'SCAN ERROR', err_msg, parent=app.GetTopWindow())
        except:
            # If we do not display an error message,
            # the scanning process should not stop
            log_func.fatal(u'Error in function <showScanErrorMsg> of scan manager')

    def scanPack(self, scan_filenames=()):
        """
        Scan documents in batch mode and save them to files.

        :param scan_filenames: Scan file names with the number of sheets
            and a sign of 2-sided scanning.
            For example:
                ('D:/tmp/scan001', 3, True), ('D:/tmp/scan002', 1, False), ('D:/tmp/scn003', 2, True), ...
        :return: List of scan file names. None - in case of an error.
        """
        result = list()
        # Scanned Sheet Counter
        tray_sheet_count = 0
        # Tray volume in sheets
        max_sheets = self.getMaxSheets()

        # In batch mode, do not use the dialog box
        # But in the case of gluing the document in parts, the dialog boxes are used
        # Dialog Box Application Object
        wx_app = None

        for scan_filename, n_pages, is_duplex in scan_filenames:
            tray_sheet_count += n_pages if not is_duplex else n_pages/2

            if tray_sheet_count <= max_sheets:
                # Until the scan counter has exceeded the tray size limit,
                # then continue the usual scan
                scan_result = self.scanPackPart(scan_filename, n_pages, is_duplex)
                result.append(scan_filename if scan_result and os.path.exists(scan_filename) else None)
            else:
                log_func.debug(u'Enabling document scan mode <%s> piecemeal. Number of pages [%d] Current counter %d. ' % (scan_filename, n_pages, tray_sheet_count))
                if wx_app is None:
                    wx_app = wx.PySimpleApp()

                    locale = wx.Locale()
                    locale.Init(wx.LANGUAGE_RUSSIAN)

                # If the tray runs out of paper, you need to start the process of gluing the last document
                glue_result = self.scanGlue(scan_filename, n_pages, is_duplex)
                result.append(scan_filename if glue_result and os.path.exists(scan_filename) else None)

                # ATTENTION! After a successfully scanned large document,
                # reset the counter of scanned sheets
                tray_sheet_count = 0

        # ATTENTION! Because Since the interaction is built on modal dialogs,
        # MainLoop does not need to be done otherwise
        # the main application freezes
        # if wx_app:
        #    wx_app.MainLoop()

        return result

    def scanPackPart(self, scan_filename, n_pages, is_duplex):
        """
        Scan one part of the package.

        :param scan_filename: The name of the resulting scan file.
        :param n_pages: Number of sheets.
        :param is_duplex: Duplex scanning?
        :return: True/False.
        """
        # On/off. 2-sided scanning
        self.setDuplexOption(is_duplex)
        if n_pages == 1:
            scan_result = self.scanSingle(scan_filename)
            return scan_result
        elif n_pages > 1:
            scan_result = self.scanMulti(scan_filename, n_pages)
            return scan_result
        else:
            log_func.warning(u'Invalid page count <%s> batch scan' % n_pages)
        return False

    def scanGlue(self, scan_filename, n_pages, is_duplex):
        """
        Starting the document gluing mode from parts.

        :param scan_filename: The name of the resulting scan file.
        :param n_pages: Number of pages.
        :param is_duplex: Duplex scanning?
        :return: True/False.
        """
        # On/off. 2-sided scanning
        self.setDuplexOption(is_duplex)
        n_sheets = n_pages/2 if is_duplex else n_pages
        return ext_scan_dlg.scan_glue_mode(self, scan_filename, n_sheets, is_duplex,
                                           self.getMaxSheets())


def test():
    """
    Test function.
    """
    scan_manager = iqScanManager()
    scan_manager.init()
    devices = scan_manager.getDeviceNames()
    print(devices)

    scan_manager.open(devices[0])
    scan_manager.startScan()
    scan_manager.scan()
    scan_manager.close()

    scan_manager.open(devices[0])
    scan_manager.startScan()
    scan_manager.scanMulti('test.pdf')
    scan_manager.close()


if __name__ == '__main__':
    test()
