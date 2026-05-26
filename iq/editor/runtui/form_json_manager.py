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

__version__ = (0, 1, 1, 1)

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


def runRunTUIRadDesigner(filename=None, do_generate=False, *args, **kwargs):
    """
    Run RunTUI RAD designer.

    :param filename: File opened in RAD designer.
        If not specified, then nothing opens.
    :param do_generate: Generate the resulting resource / project module.
    :return: True/False
    """
    cmd = 'python3 -m runtui.rad_designer --theme=nord'
    if filename and os.path.exists(filename):
        cmd += ' --open=%s' % filename
        if do_generate:
            cmd += ' --gen_app'
    return exec_func.execSystemCommand(cmd)


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
            runRunTUIRadDesigner()
            return True
        except:
            log_func.fatal(u'Error creating RunTUI RAD designer project file <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Additional project generation.

        :param prj_filename: The full name of the project file.
        :return: True/False.
        """
        try:
            runRunTUIRadDesigner(prj_filename, do_generate=True, *args, **kwargs)
            return True
        except:
            log_func.fatal(u'Error generating application module RunTUI RAD designer project file <%s>' % prj_filename)
        return False
