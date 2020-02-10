#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Components package.
"""

import os
import os.path

from .. import project
from .. import user
from .. import role

from ..util import log_func
from ..util import imp_func
from ..util import file_func

__version__ = (0, 0, 0, 1)

COMPONENT_SPC_CACHE = None
UNKNOWN_PACKAGE_NAME = 'Other'
DEFAULT_SPC_PY = 'spc.py'


def getComponentSpc(py_pkg, py_pkg_path):
    """
    Get component SPC dictionary.

    :return: Component SPC dictionary or None if not find it.
    """
    component_module = imp_func.loadPyModule(py_pkg, py_pkg_path)
    if component_module and hasattr(component_module, 'SPC'):
        return component_module.SPC
    return None


def buildComponentSpcCache():
    """
    Build component specification cache.

    :return: Component specification cache dictionary or empty dictionary if error.
    """
    result = dict()
    try:
        prj_pkg = project.SPC['__package__']
        result[prj_pkg] = list()
        result[prj_pkg].append(project.SPC)
        result[prj_pkg].append(user.SPC)
        result[prj_pkg].append(role.SPC)

        components_dirname = os.path.dirname(__file__)
        component_names = file_func.getDirectoryNames(components_dirname)

        for py_pkg in component_names:
            py_pkg_path = os.path.join(components_dirname, py_pkg)
            component_spc = getComponentSpc(py_pkg, py_pkg_path)
            if component_spc is not None:
                pkg_name = component_spc.get('__package__', UNKNOWN_PACKAGE_NAME)
                if pkg_name not in result:
                    result[pkg_name] = list()
                result[pkg_name].append(component_spc)
            else:
                py_pkg_path = os.path.join(components_dirname, py_pkg, DEFAULT_SPC_PY)
                component_spc = getComponentSpc(py_pkg, py_pkg_path)
                if component_spc is not None:
                    pkg_name = component_spc.get('__package__', UNKNOWN_PACKAGE_NAME)
                    if pkg_name not in result:
                        result[pkg_name] = list()
                    result[pkg_name].append(component_spc)
                else:
                    log_func.error(u'Find component <%s> SPC error' % py_pkg)

        return result
    except:
        log_func.fatal(u'Build component specification cache error')
    return dict()


def initComponentSpcCache():
    """
    Initialization component specification cache.

    :return: True/False.
    """
    component_spc_cache = buildComponentSpcCache()
    globals()['COMPONENT_SPC_CACHE'] = buildComponentSpcCache() if component_spc_cache else dict()
    return bool(component_spc_cache)


def getComponentSpcCache():
    """
    Get component specification cache.

    :return: Component specification cache dictionary or empty dictionary if error.
    """
    if globals()['COMPONENT_SPC_CACHE'] is None:
        initComponentSpcCache()
    return globals()['COMPONENT_SPC_CACHE']


def findComponentSpc(component_type):
    """
    Find component specification by component type in cache.

    :param component_type: Component type.
    :return: Component specification or None if error.
    """
    packages = getComponentSpcCache()
    for package_name, package in packages.items():
        log_func.debug(u'Package <%s>' % package_name)
        component_types = [component_spc.get('type', None) for component_spc in package]
        if component_type in component_types:
            find_spc = package[component_types.index(component_type)]
            return find_spc
    log_func.warning(u'Component <%s> not found in specification cache' % component_type)
    return None