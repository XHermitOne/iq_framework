#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global functions module.
"""

from .. import config

__version__ = (0, 0, 0, 1)


def isRuntimeMode():
    """
    Is GUI runtime mode?
    """
    return config.get_cfg_param('RUNTIME_MODE')


def setRuntimeMode(runtime_mode=True):
    """
    Set GUI runtime mode.
    """
    config.set_cfg_param('RUNTIME_MODE', runtime_mode)
    if runtime_mode:
        config.set_cfg_param('CONSOLE_MODE', False)


# def isConsoleMode():
#     """
#     Is CUI runtime mode?
#     """
#     return config.get_cfg_param('CONSOLE_MODE')
#
#
# def setConsoleMode(console_mode=True):
#     """
#     Set CUI runtime mode.
#     """
#     config.set_cfg_param('CONSOLE_MODE', console_mode)
#     if console_mode:
#         config.set_cfg_param('RUNTIME_MODE', False)
#

def isEditorMode():
    """
    Is editor mode?
    """
    return not config.get_cfg_param('RUNTIME_MODE') # and not config.get_cfg_param('CONSOLE_MODE')


def isDebugMode():
    """
    Is debug mode?
    """
    return config.get_cfg_param('DEBUG_MODE')


def setDebugMode(debug_mode=True):
    """
    Set debug mode.
    """
    config.set_cfg_param('DEBUG_MODE', debug_mode)


def isLogMode():
    """
    Is logging mode?
    """
    return config.get_cfg_param('LOG_MODE')


def setLogMode(log_mode=True):
    """
    Set logging mode.
    """
    config.set_cfg_param('LOG_MODE', log_mode)


def getKernel():
    """
    Get kernel object.

    :return: Kernel object.
    """
    return config.get_cfg_param('KERNEL')


def setProjectName(project_name=None):
    """
    Set project_name name.
    """
    config.set_cfg_param('PROJECT_NAME', project_name)


def getProjectName():
    """
    Get project_name name.

    :return: Project name.
    """
    return config.get_cfg_param('PROJECT_NAME')
