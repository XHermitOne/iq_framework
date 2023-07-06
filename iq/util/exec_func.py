#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execute functions module.
"""

import os
import os.path
import stat
import sys
import uuid
import subprocess
import locale

from . import log_func
from . import sys_func
from . import file_func
from . import global_func
from . import txtfile_func

__version__ = (0, 0, 1, 4)


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


def getLinesExecutedCommand(cmd='', console_encoding=None):
    """
    Execute command and get output lines.

    :param cmd: Command string. May be as string and list of string.
    :param console_encoding: Console/Shell code page.
    :return: Tuple of string.
    """
    if console_encoding is None:
        console_encoding = locale.getpreferredencoding()

    if cmd:
        try:
            log_func.info(u'Run command <%s> and get lines' % str(cmd))
            cmd_list = cmd if isinstance(cmd, (list, tuple)) else cmd.split(' ')
            process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
            b_lines = process.stdout.readlines()

            # Decode lines
            lines = list()
            for i, line in enumerate(b_lines):
                try:
                    lines.append(line.decode(console_encoding).strip())
                except UnicodeDecodeError:
                    log_func.fatal(u'Error decode line [%d]' % i)
                    lines.append('')

            return lines
        except:
            log_func.fatal(u'Error execute command <%s> and get output lines' % cmd)
    else:
        log_func.warning(u'Not define command')
    return tuple()


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


def execTxtFunction(function, context=None, show_debug=False):
    """
    Execute function.

    :param function: Function text body.
    :param context: Run function context dictionary.
    :param show_debug: Show debug info?
    :return: Run function result.
    """
    if context is None:
        context = globals()

    if not isinstance(function, str):
        log_func.warning(u'Not valid function body type <%s>' % type(function))
        return None

    # Find source line separator
    linesep = os.linesep
    for sep in sys_func.LINE_SEPARATORS:
        if sep in function:
            linesep = sep

    function_body = sys_func.LINESEP.join(INDENTATION + line for line in function.split(linesep))
    function_name = str(uuid.uuid4()).replace('-', '_')
    function_header = 'def __%s():%s' % (function_name, sys_func.LINESEP)
    function_footer = '%s__result__ = __%s()' % (sys_func.LINESEP, function_name)
    function_txt = function_header + function_body + function_footer

    try:
        exec(function_txt, context)
        if show_debug:
            log_func.debug(u'Execute function:\n%s' % function_txt)
        return context['__result__']
    except:
        log_func.fatal(u'Error execute function:\n%s' % function_txt)
    return None


def runTask(command, run_filename=None, rewrite=True):
    """
    Running a command as a separate task.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    :param rewrite: Rewrite command file.
    :return: True/False.
    """
    if sys_func.isWindowsPlatform():
        return runTaskWindows(command, run_filename=run_filename, rewrite=rewrite)
    return runTaskLinux(command, run_filename=run_filename, rewrite=rewrite)


def runTaskLinux(command, run_filename=None, rewrite=True):
    """
    Running a command as a separate task with a separate console in Linux.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    :param rewrite: Rewrite command file.
    :return: True/False.
    """
    if run_filename is None:
        run_filename = global_func.getProjectName() if global_func.getProjectName() else 'run'

    run_sh_filename = file_func.getAbsolutePath('./%s.sh' % run_filename,
                                                cur_dir=file_func.getFrameworkPath())
    try:
        result = txtfile_func.saveTextFile(txt_filename=run_sh_filename,
                                           txt=command, rewrite=rewrite)

        if os.path.exists(run_sh_filename):
            sh_state = os.stat(run_sh_filename)
            os.chmod(run_sh_filename, sh_state.st_mode | stat.S_IEXEC)

        log_func.info(u'Run task <%s>' % run_sh_filename)
        os.system('gnome-terminal -- \'%s\'' % run_sh_filename)
        return result
    except:
        log_func.fatal(u'Error run task <%s>' % run_sh_filename)
    return False


def runTaskWindows(command, run_filename=None, rewrite=True):
    """
    Running a command as a separate task with a separate console in Windows.

    :type command: C{string}
    :param command: Command.
    :param run_filename: Run filename.
    :param rewrite: Rewrite command file.
    :return: True/False.
    """
    if run_filename is None:
        run_filename = global_func.getProjectName() if global_func.getProjectName() else 'run'

    run_bat_filename = file_func.getAbsolutePath('./%s.bat' % run_filename,
                                                 cur_dir=file_func.getFrameworkPath())
    try:
        result = txtfile_func.saveTextFile(txt_filename=run_bat_filename,
                                           txt=command, rewrite=rewrite)

        log_func.info(u'Run task <%s>' % run_bat_filename)
        os.startfile(run_bat_filename)
        return result
    except:
        log_func.fatal(u'Error run task <%s>' % run_bat_filename)
    return False
