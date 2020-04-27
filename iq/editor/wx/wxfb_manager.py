#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
wxFormBuilder Form designer management manager.
"""

import os
import os.path

from ...util import log_func
from ...util import exec_func
from ...util import py_func
from ...util import file_func

from ...script import migrate_fbp

__version__ = (0, 0, 0, 1)

WXFB_PROJECT_FILE_EXT = '.fbp'

ALTER_WXFORMBUILDER = 'flatpak run org.wxformbuilder.wxFormBuilder'

WXFB_PY_MODULE_SIGNATURE = '## Python code generated with wxFormBuilder'

STARTSWITH_SIGNATURE = '..)'
ENDSWITH_SIGNATURE = '(..'
CONTAIN_SIGNATURE = '(..)'

COMMENT_COMMAND_SIGNATIRE = '#'

ADAPTATION_REPLACES = (
    # Gettext
    dict(compare=STARTSWITH_SIGNATURE, src='import gettext', dst='from iq.util import lang_func'),
    dict(compare=STARTSWITH_SIGNATURE, src='_ = gettext.gettext', dst='_ = lang_func.getTranslation().gettext'),
    # Wx imports
    dict(compare=STARTSWITH_SIGNATURE, src='import wx.combo', dst='# import wx.combo'),
    dict(compare=STARTSWITH_SIGNATURE, src='import wx.xrc', dst='import wx.adv\nimport wx.lib.gizmos\nimport wx.aui'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.combo.', dst='wx.adv.'),
    # Calendar
    dict(compare=STARTSWITH_SIGNATURE, src='import wx.calendar', dst='# import wx.calendar'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.calendar.', dst='wx.adv.'),
    # DatePickerCtrl
    dict(compare=CONTAIN_SIGNATURE, src='wx.DatePickerCtrl', dst='wx.adv.DatePickerCtrl'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.DP_', dst='wx.adv.DP_'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_DATE_CHANGED', dst='wx.adv.EVT_DATE_CHANGED'),
    # Bitmap
    dict(compare=CONTAIN_SIGNATURE, src='.Ok()', dst='.IsOk()'),
    # Sizers
    dict(compare=CONTAIN_SIGNATURE, src='.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )', dst='.AddStretchSpacer()'),
    dict(compare=CONTAIN_SIGNATURE, src='.AddSpacer( ( 0, 0), 1, wx.EXPAND,', dst='.AddSpacer('),
    dict(compare=CONTAIN_SIGNATURE, src='.SetSizeHintsSz', dst='.SetSizeHints'),
    # ToolBar
    dict(compare=CONTAIN_SIGNATURE, src='.AddLabelTool(', dst='.AddTool('),
    # Wizard
    dict(compare=CONTAIN_SIGNATURE, src='wx.wizard', dst='wx.adv'),
    # TextCtrl
    dict(compare=CONTAIN_SIGNATURE, src='.SetMaxLength', dst=COMMENT_COMMAND_SIGNATIRE),
    # TreeListCtrl
    dict(compare=CONTAIN_SIGNATURE, src='wx.TreeListCtrl', dst='wx.lib.gizmos.TreeListCtrl'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.TL_DEFAULT_STYLE', dst='wx.lib.gizmos.TR_DEFAULT_STYLE'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.TL_SINGLE', dst='wx.lib.gizmos.TR_SINGLE'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.TR_FULL_ROW_HIGHLIGHT', dst='wx.lib.gizmos.TR_FULL_ROW_HIGHLIGHT'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_TREELIST_SELECTION_CHANGED', dst='wx.EVT_TREE_SEL_CHANGED'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_TREELIST_SELECTION_CHANGING', dst='wx.EVT_TREE_SEL_CHANGING'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_TREE_ITEM_ACTIVATED', dst='wx.EVT_TREE_ITEM_ACTIVATED'),
    dict(compare=CONTAIN_SIGNATURE, src='wx.EVT_TREELIST_ITEM_CONTEXT_MENU', dst='wx.EVT_TREE_ITEM_RIGHT_CLICK'),
    dict(compare=CONTAIN_SIGNATURE, src='_treeListCtrl.AppendColumn(', dst='_treeListCtrl.AddColumn('),
    dict(compare=CONTAIN_SIGNATURE, src=', wx.COL_RESIZABLE )', dst=')'),
    dict(compare=CONTAIN_SIGNATURE, src=')', dst=')'),
    dict(compare=CONTAIN_SIGNATURE, src=')', dst=')'),
    dict(compare=CONTAIN_SIGNATURE, src=', agwStyle=wx.lib.gizmos.TR_', dst=', agwStyle=wx.lib.gizmos.TR_'),
    # StatusBar
    dict(compare=CONTAIN_SIGNATURE, src='wx.ST_SIZEGRIP', dst='wx.STB_SIZEGRIP'),
    # Menu
    dict(compare=CONTAIN_SIGNATURE, src='.AppendItem( ', dst='.Append('),
    )


def isWXFormBuilderProjectFile(filename):
    """
    Check if the file is wxFormBuilder project.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, WXFB_PROJECT_FILE_EXT)


def getWXFormBuilderExecutable():
    """
    The path to the main wxFormBuilder program to run.
    """
    if os.path.exists('/bin/wxformbuilder') or os.path.exists('/usr/bin/wxformbuilder'):
        return 'wxformbuilder'
    else:
        alter_wxfb_path = os.path.normpath(ALTER_WXFORMBUILDER)
        return alter_wxfb_path
    return None


