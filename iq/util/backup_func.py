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

__version__ = (0, 0, 2, 1)

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

    do_zip = os.path.splitext(src_filename)[1] != zip_func.ZIP_EXT

    if zip_filename is None:
        zip_filename = os.path.splitext(src_filename)[0] + zip_func.ZIP_EXT

    try:
        zip_result = True
        if do_zip:
            zip_result = zip_func.zipFile(src_filename=src_filename, zip_filename=zip_filename)

        if zip_result:
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
