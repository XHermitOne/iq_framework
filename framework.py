#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iQ Framework - RAD Software platform for developing applications in Python using the PyQt GUI.

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
        --prj=              Project name
        --username=         User name
        --password=         User password
"""

import sys
import getopt

from iq import config
from iq.util import log_func
from iq.util import global_func
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
                                       'mode=', 'prj=', 'username=', 'password='])
    except getopt.error as msg:
        log_func.error(str(msg), is_force_print=True)
        log_func.print_color_txt(__doc__, color=log_func.GREEN_COLOR_TEXT)
        sys.exit(2)

    mode=None
    project = None
    username = None
    password = None
    # runtime_mode = False

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            log_func.print_color_txt(__doc__, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-v', '--version'):
            str_version = 'iQ Framework %s' % '.'.join([str(sign) for sign in config.VERSION])
            log_func.print_color_txt(str_version, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            global_func.setDebugMode()
            log_func.init(config)
        elif option in ('-l', '--log'):
            global_func.setLogMode()
            log_func.init(config)
        elif option in ('--mode',):
            mode = arg.lower()
            runtime_mode = mode == iq.RUNTIME_MODE_STATE
            global_func.setRuntimeMode(runtime_mode)
        elif option in ('--prj',):
            project = arg
        elif option in ('--username',):
            username = arg
        elif option in ('--password',):
            password = arg

    kernel = iq.createKernel()
    kernel.start(mode=mode, project_name=project, username=username, password=password)


if __name__ == '__main__':
    main(*sys.argv[1:])