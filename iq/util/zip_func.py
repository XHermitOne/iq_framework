#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZIP archive file manipulate functions.
"""

import os
import os.path
import subprocess
import locale
import zipfile

from . import log_func
from . import file_func
from . import sys_func

__version__ = (0, 0, 4, 1)

ZIP_EXT = '.zip'


def unzipToDir(zip_filename, dst_dir=None, overwrite=True, to_console=True, options=()):
    """
    Extract *.zip file to directory.

    :param zip_filename: Zip filename.
    :param dst_dir: Destination directory.
        If not specified, then it is unzipped in the same folder
        where is the archive. 
    :param overwrite: Overwrite existing files without prompting?
    :param to_console: Console output?
    :param options: Unzip options.
    :return: True/False or lines if not console output.
    """
    if dst_dir is None:
        dst_dir = os.path.dirname(zip_filename)

    unzip_cmd = ''
    try:
        if sys_func.isLinuxPlatform():
            overwrite = ''
            if overwrite:
                overwrite = '-o'
            unzip_options = ' '.join(options)
            unzip_cmd = 'unzip %s %s %s -d %s' % (overwrite, unzip_options, zip_filename, dst_dir)
        elif sys_func.isWindowsPlatform():
            unzip_options = ' '.join(options)
            unzip_cmd = 'powershell expand-archive %s %s %s' % (unzip_options, zip_filename, dst_dir)
        else:
            log_func.warning(u'Unsupported unzip for this platform')
            return False

        if to_console:
            log_func.info(u'Unzip command <%s>' % unzip_cmd)
            os.system(unzip_cmd)
            return True
        else:
            process = subprocess.Popen(unzip_cmd, stdout=subprocess.PIPE)
            b_lines = process.stdout.readlines()
            console_encoding = locale.getpreferredencoding()
            lines = [line.decode(console_encoding).strip() for line in b_lines]
            return lines
    except:
        log_func.fatal(u'Error unzip <%s>' % unzip_cmd)
    return False


def zipFile(src_filename, zip_filename=None, overwrite=True, to_console=True, options=()):
    """
    Compress file to *.zip.

    :param src_filename: Compressed file name.
    :param zip_filename: Zip filename.
    :param overwrite: Overwrite existing files without prompting?
    :param to_console: Console output?
    :param options: Zip options.
    :return: True/False or lines if not console output.
    """
    if not os.path.exists(src_filename):
        log_func.warning(u'Compressed file <%s> to ZIP not found' % src_filename)
        return False

    if zip_filename is None:
        zip_filename = os.path.splitext(src_filename)[0] + ZIP_EXT

    zip_cmd = ''
    try:
        if overwrite and os.path.exists(zip_filename):
            file_func.removeFile(zip_filename)

        zip_options = ' '.join(options)
        if sys_func.isLinuxPlatform():
            zip_cmd = 'zip %s %s %s' % (zip_options, zip_filename, src_filename)
        elif sys_func.isWindowsPlatform():
            zip_cmd = 'powershell compress-archive %s -Path %s -DestinationPath %s' % (zip_options, src_filename, zip_filename)
        else:
            log_func.warning(u'Unsupported zip for this platform')
            return False

        if to_console:
            log_func.info(u'ZIP. Command <%s>' % zip_cmd)
            os.system(zip_cmd)
            return True
        else:
            process = subprocess.Popen(zip_cmd, stdout=subprocess.PIPE)
            b_lines = process.stdout.readlines()
            console_encoding = locale.getpreferredencoding()
            lines = [line.decode(console_encoding).strip() for line in b_lines]
            return lines
    except:
        log_func.fatal(u'Error zip <%s>' % zip_cmd)
    return False


def zipFilesByMask(src_filename_mask, zip_filename=None, overwrite=True, to_console=True, options=()):
    """
    Compress file to *.zip.

    :param src_filename_mask: File mask. For example /home/user/tmp/*.xml.
    :param zip_filename: Zip filename.
    :param overwrite: Overwrite existing files without prompting?
    :param to_console: Console output?
    :param options: Zip options.
    :return: True/False or lines if not console output.
    """
    src_filenames = file_func.getFilesByMask(filename_mask=src_filename_mask)
    if src_filenames:
        return zipFiles(src_filenames=src_filenames,
                        zip_filename=zip_filename,
                        overwrite=overwrite,
                        to_console=to_console,
                        options=options)
    return False


def zipFiles(src_filenames, zip_filename=None, overwrite=True, to_console=True, options=()):
    """
    Compress file to *.zip.

    :param src_filenames: File names.
    :param zip_filename: Zip filename.
    :param overwrite: Overwrite existing files without prompting?
    :param to_console: Console output?
    :param options: Zip options.
    :return: True/False or lines if not console output.
    """
    if not all([os.path.exists(src_filename) for src_filename in src_filenames]):
        log_func.warning(u'Compressed files %s to ZIP not found' % ['%s : %s' % (src_filename, 'exists' if os.path.exists(src_filename) else 'NOT EXISTS') for src_filename in src_filenames])
        return False

    if zip_filename is None:
        zip_filename = os.path.splitext(src_filenames)[0] + ZIP_EXT

    zip_cmd = ''
    try:
        if overwrite and os.path.exists(zip_filename):
            file_func.removeFile(zip_filename)

        zip_options = ' '.join(options)
        if sys_func.isLinuxPlatform():
            zip_cmd = 'zip %s %s %s' % (zip_options, zip_filename, ' '.join(src_filenames))
        elif sys_func.isWindowsPlatform():
            zip_cmd = 'powershell compress-archive %s -Path %s -DestinationPath %s' % (zip_options, ', '.join(src_filenames), zip_filename)
        else:
            log_func.warning(u'Unsupported zip for this platform')
            return False

        if to_console:
            log_func.info(u'ZIP. Command <%s>' % zip_cmd)
            os.system(zip_cmd)
            return True
        else:
            process = subprocess.Popen(zip_cmd, stdout=subprocess.PIPE)
            b_lines = process.stdout.readlines()
            console_encoding = locale.getpreferredencoding()
            lines = [line.decode(console_encoding).strip() for line in b_lines]
            return lines
    except:
        log_func.fatal(u'Error zip <%s>' % zip_cmd)
    return False


def isZipFile(zip_filename):
    """
    Check is zip file.

    :param zip_filename: Zip file name.
    :return: True/False.
    """
    if not zip_filename:
        log_func.warning(u'Zip file not defined')
        return False

    if not os.path.exists(zip_filename):
        log_func.warning(u'Zip file <%s> not found' % zip_filename)
        return False

    try:
        result = zipfile.is_zipfile(zip_filename)
        if result:
            log_func.info(u'<%s> is ZIP file' % zip_filename)
        else:
            log_func.warning(u'<%s> is not ZIP file' % zip_filename)
        return result
    except:
        log_func.fatal(u'Error check is zip file <%s>' % zip_filename)
    return None


def openZipFile(zip_filename):
    """
    Open zip file in archive manager.

    :param zip_filename: Zip file name.
    :return: True/False.
    """
    if not zip_filename:
        log_func.warning(u'Zip file not defined')
        return False

    if not os.path.exists(zip_filename):
        log_func.warning(u'Zip file <%s> not found' % zip_filename)
        return False

    try:
        if sys_func.isLinuxPlatform():
            open_zip_cmd = 'file-roller %s &' % zip_filename
        elif sys_func.isWindowsPlatform():
            if not file_func.isFilenameExt(zip_filename, ZIP_EXT):
                if file_func.changeFileExt(zip_filename, ZIP_EXT):
                    zip_filename = file_func.setFilenameExt(zip_filename, ZIP_EXT)
            open_zip_cmd = 'explorer %s &' % zip_filename
        else:
            log_func.warning(u'Unsupported open zip for this platform')
            return False

        log_func.info(u'Open ZIP. Command <%s>' % open_zip_cmd)
        os.system(open_zip_cmd)
        return True
    except:
        log_func.fatal(u'Error open zip file <%s> in archive manager' % zip_filename)
    return False
