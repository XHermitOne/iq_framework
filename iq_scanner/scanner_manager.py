#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
Control system for launching an external document scanning program.
"""

import sys
import os
import os.path

from . import config
from iq.util import log_func

__version__ = (0, 3, 1, 1)


# Scanner manager object
SCANNER_MANAGER = None


class iqScannerManager(object):
    """
    Manager class for launch of an external document scanning program.
    """
    def __init__(self, scanner_exec_filename=None):
        """
        Constructor.

        :param scanner_exec_filename: Full path to <scanner.py>.
            If not defined, it is taken from the configuration file.
        """
        self._scanner_exec_filename = config.getConfigParam('DEFAULT_SCANNER_EXEC_FILENAME') if scanner_exec_filename is None else scanner_exec_filename

    def getScannerExec(self):
        return self._scanner_exec_filename

    def getScanPath(self):
        return config.getConfigParam('DEFAULT_SCAN_PATH')

    def scan(self):
        """
        Starting document scanning.

        :return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            cmd = '%s %s' % (sys.executable, self._scanner_exec_filename)
            try:
                log_func.info(u'Exec scanner program <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log_func.fatal(u'Error exec scanner program: <%s>' % cmd)
        else:
            log_func.warning(u'Scanner program module <%s> not found' % self._scanner_exec_filename)
        return False

    def scanPreview(self):
        """
        Start scanning a document with previewing the scan result.

        :return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            cmd = '%s %s --preview' % (sys.executable, self._scanner_exec_filename)
            try:
                log_func.info(u'Exec scanner program <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log_func.fatal(u'Error scanner program <%s> in preview mode' % cmd)
        else:
            log_func.warning(u'Scanner program module <%s> not found' % self._scanner_exec_filename)
        return False

    def scanExport(self, scan_filename):
        """
        Start scanning a document with saving in a specific file.

        :param scan_filename: Scan document file name.
        :return: True/False.
        """
        if os.path.exists(self._scanner_exec_filename):
            scan_dir = os.path.dirname(scan_filename)
            file_name = os.path.splitext(os.path.basename(scan_filename))[0]
            file_type = os.path.splitext(os.path.basename(scan_filename))[1].replace('.', '').upper()
            cmd = '%s %s --scan_dir=%s --file_name=%s --file_type=%s' % (sys.executable,
                                                                         self._scanner_exec_filename,
                                                                         scan_dir, file_name, file_type)
            try:
                log_func.info(u'Exec scanner program <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log_func.fatal(u'Error scanner program <%s> in export mode' % cmd)
        else:
            log_func.warning(u'Scanner program module <%s> not found' % self._scanner_exec_filename)
        return False

    def scanPack(self, *scan_filenames):
        """
        Start scanning a package of documents.

        :param scan_filenames: List of scan document file names
            with an indication of the number of pages of each document (optional)
            and a sign of a 2-way scan (optional).
            For example:
            ('/tmp/scan001.pdf', 2, True), ('/tmp/scan002.pdf', ), ('/tmp/scan003.pdf', 1), ...
        :return: True/False.
        """
        if not scan_filenames:
            log_func.warning(u'The list of scanned files is not defined during pack scanning')
            return False
        if not min([type(scan_option) in (list, tuple) for scan_option in scan_filenames]):
            log_func.warning(u'Scan manager input parameter type error')
            return False        

        # Attention! Delete all previously scanned pages before launching
        full_scan_filenames = [scan[0] for scan in scan_filenames]
        self.deleteScanFiles(*full_scan_filenames)
        
        # Prepare data for processing
        scan_filenames = [(scan, 1, False) if len(scan) == 1 else (tuple(list(scan)+[False]) if len(scan) == 2 else scan) for scan in scan_filenames]        
        if os.path.exists(self._scanner_exec_filename):
            # The scan folder and the scan file type are determined by the first file
            scan_dir = os.path.dirname(scan_filenames[0][0])
            file_type = os.path.splitext(os.path.basename(scan_filenames[0][0]))[1].replace('.', '').upper()

            filename_list = [os.path.splitext(os.path.basename(scan_filename))[0] for scan_filename, n_page, is_duplex in scan_filenames]
            filenames = ';'.join(filename_list)
            n_pages = ';'.join([str(n_page) + (u'/1' if is_duplex else u'') for scan_filename, n_page, is_duplex in scan_filenames])
            cmd = '%s %s --scan_dir=%s --file_type=%s --pack_mode --file_name=\"%s\" --pack_pages=\"%s\"' % (sys.executable,
                                                                                                             self._scanner_exec_filename,
                                                                                                             scan_dir,
                                                                                                             file_type,
                                                                                                             filenames,
                                                                                                             n_pages)
            try:
                log_func.info(u'Exec scanner program <%s>' % cmd)
                os.system(cmd)
                return True
            except:
                log_func.fatal(u'Error exec scanner program <%s>' % cmd)
        else:
            log_func.warning(u'Scanner program module <%s> not found' % self._scanner_exec_filename)
        return False

    def deleteScanFiles(self, *scan_filenames):
        """
        Delete scan files.

        :param scan_filenames: List of scan document file names.
        """
        for scan_filename in scan_filenames:
            if os.path.exists(scan_filename):
                try:
                    os.remove(scan_filename)
                    log_func.info(u'File <%s> deleted' % scan_filename)
                except OSError:
                    log_func.fatal(u'Error delete file <%s>' % scan_filename)


def getScannerManager():
    """
    Get scanner manager object.

    :return:
    """
    if globals()['SCANNER_MANAGER'] is None:
        globals()['SCANNER_MANAGER'] = iqScannerManager()
    return globals()['SCANNER_MANAGER']
