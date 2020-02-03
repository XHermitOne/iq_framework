#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resource file functions module.
"""

import os
import os.path
import pickle

from . import log_func
from . import file_func

__version__ = (0, 0, 0, 1)


def loadResource(res_filename):
    """
    Load resource file.

    :param res_filename: Resource file path.
    """
    res_filename = file_func.getAbsolutePath(res_filename)
    struct = loadResourcePickle(res_filename)
    if struct is None:
        struct = loadResourceText(res_filename)
    if struct is None:
        log_func.warning(u'Resource file format error: <%s>.' % res_filename)
        return None
    return struct


def loadResourcePickle(res_filename):
    """
    Load resource file as Pickle.

    :param res_filename: Resource file path.
    """
    res_filename = file_func.getAbsolutePath(res_filename)
    if os.path.isfile(res_filename):
        f = None
        try:
            f = open(res_filename, 'rb')
            struct = pickle.load(f)
            f.close()
            return struct
        except:
            if f:
                f.close()
            log_func.fatal(u'Error load pickle resource file <%s>' % res_filename)
    else:
        log_func.warning(u'Pickle resource file <%s> not found' % res_filename)
    return None


def loadResourceText(res_filename):
    """
    Load resource file as text.

    :param res_filename: Resource file path.
    """
    res_filename = file_func.getAbsolutePath(res_filename)
    if os.path.isfile(res_filename):
        f = None
        try:
            f = open(res_filename, 'rt')
            txt = f.read().replace('\r\n', '\n')
            f.close()
            return eval(txt)
        except:
            if f:
                f.close()
            log_func.fatal(u'Error load text resource file <%s>' % res_filename)
    else:
        log_func.warning(u'Text resource file <%s> not found' % res_filename)
    return None


def saveResourcePickle(res_filename, resource_data):
    """
    Save resource file as Pickle.

    :param res_filename: Resource file path.
    :param resource_data: Resource data structure.
    :return: True/False.
    """
    res_filename = file_func.getAbsolutePath(res_filename)
    f = None
    try:
        dir_name = os.path.dirname(res_filename)
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except:
                log_func.fatal(u'Create path <%s> error' % dir_name)

        f = open(res_filename, 'wb')
        pickle.dump(resource_data, f)
        f.close()
        log_func.info(u'Pickle resource file <%s> saved' % res_filename)
        return True
    except:
        if f:
            f.close()
        log_func.fatal(u'Pickle resource file <%s> save error' % res_filename)
    return False


def saveResourceText(res_filename, resource_data):
    """
    Save resource file as Text.

    :param res_filename: Resource file path.
    :param resource_data: Resource data structure.
    :return: True/False.
    """
    res_filename = file_func.getAbsolutePath(res_filename)
    f = None
    try:
        dir_name = os.path.dirname(res_filename)
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except:
                log_func.fatal(u'Create path <%s> error' % dir_name)

        f = open(res_filename, 'wt')
        text = str(resource_data)
        f.write(text)
        f.close()
        log_func.info(u'Text resource file <%s> saved' % res_filename)
        return True
    except:
        if f:
            f.close()
        log_func.fatal(u'Text resource file <%s> save error' % res_filename)
    return False

