#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iqScanner - A program for launching scanning documents and
batch processing of scanned documents.
"""

import wx

from iq.util import log_func

from .scanner import scanner_dlg
from .scanner import scan_manager
from .scanner import config

__version__ = (0, 0, 0, 1)


def scan(scanner=None, source=None, mode=None, depth=None,
         multi_scan=False, preview=False, page_size=None,
         area=None, scan_dir=None, file_name=None, file_type=None,
         ext_cmd=None, pack_mode=False, pack_pages=None, max_sheets=None,
         version=False):
    """
    Main run scanner function.

    :param scanner: Explicit scanner name
    :param source: Scan source:
        Flatbed     (Flat)
        ADF_Front   (Front side)
        ADF_Back    (back side)
        ADF_Duplex  (Duplex / Both Sides)
    :param mode: Scan mode:
        Lineart     (Dashed)
        Halftone    (Halftone)
        Grey        (Black and white)
        Color       (Color)
    :param depth: Depth. Default 8
    :param multi_scan: On multi-page scanning mode
    :param preview: On view scan result
    :param page_size: Page size A4 or A3
    :param area: Scan area
    :param scan_dir: Scan folder
    :param file_name: Scan file name (without extension)
       In the case of batch processing, you must specify the file names via <;>
    :param file_type: Scan file fype PDF, JPEG, JPG, TIF, BMP
    :param ext_cmd: Command to launch an external scan tool
    :param pack_mode: Enabling batch processing.
        Batch mode means starting the program without a dialog box.
    :param pack_pages: The number of pages in each document
       If pack_pages is not specified, then we assume that all documents are single-page
       In the indication of the pages, you can specify through / there is 2-sided scanning or not.
       For example: 2/1 - 2 sheets on both sides.
                    3/0 - 3 sheets on one side
    :param max_sheets: Limit the number of sheets in the scanner tray.
    :param version: Print project version.
    """
    txt_version = '.'.join([str(ver) for ver in __version__])
    if version:
        log_func.info('iqScanner version: %s' % txt_version, is_force_print=True)
        return

    log_func.init(config.getConfigParam('LOG_FILENAME'))

    cmd_options = dict()

    if scanner is not None:
        cmd_options['scanner'] = scanner
    if source:
        cmd_options['scan_source'] = source
    if mode is not None:
        cmd_options['scan_mode'] = mode
    if multi_scan:
        cmd_options['is_multi_scan'] = multi_scan
    if preview:
        cmd_options['is_preview'] = True
    if page_size is not None:
        if page_size in ('A4', 'a4'):
            cmd_options['page_size'] = scan_manager.A4_PORTRAIT_PAGE_SIZE
        elif page_size in ('A3', 'a3'):
            cmd_options['page_size'] = scan_manager.A3_PORTRAIT_PAGE_SIZE
        else:
            log_func.warning(u'Not support page size <%s>' % page_size)
    if area is not None:
        try:
            area = tuple([float(x.strip()) for x in area.split(',')])
            cmd_options['scan_area'] = area
        except:
            log_func.fatal(u'Scan area parameter parsing error <%s>' % area)
    if scan_dir is not None:
        cmd_options['scan_dir'] = scan_dir
    if file_name is not None:
        cmd_options['scan_filename'] = file_name
    if file_type is not None:
        cmd_options['scan_filetype'] = file_type.lower()
    if depth is not None:
        cmd_options['depth'] = int(depth)
    if ext_cmd is not None:
        cmd_options['ext_scan_cmd'] = ext_cmd
    if pack_mode is not None:
        cmd_options['pack_mode'] = pack_mode
    if pack_pages is not None:
        cmd_options['pack_pages'] = pack_pages
    if max_sheets is not None:
        config.setConfigParam('DEFAULT_SCANNER_MAX_SHEETS', int(max_sheets))

    # By default, batch mode is disabled--+
    #                                     v
    if not cmd_options.get('pack_mode', False):
        app = wx.App()
        # Set locale
        # This is necessary for the correct display of calendars, date formats, time, data, etc.
        locale = wx.Locale()
        locale.Init(wx.LANGUAGE_RUSSIAN)

        scanner_dlg.do_scan_dlg(options=cmd_options, 
                                title=u'iqScanner ' + txt_version)
        app.MainLoop()
    else:
        # In batch mode, do not use the dialog box
        # But in the case of gluing the document in parts, the dialog boxes are used
        filenames = cmd_options.get('scan_filename', u'').split(';')
        pack_page_list = cmd_options.get('pack_pages', u'').split(';')
        n_pages = [int(pack_page.split('/')[0]) if '/' in pack_page else int(pack_page) for pack_page in pack_page_list]
        duplexes = [bool(int(pack_page.split('/')[1])) if '/' in pack_page else False for pack_page in pack_page_list]
        scan_filenames = [(filename, n_pages[i] if i < len(n_pages) else 1,
                           duplexes[i] if i < len(duplexes) else False) for i, filename in enumerate(filenames)]
        scan_admin = scanner_dlg.iqScanAdministrator()
        # Install advanced options from the command line
        scan_admin.setExtOptions(scan_dir=cmd_options['scan_dir'])
        scan_admin.runScanPack(*scan_filenames)
