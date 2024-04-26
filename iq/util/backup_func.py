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
from . import dt_func
from . import file_func
from . import exec_func
from . import global_func

__version__ = (0, 0, 3, 1)

_ = lang_func.getTranslation().gettext


def backupFileZip(src_filename, backup_url, zip_filename=None, dst_path=None, parent_win=None, *args, **kwargs):
    """
    Backup file to network resource by URL.

    :param src_filename: Source backup file name.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :return: True/False.
    """
    if isinstance(backup_url, str) and backup_url.startswith(nfs_func.NFS_URL_TYPE):
        do_zip = os.path.splitext(src_filename)[1] != zip_func.ZIP_EXT

        return backupFilesZipNfs(src_filenames=src_filename,
                                 backup_url=backup_url,
                                 zip_filename=zip_filename,
                                 dst_path=dst_path,
                                 parent_win=parent_win,
                                 do_zip=do_zip,
                                 *args, **kwargs)
    else:
        log_func.warning(u'Not supported backup network resource')
    return False


def backupFilesZip(src_filenames, backup_url, zip_filename=None, dst_path=None, parent_win=None, *args, **kwargs):
    """
    Backup files to network resource by URL.

    :param src_filenames: Source backup file names.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :return: True/False.
    """
    if isinstance(backup_url, str) and backup_url.startswith(nfs_func.NFS_URL_TYPE):
        do_zip = not all([os.path.splitext(src_filename)[1] == zip_func.ZIP_EXT for src_filename in src_filenames])
        return backupFilesZipNfs(src_filenames=src_filenames,
                                 backup_url=backup_url,
                                 zip_filename=zip_filename,
                                 dst_path=dst_path,
                                 parent_win=parent_win,
                                 do_zip=do_zip,
                                 *args, **kwargs)
    else:
        log_func.warning(u'Not supported backup network resource')
    return False


def backupFilesZipByMask(src_filenames_mask, backup_url, zip_filename=None, dst_path=None, parent_win=None, *args, **kwargs):
    """
    Backup files by mask to network resource by URL.

    :param src_filenames_mask: Source backup file names mask.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :return: True/False.
    """
    src_filenames = file_func.getFilesByMask(filename_mask=src_filenames_mask)
    if not src_filenames:
        log_func.warning(u'Not found files for backup')
        return False

    if isinstance(backup_url, str) and backup_url.startswith(nfs_func.NFS_URL_TYPE):
        do_zip = not all([os.path.splitext(src_filename)[1] == zip_func.ZIP_EXT for src_filename in src_filenames])
        return backupFilesZipNfs(src_filenames=src_filenames,
                                 backup_url=backup_url,
                                 zip_filename=zip_filename,
                                 dst_path=dst_path,
                                 parent_win=parent_win,
                                 do_zip=do_zip,
                                 *args, **kwargs)
    else:
        log_func.warning(u'Not supported backup network resource')
    return False


def backupFilesZipNfs(src_filenames, backup_url, zip_filename=None, dst_path=None, parent_win=None, do_zip=True, *args, **kwargs):
    """
    Backup file to NFS network resource by URL. Only for Linux platforms.

    :param src_filenames: Source backup filenames.
    :param backup_url: Backup network URL.
    :param zip_filename: Backup ZIP file name.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :param do_zip: Make ZIP archive for backup.
    :return: True/False.
    """
    result = False
    if isinstance(src_filenames, str):
        src_filenames = [src_filenames]
    if not all([os.path.exists(src_filename) for src_filename in src_filenames]):
        log_func.warning(u'Backup files %s not all found' % str(src_filenames))
        return False

    try:
        # Get Root password
        root_password = sys_func.getSysRootPassword(parent_win=parent_win) if sys_func.isLinuxPlatform() else None

        if do_zip:
            if zip_filename is None:
                zip_filename = os.path.splitext(src_filenames[0])[0] + zip_func.ZIP_EXT
            zip_result = zip_func.zipFiles(src_filenames=src_filenames, zip_filename=zip_filename)

            if zip_result:
                result = nfs_func.uploadNfsFile(upload_url=backup_url,
                                                filename=zip_filename,
                                                dst_path=dst_path,
                                                rewrite=kwargs.get('rewrite', True),
                                                mnt_path=kwargs.get('mnt_path', None),
                                                options=kwargs.get('options', None),
                                                root_password=root_password)
        else:
            for src_filename in src_filenames:
                result = nfs_func.uploadNfsFile(upload_url=backup_url,
                                                filename=src_filename,
                                                dst_path=dst_path,
                                                rewrite=kwargs.get('rewrite', True),
                                                mnt_path=kwargs.get('mnt_path', None),
                                                options=kwargs.get('options', None),
                                                root_password=root_password)
    except:
        log_func.fatal(u'Error backup file <%s> to NFS network resource <%s>' % (src_filenames, backup_url))

    return result


