#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cross-platform functions of working with files on shared SAMBA resources.

URL SMB resource format:
smb://[[<domain>;]<username>[:<password>]@]<server>[:<port>][/[<share>[/[<path>]]]

For example:
smb://workgroup;user:password@server/share/folder/file.txt
"""

import os
import os.path
import tempfile
import fnmatch
import shutil
import urllib.parse
import urllib.request

from . import log_func
from . import file_func
from . import sys_func
from . import net_func
from . import dt_func

try:
    from smb.SMBConnection import SMBConnection
except ImportError:
    log_func.error('Import error pysmb. For install: pip3 install --break-system-packages --user pysmb', is_force_print=True)

__version__ = (0, 0, 2, 1)


DEFAULT_WORKGROUP = 'WORKGROUP'
ANONYMOUS_USERNAME = 'guest'
URL_SEPARATOR = '/'


def splitSmbUrlPath(smb_url):
    """
    Correct breakdown of the SMB resource URL path into components.
    If the <#> character occurs in the path, the URL parsing library perceives further
    standing characters as fragment. This should be taken into account.
    This is what this function is designed for.

    :param smb_url: urlparse.ParseResult object.
    :return: List of elements of the path to the SMB resource.
    """
    path_list = smb_url.path.split(URL_SEPARATOR)
    if smb_url.fragment:
        fragment_path_list = smb_url.fragment.split(URL_SEPARATOR)
        fragment_path_list[0] = u'#' + fragment_path_list[0]
        path_list += fragment_path_list
    return path_list


def getSmbPathFromUrl(url):
    """
    Get path to the SMB resource by URL.

    :param url: Samba resource URL.
    :return: Samba resource path.
    """
    url = urllib.parse.urlparse(url)
    path_list = splitSmbUrlPath(url)
    path_list = path_list[2:]
    try:
        pathname = os.path.join(*path_list) if path_list else ''
        smb_path = urllib.request.pathname2url(pathname)
    except TypeError:
        log_func.fatal(u'Error get SMB path from url %s. Path list %s' % (str(url), str(path_list)))
        smb_path = ''
    return smb_path


def getSmbShareFromUrl(url):
    """
    Get share to the SMB resource by URL.

    :param url: Samba resource URL.
    :return: Samba resource path.
    """
    smb_url = urllib.parse.urlparse(url)
    smb_share = smb_url.path.split(URL_SEPARATOR)[1] if smb_url.path.split(URL_SEPARATOR) else ''
    return smb_share


def connectSmb(url):
    """
    Connect to samba resource.

    :param url: Samba resource URL.
    :return: SAMBA resource object or None if error.
    """
    smb_connection = None
    try:
        smb_url = urllib.parse.urlparse(url)
        smb_server = smb_url.hostname if smb_url.hostname is not None else ''
        if not smb_server:
            log_func.warning(u'Samba server not defined')
            return None
        smb_server_ip = net_func.getIpByHostName(smb_server)

        smb_share = smb_url.path.split(URL_SEPARATOR)[1]
        # If the user is not specified, then we log in
        smb_username = smb_url.username if smb_url.username else ANONYMOUS_USERNAME
        smb_password = smb_url.password if smb_url.password is not None else ''
        localhost_name = sys_func.getLocalhostName()

        smb_connection = SMBConnection(username=smb_username,
                                       password=smb_password,
                                       my_name=localhost_name,
                                       remote_name=smb_server)
        assert smb_connection.connect(smb_server_ip, 139)

        log_func.info(u'SMB resource connected')
        log_func.info(u'\tHost <%s>' % smb_server)
        log_func.info(u'\tPath <%s>' % smb_share)
        log_func.info(u'\tUsername <%s>' % smb_username)
        log_func.info(u'\tURL <%s>' % str(url))
    except:
        log_func.fatal(u'Error connect to samba resource. URL <%s>' % str(url))
    return smb_connection


def disconnectSmb(smb):
    """
    Samba resource disconnect.

    :param smb: SAMBA resource object.
    :return: True/False.
    """
    try:
        if smb:
            log_func.info(u'SMB resource disconnected')
            smb.close()
            return True
    except:
        log_func.fatal(u'Error disconnect samba resource')
    return False


def getSmbListdirFilenames(url=None, filename_pattern=None, smb=None):
    """
    List of SMB resource files.

    :param url: Samba resource URL.
    :param filename_pattern: Select the file names according to the specified pattern.
        For example: *.DBF.
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: List of samba resource file names.
        The function returns only file names.
        Folder names are not included in the list.
    """
    filenames = list()

    if url is None:
        log_func.warning(u'The URL of the samba resource for determining the list of files is not specified')
        return filenames

    smb_share = getSmbShareFromUrl(url)
    smb_path = getSmbPathFromUrl(url)
    try:
        if smb is not None:
            # The resource is already open
            filenames = [shared_file.filename for shared_file in smb.listPath(smb_share, smb_path) if shared_file.isNormal]
        else:
            try:
                smb = connectSmb(url)
                filenames = [shared_file.filename for shared_file in smb.listPath(smb_share, smb_path) if shared_file.isNormal]
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error get samba resource filenames. URL <%s>' % url)
    except:
        log_func.fatal(u'Error get samba resource filenames')

    # log.debug(u'SMB. Filenames %s' % str(filenames))
    if filename_pattern:
        filenames = [filename for filename in filenames if fnmatch.fnmatch(filename, filename_pattern)]
        # log.debug(u'SMB. Filtered filenames %s' % str(filenames))
    return filenames


def getSmbSharedFile(url=None, filename=None, smb=None):
    """
    Get shared file object.

    :param url: Samba resource URL.
    :param filename: File name. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: smb.base.SharedFile or None if error.
    """
    smb_shared_file = None
    smb_share = getSmbShareFromUrl(url)
    smb_path = getSmbPathFromUrl(url)
    try:
        pathname = os.path.join(smb_path, os.path.dirname(filename))
        smb_path = urllib.request.pathname2url(pathname)
        smb_base_filename = os.path.basename(filename)
        if smb is not None:
            # The resource is already open
            shared_files = [shared_file for shared_file in smb.listPath(smb_share, smb_path) if shared_file.filename == smb_base_filename]
            if not shared_files:
                log_func.warning(u'SMB. File <%s> not found. URL <%s>' % (filename, url))
                return None
            smb_shared_file = shared_files[0]
        else:
            try:
                smb = connectSmb(url)
                shared_files = [shared_file for shared_file in smb.listPath(smb_share, smb_path) if
                                shared_file.filename == smb_base_filename]
                if not shared_files:
                    log_func.warning(u'SMB. File <%s> not found. URL <%s>' % (filename, url))
                else:
                    smb_shared_file = shared_files[0]
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error get samba shared file. URL <%s>' % url)
    except:
        log_func.fatal(u'Error get samba shared file <%s>' % filename)
    return smb_shared_file


def getSmbFileInfo(url=None, filename=None, smb=None, to_datetime=True):
    """
    Get all the information about the file in the form of a structure.

    :param url: Samba resource URL.
    :param filename: File name. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :param to_datetime: Convert the time from string representation to datetime immediately?
    :return: File information:
        {
            'create_time': File creation time,
            'access_time': The time of the last access to the file,
            'write_time': File saving time,
            'change_time': File modification time,
            ...
        }
    """
    file_info = dict()
    smb_shared_file = getSmbSharedFile(url=url, filename=filename, smb=smb)
    if smb_shared_file is not None:
        file_info = dict(create_time=dt_func.time2datetime(smb_shared_file.create_time) if to_datetime else smb_shared_file.create_time,
                         access_time=dt_func.time2datetime(smb_shared_file.last_access_time) if to_datetime else smb_shared_file.last_access_time,
                         write_time=dt_func.time2datetime(smb_shared_file.last_write_time) if to_datetime else smb_shared_file.last_write_time,
                         change_time=dt_func.time2datetime(smb_shared_file.last_attr_change_time) if to_datetime else smb_shared_file.last_attr_change_time,
                         file_size=smb_shared_file.file_size,
                         )

    return file_info


def deleteSmbFile(url=None, filename=None, smb=None):
    """
    Delete remote samba file.

    :param url: Samba resource URL.
    :param filename: File name. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    result = False
    smb_share = getSmbShareFromUrl(url)
    smb_path = getSmbPathFromUrl(url)
    try:
        pathname = os.path.join(smb_path, os.path.dirname(filename))
        smb_path = urllib.request.pathname2url(pathname)
        smb_base_filename = os.path.basename(filename)
        if smb is not None:
            # The resource is already open
            smb.deleteFiles(smb_share, smb_path + smb_base_filename)
            result = True
        else:
            try:
                smb = connectSmb(url)
                smb_filename = smb_path + smb_base_filename
                smb.deleteFiles(smb_share, smb_filename)
                log_func.debug(u'SMB. Delete <%s> file' % smb_filename)
                result = True
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error delete samba file. URL <%s>' % url)
    except:
        log_func.fatal(u'Error delete samba file <%s>' % filename)
    return result


