#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Import python modules functions.
"""

import os
import sys
import importlib.util

from . import log_func
from . import py_func

__version__ = (0, 0, 0, 1)


def importPyModule(import_name, import_filename):
    """
    Load/Import python module.

    :type import_name: C{string}
    :param import_name: Module import name.
    :type import_filename: C{string}
    :param import_filename: Module path.
    :return: Python module or None is error.
    """
    if import_name in sys.modules:
        return sys.modules[import_name]

    if os.path.isdir(import_filename):
        import_filename = os.path.join(import_filename, py_func.INIT_PY_FILENAME)

    if not os.path.exists(import_filename):
        log_func.warning(u'Module file <%s> not exists' % import_filename)
        return None

    module = None
    try:
        log_func.info(u'Load/Import python module <%s> by path <%s>' % (import_name, import_filename))
        module_spec = importlib.util.spec_from_file_location(import_name, import_filename)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        sys.modules[import_name] = module
    except ImportError:
        log_func.fatal(u'Error import module <%s> by path <%s>' % (import_name, path))

    return module


def deImportPyModule(import_name):
    """
    UnLoad/DeImport python module.

    :type import_name: C{string}
    :param import_name: Module import name.
    """
    if import_name in sys.modules:
        log_func.info(u'UnLoad/DeImport python module <%s>' % import_name)
        del sys.modules[import_name]
        return True
    return False


def reImportPyModule(import_name, path=None):
    """
    ReLoad/ReImport python module.

    :type import_name: C{string}
    :param import_name: Module import name.
    :type path: C{string}
    :param path: Module path.
        If None then define from imported module object.
    :return: Python module or None is error.
    """
    if path is None:
        if import_name in sys.modules:
            try:
                py_file_name = sys.modules[import_name].__file__
                py_file_name = os.path.splitext(py_file_name)[0]+'.py'
                path = py_file_name
            except:
                log_func.fatal(u'Error get path python module')
                return None
        else:
            return None
    deImportPyModule(import_name)
    return importPyModule(import_name, path)


def canImportName(import_name):
    """
    Can import library name?

    :param import_name: Imported library name.
    :return: True/False.
    """
    import_cmd = 'import ' + str(import_name)
    try:
        exec(import_cmd)
        return True
    except ImportError:
        log_func.warning(u'It is not possible to import <%s>' % import_name)
    return False