PG_DUMP_LINUX_CMD_FMT = 'pg_dump --host=%s --port=%s --dbname=%s --username=%s --file=%s'


def backupPostgreSQLDBFileLinux(db_host, db_port, db_name, db_username, db_password=None,
                                filename=None, filename_fmt=None):
    """
    Create PostgreSQL database backup file for Linux. Create by pg_dump tool.

    :param db_host: Database host.
    :param db_port: Database port.
    :param db_name: Database name.
    :param db_username: Database user name.
    :param db_password: Database user password. If None then no password.
    :param filename: Result file name. If None then get file name by format.
    :param filename_fmt: Result file name format.
    :return: Created result file name or None if error.
    """
    if not filename and filename_fmt:
        filename = dt_func.datetime2str(dt_func.getNow(), filename_fmt)
    elif not filename and not filename_fmt:
        filename = file_func.getTempFilename()

    try:
        cmd = PG_DUMP_LINUX_CMD_FMT % (db_host, db_port, db_name, db_username, filename)
        if not db_password:
            cmd += ' --no-password'
        else:
            cmd = 'PGPASSWORD=\"%s\" ' % db_password + cmd
        exec_func.execSystemCommand(cmd=cmd)

        if os.path.exists(filename):
            return filename
        else:
            log_func.warning(u'Error create PostgreSQL postgresql://%s:%s/%s backup file <%s>' % (db_host, db_port,
                                                                                                  db_name, filename))
    except:
        log_func.fatal(u'Error create PostgreSQL postgresql://%s:%s/%s backup file <%s>' % (db_host, db_port,
                                                                                            db_name, filename))
    return None


def backupPostgreSQLDB(db_host, db_port, db_name, db_username, db_password=None,
                       backup_url=None, *args, **kwargs):
    """
    Create PostgreSQL database backup file for Linux. Create by pg_dump tool.

    :param db_host: Database host.
    :param db_port: Database port.
    :param db_name: Database name.
    :param db_username: Database user name.
    :param db_password: Database user password. If None then no password.
    :param backup_url: Backup network URL.
    :param dst_path: Destination network backup folder.
    :param parent_win: Parent window for dialogs.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        src_base_filename_fmt = db_name+'_'+sys_func.getComputerName()+'_'+global_func.getUsername()+'_%Y_%m_%d_%H_%M_%S.sql'
        src_filename_fmt = os.path.join(file_func.getTempDirname(auto_create=True), src_base_filename_fmt)
        src_filename = backupPostgreSQLDBFileLinux(db_host=db_host, db_port=db_port, db_name=db_name,
                                                   db_username=db_username, db_password=db_password,
                                                   filename_fmt=src_filename_fmt)
    else:
        log_func.warning(u'Not supported OS for backup network NFS resource')
        src_filename = None

    if src_filename:
        return backupFileZip(src_filename=src_filename, backup_url=backup_url, *args, **kwargs)
    return False
