#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions of working with files on shared NFS resources (only for Linux).

Install:
sudo apt install nfs-common

URL SMB resource format:
nfs://[[<domain>;]<username>[:<password>]@]<server>:[/[<share>/<path>]]

For example:
nfs://workgroup;user:password@server:/share/folder
"""

import os
import os.path
import urllib.parse
import time

from . import log_func
from . import sys_func
from . import file_func
from . import exec_func
from . import net_func

__version__ = (0, 0, 2, 3)

NFS_URL_TYPE = 'nfs://'
DEFAULT_WORKGROUP = 'WORKGROUP'
ANONYMOUS_USERNAME = 'guest'

LINUX_NFS_MOUNT_CMD_FMT = 'echo "%s" | sudo --stdin mount --verbose --types nfs %s %s:/%s %s'
LINUX_NFS_UMOUNT_CMD_FMT = 'echo "%s" | sudo --stdin umount --verbose %s'

WINDOWS_NFS_MOUNT_CMD_FMT = 'mount -o anon %s \\\\%s%s %s'
WINDOWS_NFS_UMOUNT_CMD_FMT = 'umount %s'

DEFAULT_AUTO_DELETE_DELAY = 0

DEFAULT_WINDOWS_NFS_DRIVE_NAME = 'Z:'


def splitNfsUrlPath(url):
    """
    Correct breakdown of the NFS resource URL path into components.
    If the <#> character occurs in the path, the URL parsing library perceives further
    standing characters as fragment. This should be taken into account.
    This is what this function is designed for.

    :param url: urlparse.ParseResult object.
    :return: List of elements of the path to the SMB resource.
    """
    path_list = url.path.split(os.path.sep)
    if url.fragment:
        fragment_path_list = url.fragment.split(os.path.sep)
        fragment_path_list[0] = u'#' + fragment_path_list[0]
        path_list += fragment_path_list
    return path_list


def getNfsPathFromUrl(url):
    """
    Determine the path to the NFS resource by URL.

    :param url: NFS resource URL.
    :return: Samba resource path.
    """
    url = urllib.parse.urlparse(url)
    path_list = splitNfsUrlPath(url)
    smb_path = os.path.join(*path_list)
    return smb_path


def getNfsHostFromUrl(url):
    """
    Determine NFS resource host by URL.

    :param url: NFS resource URL.
    :return: Samba resource path.
    """
    url = urllib.parse.urlparse(url)
    host = url.netloc.split('@')[1] if '@' in url.netloc else url.netloc
    return host.replace(':', '')


def mountNfsResourceLinux(url, dst_path=None, options=None, root_password=None):
    """
    Linux. Mount NFS resource to destination path.

    :param url: Nfs resource URL.
    :param dst_path: Destination path. If not defined then create template destination path.
    :param options: Additional mount options.
    :param root_password: Root user password.
    :return: True/False.
    """
    if dst_path is None:
        dst_path = file_func.getTempDirname(auto_create=True)

    if isinstance(options, str):
        options = '--options %s' % options.replace(' ', '')
    elif isinstance(options, (tuple, list)):
        options = '--options %s' % ','.join([str(item) for item in options])
    elif isinstance(options, dict):
        options = '--options %s' % ','.join(['%s=%s' % (str(opt_name), str(opt_value)) for opt_name, opt_value in options.items()])
    else:
        options = ''

    if root_password is None:
        root_password = sys_func.getSysRootPassword()

    try:
        nfs_host = getNfsHostFromUrl(url)
        if not net_func.validPingHost(nfs_host):
            log_func.warning(u'NFS resource host <%s> not found' % nfs_host)
            return False

        nfs_path = getNfsPathFromUrl(url)
        mount_cmd = LINUX_NFS_MOUNT_CMD_FMT % (root_password, options, nfs_host, nfs_path, dst_path)
        # lines = exec_func.getLinesExecutedCommand(cmd=mount_cmd, echo=True)
        # result = not any(['Protocol not supported' in line for line in lines]) if lines else True
        result = exec_func.execSystemCommand(cmd=mount_cmd)
        if result:
            log_func.info(u'NFS resource <%s> mounted to <%s>' % (url, dst_path))
        else:
            log_func.warning(u'Error mount NFS resource <%s> to <%s>' % (url, dst_path))
        return result
    except:
        log_func.fatal(u'Error mount NFS resource <%s>' % url)
    return False


def umountNfsResourceLinux(mnt_path, root_password=None, auto_delete=False):
    """
    Linux. Umount NFS resource.

    :param mnt_path: Mount resource path.
    :param root_password: Root user password.
    :param auto_delete: Auto delete mount path after umount.
    :return: True/False.
    """
    if not mnt_path or not os.path.exists(mnt_path):
        log_func.warning(u'NFS resource mount folder <%s> not found' % mnt_path)
        return False

    if root_password is None:
        root_password = sys_func.getSysRootPassword()

    try:
        umount_cmd = LINUX_NFS_UMOUNT_CMD_FMT % (root_password, mnt_path)
        result = exec_func.execSystemCommand(umount_cmd)
        if result:
            if auto_delete:
                # Make a delay 1 sec
                if DEFAULT_AUTO_DELETE_DELAY:
                    time.sleep(DEFAULT_AUTO_DELETE_DELAY)

                if file_func.isEmptyFolder(mnt_path):
                    os.rmdir(mnt_path)
                else:
                    log_func.warning(u'The mounted folder was not deleted because it is not empty')
                    return False

            log_func.info(u'NFS resource umounted from <%s>' % mnt_path)
        return result
    except:
        log_func.fatal(u'Error umount NFS resource <%s>' % mnt_path)
    return False


def mountNfsResourceWindows(url, dst_drive=None, options=None):
    """
    Windows. Mount NFS resource to destination path.
    The Service components for NFS must be installed.

    :param url: Nfs resource URL.
    :param dst_drive: Destination drive name. If not defined then get Z:.
    :param options: Additional mount options.
    :return: True/False.
    """
    if dst_drive is None:
        dst_drive = DEFAULT_WINDOWS_NFS_DRIVE_NAME

    if isinstance(options, str):
        options = '-o %s' % options.replace(' ', '')
    elif isinstance(options, (tuple, list)):
        options = '-o %s' % ' '.join([str(item) for item in options])
    elif isinstance(options, dict):
        options = '-o %s' % ' '.join(['%s=%s' % (str(opt_name), str(opt_value)) for opt_name, opt_value in options.items()])
    else:
        options = ''

    try:
        nfs_host = getNfsHostFromUrl(url)
        if not net_func.validPingHost(nfs_host):
            log_func.warning(u'NFS resource host <%s> not found' % nfs_host)
            return False

        nfs_path = getNfsPathFromUrl(url)
        nfs_path = nfs_path.replace('/', os.path.sep)
        mount_cmd = WINDOWS_NFS_MOUNT_CMD_FMT % (options, nfs_host, nfs_path, dst_drive)
        result = exec_func.execSystemCommand(mount_cmd)
        if result:
            log_func.info(u'NFS resource <%s> mounted to <%s>' % (url, dst_drive))
        return result
    except:
        log_func.fatal(u'Error mount NFS resource <%s>' % url)
    return False


def umountNfsResourceWindows(mnt_drive):
    """
    Windows. Umount NFS resource.
    The Service components for NFS must be installed.

    :param mnt_drive: Mount resource drive name.
    :return: True/False.
    """
    if not mnt_drive or not os.path.exists(mnt_drive):
        log_func.warning(u'NFS resource mount drive <%s> not found' % mnt_drive)
        return False

    try:
        umount_cmd = WINDOWS_NFS_UMOUNT_CMD_FMT % mnt_drive
        result = exec_func.execSystemCommand(umount_cmd)
        if result:
            log_func.info(u'NFS resource umounted from <%s>' % mnt_drive)
        return result
    except:
        log_func.fatal(u'Error umount NFS resource <%s>' % mnt_drive)
    return False


def mountNfsResource(url, mnt=None, options=None, *args, **kwargs):
    """
    Mount NFS resource to destination path.

    :param url: Nfs resource URL.
    :param mnt: Destination drive name or path.
    :param options: Additional mount options.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        return mountNfsResourceLinux(url=url, dst_path=mnt, options=options, *args, **kwargs)
    elif sys_func.isWindowsPlatform():
        return mountNfsResourceWindows(url=url, dst_drive=mnt, options=options)
    else:
        log_func.warning(u'Mounting to an NFS network resource is not supported on this system')
    return False