def isSmbDir(url=None, path=None, smb=None):
    """
    Checking that the file object is a directory.

    :param url: Samba resource URL.
    :param path: Name of the file object. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    smb_shared_file = getSmbSharedFile(url=url, filename=path, smb=smb)
    is_dir = smb_shared_file.isDirectory
    return is_dir


def isSmbFile(url=None, path=None, smb=None):
    """
    Checking that the file object is a file.

    :param url: Samba resource URL.
    :param path: Name of the file object. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    smb_shared_file = getSmbSharedFile(url=url, filename=path, smb=smb)
    is_file = not smb_shared_file.isDirectory
    return is_file


def existsSmbPath(url=None, path=None, smb=None):
    """
    Checking that the exists path.

    :param url: Samba resource URL.
    :param path: Name of the file object. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    exists = False
    smb_share = getSmbShareFromUrl(url)
    smb_path = getSmbPathFromUrl(url)
    try:
        pathname = os.path.join(smb_path, os.path.dirname(path))
        smb_path = urllib.request.pathname2url(pathname)
        smb_base_filename = os.path.basename(path)
        if smb is not None:
            # The resource is already open
            shared_files = [shared_file for shared_file in smb.listPath(smb_share, smb_path) if shared_file.filename == smb_base_filename]
            exists = bool(shared_files)
        else:
            try:
                smb = connectSmb(url)
                shared_files = [shared_file for shared_file in smb.listPath(smb_share, smb_path) if
                                shared_file.filename == smb_base_filename]
                exists = bool(shared_files)
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error exists samba path. URL <%s>' % url)
    except:
        log_func.fatal(u'Error exists samba path <%s>' % path)
    return exists


def downloadSmbFile(download_urls=None, filename=None, dst_path=None, rewrite=True, smb=None):
    """
    Find and download a file.

    :param download_urls: List of file search URLs.
        For example:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        The parameter can be set as a string. In this case, we assume that the URL is one.
    :param filename: Relative file name.
        For example:
        '/2017/FDOC/RC001.DCM'
    :param dst_path: The local path to save the file.
    :param rewrite: Overwrite a local file if it already exists?
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    if download_urls is None:
        log_func.warning(u'File search paths on SMB resources are not defined')
        return False
    elif isinstance(download_urls, str):
        # 1 URL
        download_urls = [download_urls]

    if dst_path is None:
        dst_path = file_func.getProjectProfilePath()

    result = False
    do_close = False
    for download_url in download_urls:
        try:
            if smb is None:
                smb = connectSmb(download_url)
                do_close = True

            # Get the names of uploaded files
            url = urllib.parse.urlparse(download_url)
            path_list = splitSmbUrlPath(url)
            if filename is None:
                filename = path_list[-1]
                log_func.debug(u'\tFile: <%s>' % filename)
                path_list = path_list[2:]
            else:
                path_list = path_list[2:] + [filename]
            pathname = os.path.join(*path_list)
            download_filename = urllib.request.pathname2url(pathname)

            log_func.info(u'Download file <%s>' % download_filename)

            dst_filename = os.path.join(dst_path, filename)
            if os.path.exists(dst_filename) and rewrite:
                log_func.info(u'Delete file <%s>' % dst_filename)
                try:
                    os.remove(dst_filename)
                except:
                    log_func.fatal(u'Error delete file <%s>' % dst_filename)
            dst_path = os.path.dirname(dst_filename)
            if not os.path.exists(dst_path):
                try:
                    os.makedirs(dst_path)
                    log_func.info(u'Create folder <%s>' % dst_path)
                except:
                    log_func.fatal(u'Error create folder <%s>' % dst_path)

            try:
                smb_share = getSmbShareFromUrl(download_url)
                with open(dst_filename, 'wb') as file_obj:
                    smb.retrieveFile(smb_share, download_filename, file_obj)
                log_func.info(u'File <%s> is downloaded' % download_filename)
                result = True
            except:
                log_func.fatal(u'SMB. Error download SMB file <%s>' % download_filename)
                result = False

            if do_close:
                disconnectSmb(smb)
            break
        except:
            if do_close:
                disconnectSmb(smb)
            log_func.fatal(u'Error download file <%s> from SMB resource <%s>' % (filename, download_url))
            result = False
    return result


