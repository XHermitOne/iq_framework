#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File functions module.
"""

import stat
import os
import os.path
import tempfile
import platform
import hashlib
import shutil
import glob
import pathlib

from . import log_func
from . import global_func
from .. import global_data

__version__ = (0, 2, 3, 1)

HIDDEN_DIRNAMES = ('.svn', '.git', '.idea', '__pycache__')

ALTER_HOME_DIRNAME = '~'
ALTER_CUR_DIRNAME = '.'
ALTER_PARENT_DIRNAME = '..'

ALTER_HOME_DIRNAME_SEP = ALTER_HOME_DIRNAME + os.sep
ALTER_CUR_DIRNAME_SEP = ALTER_CUR_DIRNAME + os.sep
ALTER_PARENT_DIRNAME_SEP = ALTER_PARENT_DIRNAME + os.sep

BACKUP_FILENAME_EXT = '.bak'

FILE_MODE777 = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH


def getDirectoryNames(path):
    """
    Get directory names in path.

    :param path: Path.
    :return: Directory name list.
    """
    return [dirname for dirname in os.listdir(path) if os.path.isdir(os.path.join(path,
                                                            dirname)) and dirname not in HIDDEN_DIRNAMES]


def getDirectoryPaths(path):
    """
    Get directory paths in path.

    :param path: Path.
    :return: Directory path list.
    """
    return [os.path.join(path,
                         dirname) for dirname in os.listdir(path) if os.path.isdir(os.path.join(path,
                         dirname)) and dirname not in HIDDEN_DIRNAMES]


def getFileNames(path):
    """
    Get file names in path.

    :param path: Path.
    :return: Directory name list.
    """
    try:
        return [dirname for dirname in os.listdir(path) if os.path.isfile(os.path.join(path,
                                                                                       dirname)) and dirname not in HIDDEN_DIRNAMES]
    except:
        log_func.fatal(u'Error get filenames in <%s>' % path)
    return list()


def getFilePaths(path):
    """
    Get file paths in path.

    :param path: Path.
    :return: Directory path list.
    """
    return [os.path.join(path,
                         dirname) for dirname in os.listdir(path) if os.path.isfile(os.path.join(path,
                                                                                    dirname)) and dirname not in HIDDEN_DIRNAMES]


def getAbsolutePath(path, cur_dir=None):
    """
    Get absolute path relative to the directory.

    :param path: Path.
    :param cur_dir: Current directory.
    """
    try:
        if not path:
            log_func.warning(u'Not define path')
            return None

        if not isinstance(path, str):
            log_func.warning(u'Not valid path <%s : %s>' % (str(path), type(path)))
            return path

        if global_func.getProjectName():
            cur_dir = getCurDirPrj(cur_dir)
            if cur_dir:
                path = os.path.abspath(path.replace('.%s' % os.path.sep, cur_dir).strip())
        else:
            path = os.path.abspath(path)
        return path
    except:
        log_func.fatal(u'Define absolute path error <%s>. Current directory <%s>' % (path, cur_dir))
    return path


def getProjectPath():
    """
    Get project path.

    :return: Full project path or None if error.
    """
    prj_name = global_func.getProjectName()
    if prj_name:
        framework_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(framework_path, prj_name)
    else:
        log_func.warning(u'Error get project path')
    return None


def getFrameworkPath():
    """
    Get framework path.

    :return: Full framework path or None if error.
    """
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if path and os.path.exists(path):
        return path
    else:
        log_func.warning(u'Error get framework path')
    return None


def getProfilePath():
    """
    Get profile directory path.
    """
    return global_data.getGlobal('PROFILE_PATH')


def getProjectProfilePath():
    """
    Get project profile directory path.
    """
    prj_name = global_func.getProjectName()
    profile_path = os.path.join(global_data.getGlobal('PROFILE_PATH'), prj_name if prj_name else '')
    if profile_path and not os.path.exists(profile_path):
        createDir(profile_path)
    return profile_path


def getCurDirPrj(path=None):
    """
    Get current path relative to the project directory.
    """
    if path is None:
        try:
            prj_dir = getProjectPath()
            if prj_dir:
                path = os.path.dirname(prj_dir)
            else:
                path = getProfilePath()
        except:
            log_func.fatal(u'Define current project path error <%s>' % path)
            path = os.getcwd()

    if path[-1] != os.path.sep:
        path += os.path.sep
    return path


def getFilenameExt(filename):
    """
    Get filename extension.

    :param filename: File name.
    :return: File name extension.
    """
    return os.path.splitext(filename)[1]


def isFilenameExt(filename, ext):
    """
    Verify filename extension.

    :param filename: File name.
    :param ext: File name extension.
    :return: True/False.
    """
    return getFilenameExt(filename) == ext


def isFilenameExts(filename, exts=()):
    """
    Verify filename extensions.

    :param filename: File name.
    :param exts: File name extensions list.
    :return: True/False.
    """
    return any([getFilenameExt(filename) == ext for ext in exts])


def setFilenameExt(filename, ext):
    """
    Set filename extension.

    :param filename: File name.
    :param ext: File name extension.
    :return: New filename with new extension or None if error.
    """
    return os.path.splitext(filename)[0] + ext


def getHomePath():
    """
    Home directory path.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        log_func.warning(u'OS <%s> not support' % os_platform)
        return None
    return os.path.normpath(home_path)


