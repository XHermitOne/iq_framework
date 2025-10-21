#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iqFramework - RAD Software platform for developing applications in Python using the wxPython GUI.

Command line parameters:

        python3 framework.py [Launch parameters]

Launch parameters:

    [Help and debugging]
        --help|-h|-?        Print help lines
        --version|-v        Print version of the program
        --debug|-d          Enable debug mode
        --log|-l            Enable logging mode
        --os                Show OS information

    [Options]
        --mode=             Startup mode (runtime, editor)
        --engine=           Engine type (WX, QT or CUI)
        --prj=              Project name
        --username=         User name
        --password=         User password
        --res_filename=     Resource filename for resource editor
"""

import sys
import getopt
import os.path
import locale
import time

from iq import global_data
from iq.util import log_func
from iq.util import global_func
from iq.util import file_func
from iq.util import sys_func
from iq import editor
import iq

__version__ = (0, 1, 1, 1)


def main(*argv):
    """
    Main function triggered.

    :param argv: Command line parameters.
    """
    # Parse command line arguments
    try:
        options, args = getopt.getopt(argv, 'h?vdl',
                                      ['help', 'version', 'debug', 'log', 'os',
                                       'mode=', 'engine=', 'prj=', 'username=', 'password=',
                                       'res_filename='])
    except getopt.error as msg:
        log_func.warning(str(msg), is_force_print=True)
        log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
        log_func.printColourText(__doc__, color=log_func.GREEN_COLOR_TEXT)
        sys.exit(2)

    mode = None
    runtime_mode = False
    engine = global_data.ENGINE_TYPE
    project = None
    username = None
    password = None
    res_filename = None

    if any([arg in ('-h', '--help', '-?') for arg in args]):
        log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
        log_func.printColourText(__doc__, color=log_func.GREEN_COLOR_TEXT)
        sys.exit(0)

    if any([arg in ('-v', '--version') for arg in args]):
        str_version = 'iqFramework %s' % '.'.join([str(sign) for sign in global_data.VERSION])
        log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
        log_func.printColourText(str_version, color=log_func.GREEN_COLOR_TEXT)
        sys.exit(0)

    log_func.printColourText('OPTIONS', color=log_func.CYAN_COLOR_TEXT)
    for option, arg in options:
        if option in ('-d', '--debug'):
            log_func.printColourText('\tDebug: ON', color=log_func.CYAN_COLOR_TEXT)
            global_func.setDebugMode()
        elif option in ('-l', '--log'):
            log_func.printColourText('\tLog: ON', color=log_func.CYAN_COLOR_TEXT)
            global_func.setLogMode()
            log_func.init()
        elif option in ('--os',):
            sys_func.printOSFetchInfo()
        elif option in ('--mode',):
            mode = arg.lower()
            runtime_mode = mode == iq.RUNTIME_MODE_STATE
            log_func.printColourText('\tMode: %s' % mode, color=log_func.CYAN_COLOR_TEXT)
            global_func.setRuntimeMode(runtime_mode)
        elif option in ('--engine',):
            engine = arg
            log_func.printColourText('\tEngine: %s' % engine, color=log_func.CYAN_COLOR_TEXT)
            global_func.setEngineType(engine)
        elif option in ('--prj',):
            project = arg
            log_func.printColourText('\tProject: %s' % project, color=log_func.CYAN_COLOR_TEXT)
        elif option in ('--username',):
            username = arg
            log_func.printColourText('\tUsername: %s' % username, color=log_func.CYAN_COLOR_TEXT)
        elif option in ('--password',):
            password = arg
        elif option in ('--res_filename',):
            res_filename = arg
            log_func.printColourText('\tResource: %s' % res_filename, color=log_func.CYAN_COLOR_TEXT)
        else:
            log_func.warning(u'Not supported parameter <%s>' % option)

    start_time = time.time()
    log_func.info(u'iqFramework <Engine: %s / Mode: %s / Path: %s / IQ path: %s>... START' % (engine, mode,
                                                                                              file_func.getFrameworkPath(),
                                                                                              os.path.dirname(iq.__file__)))

    # Set system locale
    cur_locale = locale.getlocale()
    locale.setlocale(locale.LC_ALL, cur_locale)
    log_func.info(u'Set locale <%s.%s>' % tuple(cur_locale))

    try:
        if runtime_mode:
            kernel = iq.createKernel()
            kernel.start(mode=mode, project_name=project, username=username, password=password)
            kernel.stop()
        elif mode == iq.EDITOR_MODE_STATE and os.path.basename(__file__) == os.path.basename(res_filename):
            editor.openFrameworkEditor()
        elif mode == iq.EDITOR_MODE_STATE:
            editor.openResourceEditor(res_filename=res_filename)
        else:
            log_func.warning(u'Engine type <%s : %s> not support' % (engine, mode))
    except:
        log_func.fatal(u'Run iqFramework error')

    log_func.info(u'iqFramework <Engine: %s / Mode: %s / Total time: %s>... STOP' % (engine, mode,
                                                                                     str(time.time() - start_time)))


if __name__ == '__main__':
    main(*sys.argv[1:])