def umountNfsResource(mnt, *args, **kwargs):
    """
    Umount NFS resource.

    :param mnt: Mount resource drive name or path.
    :return: True/False.
    """
    if sys_func.isLinuxPlatform():
        return umountNfsResourceLinux(mnt_path=mnt, *args, **kwargs)
    elif sys_func.isWindowsPlatform():
        return umountNfsResourceWindows(mnt_drive=mnt)
    else:
        log_func.warning(u'Unmounting to an NFS network resource is not supported on this system')
    return False


def downloadNfsFile(download_url=None, filename=None, dst_path=None, rewrite=True, mnt_path=None, *args, **kwargs):
    """
    Download file from NFS resource.

    :param download_url: NFS resource URL.
        For example:
        'nfs://SAFE/Backup'
    :param filename: Relative file name.
        For example:
        '/2017/FDOC/RC001.DCM'
    :param dst_path: The local path to save the file.
    :param rewrite: Overwrite a local file if it already exists?
    :param mnt_path: Mount path in the case of an already NFS resource is mounted.
    :return: True/False.
    """
    result = False

    if mnt_path is None:
        mnt_path = file_func.getTempDirname(auto_create=True)
        mount_result = mountNfsResource(url=download_url, mnt=mnt_path, *args, **kwargs)
        mounted = True
    else:
        mount_result = True
        mounted = False

    if mount_result:
        if os.path.exists(mnt_path):
            mnt_res_path = mnt_path
            if sys_func.isWindowsPlatform() and mnt_res_path.endswith(':'):
                mnt_res_path += os.path.sep
            src_filename = os.path.join(mnt_res_path, filename)

            dst_file_path = dst_path
            if sys_func.isWindowsPlatform() and dst_file_path.endswith(':'):
                dst_file_path += os.path.sep
            dst_filename = os.path.join(dst_file_path, os.path.basename(filename))
            result = file_func.copyFile(src_filename=src_filename, dst_filename=dst_filename, rewrite=rewrite)
        else:
            log_func.warning(u'NFS resource mount path <%s> not found' % mnt_path)

    if mounted:
        umountNfsResource(mnt=mnt_path, auto_delete=True, *args, **kwargs)
    return result