def getUserHomePath():
    """
    User home directory path.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'linux':
        if 'SUDO_USER' in os.environ:
            home_path = os.path.join('/home', os.environ['SUDO_USER'])
            return os.path.normpath(home_path)
    return getHomePath()


def getFileCheckSum(filename):
    """
    Calculation of the checksum of a file.

    :param filename: File name.
    :return: Check sum or None if error.
    """
    md5_obj = hashlib.md5()

    f = None
    try:
        f = open(filename, 'rb')
        data = f.read(1024)
        while data:
            md5_obj.update(data)
            data = f.read(1024)
        f.close()
    except:
        if f:
            f.close()
            f = None
        return None
    return md5_obj.hexdigest()


def isSameFile(first_filename, second_filename):
    """
    Check that file1 and file2 match.
    Validation is done by file size.

    :return: True/False.
    """
    if os.path.exists(first_filename) and os.path.exists(second_filename):
        file_size1 = os.path.getsize(first_filename)
        file_size2 = os.path.getsize(second_filename)
        if file_size1 != file_size2:
            return file_size1 == file_size2
        else:
            file1_check_sum = getFileCheckSum(first_filename)
            file2_check_sum = getFileCheckSum(second_filename)
            return file1_check_sum == file2_check_sum
    return False


def copyFile(src_filename, dst_filename, rewrite=True):
    """
    Make a copy of the file with a new name.

    :param src_filename: Source file name.
    :param dst_filename: Result file name.
    :param rewrite: Overwrite existing file?
    :return: True/False.
    """
    try:
        if not os.path.exists(src_filename):
            msg = u'Copy file <%s> -> <%s>. Source file <%s> not found' % (src_filename, dst_filename, src_filename)
            log_func.warning(msg)
            return False

        if os.path.exists(src_filename) and src_filename == dst_filename:
            log_func.warning(u'Unable to copy file to itself <%s> ' % src_filename)
            return False

        dst_dirname = os.path.dirname(dst_filename)
        try:
            if dst_dirname and not os.path.exists(dst_dirname):
                os.makedirs(dst_dirname)
                log_func.info(u'Create folder <%s>' % dst_dirname)
        except OSError:
            log_func.fatal(u'Error make directory <%s>' % dst_dirname)

        if not rewrite:
            if os.path.exists(dst_filename):
                log_func.warning(u'File <%s> exists. Overwrite prohibited' % dst_filename)
                return False
        else:
            if os.path.exists(dst_filename):
                os.remove(dst_filename)
                log_func.info(u'Remove file <%s>' % dst_filename)

        if os.path.exists(src_filename) and os.path.exists(dst_filename) and os.path.samefile(src_filename, dst_filename):
            log_func.warning(u'Attempting to copy a file to itself <%s>' % src_filename)
        else:
            shutil.copyfile(src_filename, dst_filename)
            log_func.info(u'Copy file <%s> to <%s>' % (src_filename, dst_filename))
        return True
    except:
        log_func.fatal(u'Error copy file <%s> -> <%s>' % (src_filename, dst_filename))
        return False


def renameFile(filename, new_filename):
    """
    Rename file.

    :param filename: Source filename.
    :param new_filename: New filename.
    :return: True/False.
    """
    result = copyFile(src_filename=filename, dst_filename=new_filename, rewrite=True)
    result = result and removeFile(filename)
    return result


def changeFileExt(filename, new_ext, create_copy=False):
    """
    Change file extension.

    :param filename: Full filename.
    :param new_ext: New extension.
    :param create_copy: Create copy file with new extension?
    :return: True/False.
    """
    new_filename = setFilenameExt(filename, new_ext)
    if create_copy:
        return copyFile(filename, new_filename)
    else:
        return renameFile(filename, new_filename)


def copyToDir(src_filename, dst_dirname, rewrite=True):
    """
    Make a copy of the file in destination directory.

    :param src_filename: Source file name.
    :param dst_dirname: Destination directory name.
    :param rewrite: Overwrite existing file?
    :return: True/False.
    """
    base_filename = os.path.basename(src_filename)
    dst_filename = os.path.join(dst_dirname, base_filename)
    return copyFile(src_filename=src_filename, dst_filename=dst_filename, rewrite=rewrite)


def getFilesByMask(filename_mask):
    """
    List of files by mask.

    :param filename_mask: File mask. For example /home/user/tmp/*.pyc.
    :return: File path list or empty list if error
    """
    try:
        if isinstance(filename_mask, str):
            dir_path = os.path.dirname(filename_mask)
            if os.path.exists(dir_path):
                filenames = glob.glob(pathname=filename_mask, recursive=False)
                return [os.path.abspath(file_name) for file_name in filenames]
            else:
                log_func.warning(u'Folder <%s> not found. to determine the list of files by mask <%s>' % (dir_path, filename_mask))
        elif isinstance(filename_mask, tuple) or isinstance(filename_mask, list):
            filenames = list()
            for file_mask in filename_mask:
                filenames = glob.glob(pathname=filename_mask, recursive=False)
                filenames += [os.path.abspath(file_name) for file_name in filenames]
            return filenames
        else:
            log_func.warning(u'Error type mask <%s>' % filename_mask)
    except:
        log_func.fatal(u'Error define file list by mask <%s>' % str(filename_mask))
    return list()


def deleteFile(filename, make_backup=False):
    """
    Delete file.

    :param filename: Filename.
    :param make_backup: Make backup file?
    :return: True/False.
    """
    try:
        if make_backup:
            bak_filename = setFilenameExt(filename, BACKUP_FILENAME_EXT)
            return renameFile(filename, bak_filename)
        else:
            return removeFile(filename)
    except:
        log_func.fatal(u'Error delete file <%s>' % filename)
    return False


def delFilesByMask(delete_dir, *mask_filters):
    """
    Delete all files from a folder filtered by file mask.
    Delete recursively by subdirectory.

    :param delete_dir: Source folder.
    :param mask_filters: List of file masks to be deleted.
        For example '*.pyc'.
    """
    try:
        subdirs = getSubDirs(delete_dir)
        if subdirs:
            for sub_dir in subdirs:
                delFilesByMask(sub_dir, *mask_filters)
        for file_mask in mask_filters:
            del_files = getFilesByMask(os.path.join(delete_dir, file_mask))
            for del_file in del_files:
                os.remove(del_file)
                log_func.info(u'File <%s> deleted' % del_file)
        return True
    except:
        log_func.fatal(u'Error delete files by mask <%s> from folder <%s>' % (str(mask_filters), delete_dir))
    return False


def getSubDirs(dir_path):
    """
    The function returns a list of subdirectories.

    :param dir_path: Directory path.
    :return: subdirectories or None if error.
    """
    try:
        if not os.path.exists(dir_path):
            log_func.warning(u'Directory <%s> not found' % dir_path)
            return list()
        dir_list = [os.path.join(dir_path, cur_name) for cur_name in os.listdir(dir_path)]
        dir_list = [cur_path for cur_path in dir_list if os.path.isdir(cur_path)]
        return dir_list
    except:
        log_func.fatal(u'Error get subdirectories <%s>' % dir_path)
    return None


def removeFile(filename):
    """
    Remove file.

    :param filename: Removed filename.
    :return: True/False.
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
            log_func.info(u'Remove file <%s>' % filename)
            return True
        else:
            log_func.warning(u'File <%s> not found for removing' % filename)
    except:
        log_func.fatal(u'Error remove file <%s>' % filename)
    return False


def removeDir(folder):
    """
    Delete directory.

    :param folder: Removed folder.
    :return: True/False.
    """
    try:
        shutil.rmtree(folder, ignore_errors=True)
        log_func.info(u'Remove directory <%s>' % folder)
        return True
    except:
        log_func.fatal(u'Error remove directory <%s>' % folder)
    return False


def getFileModifyDatetime(filename):
    """
    Date-time of file modification.

    :param filename: Full filename.
    :return: Date-time of file change or None in case of error.
    """
    if not os.path.exists(filename):
        log_func.warning(u'Get file modify datetime. File <%s> not found' % filename)
        return None

    try:
        if platform.system() == 'Windows':
            return os.path.getmtime(filename)
        else:
            stat = os.stat(filename)
            return stat.st_mtime
    except:
        log_func.fatal(u'Error determining date-time of file modification <%s>' % filename)
    return None


def getProjectSettingsFilename():
    """
    Get project settings filename.

    :return: Project settings file name or None if error.
    """
    prj_path = getProfilePath()
    prj_name = global_func.getProjectName()

    if prj_path and prj_name:
        return os.path.join(prj_path, '%s.ini' % prj_name)
    else:
        log_func.warning(u'Not define project')
    return None


def createDir(dirname):
    """
    Create directory if not exists.

    :param dirname: Dir path.
    :return: True/False.
    """
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            log_func.info(u'Create directory <%s>' % dirname)
            return True
    except:
        log_func.fatal(u'Error create directory <%s>' % dirname)
    return False


def getNormalPath(path):
    """
    Get normal path.

    :param path: Path
    :return: Normal path.
    """
    try:
        if path.startswith(ALTER_PARENT_DIRNAME_SEP):
            return os.path.normpath(os.path.join(os.path.dirname(os.getcwd()),
                                                 path.lstrip(ALTER_PARENT_DIRNAME_SEP)))
        elif path.startswith(ALTER_CUR_DIRNAME_SEP):
            return os.path.normpath(os.path.join(os.getcwd(),
                                                 path.lstrip(ALTER_CUR_DIRNAME_SEP)))
        elif path.startswith(ALTER_HOME_DIRNAME_SEP):
            return os.path.normpath(os.path.join(getHomePath(),
                                                 path.lstrip(ALTER_HOME_DIRNAME_SEP)))
        return os.path.normpath(path)
    except:
        log_func.fatal(u'Error normal path <%s>' % path)
    return path


def getRelativePath(path):
    """
    Get relative path.

    :param path: Path.
    :return: Relative path.
    """
    try:
        path = os.path.normpath(path)

        cur_path = os.getcwd()
        if path.startswith(cur_path):
            return path.replace(cur_path, ALTER_CUR_DIRNAME)

        parent_path = os.path.dirname(os.getcwd())
        if path.startswith(parent_path):
            return path.replace(parent_path, ALTER_PARENT_DIRNAME)

        home_path = getHomePath()
        if path.startswith(home_path):
            return path.replace(home_path, ALTER_HOME_DIRNAME)

        return path
    except:
        log_func.fatal(u'Error relative path <%s>' % path)
    return path


def getTempDirname(auto_create=False):
    """
    Get temp dirname.

    :param auto_create: Auto create temp directory?
    :return: Temp dirname or None if error.
    """
    tmp_dirname = None
    try:
        tmp_dirname = tempfile.mktemp()
        if auto_create and not os.path.exists(tmp_dirname):
            os.makedirs(tmp_dirname)
        return tmp_dirname
    except:
        log_func.fatal(u'Error get temp dirname <%s>' % tmp_dirname)
    return None


def getTempFilename(to_path=None):
    """
    Get temp filename.

    :param to_path: Locate temp file to path.
    :return: Temp filename or None if error.
    """
    tmp_filename = None
    try:
        tmp_filename = tempfile.mktemp(dir=to_path) if to_path is not None else tempfile.mktemp()
        return tmp_filename
    except:
        log_func.fatal(u'Error get temp filename <%s>' % tmp_filename)
    return None


def getPrjProfileTempFilename():
    """
    Get temp filename in project profile path.

    :return: Temp filename or None if error.
    """
    return getTempFilename(to_path=getProjectProfilePath())


def extractProjectNameFromPath(path):
    """
    Extract project name from path. If path not in framework folder then return THIS.

    :param path: Path for exctract.
    :return: Project name or THIS.
    """
    path = getAbsolutePath(path)
    framework_path = getFrameworkPath()
    if path.startswith(framework_path):
        path = path.replace(framework_path, '')
        path_parts = pathlib.Path(path).parts
        if path_parts:
            return path_parts[0] if path_parts[0] != os.path.sep else path_parts[1]
    return 'THIS'


def isEmptyFolder(path):
    """
    Checking for an empty folder.

    :param path: Folder path.
    :return: True/False.
    """
    return not bool(os.listdir(path))


def clearFolder(folder, del_subfolders=False):
    """
    Deleting all files from a folder. Deletion is recursive by subdirectories.

    :param folder: Source folder.
    :param del_subfolders: Delete subfolders?
    :return: True/False.
    """
    try:
        result = delFilesByMask(folder, '*.*')
        if del_subfolders:
            subdirs = getSubDirs(folder)
            if subdirs:
                for subdir in subdirs:
                    shutil.rmtree(subdir, ignore_errors=True)
    except:
        log_func.fatal(u'Error clear folder <%s>' % folder)
        result = False
    return result

def setChmod(filename, mode=None):
    """
    Set chmod.

    :param filename: File name.
    :param mode: File mode bits. If None then set 777 mode.
    :return: True/False.
    """
    if mode is None:
        mode = FILE_MODE777

    if os.path.exists(filename):
        try:
            os.chmod(filename, mode=mode)
            log_func.info(u'Set file <%s> mode [%o]' % (filename, mode))
            return True
        except:
            log_func.fatal(u'Error set chmod as 777 file <%s>' % filename)
    return False


def getFileSize(filename):
    """
    Get file size

    :param filename: File name.
    :return: File size.
    """
    if os.path.exists(filename):
        return os.path.getsize(filename)
    else:
        log_func.warning(u'File <%s> not found for get size' % filename)
    return 0
