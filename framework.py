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
from iq.util.log import log_func
import iq

__version__ = (0, 0, 0, 1)


def main(*argv):
    """
    Main function triggered.
    @param argv: Command line parameters.
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

    username = None
    password = None

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            log_func.print_color_txt(__doc__, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-v', '--version'):
            str_version = 'iQ Framework %s' % '.'.join([str(sign) for sign in config.VERSION])
            log_func.print_color_txt(str_version, color=log_func.GREEN_COLOR_TEXT)
            sys.exit(0)
        elif option in ('-d', '--debug'):
            config.set_cfg_param('DEBUG_MODE', True)
            log_func.init(config)
        elif option in ('-l', '--log'):
            config.set_cfg_param('LOG_MODE', True)
            log_func.init(config)
        elif option in ('--mode',):
            runtime_mode = arg.lower() == 'runtime'
            editor_mode = arg.lower() == 'editor'
            config.set_cfg_param('RUNTIME_MODE', runtime_mode)
            config.set_cfg_param('EDITOR_MODE', editor_mode)
        elif option in ('--prj',):
            config.set_cfg_param('PROJECT_NAME', arg)
        elif option in ('--username',):
            username = arg
        elif option in ('--password',):
            password = arg

    kernel = iq.createKernel()
    kernel.start(username=username, password=password)


if __name__ == '__main__':
    main(*sys.argv[1:])
