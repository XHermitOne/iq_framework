#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project manager module.
"""

import os
import os.path

from ..util import file_func
from ..util import log_func
from ..dialog import dlg_func

__version__ = (0, 0, 0, 1)


class iqProjectManager(object):
    """
    Project manager class.
    """
    def __init__(self, name=None):
        """
        Constructor.

        :param name: Project name.
        """
        self.name = name

    def setName(self, name):
        """
        Set name of actual project.

        :param name: Project name.
        :return:
        """
        self.name = name

    def create(self, name=None, parent=None):
        """
        Create new project.

        :param name: New project name.
            If None then open dialog for input.
        :param parent: Parent from.
        :return: True/False.
        """
        if name is None:
            name = dlg_func.getTextEntryDlg(parent=parent, title=u'PROJECT NAME',
                                            prompt_text=u'Enter the name of the project:', default_value='new_name')
        if name:
            prj_path = self.getPath(name)
            result = self.createPath(prj_path)
            if result:

                self.setName(name)
                return True
        return False

    def createPath(self, prj_path):
        """
        Create project directory.

        :param prj_path: Project directory path.
        :return: True/False.
        """
        if prj_path and os.path.exists(prj_path):
            log_func.warning(u'Project path <%s> exists' % prj_path)
        elif not prj_path:
            log_func.warning(u'Project path <%s> not defined' % prj_path)
        elif prj_path and not os.path.exists(prj_path):
            log_func.info(u'Create project path <%s>' % prj_path)
            try:
                os.makedirs(prj_path)
            except OSError:
                log_func.fatal(u'Create project path <%s> error' % prj_path)
        return False

    def getPath(self, name=None):
        """
        Get project path by project name.

        :param name: Project name.
        :return: Full path to project or None if error.
        """
        if name is None:
            name = self.name

        framework_path = file_func.getFrameworkPath()
        if framework_path:
            if name:
                return os.path.join(framework_path, name)
            else:
                log_func.warning(u'Not define project name')
        return None

    def run(self, name=None):
        """
        Run project.

        :param name: Project name. If None run actual.
        :return: True/False.
        """
        if name:
            self.setName(name)

        pass

    def debug(self, name=None):
        """
        Debug project.

        :param name: Project name. If None debug actual.
        :return: True/False.
        """
        if name:
            self.setName(name)

        pass
