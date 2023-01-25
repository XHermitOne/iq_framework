#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Backup files functions.
"""

import os.path

from . import log_func
from . import sys_func
from . import zip_func
from . import nfs_func
from . import lang_func

__version__ = (0, 0, 1, 1)

_ = lang_func.getTranslation().gettext


def backupFileZip(src_filename, backup_url, zip_filename=None, dst_path=None, parent_win=None, *args, **kwargs):
    """
    Backup file to network resource by URL.

    :param src_filename: Source backup file name.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :param mnt_path: Mount path in the case of an already NFS resource is mounted.
    :param options: Additional mount options.
    :param rewrite: Overwrite a file if it already exists?
    :return: True/False.
    """
    if isinstance(backup_url, str) and backup_url.startswith(nfs_func.NFS_URL_TYPE):
        return backupFileZipNfs(src_filename=src_filename,
                                backup_url=backup_url,
                                zip_filename=zip_filename,
                                dst_path=dst_path,
                                parent_win=parent_win,
                                *args, **kwargs)
    else:
        log_func.warning(u'Not supported backup network resource')
    return False


def backupFileZipNfs(src_filename, backup_url, zip_filename=None, dst_path=None, parent_win=None, *args, **kwargs):
    """
    Backup file to NFS network resource by URL. Only for Linux platforms.

    :param src_filename: Source backup file name.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :param mnt_path: Mount path in the case of an already NFS resource is mounted.
    :param options: Additional mount options.
    :param rewrite: Overwrite a file if it already exists?
    :return: True/False.
    """
    result = False
    if not os.path.exists(src_filename):
        log_func.warning(u'Backup file <%s> not found' % src_filename)
        return False

    if zip_filename is None:
        zip_filename = os.path.splitext(src_filename)[0] + zip_func.ZIP_EXT

    try:
        if zip_func.zipFile(src_filename=src_filename, zip_filename=zip_filename):
            # Get Root password
            root_password = sys_func.getSysRootPassword(parent_win=parent_win) if sys_func.isLinuxPlatform() else None

            result = nfs_func.uploadNfsFile(upload_url=backup_url,
                                            filename=zip_filename,
                                            dst_path=dst_path,
                                            rewrite=kwargs.get('rewrite', True),
                                            mnt_path=kwargs.get('mnt_path', None),
                                            options=kwargs.get('options', None),
                                            root_password=root_password)
    except:
        log_func.fatal(u'Error backup file <%s> to NFS network resource <%s>' % (src_filename, backup_url))

    return result