def runWXFormBuilder(filename=None, do_generate=False, language=None):
    """
    Run wxFormBuilder.
    For a more detailed description of the wxFormBuilder startup options, run: wxformbuilder --help.

    :param filename: File opened in wxFormBuilder.
        If not specified, then nothing opens.
    :param do_generate: Generate the resulting resource / project module.
    :param language: Explicit language specification for generation.
    :return: True/False
    """
    cmd = ''
    cmd_args = filename
    if cmd_args:
        cmd_args += '--generate' if do_generate else ''
        cmd_args += ('--language=%s' % language) if language else ''

    wxformbuilder_exec = getWXFormBuilderExecutable()
    if wxformbuilder_exec:
        cmd = '%s %s&' % (wxformbuilder_exec, cmd_args) if cmd_args else '%s &' % wxformbuilder_exec

    return exec_func.execSystemCommand(cmd)


def isWXFormBuilderFormPy(py_filename):
    """
    Check if python file is a wxFormBuilder form file.

    :param py_filename: Python file path.
    :return: True/False.
    """
    return py_func.isPyFileSignature(py_filename, WXFB_PY_MODULE_SIGNATURE)


class iqWXFormBuilderManager(object):
    """
    wxFormBuilder Form designer management manager.
    """
    def openProject(self, prj_filename):
        """
        Open project file.

        :param prj_filename: The full name of the project file.
        :return: True/False
        """
        try:
            runWXFormBuilder(prj_filename)
            return True
        except:
            log_func.fatal(u'Error opening wxFormBuilder project file <%s>' % prj_filename)
        return False

    def createProject(self, default_prj_filename=None):
        """
        Create a new project file.

        :param default_prj_filename: The default project file name.
        :return: True/False.
        """
        try:
            runWXFormBuilder(default_prj_filename)
            return True
        except:
            log_func.fatal(u'Error creating wxFormBuilder project file <%s>' % default_prj_filename)
        return False

    def generate(self, prj_filename, *args, **kwargs):
        """
        Additional project generation.

        :param prj_filename: The full name of the project file.
        :return: True/False.
        """
        try:
            runWXFormBuilder(prj_filename, do_generate=True, *args, **kwargs)
            return True
        except:
            log_func.fatal(u'Error generating wxFormBuilder project file <%s>' % prj_filename)
        return False

    def _replaceAdaptation(self, line, replacement_src, replacement_dst):
        """
        Replace the module line.

        :param line: Module line string.
        :param replacement_src: Original replacement.
        :param replacement_dst: Resulting replacement.
        :return: Modified module string.
        """
        if replacement_dst == COMMENT_COMMAND_SIGNATIRE:
            log_func.info(u'Line <%s> commented' % line)
            return COMMENT_COMMAND_SIGNATIRE + line
        log_func.info(u'Replaced <%s> to <%s> in line <%s>' % (replacement_src, replacement_dst, line))
        return line.replace(replacement_src, replacement_dst)

    def adaptFormPy(self, py_filename):
        """
        Adapting the generated Python module for use in the program
        with the current version of wxPython.

        :param py_filename: The full name of the generated form module using wxFormBuilder.
        :return: True/False.
        """
        if not os.path.exists(py_filename):
            log_func.warning(u'File <%s> not found' % py_filename)
            return False

        lines = list()
        file_obj = None
        try:
            file_obj = open(py_filename, 'rt')
            lines = file_obj.readlines()
            file_obj.close()
        except:
            log_func.fatal(u'Error reading module file <%s> for adaptation' % py_filename)
            if file_obj:
                file_obj.close()
            return False

        for i, line in enumerate(lines):
            new_line = line
            for replacement in ADAPTATION_REPLACES:
                signature = replacement.get('compare', None)
                if signature == STARTSWITH_SIGNATURE and new_line.startswith(replacement['src']):
                    new_line = self._replaceAdaptation(new_line, replacement['src'], replacement['dst'])
                elif signature == ENDSWITH_SIGNATURE and new_line.endswith(replacement['src']):
                    new_line = self._replaceAdaptation(new_line, replacement['src'], replacement['dst'])
                elif signature == CONTAIN_SIGNATURE and replacement['src'] in new_line:
                    new_line = self._replaceAdaptation(new_line, replacement['src'], replacement['dst'])
            lines[i] = new_line

        file_obj = None
        try:
            file_obj = open(py_filename, 'wt')
            file_obj.writelines(lines)
            file_obj.close()
            return True
        except:
            log_func.fatal(u'Error writing module file <%s> for adaptation' % py_filename)
            if file_obj:
                file_obj.close()
        return False


def adaptWXWFormBuilderPy(py_filename):
    """
    Adapting the generated Python module for use in the program
    with the current version of wxPython.

    :param py_filename: The full name of the generated form module using wxFormBuilder.
    :return: True/False.
    """
    manager = iqWXFormBuilderManager()
    result = manager.adaptFormPy(py_filename)
    if result:
        log_func.info(u'Python adaptation of wxFormBuilder module <%s> ... OK' % py_filename)
    else:
        log_func.error(u'Python adaptation of wxFormBuilder module <%s> ... FAIL' % py_filename)
    return result


def migrateWXFormBuilderProject(fbp_filename):
    """
    Make wxFormBuilder project module migration replacements.

    :param fbp_filename: Python file path.
    :return: True/False.
    """
    try:
        return migrate_fbp.migrateFBP(fbp_filename=fbp_filename)
    except:
        log_func.fatal(u'Error make wxFormBuilder project module <%s> migration' % fbp_filename)
    return False