def downloadAndRenameSmbFile(download_urls=None, filename=None, dst_filename=None, rewrite=True, smb=None):
    """
    Find and upload a file with renaming.

    :param download_urls: List of file search URLs.
        For example:
        ('smb://xhermit@SAFE/Backup/daily.0/Nas_pvz/smb/sys_bucks/Nas_pvz/NSI/',
         'smb://xhermit@TELEMETRIA/share/install/', ...
         )
        The parameter can be set as a string. In this case, we assume that the URL is one.
    :param filename: Relative file name.
        For example:
        '/2017/FDOC/RC001.DCM'
    :param dst_filename: New full name for saving the file.
    :param rewrite: Overwrite a local file if it already exists?
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    # First, just download the file
    tmp_path = tempfile.mktemp()
    result = downloadSmbFile(download_urls, filename, tmp_path, rewrite, smb)

    if result:
        new_filename = None
        try:
            # Successfully downloaded
            # Rename file
            new_filename = os.path.join(tmp_path, filename)
            file_func.copyFile(new_filename, dst_filename, rewrite)

            # After copying, delete the temporary directory
            shutil.rmtree(tmp_path, True)

            return True
        except:
            log_func.fatal(u'Error rename file <%s> -> <%s>' % (new_filename, dst_filename))

    return False
