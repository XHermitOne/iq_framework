#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZIP archive file manipulate functions.
"""

import os
import os.path
import subprocess
import locale

from . import log_func
from . import file_func

__version__ = (0, 0, 1, 3)

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
        overwrite = ''
        if overwrite:
            overwrite = '-o'
        unzip_options = ' '.join(options)
        unzip_cmd = 'unzip %s %s %s -d %s' % (overwrite, unzip_options, zip_filename, dst_dir)
        if to_console:
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
        zip_cmd = 'zip %s %s %s' % (zip_options, zip_filename, src_filename)
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
