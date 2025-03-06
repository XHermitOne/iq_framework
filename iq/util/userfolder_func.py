#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User folder functions module.
"""

import os
import os.path
import subprocess

from . import log_func

__version__ = (0, 0, 1, 1)

DEFAULT_MY_DOCUMENTS_FOLDER_NAME = 'Documents'
DEFAULT_MY_DOWNLOADS_FOLDER_NAME = 'Downloads'
DEFAULT_MY_DESKTOP_FOLDER_NAME = 'Desktop'
DEFAULT_MY_PICTURES_FOLDER_NAME = 'Pictures'
DEFAULT_MY_MUSIC_FOLDER_NAME = 'Music'
DEFAULT_MY_VIDEOS_FOLDER_NAME = 'Videos'


def getMyUserFolder(userfolder_name=DEFAULT_MY_DOCUMENTS_FOLDER_NAME):
    """
    Get My user folder path.

    :return: My user folder path.
    """
    try:
        if os.name == 'nt':
            return os.path.join(os.path.join(os.environ['USERPROFILE']), userfolder_name)
        else:
            userfolder_upper_name = userfolder_name.upper() if userfolder_name != DEFAULT_MY_DOWNLOADS_FOLDER_NAME else userfolder_name.upper()[:-1]
            userfolder_path = subprocess.check_output(['xdg-user-dir', userfolder_upper_name], universal_newlines=True).strip()
            if os.path.exists(userfolder_path):
                return userfolder_path
            else:
                log_func.warning(u'Not found my user folder <%s>' % userfolder_path)
    except:
        log_func.fatal(u'Error get my user folder <%s>' % userfolder_name)
    return ''


def getMyDocumentsFolder():
    """
    Get MyDocuments folder.

    :return: MyDocuments folder path.
    """
    return getMyUserFolder(DEFAULT_MY_DOCUMENTS_FOLDER_NAME)


def getMyDownloadsFolder():
    """
    Get MyDownloads folder.

    :return: MyDownloads folder path.
    """
    return getMyUserFolder(DEFAULT_MY_DOWNLOADS_FOLDER_NAME)


def getMyDesktopFolder():
    """
    Get MyDesktop folder.

    :return: MyDesktop folder path.
    """
    return getMyUserFolder(DEFAULT_MY_DESKTOP_FOLDER_NAME)


def getMyPicturesFolder():
    """
    Get MyPictures folder.

    :return: MyPictures folder path.
    """
    return getMyUserFolder(DEFAULT_MY_PICTURES_FOLDER_NAME)


def getMyMusicFolder():
    """
    Get MyMusic folder.

    :return: MyMusic folder path.
    """
    return getMyUserFolder(DEFAULT_MY_MUSIC_FOLDER_NAME)


def getMyVideosFolder():
    """
    Get MyVideos folder.

    :return: MyVideos folder path.
    """
    return getMyUserFolder(DEFAULT_MY_VIDEOS_FOLDER_NAME)
