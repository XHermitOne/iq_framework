#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
icScanner - The program for starting document scanning.
            Batch processing of scanned documents.

Command line options:
    
    python icscanner.py <Launch parameters>
    
Launch parameters:

    [Help and debugging]
        --help|-h|-?        Print help
        --version|-v        Print version
        --debug|-d          Set debug mode
        --log|-l            set log mode

   [Launch modes]
        --scanner=          Scaner name
        --source=           Scan source:
                            Flatbed
                            ADF_Front   (Front)
                            ADF_Back    (Back)
                            ADF_Duplex  (Duplex)
        --mode=             Scan mode:
                            Lineart
                            Halftone
                            Grey
        --depth=            Depth. By default 8
        --multi_scan        On multi-page scanning mode
        --preview           On previewing the scan result
        --page_size=        Page size:
                            A4 or A3
        --area=             Scan area
        --scan_dir=         Scan folder
        --file_name=        Scan file name (without extension)
                            In case of batch processing, it is necessary
                            specify file names via <;>
        --file_type=        Scan file type:
                            PDF, JPEG, JPG, TIF, BMP
        --ext_cmd=          External launch command
                            scanning tool
        --pack_mode         Pack mode.
                            Pack mode involves running the program
                            without a dialog box.
        --pack_pages=       Number of pages in each document
                            If --pack_pages is not specified, then we assume
                            that all documents are single-page.
                            In specifying pages, you can specify via /
                            is there a 2-way scan or not.
                            For example: 2/1 - 2 sheets on both sides
                            3/0 - 3 sheets on one side
        --max_sheets=       Limiting the number of sheets in the scanner tray
"""

import sys
import getopt
import wx

from iq.util import global_func
from iq.util import log_func
from iq.util import lang_func

from iq_scanner.scanner import config
from iq_scanner.scanner import scanner_dlg
from iq_scanner.scanner import scan_manager


__version__ = (0, 2, 1, 2)

_ = lang_func.getTranslation().gettext


def main(argv):
    """
    Main function.

    :param argv: List of command line parameters.
    """
    try:
        options, args = getopt.getopt(argv, 'h?vdl',
                                      ['help', 'version', 'debug', 'log',
                                       'scanner=', 'source=',
                                       'mode=', 'multi_scan', 'preview',
                                       'page_size=', 'area=',
                                       'scan_dir=',
                                       'file_name=', 'file_type=',
                                       'ext_cmd=',
                                       'pack_mode', 'pack_pages=',
                                       'glue', 'max_sheets='])
    except getopt.error as msg:
        log_func.error(str(msg), is_force_print=True)
        log_func.info(__doc__)
        sys.exit(2)

    log_func.init()

    txt_version = '.'.join([str(ver) for ver in __version__])
    cmd_options = dict()
    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            print(__doc__)
            sys.exit(0)   
        elif option in ('-v', '--version'):
            print('icScanner version: %s' % txt_version)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            global_func.setDebugMode(True)
        elif option in ('-l', '--log'):
            global_func.setLogMode(True)
        elif option in ('--scanner', ):
            cmd_options['scanner'] = arg
        elif option in ('--source',):
            cmd_options['scan_source'] = arg
        elif option in ('--mode',):
            cmd_options['scan_mode'] = arg
        elif option in ('--multi_scan',):
            cmd_options['is_multi_scan'] = True
        elif option in ('--preview',):
            cmd_options['is_preview'] = True
        elif option in ('--page_size',):
            if arg in ('A4', 'a4'):
                cmd_options['page_size'] = scan_manager.A4_PORTRAIT_PAGE_SIZE
            elif arg in ('A3', 'a3'):
                cmd_options['page_size'] = scan_manager.A3_PORTRAIT_PAGE_SIZE
            else:
                log_func.warning(u'Unprocessed page size <%s>' % arg)
        elif option in ('--area',):
            try:
                area = tuple([float(x.strip()) for x in arg.split(',')])
                cmd_options['scan_area'] = area
            except:
                log_func.fatal(u'Error parsing the scan area parameter <%s>' % arg)
        elif option in ('--scan_dir',):
            cmd_options['scan_dir'] = arg
        elif option in ('--file_name',):
            cmd_options['scan_filename'] = arg
        elif option in ('--file_type',):
            cmd_options['scan_filetype'] = arg.lower()
        elif option in ('--depth',):
            cmd_options['depth'] = int(arg)
        elif option in ('--ext_cmd',):
            cmd_options['ext_scan_cmd'] = arg
        elif option in ('--pack_mode',):
            cmd_options['pack_mode'] = True
        elif option in ('--pack_pages',):
            cmd_options['pack_pages'] = arg
        elif option in ('--max_sheets',):
            config.setConfigParam('DEFAULT_SCANNER_MAX_SHEETS', int(arg))
        else:
            log_func.warning(u'An unprocessed command line parameter <%s>' % option)

    # By default, pack mode is disabled---+
    #                                     v
    if not cmd_options.get('pack_mode', False):
        # Attention! The application is created to manage dialog boxes
        app = wx.PySimpleApp()
        # Set locale for correct display of calendars,
        # formats of dates, times, data, etc.
        locale = wx.Locale()
        locale.Init(wx.LANGUAGE_RUSSIAN)

        scanner_dlg.openScanDlg(options=cmd_options,
                                title=_(u'Scanner ') + txt_version)
        app.MainLoop()
    else:
        # In pack mode, we do not use the dialog box
        # But in the case of the mode of gluing the document in parts, dialog boxes are used
        filenames = cmd_options.get('scan_filename', u'').split(';')
        pack_page_list = cmd_options.get('pack_pages', u'').split(';')
        n_pages = [int(pack_page.split('/')[0]) if '/' in pack_page else int(pack_page) for pack_page in pack_page_list]
        duplexes = [bool(int(pack_page.split('/')[1])) if '/' in pack_page else False for pack_page in pack_page_list]
        scan_filenames = [(filename, n_pages[i] if i < len(n_pages) else 1,
                           duplexes[i] if i < len(duplexes) else False) for i, filename in enumerate(filenames)]
        scan_admin = scanner_dlg.iqScanAdministrator()
        # Set additional options from the command line
        scan_admin.setExtOptions(scan_dir=cmd_options['scan_dir'])
        scan_admin.runScanPack(*scan_filenames)


if __name__ == '__main__':
    main(sys.argv[1:])
