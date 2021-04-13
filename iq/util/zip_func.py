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

__version__ = (0, 0, 0, 1)


def unzipToDir(zip_filename, dst_dir=None, overwrite=True, to_console=True):
    """
    Extract *.zip file to directory.

    :param zip_filename: Zip filename.
    :param dst_dir: Destination directory.
        If not specified, then it is unzipped in the same folder
        where is the archive. 
    :param overwrite: Overwrite existing files without prompting?
    :param to_console: Console output?
    :return: True/False or lines if not console output.
    """
    if dst_dir is None:
        dst_dir = os.path.dirname(zip_filename)

    unzip_cmd = ''
    try:
        overwrite = ''
        if overwrite:
            overwrite = '-o'
        unzip_cmd = 'unzip %s %s -d %s' % (overwrite, zip_filename, dst_dir)
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