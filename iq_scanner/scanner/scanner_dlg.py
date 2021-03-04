#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scan control dialog box.
"""

import os
import os.path
import shutil
import wx

from iq.util import log_func
from iq.util import ini_func
from iq.util import file_func
from iq.util import exec_func
from iq.util import global_func
from iq.dialog import dlg_func

from . import config
from . import scanner_dlg_proto
from . import scan_manager

__version__ = (0, 0, 0, 1)


class iqScanOptions:
    """
    Scan options management class.
    """
    def __init__(self):
        """
        Constructor.
        """
        self.opt_filename = None

        self.scanner = None
        self.scan_source = None
        self.scan_mode = None
        self.is_multi_scan = False
        self.is_preview = False
        self.page_size = None
        self.scan_area = None
        self.scan_dir = None
        self.scan_filename = None
        self.scan_filetype = None
        self.depth = None
        self.ext_scan_cmd = None

        self.loadOptions()

    def genOptFileName(self):
        """
        Generating a parameter file name.
        """
        if self.opt_filename is None:
            self.opt_filename = config.DEFAULT_OPTIONS_FILENAME
        return self.opt_filename

    def loadOptions(self, filename=None):
        """
        Load scan settings from the configuration file.

        :param filename: The name of the parameter file.
        """
        if filename is None:
            filename = self.genOptFileName()

        ini_dict = ini_func.INI2Dict(filename)
        if ini_dict:
            self.setExtOptions(**ini_dict['SCAN_OPTIONS'])
        else:
            log_func.warning(u'Scan settings not loaded from configuration file')

    def saveOptions(self, filename=None):
        """
        Write scan settings to the configuration file.

        :param filename: The name of the parameter file.
        """
        if filename is None:
            filename = self.genOptFileName()

        ini_dict = dict()
        ini_dict['SCAN_OPTIONS'] = dict()
        ini_dict['SCAN_OPTIONS']['scanner'] = self.scanner
        ini_dict['SCAN_OPTIONS']['source'] = self.scan_source
        ini_dict['SCAN_OPTIONS']['mode'] = self.scan_mode
        ini_dict['SCAN_OPTIONS']['is_multi_scan'] = self.is_multi_scan
        ini_dict['SCAN_OPTIONS']['is_preview'] = self.is_preview
        ini_dict['SCAN_OPTIONS']['page-size'] = self.page_size
        ini_dict['SCAN_OPTIONS']['area'] = self.scan_area
        ini_dict['SCAN_OPTIONS']['scan_dir'] = self.scan_dir
        ini_dict['SCAN_OPTIONS']['file_name'] = self.scan_filename
        ini_dict['SCAN_OPTIONS']['file_type'] = self.scan_filetype
        ini_dict['SCAN_OPTIONS']['depth'] = self.depth
        ini_dict['SCAN_OPTIONS']['ext_scan_cmd'] = self.ext_scan_cmd

        ini_func.Dict2INI(ini_dict, filename)
        
    def setExtOptions(self, **options):
        """
        Set advanced options.

        :param options: Dictionary of options.
        """
        log_func.debug(u'Scan options: %s' % options)
        if options:
            if 'scanner' in options:
                self.scanner = options.get('scanner', None)
            if 'source' in options:
                self.scan_source = options.get('source', None)
            if 'mode' in options:
                self.scan_mode = options.get('mode', None)
            if 'is_multi_scan' in options:
                self.is_multi_scan = options.get('is_multi_scan', None)
            if 'is_preview' in options:
                self.is_preview = options.get('is_preview', None)
            if 'page_size' in options:
                self.page_size = options.get('page_size', None)
            if 'area' in options:
                self.scan_area = options.get('area', None)
            if 'scan_dir' in options:
                self.scan_dir = options.get('scan_dir', None)
            if 'file_name' in options:
                self.scan_filename = options.get('file_name', None)
            if 'file_type' in options:
                self.scan_filetype = options.get('file_type', None)
            if 'depth' in options:
                self.depth = options.get('depth', None)
            if 'ext_scan_cmd' in options:
                self.ext_scan_cmd = options.get('ext_scan_cmd', None)
        else:
            log_func.warning(u'Undefined scan options for set')


class iqScanAdministrator(iqScanOptions):
    """
    Intermediate class manager scan manager.
    """
    def __init__(self):
        """
        Constructor.
        """
        iqScanOptions.__init__(self)

        self.scan_manager = scan_manager.iqScanManager()
        self.scan_manager.init()

    def getScanManager(self):
        """
        Scan manager.

        :return: Scan manager object.
        """
        if hasattr(self, 'scan_manger'):
            return self.scan_manager
        return None

    def runScan(self):
        """
        Start the scanning process according to the set parameters.

        :return: True/False
        """
        try:
            return self._runScan()
        except:
            log_func.fatal(u'Scan error')
        return False
            
    def _runScan(self):
        """
        Start the scanning process according to the set parameters.

        :return: True/False
        """
        if self.scan_manager is None:
            log_func.warning(u'Scan manager not defined')
            return False
        if self.scanner is None:
            log_func.warning(u'Undefined scan device')
            return False

        self.scan_manager.init()

        self.scan_manager.open(self.scanner)

        # Set options
        options = dict()
        if self.scan_source:
            options['source'] = self.scan_source
        if self.scan_mode:
            options['mode'] = self.scan_mode
        if self.depth:
            options['depth'] = self.depth
        if self.page_size:
            options['page_width'] = self.page_size[0]
            options['page_height'] = self.page_size[1]
        else:
            # If you do not determine the page size,
            # the edge of the scan will be cropped.
            # Default A4 portrait orientation
            options['page_width'] = 210.0
            options['page_height'] = 297.0
        if self.scan_area:
            options['tl_x'] = self.scan_area[0]
            options['tl_y'] = self.scan_area[1]
        if self.scan_area and self.page_size:
            options['br_x'] = self.page_size[0] - self.scan_area[2]
            options['br_y'] = self.page_size[1] - self.scan_area[3]
        else:
            # If you do not determine the page size,
            # the edge of the scan will be cropped.
            # Default A4 portrait orientation
            options['br_x'] = 210.0
            options['br_y'] = 297.0
            
        self.scan_manager.setScanOptions(**options)

        # Defining a scan file name
        scan_filename = os.path.join(file_func.getHomePath(),
                                     global_func.getProjectName(),
                                     self.scan_filename + '.' + self.scan_filetype) if self.scan_filename else config.DEFAULT_SCAN_FILENAME
        if os.path.exists(scan_filename):
            # Delete old scan file
            try:
                os.remove(scan_filename)
                log_func.info(u'Delete file <%s>' % scan_filename)
            except OSError:
                log_func.fatal(u'Error delete file <%s>' % scan_filename)
        log_func.debug(u'Scan to file <%s>' % scan_filename)

        try:
            if not self.is_multi_scan:
                result = self.scan_manager.scanSingle(scan_filename)
            else:
                result = self.scan_manager.scanMulti(scan_filename)

            if not result:
                dlg_func.openErrBox(u'ERROR',
                                    u'Scan error. Check the sheets in the scanner tray')
                return False

            if self.scan_dir:
                self.copyToScanDir(scan_filename, self.scan_dir)

            if self.is_preview:
                self.previewScanFile(scan_filename)
            return True
        except:
            log_func.fatal(u'Scan error')
        return False

    def pages2sheets(self, page_count, is_duplex=False):
        """
        Translation of the number of pages in the number of sheets.

        :param page_count: Number of pages.
        :param is_duplex: Duplex scanning?
        :return: Number of sheets.
        """
        if not is_duplex:
            # If there is no two-sided scanning,
            # then the number of pages matches the number of sheets
            return page_count
        else:
            # For duplex scanning:
            return page_count / 2

    def runScanPack(self, *scan_filenames):
        """
        Start the scanning process in batch mode,
        according to the parameters set.

        :param scan_filenames: Scan file names with the number of sheets
            and a sign of 2-sided scanning.
            For example:
                (scan001, 3, True), (scan002, 1, False), (scn003, 2, True), ...
        :return: True/False
        """
        if self.scan_manager is None:
            log_func.warning(u'Scan Manager not defined')
            return False
        if self.scanner is None:
            log_func.warning(u'Undefined scan device')
            return False

        self.scan_manager.init()
        self.scan_manager.open(self.scanner)

        options = dict()
        if self.scan_source:
            options['source'] = self.scan_source
        if self.scan_mode:
            options['mode'] = self.scan_mode
        if self.depth:
            options['depth'] = self.depth
        if self.page_size:
            options['page_width'] = self.page_size[0]
            options['page_height'] = self.page_size[1]
        else:
            options['page_width'] = 210.0
            options['page_height'] = 297.0
        if self.scan_area:
            options['tl_x'] = self.scan_area[0]
            options['tl_y'] = self.scan_area[1]
        if self.scan_area and self.page_size:
            options['br_x'] = self.page_size[0] - self.scan_area[2]
            options['br_y'] = self.page_size[1] - self.scan_area[3]
        else:
            options['br_x'] = 210.0
            options['br_y'] = 297.0
            
        self.scan_manager.setScanOptions(**options)

        scans = [(os.path.join(file_func.getHomePath(),
                               global_func.getProjectName(),
                               scan_filename + '.' + self.scan_filetype) if scan_filename else config.DEFAULT_SCAN_FILENAME,
                  int(n_pages), bool(is_duplex)) for scan_filename, n_pages, is_duplex in scan_filenames]
        for scan_filename, n_pages, is_duplex in scans:
            full_scan_filename = os.path.join(os.environ.get('HOME', '/home/user'),
                                              global_func.getProjectName(),
                                              scan_filename)
            if os.path.exists(full_scan_filename):
                try:
                    os.remove(full_scan_filename)
                    log_func.info(u'Previously scanned file deleted <%s>' % full_scan_filename)
                except OSError:
                    log_func.fatal(u'Error delete file <%s>' % full_scan_filename)

        try:
            scan_filenames = self.scan_manager.scanPack(scan_filenames=scans)

            # Transfer scanned files to the resulting folder
            if self.scan_dir and os.path.exists(self.scan_dir):
                for scan_filename in scan_filenames:
                    if scan_filename and os.path.exists(scan_filename):
                        log_func.debug(u'File transfer <%s> to the resulting folder <%s>' % (scan_filename, self.scan_dir))
                        self.copyToScanDir(scan_filename, self.scan_dir)
                    else:
                        log_func.warning(u'Result scan file not defined')
            else:
                log_func.warning(u'Result scan folder not defined')
                        
            return True
        except:
            log_func.fatal(u'Scan Error in Batch Processing')

        return False

    def copyToScanDir(self, scan_filename=None, scan_dir=None, bDoRemove=True):
        """
        Copy file - the result of scanning to a folder.

        :param scan_filename: The resulting scan file.
            If not specified, then the default file is taken.
        :param scan_dir: Folder scan.
        :param bDoRemove: Transfer file?
        :return: True/False
        """
        if scan_filename is None:
            scan_filename = config.DEFAULT_SCAN_FILENAME

        if scan_dir is None:
            scan_dir = self.scan_dir

        if not os.path.exists(scan_filename):
            log_func.warning(u'Scan file does not exist <%s>' % scan_filename)
            return False

        if scan_dir:
            if not os.path.exists(scan_dir):
                try:
                    os.makedirs(scan_dir)
                    log_func.info(u'Scan folder created <%s>' % scan_dir)
                except OSError:
                    log_func.fatal(u'Error creating scan folder <%s>' % scan_dir)
                    return False

            new_filename = os.path.join(scan_dir,
                                        os.path.basename(scan_filename))
            if scan_filename != new_filename:
                shutil.copyfile(scan_filename, new_filename)
                log_func.info(u'Copy file <%s> to folder <%s>' % (scan_filename, scan_dir))
                if bDoRemove:
                    try:
                        os.remove(scan_filename)
                        log_func.info(u'Delete file <%s>' % scan_filename)
                    except:
                        log_func.fatal(u'Error delete file <%s>' % scan_filename)
            return True
        else:
            log_func.warning(u'Scan folder not defined')
        return False

    def runExtScan(self):
        """
        Launch an external scan tool.

        :return: True/False.
        """
        if self.ext_scan_cmd:
            log_func.info(u'Run command <%s>' % self.ext_scan_cmd)
            os.system(self.ext_scan_cmd)
            return True
        return False

    def previewScanFile(self, scan_filename=None):
        """
        View scan result.

        :param scan_filename: The resulting scan file.
            If not specified, then the default file is taken.
        :return: True/False.
        """
        if scan_filename is None:
            scan_filename = config.DEFAULT_SCAN_FILENAME
        # Perhaps the file after the scan has already been transferred to the resulting folder
        # therefore, you need to view the file in the scan folder
        if not os.path.exists(scan_filename):
            scan_filename = os.path.join(self.scan_dir if self.scan_dir else config.PROFILE_PATH,
                                         os.path.basename(scan_filename))

        return exec_func.view_file_ext(scan_filename)


class iqScannerDlg(scanner_dlg_proto.iqScannerDlgProto,
                   iqScanAdministrator):
    """
    Scan control dialog box.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        scanner_dlg_proto.iqScannerDlgProto.__init__(self, *args, **kwargs)
        iqScanAdministrator.__init__(self)

        self.init_ctrl()
        self.showOptions()

    def onInitDlg(self, event):
        """
        Initialization of the dialogue.
        """
        event.Skip()

    def init_ctrl(self):
        """
        Initialization of controls.
        """
        if self.scan_manager.isDevices():
            self.initComboBoxScanners()

        # Sources list
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner--arrow.png'))
        self.source_comboBox.Append(u'Планшет', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document--arrow.png'))
        self.source_comboBox.Append(u'Фронтальная сторона', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'arrow-continue-180-top.png'))
        self.source_comboBox.Append(u'Обратная сторона', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'documents.png'))
        self.source_comboBox.Append(u'Дуплекс/Двустороннее сканирование', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.source_comboBox.SetSelection(0)

        # Page Size List
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document-number-4.png'))
        self.pagesize_comboBox.Append(u'A4', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document-number-3.png'))
        self.pagesize_comboBox.Append(u'A3', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.pagesize_comboBox.SetSelection(0)

        # List of scan file formats
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_pdf.png'))
        self.fileext_comboBox.Append(u'PDF', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_jpeg.png'))
        self.fileext_comboBox.Append(u'JPEG', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_jpg.png'))
        self.fileext_comboBox.Append(u'JPG', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_tif.png'))
        self.fileext_comboBox.Append(u'TIF', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'file_extension_bmp.png'))
        self.fileext_comboBox.Append(u'BMP', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.fileext_comboBox.SetSelection(0)

        # Mode list
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'border-weight.png'))
        self.mode_comboBox.Append(u'Штриховой', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'contrast.png'))
        self.mode_comboBox.Append(u'Полутоновой', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'gradient.png'))
        self.mode_comboBox.Append(u'Черно-белый', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'color.png'))
        self.mode_comboBox.Append(u'Цветной', wx.Image.ConvertToBitmap(wx.Image(img_filename)))
        self.mode_comboBox.SetSelection(2)

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'page.png'))
        bitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        self.m_bitmap1.SetBitmap(bitmap)

        option_notebookImageSize = wx.Size(16, 16)
        option_notebookIndex = 0
        option_notebookImages = wx.ImageList(option_notebookImageSize.GetWidth(), option_notebookImageSize.GetHeight())
        self.option_notebook.AssignImageList(option_notebookImages)

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'document_spacing.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'property-blue.png'))
        option_notebookBitmap = wx.Bitmap(img_filename, wx.BITMAP_TYPE_ANY)
        if option_notebookBitmap.IsOk():
            option_notebookImages.Add(option_notebookBitmap)
            self.option_notebook.SetPageImage(option_notebookIndex, option_notebookIndex)
            option_notebookIndex += 1

        filename = os.path.splitext(os.path.basename(config.DEFAULT_SCAN_FILENAME))[0] if not self.scan_filename else self.scan_filename
        self.filename_textCtrl.SetValue(filename)

        self.depth_spinCtrl.SetValue(scan_manager.DEFAULT_DEPTH)
        # External scan tool
        self.extern_cmd_textCtrl.SetValue(config.DEFAULT_EXT_SCAN_PRG)

        self.ok_button.SetFocus()

    def showOptions(self):
        """
        Set scan parameters in window controls.
        """
        if self.scanner:
            self.scanner_comboBox.SetStringSelection(self.scanner)

        if self.scan_source:
            i = 0
            try:
                log_func.debug(u'Setting the scan source <%s>' % self.scan_source)
                i = scan_manager.SCAN_SOURCES.index(self.scan_source)
            except ValueError:
                log_func.warning(u'Scan source not found <%s>' % self.scan_source)
            self.source_comboBox.Select(i)

        if self.scan_mode:
            i = 0
            try:
                i = scan_manager.SCAN_MODES.index(self.scan_mode)
            except ValueError:
                log_func.warning(u'Scan mode not found <%s>' % self.scan_mode)
            self.mode_comboBox.Select(i)

        self.multiscan_checkBox.SetValue(bool(self.is_multi_scan))
        self.preview_checkBox.SetValue(bool(self.is_preview))

        if self.page_size:
            i = 0
            try:
                i = scan_manager.SCAN_PAGE_SIZES.index(self.page_size)
            except ValueError:
                log_func.warning(u'Scan page size not found <%s>' % self.page_size)
            self.pagesize_comboBox.Select(i)

        if self.scan_area:
            self.left_spinCtrl.SetValue(self.scan_area[0])
            self.top_spinCtrl.SetValue(self.scan_area[1])
            self.right_spinCtrl.SetValue(self.scan_area[2])
            self.bottom_spinCtrl.SetValue(self.scan_area[3])

        if self.scan_dir:
            self.scan_dirPicker.SetPath(self.scan_dir)

        if self.scan_filename:
            self.filename_textCtrl.SetValue(self.scan_filename)

        if self.scan_filetype:
            i = 0
            try:
                i = scan_manager.SCAN_FILE_TYPES.index(self.scan_filetype)
            except ValueError:
                log_func.warning(u'Scan file type not found <%s>' % self.scan_filetype)
            self.fileext_comboBox.Select(i)

        if self.depth:
            self.depth_spinCtrl.SetValue(self.depth)

        if self.ext_scan_cmd:
            self.extern_cmd_textCtrl.SetValue(self.ext_scan_cmd)

    def readOptions(self):
        """
        Read scan parameters from controls.
        """
        self.scanner = self.scanner_comboBox.GetStringSelection()
        self.scan_source = scan_manager.SCAN_SOURCES[self.source_comboBox.GetSelection()]
        self.scan_mode = scan_manager.SCAN_MODES[self.mode_comboBox.GetSelection()]
        self.is_multi_scan = self.multiscan_checkBox.IsChecked()
        self.is_preview = self.preview_checkBox.IsChecked()
        self.page_size = scan_manager.SCAN_PAGE_SIZES[self.pagesize_comboBox.GetSelection()]
        self.scan_area = (self.left_spinCtrl.GetValue(),
                          self.top_spinCtrl.GetValue(),
                          self.right_spinCtrl.GetValue(),
                          self.bottom_spinCtrl.GetValue())
        self.scan_dir = self.scan_dirPicker.GetPath()
        self.scan_filename = self.filename_textCtrl.GetValue()
        self.scan_filetype = scan_manager.SCAN_FILE_TYPES[self.fileext_comboBox.GetSelection()]
        self.depth = self.depth_spinCtrl.GetValue()
        self.ext_scan_cmd = self.extern_cmd_textCtrl.GetValue()

    def setOptions(self, **options):
        """
        Set scan options in the dialog box.

        :param options: Options.
        :return: True/False.
        """
        for option_name, option_value in options.items():
            if hasattr(self, option_name):
                try:
                    setattr(self, option_name, option_value)
                    log_func.info(u'Set option <%s>. Value <%s>' % (option_name, option_value))
                except:
                    log_func.warning(u'Error set option <%s>. Value <%s>' % (option_name, option_value))
        # After setting the attributes, display them in the dialog box
        self.showOptions()

    def onCanceButtonClick(self, event):
        """
        Cancel button click handler.
        """
        self.EndModal(wx.CANCEL)
        event.Skip()

    def onOkButtonClick(self, event):
        """
        Scan button click handler.
        """
        self.readOptions()
        self.runScan()

        self.saveOptions()

        self.EndModal(wx.OK)
        event.Skip()

    def onExternButtonClick(self, event):
        """
        <Scan tool> button click handler.
        """
        self.readOptions()
        self.runExtScan()

        self.saveOptions()

        self.EndModal(wx.OK)
        event.Skip()

    def initComboBoxScanners(self, select_scanner=None):
        """
        Initialization of the combobox list of system scanners.

        :param select_scanner: Which scanner to choose after
             initialization of the combo box,
             if None, then the first one in the list is selected.
        """
        scanner_devices = self.scan_manager.getDeviceNames()

        self.scanner_comboBox.Clear()

        if scanner_devices:
            default_select = 0
            i = 0
            for scanner_name in scanner_devices:

                img_filename = os.path.normpath(os.path.join(os.path.dirname(__file__), u'img', u'scanner.png'))
                if scanner_name == select_scanner:
                    default_select = i

                self.scanner_comboBox.Append(scanner_name, wx.Image.ConvertToBitmap(wx.Image(img_filename)))
                i += 1

            self.scanner_comboBox.Select(default_select)
        else:
            log_func.warning(u'No scan devices found')
            msg = u'No scan devices found. Check if the devices are on / connected to them.'
            dlg_func.openWarningBox(u'WARNING', msg)
            try:
                self.EndModal(wx.ID_CANCEL)
            except:
                log_func.fatal()

    def onMultiScanCheckBox(self, event):
        """
        Multipage Scan Option Marker Handler.
             If multi-page scanning is enabled, then
             The scan file can only be a PDF.
        """
        if event.IsChecked():
            self.fileext_comboBox.Select(0)
        event.Skip()

    def onFileTypeCombobox(self, event):
        """
        A handler for selecting the type of scan file.
             If you select a scan file type
             not pdf / picture format then it turns off
             multi-page scanning.
        """
        if event.GetSelection():
            self.multiscan_checkBox.SetValue(False)
        event.Skip()


def do_scan_dlg(parent=None, options=None, title=None):
    """
    Calling the dialogue form of scanning.

    :param parent: Parent form.
    :param options: Scan options.
    :param title: Title dielog form.
    :return: True/False.
    """
    result = True
    scan_dlg = iqScannerDlg(parent=parent)
    if title:
        scan_dlg.SetTitle(title)
        
    if options:
        scan_dlg.setOptions(**options)

    if scan_dlg.scan_manager.isDevices():
        dlg_result = scan_dlg.ShowModal()
        result = dlg_result == wx.ID_OK
    else:
        msg = u'No scan devices found. Check if the devices are on / connected to them.'
        dlg_func.openWarningBox(u'WARNING', msg)
        result = False

    scan_dlg.Destroy()

    return result
