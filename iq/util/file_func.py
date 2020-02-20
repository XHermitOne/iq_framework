#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File functions module.
"""

import os
import os.path

from . import log_func
from . import global_func
from .. import config

__version__ = (0, 0, 0, 1)

HIDDEN_DIRNAMES = ('.svn', '.git', '.idea', '__pycache__')


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
    return [dirname for dirname in os.listdir(path) if os.path.isfile(os.path.join(path,
                                                            dirname)) and dirname not in HIDDEN_DIRNAMES]


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
            log_func.error(u'Not define path')
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
    return config.get_cfg_param('PROFILE_PATH')


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


def setFilenameExt(filename, ext):
    """
    Set filename extension.

    :param filename: File name.
    :param ext: File name extension.
    :return: New filename with new extension.
    """
    return os.path.splitext(filename)[0] + ext
