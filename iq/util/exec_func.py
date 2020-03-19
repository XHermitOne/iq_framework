#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execute functions module.
"""

import os
import os.path
import stat
import uuid

from . import log_func
from . import sys_func
from . import file_func
from . import global_func
from . import txtfile_func

__version__ = (0, 0, 0, 1)


def execSystemCommand(cmd=''):
    """
    Execute system command.

    :param cmd: Command string.
    :return: True/False.
    """
    if cmd:
        try:
            log_func.info(u'Run system command <%s>' % cmd)
            os.system(cmd)
            return True
        except:
            log_func.fatal(u'Error execute system command <%s>' % cmd)
    else:
        log_func.warning(u'Not define system command')
    return False


def openHtmlBrowser(html_filename=None):
    """
    Open default HTML browser.

    :param html_filename: HTML filename.
    :return: True/False
    """
    if html_filename:
        cmd_fmt = 'open %s'
        cmd = cmd_fmt % html_filename
        return execSystemCommand(cmd)
    else:
        log_func.warning(u'Not define HTML file for view')
    return False


INDENTATION = u' ' * 4


def execTxtFunction(function, context=None):
    """
    Execute function.

    :param function: Function text body.
    :param context: Run function context dictionary.
    :return: Run function result.
    """
    if context is None:
        context = globals()

    if not isinstance(function, str):
        log_func.error(u'Not valid function body type <%s>' % type(function))
        return None

    function_body = os.linesep.join(INDENTATION + line for line in function.split(os.linesep))
    function_name = str(uuid.uuid4()).replace('-', '_')
    function_header = 'def __%s():%s' % (function_name, os.linesep)
    function_footer = '%s__result__ = __%s()' % (os.linesep, function_name)
    function_txt = function_header + function_body + function_footer
    try:
        exec(function_txt, context)
        return context['__result__']
    except:
        log_func.error(u'Execute function:')
        log_func.error(function_txt)
        log_func.fatal(u'Error execute function')
    return None


def runTask(command, run_filename=None):
    """
    Running a command as a separate task.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    :return: True/False.
    """
    if sys_func.isWindowsPlatform():
        return runTaskWindows(command, run_filename=run_filename)
    return runTaskLinux(command, run_filename=run_filename)


def runTaskLinux(command, run_filename=None):
    """
    Running a command as a separate task with a separate console in Linux.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    :return: True/False.
    """
    if run_filename is None:
        run_filename = global_func.getProjectName() if global_func.getProjectName() else 'run'

    run_sh_filename = file_func.getAbsolutePath('./%s.sh' % run_filename,
                                                cur_dir=file_func.getFrameworkPath())
    try:
        result = txtfile_func.saveTextFile(txt_filename=run_sh_filename,
                                           txt=command, rewrite=False)

        if os.path.exists(run_sh_filename):
            sh_state = os.stat(run_sh_filename)
            os.chmod(run_sh_filename, sh_state.st_mode | stat.S_IEXEC)

        log_func.info(u'Run task <%s>' % run_sh_filename)
        os.system('gnome-terminal -- \'%s\'' % run_sh_filename)
        return result
    except:
        log_func.fatal(u'Error run task <%s>' % run_sh_filename)
    return False


def runTaskWindows(command, run_filename=None):
    """
    Running a command as a separate task with a separate console in Windows.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    """
    if run_filename is None:
        run_filename = global_func.getProjectName() if global_func.getProjectName() else 'run'

    run_bat_filename = file_func.getAbsolutePath('./%s.bat' % run_filename,
                                                 cur_dir=file_func.getFrameworkPath())
    try:
        result = txtfile_func.saveTextFile(txt_filename=run_bat_filename,
                                           txt=command, rewrite=False)

        log_func.info(u'Run task <%s>' % run_bat_filename)
        os.startfile(run_bat_filename)
        return result
    except:
        log_func.fatal(u'Error run task <%s>' % run_bat_filename)
    return False
