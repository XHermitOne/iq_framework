#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Glade form designer manager.
"""

import os
import os.path

from ...util import log_func
from ...util import exec_func
from ...util import py_func
from ...util import file_func
from ...util import txtfile_func

from .code_generator import gui_generator

__version__ = (0, 0, 1, 1)

GLADE_PROJECT_FILE_EXT = '.glade'

ALTER_GLADE_PATH = 'glade'
ALTER_GLADE_PREVIEW_PATH = 'glade-previewer'


def isGladeProjectFile(filename):
    """
    Check if the file is Glade project.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, GLADE_PROJECT_FILE_EXT)


def getGladeExecutable():
    """
    The path to the main Glade program to run.
    """
    if os.path.exists('/bin/glade') or os.path.exists('/usr/bin/glade'):
        return 'glade'
    else:
        alter_glade_path = os.path.normpath(ALTER_GLADE_PATH)
        return alter_glade_path
    return None


def getGladePreviewExecutable():
    """
    The path to the main Glade preview program to run.
    """
    if os.path.exists('/bin/glade-previewer') or os.path.exists('/usr/bin/glade-previewer'):
        return 'glade-previewer'
    else:
        alter_glade_preview_path = os.path.normpath(ALTER_GLADE_PREVIEW_PATH)
        return alter_glade_preview_path
    return None


def runGlade(filename=None, asynchro=True):
    """
    Run Glade.
    For a more detailed description of the Glade startup options,
    run: glade --help.

    :param filename: File opened in Glade.
        If not specified, then nothing opens.
    :param do_generate: Generate the resulting resource / project module.
    :param language: Explicit language specification for generation.
    :param asynchro: Asynchronous start?
    :return: True/False
    """
    cmd = ''
    cmd_args = filename

    glade_exec = getGladeExecutable()
    if glade_exec:
        async_symb = '&' if asynchro else ''
        cmd = '%s %s%s' % (glade_exec,
                           cmd_args,
                           async_symb) if cmd_args else '%s %s' % (glade_exec, async_symb)

    return exec_func.execSystemCommand(cmd)


def previewGlade(filename=None, asynchro=True):
    """
    Preview Glade file.
    For a more detailed description of the Glade startup options,
    run: glade-preview --help.

    :param filename: File opened in Glade.
        If not specified, then nothing opens.
    :param asynchro: Asynchronous start?
    :return: True/False
    """
    cmd = ''
    cmd_args = '--filename=%s' % filename

    css_filename = gui_generator.getGladeProjectCSSFilename(filename=filename)
    if css_filename:
        if os.path.exists(css_filename):
            cmd_args += ' --css=%s' % css_filename
        else:
            log_func.warning(u'CSS file <%s> not found for preview glade project <%s>' % (css_filename, filename))

    glade_preview_exec = getGladePreviewExecutable()
    if glade_preview_exec:
        async_symb = '&' if asynchro else ''
        cmd = '%s %s%s' % (glade_preview_exec,
                           cmd_args,
                           async_symb) if cmd_args else '%s %s' % (glade_preview_exec, async_symb)

    return exec_func.execSystemCommand(cmd)


class iqGladeManager(object):
    """
    Glade form designer manager.
    """
    def openProject(self, prj_filename):
        """
        Open project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        try:
            runGlade(prj_filename)
            return True
        except:
            log_func.fatal(u'Error opening Glade project file <%s>' % prj_filename)
        return False

    def previewProject(self, prj_filename):
        """
        Open preview project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        try:
            previewGlade(prj_filename)
            return True
        except:
            log_func.fatal(u'Error preview Glade project file <%s>' % prj_filename)
        return False

    def createProject(self, default_prj_filename=None):
        """
        Create a new project file.

        :param default_prj_filename: The default project file name.
        :return: True/False.
        """
        try:
            runGlade(default_prj_filename)
            return True
        except:
            log_func.fatal(u'Error creating Glade project file <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Additional project generation.

        :param prj_filename: The full name of the project file.
        :return: True/False.
        """
        return False