def uploadNfsFile(upload_url=None, filename=None, dst_path=None, rewrite=True, mnt_path=None, *args, **kwargs):
    """
    Upload file to NFS resource.

    :param upload_url: NFS resource URL.
        For example:
        'nfs://SAFE/Backup'
    :param filename: Source file name.
        For example:
        '/home/user/2017/FDOC/RC001.DCM'
    :param dst_path: NFS resource path to save the file.
    :param rewrite: Overwrite a file if it already exists?
    :param mnt_path: Mount path in the case of an already NFS resource is mounted.
    :return: True/False.
    """
    result = False

    if not os.path.exists(filename):
        log_func.warning(u'Source file <%s> for upload to NFS resource not found' % filename)
        return result

    if mnt_path is None:
        mnt_path = file_func.getTempDirname(auto_create=True) if sys_func.isLinuxPlatform() else DEFAULT_WINDOWS_NFS_DRIVE_NAME
        mount_result = mountNfsResource(url=upload_url, mnt=mnt_path, *args, **kwargs)
        mounted = True
    else:
        mount_result = True
        mounted = False

    if mount_result:
        if os.path.exists(mnt_path):
            mnt_res_path = mnt_path
            if sys_func.isWindowsPlatform() and mnt_res_path.endswith(':'):
                mnt_res_path += os.path.sep
            dst_filename = os.path.join(mnt_res_path, dst_path, os.path.basename(filename))
            result = file_func.copyFile(src_filename=filename, dst_filename=dst_filename, rewrite=rewrite)
        else:
            log_func.warning(u'NFS resource mount path <%s> not found' % mnt_path)

    if mounted:
        # Options only for mount
        if 'options' in kwargs:
            del kwargs['options']
        umountNfsResource(mnt=mnt_path, auto_delete=True, *args, **kwargs)
    return result
