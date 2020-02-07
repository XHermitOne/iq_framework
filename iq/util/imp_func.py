#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Import python modules functions.
"""

import os
import sys
import importlib.util

from . import log_func

__version__ = (0, 0, 0, 1)


def loadPyModule(name, path):
    """
    Load/Import python module.

    :type name: C{string}
    :param name: Module name.
    :type path: C{string}
    :param path: Module path.
    :return: Python module or None is error.
    """
    module = None
    try:
        log_func.info(u'Load/Import python module <%s> by path <%s>' % (name, path))
        module_spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    except ImportError:
        log_func.fatal(u'Import module <%s> by path <%s> error' % (name, path))

    return module


def unloadPyModule(name):
    """
    UnLoad/DeImport python module.

    :type name: C{string}
    :param name: Module name.
    """
    if name in sys.modules:
        log_func.info(u'UnLoad/DeImport python module <%s>' % name)
        del sys.modules[name]
        return True
    return False


def reloadPyModule(name, path=None):
    """
    ReLoad/ReImport python module.

    :type name: C{string}
    :param name: Module name.
    :type path: C{string}
    :param path: Module path.
        If None then define from imported module object.
    :return: Python module or None is error.
    """
    if path is None:
        if name in sys.modules:
            try:
                py_file_name = sys.modules[name].__file__
                py_file_name = os.path.splitext(py_file_name)[0]+'.py'
                path = py_file_name
            except:
                log_func.fatal(u'Get path python module error')
                return None
        else:
            return None
    unloadPyModule(name)
    return loadPyModule(name, path)
