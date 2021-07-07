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
    import termcolor
except IndexError:
    print(u'Import error termcolor. Install: pip3 install termcolor')

if sys.platform.startswith('win'):
    try:
        import colorama
        colorama.init()
    except ImportError:
        print(u'Import error colorama. Install: pip3 install colorama')

from . import global_func

__version__ = (0, 0, 1, 2)

# Shell text colors
RED_COLOR_TEXT = 'red'
GREEN_COLOR_TEXT = 'green'
YELLOW_COLOR_TEXT = 'yellow'
BLUE_COLOR_TEXT = 'blue'
MAGENTA_COLOR_TEXT = 'magenta'
CYAN_COLOR_TEXT = 'cyan'
WHITE_COLOR_TEXT = 'white'
GREY_COLOR_TEXT = 'grey'
NORMAL_COLOR_TEXT = None

NOT_INIT_LOG_SYS_MSG = u'Not Initialized Logging System'

LOG_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'


def printColourText(text, color=NORMAL_COLOR_TEXT):
    """
    Print colour text in console/shell.

    :param text: Text.
    :param color: Colour code.
    """
    if color == NORMAL_COLOR_TEXT:
        txt = text
    elif sys.platform.startswith('win'):
        try:
            if color in termcolor.COLORS:
                txt = termcolor.colored(text, color)
            else:
                print(termcolor.colored(u'Not supported color <%s>' % color, 'red'))
                txt = text
        except NameError:
            print(u'ERROR: Not install colorama and termcolor libraries')
            txt = text
    else:
        try:
            if color in termcolor.COLORS:
                txt = termcolor.colored(text, color)
            else:
                print(termcolor.colored(u'Not supported color <%s>' % color, 'red'))
                txt = text
        except:
            print(u'ERROR: Not install termcolor library')
            txt = text
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
        try:
            os.makedirs(log_dirname)
        except OSError:
            printColourText(u'Error create log directory <%s>' % log_dirname, color=RED_COLOR_TEXT)

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
