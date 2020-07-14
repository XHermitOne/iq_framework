#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging functions.
"""

import sys
import logging
import os
import os.path
import tempfile
import stat
import traceback

try:
    import colorama
    colorama.init()
except ImportError:
    print(u'Import error colorama. Install: pip3 install colorama')

from . import global_func

__version__ = (0, 0, 0, 1)

# Shell text colors
RED_COLOR_TEXT = '\x1b[31;1m'       # red
GREEN_COLOR_TEXT = '\x1b[32m'       # green
YELLOW_COLOR_TEXT = '\x1b[33;1m'    # yellow
BLUE_COLOR_TEXT = '\x1b[34m'        # blue
PURPLE_COLOR_TEXT = '\x1b[35m'      # purple
CYAN_COLOR_TEXT = '\x1b[36m'        # cyan
WHITE_COLOR_TEXT = '\x1b[37m'       # white
NORMAL_COLOR_TEXT = '\x1b[0m'       # normal

NOT_INIT_LOG_SYS_MSG = u'Not Initialized Logging System'

LOG_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'


def printColourText(text, color=NORMAL_COLOR_TEXT):
    if sys.platform.startswith('win'):
        # Color coded for Windows systems disabled
        if color == RED_COLOR_TEXT:
            txt = colorama.Fore.RED + text + colorama.Style.RESET_ALL
        elif color == GREEN_COLOR_TEXT:
            txt = colorama.Fore.GREEN + text + colorama.Style.RESET_ALL
        elif color == YELLOW_COLOR_TEXT:
            txt = colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL
        elif color == BLUE_COLOR_TEXT:
            txt = colorama.Fore.BLUE + text + colorama.Style.RESET_ALL
        elif color == PURPLE_COLOR_TEXT:
            txt = colorama.Fore.MAGENTA + text + colorama.Style.RESET_ALL
        elif color == CYAN_COLOR_TEXT:
            txt = colorama.Fore.CYAN + text + colorama.Style.RESET_ALL
        elif color == WHITE_COLOR_TEXT:
            txt = colorama.Fore.WHITE + text + colorama.Style.RESET_ALL
        elif color == NORMAL_COLOR_TEXT:
            txt = colorama.Style.RESET_ALL + text
        else:
            txt = text
    else:
        # Add color coloring
        txt = color + text + NORMAL_COLOR_TEXT
    print(txt)        


def init(log_filename=None):
    """
    Initializing the log file.

    :param log_filename: Log file name.
    """
    if not global_func.isLogMode():
        return
    
    if log_filename is None:
        log_filename = global_func.getLogFilename()
        if not log_filename:
            log_filename = tempfile.mktemp()
    else:
        global_func.setLogFilename(log_filename)
        
    # Create a log folder if it is missing
    log_dirname = os.path.normpath(os.path.dirname(log_filename))
    if not os.path.exists(log_dirname):
        os.makedirs(log_dirname)
        
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt=LOG_DATETIME_FMT,
                        filename=log_filename,
                        filemode='a')
    # ATTENTION! immediately set write / read rights for all
    # otherwise, in some cases, it may not be written to the file and therefore fall
    if os.path.exists(log_filename):
        os.chmod(log_filename,
                 stat.S_IWUSR | stat.S_IRUSR |
                 stat.S_IWGRP | stat.S_IRGRP |
                 stat.S_IWOTH | stat.S_IROTH)

    if global_func.isDebugMode():
        printColourText('INFO. Initializing the log file <%s>' % log_filename, GREEN_COLOR_TEXT)


def debug(message=u'', is_force_print=False, is_force_log=False):
    """
    Display debug information.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    if global_func.isDebugMode() or is_force_print:
        printColourText('DEBUG. ' + message, BLUE_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.debug(message)


def info(message=u'', is_force_print=False, is_force_log=False):
    """
    Print information.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    if global_func.isDebugMode() or is_force_print:
        printColourText('INFO. ' + message, GREEN_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.info(message)


def error(message=u'', is_force_print=False, is_force_log=False):
    """
    Print error message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    if global_func.isDebugMode() or is_force_print:
        printColourText('ERROR. ' + message, RED_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.error(message)


def warning(message=u'', is_force_print=False, is_force_log=False):
    """
    Print warning message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    if global_func.isDebugMode() or is_force_print:
        printColourText('WARNING. ' + message, YELLOW_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.warning(message)


def fatal(message=u'', is_force_print=False, is_force_log=False):
    """
    Print critical error message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    trace_txt = traceback.format_exc()

    try:
        msg = message + os.linesep + trace_txt
    except UnicodeDecodeError:
        if not isinstance(message, str):
            message = str(message)
        if not isinstance(trace_txt, str):
            trace_txt = str(trace_txt)
        msg = message + os.linesep + trace_txt

    if global_func.isDebugMode() or is_force_print:
        printColourText('FATAL. ' + msg, RED_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.fatal(msg)


def service(message=u'', is_force_print=False, is_force_log=False):
    """
    Print service message.

    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    if global_func.isDebugMode() or is_force_print:
        printColourText('SERVICE. ' + message, CYAN_COLOR_TEXT)
    if global_func.isLogMode() or is_force_log:
        logging.debug('SERVICE. ' + message)
