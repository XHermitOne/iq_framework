#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kernel - general dispatcher of all program objects.
"""

import sys
from PyQt5 import QtWidgets

# from . import app
from iq import config


__version__ = (0, 0, 0, 1)

RUNTIME_MODE_STATE = 'runtime'
EDITOR_MODE_STATE = 'editor'


class iqKernel(object):
    """
    Kernel - general dispatcher of all program objects.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        # Is running state?
        self.is_running = False

        # Program object cache
        self._object_cache = dict()

        # Application object
        self.app = None

        self.app_return_code = 0

    def start(self, mode=None, project=None, username=None, password=None):
        """
        Start programm.
        @param mode: Startup mode (runtime, editor).
            If not defined, it is taken from the configuration file.
        @param project: Project name.
            If not defined, it is taken from the configuration file.
        @param username: User name.
        @param password: User password.
        @return: True/False.
        """
        if isinstance(mode, str):
            runtime_mode = mode.lower() == RUNTIME_MODE_STATE
            editor_mode = mode.lower() == EDITOR_MODE_STATE
            config.set_cfg_param('RUNTIME_MODE', runtime_mode)
            config.set_cfg_param('EDITOR_MODE', editor_mode)
        if isinstance(project, str):
            config.set_cfg_param('PROJECT_NAME', project)

        self.app = QtWidgets.QApplication(sys.argv)
        self.app_return_code = self.app.exec_()

    def stop(self):
        """
        Stop programm.
        @return: True/False
        """
        sys.exit(self.app_return_code)


def createKernel():
    """
    Create kernel object.
    @return: Kernel object.
    """
    kernel = iqKernel()
    config.set_cfg_param('KERNEL', kernel)
    return kernel


def getKernel():
    """
    Get kernel object.
    @return: Kernel object.
    """
    return config.get_cfg_param('KERNEL')
