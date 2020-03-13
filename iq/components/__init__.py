#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Components package.
"""

import os
import os.path
import importlib

from .. import project
from .. import user
from .. import role

from ..util import log_func
# from ..util import imp_func
from ..util import file_func

__version__ = (0, 0, 0, 1)

COMPONENT_SPC_CACHE = None
COMPONENTS = None
UNKNOWN_PACKAGE_NAME = 'Other'
DEFAULT_SPC_PY = 'spc.py'
DEFAULT_COMPONENT_PY = 'component.py'


def getComponentSpc(py_pkg, py_pkg_path):
    """
    Get component SPC dictionary.

    :return: Component SPC dictionary or None if not find it.
    """
    # component_module = imp_func.loadPyModule(py_pkg, py_pkg_path)
    component_module = importComponent(py_pkg)
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
                    log_func.error(u'Error find component <%s> SPC' % py_pkg)

        return result
    except:
        log_func.fatal(u'Error build component specification cache')
    return dict()


def initComponentSpcCache():
    """
    Initialization component specification cache.

    :return: True/False.
    """
    component_spc_cache = buildComponentSpcCache()
    globals()['COMPONENT_SPC_CACHE'] = component_spc_cache if component_spc_cache else dict()
    return bool(component_spc_cache)


def getComponentSpcPalette():
    """
    Get component specification cache/palette.

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
    packages = getComponentSpcPalette()
    for package_name, package in packages.items():
        # log_func.debug(u'Package <%s>' % package_name)
        component_types = [component_spc.get('type', None) for component_spc in package]
        if component_type in component_types:
            find_spc = package[component_types.index(component_type)]
            return find_spc
    log_func.warning(u'Component <%s> not found in specification cache' % component_type)
    return None


def getComponents():
    """
    Get components cache.

    :return:
    """
    if globals()['COMPONENTS'] is None:
        initComponents()
    return globals()['COMPONENTS']


def initComponents():
    """
    Initialization component cache.

    :return: True/False.
    """
    components = buildComponents()
    globals()['COMPONENTS'] = components if components else dict()
    return True


def buildComponents():
    """
    Build components cache.

    :return: Components cache dictionary.
    """
    result = dict()
    try:
        prj_type = project.COMPONENT_TYPE
        prj_component = project.COMPONENT
        result[prj_type] = prj_component
        log_func.info(u'Component <%s> registered' % prj_type)

        user_type = user.COMPONENT_TYPE
        user_component = user.COMPONENT
        result[user_type] = user_component
        log_func.info(u'Component <%s> registered' % user_type)

        role_type = role.COMPONENT_TYPE
        role_component = role.COMPONENT
        result[role_type] = role_component
        log_func.info(u'Component <%s> registered' % role_type)

        components_dirname = os.path.dirname(__file__)
        component_names = file_func.getDirectoryNames(components_dirname)

        for py_pkg in component_names:
            # py_pkg_path = os.path.join(components_dirname, py_pkg)

            # component_pkg = imp_func.loadPyModule(py_pkg, py_pkg_path)
            component_pkg = importComponent(py_pkg)
            component_type = None
            if component_pkg and hasattr(component_pkg, 'SPC'):
                component_type = component_pkg.SPC.get('type', None)
            # else:
            #     spc_module_path = os.path.join(py_pkg_path, DEFAULT_SPC_PY)
            #     spc_module = imp_func.loadPyModule(py_pkg, spc_module_path)
            #     if spc_module and hasattr(spc_module, 'SPC'):
            #         component_type = spc_module.SPC.get('type', None)

            component_class = None
            if component_pkg and hasattr(component_pkg, 'COMPONENT'):
                component_class = component_pkg.COMPONENT
            # else:
            #     component_module_path = os.path.join(py_pkg_path, DEFAULT_COMPONENT_PY)
            #     component_module = imp_func.loadPyModule(py_pkg, component_module_path)
            #     if component_module and hasattr(component_module, 'COMPONENT'):
            #         component_class = component_module.COMPONENT

            if component_type is None:
                log_func.error(u'Not find component type in <%s>' % py_pkg)
            if component_class is None:
                log_func.error(u'Not find component class in <%s>' % py_pkg)
            if component_type and component_class:
                result[component_type] = component_class
                log_func.info(u'Component <%s> registered' % component_type)

        return result
    except:
        log_func.fatal(u'Error build component specification cache')
    return dict()


def importComponent(component_pkg_name):
    """
    Import component package.

    :param component_pkg_name: Component package name.
    :return: Component package or None if error.
    """
    pkg_name = 'iq.components.%s' % str(component_pkg_name)
    try:
        component_pkg = importlib.import_module(pkg_name)
        return component_pkg
    except:
        log_func.fatal(u'Error import component package <%s>' % pkg_name)
    return None
