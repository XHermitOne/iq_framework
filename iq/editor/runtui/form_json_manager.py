#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RunTUI form designer manager.
"""

import os.path
from ...util import log_func

try:
    import runtui
except ImportError:
    log_func.error(u'Import error runtui. For install: pip3 install runtui', is_force_print=True)

from ...util import file_func
from ...util import exec_func

__version__ = (0, 0, 0, 1)

JSON_PROJECT_FILE_EXT = '.json'


def isFormJSONProjectFile(filename):
    """
    Check if the file is RunTUI form project.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, JSON_PROJECT_FILE_EXT)


def getRunTUIRadDesignerExecutable():
    """
    The path to the main RunTUI RAD designer program to run.
    """
    runtui_path = os.path.dirname(runtui.__file__)
    return os.path.join(runtui_path, 'rad_designer.py')


def runRunTUIRadDesigner(filename=None):
    """
    Run RunTUI RAD designer.

    :param filename: File opened in RAD designer.
        If not specified, then nothing opens.
    :return: True/False
    """
    cmd = ''
    cmd_args = filename if filename is not None else ''

    rad_designer_exec = getRunTUIRadDesignerExecutable()
    if rad_designer_exec:
        cmd = '%s %s' % (rad_designer_exec, cmd_args) if cmd_args else rad_designer_exec
        return exec_func.execSystemCommand(cmd)
    return False


class iqRunTUIRadDesignerManager(object):
    """
    RunTUI RAD form designer manager.
    """
    def openProject(self, prj_filename):
        """
        Open project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        try:
            runRunTUIRadDesigner(prj_filename)
            return True
        except:
            log_func.fatal(u'Error opening RunTUI RAD designer project file <%s>' % prj_filename)
        return False

    def createProject(self, default_prj_filename=None):
        """
        Create a new project file.

        :param default_prj_filename: The default project file name.
        :return: True/False.
        """
        try:
            runRunTUIRadDesigner(default_prj_filename)
            return True
        except:
            log_func.fatal(u'Error creating RunTUI RAD designer project file <%s>' % default_prj_filename)
        return False
