#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iqFramework - RAD Software platform for developing applications in Python using the PyQt GUI.

Command line parameters:

        python3 framework.py [Launch parameters]

Launch parameters:

    [Help and debugging]
        --help|-h|-?        Print help lines
        --version|-v        Print version of the program
        --debug|-d          Enable debug mode
        --log|-l            Enable logging mode

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

from iq import global_data
from iq.util import log_func
from iq.util import global_func
from iq import editor
import iq

__version__ = (0, 0, 1, 1)


def main(*argv):
    """
    Main function triggered.

    :param argv: Command line parameters.
    """
    # Parse command line arguments
    try:
        options, args = getopt.getopt(argv, 'h?vdl',
                                      ['help', 'version', 'debug', 'log',
                                       'mode=', 'engine=', 'prj=', 'username=', 'password=',
                                       'res_filename='])
    except getopt.error as msg:
        log_func.error(str(msg), is_force_print=True)
        log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
        log_func.printColourText(__doc__, color=log_func.GREEN_COLOR_TEXT)
        sys.exit(2)

    mode = None
    runtime_mode = False
    engine = global_data.DEFAULT_ENGINE_TYPE
    project = None
    username = None
    password = None
    res_filename = None

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
            log_func.printColourText(__doc__, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-v', '--version'):
            str_version = 'iqFramework %s' % '.'.join([str(sign) for sign in global_data.VERSION])
            log_func.printColourText(global_data.FRAMEWORK_LOGO_TXT, color=log_func.GREEN_COLOR_TEXT)
            log_func.printColourText(str_version, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            global_func.setDebugMode()
        elif option in ('-l', '--log'):
            global_func.setLogMode()
            log_func.init()
        elif option in ('--mode',):
            mode = arg.lower()
            runtime_mode = mode == iq.RUNTIME_MODE_STATE
            global_func.setRuntimeMode(runtime_mode)
        elif option in ('--engine',):
            engine = arg
            global_func.setEngineType(engine)
        elif option in ('--prj',):
            project = arg
        elif option in ('--username',):
            username = arg
        elif option in ('--password',):
            password = arg
        elif option in ('--res_filename',):
            res_filename = arg
        else:
            log_func.warning(u'Not supported parameter <%s>' % option)

    log_func.info(u'iqFramework <Engine: %s / Mode: %s>... START' % (engine, mode))

    if runtime_mode:
        kernel = iq.createKernel()
        kernel.start(mode=mode, project_name=project, username=username, password=password)
        kernel.stop()
    elif mode == iq.EDITOR_MODE_STATE and os.path.basename(__file__) == os.path.basename(res_filename):
        editor.openEditor()
    elif mode == iq.EDITOR_MODE_STATE:
        # kernel = iq.createKernel()
        editor.openResourceEditor(res_filename=res_filename)
    else:
        log_func.error(u'Engine type <%s : %s> not support' % (engine, mode))

    log_func.info(u'iqFramework <Engine: %s / Mode: %s>... STOP' % (engine, mode))


if __name__ == '__main__':
    main(*sys.argv[1:])
