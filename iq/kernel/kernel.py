#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kernel - general dispatcher of all program objects.
"""

import sys
# from PyQt5 import QtWidgets

# from . import app
from .. import config
from ..util import global_func


__version__ = (0, 0, 0, 1)

RUNTIME_MODE_STATE = 'runtime'
EDITOR_MODE_STATE = 'editor'

DEFAULT_RETURN_CODE = 0


class iqKernel(object):
    """
    Kernel - general dispatcher of all program objects.
    """
    def __init__(self, project_name=None, *args, **kwargs):
        """
        Constructor.
        """
        self.set_project(project_name)

        # Is running state?
        self.is_running = False

        # Program object cache
        self._object_cache = dict()

        # Application object
        # self.app = None
        #
        # self.app_return_code = 0

    def set_project(self, project_name=None):
        """
        Set current project_name.

        :param project_name: Project name.
        :return: True/False.
        """
        global_func.setProjectName(project_name)
        return True

    def start(self, mode=None, project_name=None, username=None, password=None):
        """
        Start programm.

        :param mode: Startup mode (runtime, editor).
            If not defined, it is taken from the configuration file.
        :param project_name: Project name.
            If not defined, it is taken from the configuration file.
        :param username: User name.
        :param password: User password.
        :return: True/False.
        """
        if isinstance(mode, str):
            global_func.setRuntimeMode(mode == RUNTIME_MODE_STATE)
        if isinstance(project_name, str):
            global_func.setProjectName(project_name)

        # self.app = QtWidgets.QApplication(sys.argv)
        # self.app_return_code = self.app.exec_()

    def stop(self):
        """
        Stop programm.

        :return: True/False
        """
        # sys.exit(self.app_return_code)
        sys.exit(DEFAULT_RETURN_CODE)


def createKernel():
    """
    Create kernel object.

    :return: Kernel object.
    """
    kernel = iqKernel()
    config.set_cfg_param('KERNEL', kernel)
    return kernel
