#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions of working with files on shared SAMBA resources.

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
import smbclient
import urllib.parse
import locale
import datetime

from . import log_func
from . import file_func

__version__ = (0, 0, 0, 1)


DEFAULT_WORKGROUP = 'WORKGROUP'
ANONYMOUS_USERNAME = 'guest'


def splitSmbUrlPath(smb_url):
    """
    Correct breakdown of the SMB resource URL path into components.
    If the <#> character occurs in the path, the URL parsing library perceives further
    standing characters as fragment. This should be taken into account.
    This is what this function is designed for.

    :param smb_url: urlparse.ParseResult object.
    :return: List of elements of the path to the SMB resource.
    """
    path_list = smb_url.path.split(os.path.sep)
    if smb_url.fragment:
        fragment_path_list = smb_url.fragment.split(os.path.sep)
        fragment_path_list[0] = u'#' + fragment_path_list[0]
        path_list += fragment_path_list
    return path_list


def getSmbPathFromUrl(url):
    """
    Determine the path to the SMB resource by URL.

    :param url: Samba resource URL.
    :return: Samba resource path.
    """
    url = urllib.parse.urlparse(url)
    path_list = splitSmbUrlPath(url)
    path_list = path_list[2:]
    smb_path = os.path.join(*path_list)
    return smb_path


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
            download_file = os.path.join(*path_list)

            log_func.info(u'Download file <%s>' % download_file)

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

            # Attention! smbclient library glitch found:
            # Large files may disappear from the file list.
            # Therefore, we do not check for the existence of a file in an SMB resource,
            # but immediately try to download it.
            try:
                smb.download(download_file, dst_filename)
                log_func.info(u'File <%s> is downloaded' % download_file)
                result = True
            except:
                log_func.warning(u'''If an error occurs in smbclient
perhaps the problem is in the library itself pysmbclient.
Decision:
    In file /usr/local/lib/pythonX.X/dist-packages/smbclient.py
    in the function call subprocess.Popen() remove the parameter <shell=True> 
    or set to False.
                ''')
                log_func.fatal(u'SMB. Error download SMB fail <%s>' % download_file)
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


def connectSmb(url):
    """
    Connect to samba resource.

    :param url: Samba resource URL.
    :return: SAMBA resource object or None if error.
    """
    smb = None
    try:
        smb_url = urllib.parse.urlparse(url)
        download_server = smb_url.hostname
        download_share = smb_url.path.split(os.path.sep)[1]
        # If the user is not specified, then we log in
        download_username = smb_url.username if smb_url.username else ANONYMOUS_USERNAME
        download_password = smb_url.password

        smb = smbclient.SambaClient(server=download_server,
                                    share=download_share,
                                    username=download_username,
                                    password=download_password,
                                    domain=DEFAULT_WORKGROUP)

        log_func.info(u'SMB resource connected')
        log_func.info(u'\tHost <%s>' % download_server)
        log_func.info(u'\tPath <%s>' % download_share)
        log_func.info(u'\tUsername <%s>' % download_username)
        log_func.info(u'\tURL <%s>' % str(url))
    except:
        log_func.fatal(u'Error connect to samba resource. URL <%s>' % str(url))
    return smb


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

    smb_path = getSmbPathFromUrl(url)
    try:
        if smb is not None:
            # The resource is already open
            filenames = smb.listdir(smb_path)
        else:
            try:
                smb = connectSmb(url)
                filenames = smb.listdir(smb_path)
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error get samba resource filenames. URL <%s>' % url)
    except:
        log_func.fatal(u'Error get samba resource filenames')

    # Attention! There may be an error in getting the correct file names in the smbclient library:
    # At the end of the file name is added '                           N'
    # Here we are trying to level this error
    filenames = [filename.strip('                           N').strip() for filename in filenames]
    # log.debug(u'SMB. Filenames %s' % str(filenames))
    if filename_pattern:
        filenames = [filename for filename in filenames if fnmatch.fnmatch(filename, filename_pattern)]
        # log.debug(u'SMB. Filtered filenames %s' % str(filenames))
    return filenames


DEFAULT_SMB_DATETIME_FMT = '%a %b %d %H:%M:%S %Y'


def _str_datetime2datetimeSmb(str_datetime, set_locale=False):
    """
    Convert time from string variant to datetime.

    :param str_datetime: Time in string form.
        For example: 'Thu Mar  3 23:05:25 2005'.
    :param set_locale: Set the system locale?
    :return: datetime.datetime or None if error.
    """
    if set_locale:
        # To convert the time correctly, you need to set the system locale
        locale.setlocale(locale.LC_ALL, '')

    try:
        # Deleting information about the time zone
        str_datetime = str_datetime[:-str_datetime[::-1].index(' ') - 1]
        return datetime.datetime.strptime(str_datetime, DEFAULT_SMB_DATETIME_FMT)
    except:
        log_func.fatal(u'Error convert <%s> to datetime' % str_datetime)
    return None


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
    try:
        if smb is not None:
            # The resource is already open
            file_info = smb.info(filename)
        else:
            try:
                smb = connectSmb(url)
                file_info = smb.info(filename)
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error get samba file information. URL <%s>' % url)
    except:
        log_func.fatal(u'Error get samba file <%s> information' % filename)

    if to_datetime:
        # We immediately convert the time from the string representation to datetime
        # To convert the time correctly, you need to set the locale
        locale.setlocale(locale.LC_ALL, '')

        if 'create_time' in file_info:
            file_info['create_time'] = _str_datetime2datetimeSmb(file_info['create_time'])
        if 'access_time' in file_info:
            file_info['access_time'] = _str_datetime2datetimeSmb(file_info['access_time'])
        if 'write_time' in file_info:
            file_info['write_time'] = _str_datetime2datetimeSmb(file_info['write_time'])
        if 'change_time' in file_info:
            file_info['change_time'] = _str_datetime2datetimeSmb(file_info['change_time'])

    return file_info


def isSmbDir(url=None, path=None, smb=None):
    """
    Checking that the file object is a directory.

    :param url: Samba resource URL.
    :param path: Name of the file object. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    is_dir = None
    try:
        if smb is not None:
            # The resource is already open
            is_dir = smb.isdir(path)
        else:
            try:
                smb = connectSmb(url)
                is_dir = smb.isdir(path)
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error check samba directory <%s>. URL <%s>' % (path, url))
    except:
        log_func.fatal(u'Error check samba directory <%s>' % path)

    return is_dir


def isSmbFile(url=None, path=None, smb=None):
    """
    Checking that the file object is a file.

    :param url: Samba resource URL.
    :param path: Name of the file object. For example: /2019/TEST.DBF
    :param smb: The samba object of the resource in the case of an already open resource.
    :return: True/False.
    """
    is_file = None
    try:
        if smb is not None:
            # The resource is already open
            is_file = smb.isfile(path)
        else:
            try:
                smb = connectSmb(url)
                is_file = smb.isfile(path)
                disconnectSmb(smb)
            except:
                disconnectSmb(smb)
                log_func.fatal(u'Error check samba file <%s>. URL <%s>' % (path, url))
    except:
        log_func.fatal(u'Error check samba file <%s>' % path)

    return is_file
