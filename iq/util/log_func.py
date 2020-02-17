#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging features.
"""

import sys
import logging
import os
import os.path
import tempfile
import stat
import traceback
import locale

__version__ = (0, 0, 0, 1)

# Default shell encoding
DEFAULT_ENCODING = sys.stdout.encoding if sys.platform.startswith('win') else locale.getpreferredencoding()

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


def print_color_txt(text, color=NORMAL_COLOR_TEXT):
    if sys.platform.startswith('win'):
        # Color coded for Windows systems disabled
        txt = text
    else:
        # Add color coloring
        txt = color + text + NORMAL_COLOR_TEXT
    print(txt)        


# Configuration module
CONFIG = None


def get_default_encoding():
    """
    Determine the current encoding for text output.
    :return: Actual text encoding.
    """
    global CONFIG
    if CONFIG is not None and hasattr(CONFIG, 'DEFAULT_ENCODING'):
        # The priority is the explicitly specified encoding in the configuration file
        return CONFIG.DEFAULT_ENCODING
    return DEFAULT_ENCODING


def get_debug_mode():
    """
    Determine the current debug mode.
    The default mode is off.
    :return: True - debug mode enabled / False - debug mode off.
    """
    global CONFIG
    if CONFIG is not None and hasattr(CONFIG, 'DEBUG_MODE'):
        # The priority is explicitly specified parameter in the configuration file.
        return CONFIG.DEBUG_MODE
    # The default mode is off
    return False


def get_log_mode():
    """
    Determine the current logging mode.
    The default mode is off.
    :return: True - logging mode enabled / False - logging mode is off.
    """
    global CONFIG
    if CONFIG is not None and hasattr(CONFIG, 'LOG_MODE'):
        # The priority is explicitly specified parameter in the configuration file.
        return CONFIG.LOG_MODE
    # The default mode is off.
    return False


def get_log_filename():
    """
    The name of the log file.
    :return: The name of the log file.
    """
    global CONFIG
    return CONFIG.LOG_FILENAME if CONFIG and hasattr(CONFIG, 'LOG_FILENAME') else None


def init(config=None, log_filename=None):
    """
    Initializing the log file.
    :param config: Configuration module.
    :param log_filename: Log file name.
    """
    global CONFIG
    CONFIG = config
    
    if not get_log_mode():
        return
    
    if log_filename is None:
        log_filename = CONFIG.LOG_FILENAME if hasattr(CONFIG, 'LOG_FILENAME') else tempfile.mktemp()
        
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

    if get_debug_mode():
        print_color_txt('INFO. Initializing the log file <%s>' % log_filename, GREEN_COLOR_TEXT)


def debug(message=u'', is_force_print=False, is_force_log=False):
    """
    Display debug information.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG
    
    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('DEBUG. ' + message, BLUE_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.debug(message)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('DEBUG. ' + message, BLUE_COLOR_TEXT)


def info(message=u'', is_force_print=False, is_force_log=False):
    """
    Print information.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG
    
    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('INFO. ' + message, GREEN_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.info(message)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('INFO. ' + message, GREEN_COLOR_TEXT)


def error(message=u'', is_force_print=False, is_force_log=False):
    """
    Print error message.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG
    
    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('ERROR. ' + message, RED_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.error(message)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('ERROR. ' + message, RED_COLOR_TEXT)


def warning(message=u'', is_force_print=False, is_force_log=False):
    """
    Print warning message.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG
    
    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('WARNING. ' + message, YELLOW_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.warning(message)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('WARNING. ' + message, YELLOW_COLOR_TEXT)


def fatal(message=u'', is_force_print=False, is_force_log=False):
    """
    Print critical error message.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG

    trace_txt = traceback.format_exc()

    try:
        msg = message + os.linesep + trace_txt
    except UnicodeDecodeError:
        if not isinstance(message, str):
            message = str(message)
        if not isinstance(trace_txt, str):
            trace_txt = str(trace_txt)
        msg = message + os.linesep + trace_txt

    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('FATAL. '+msg, RED_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.fatal(msg)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('FATAL. ' + msg, RED_COLOR_TEXT)


def service(message=u'', is_force_print=False, is_force_log=False):
    """
    Print service message.
    :param message: Text message.
    :param is_force_print: Forcibly display.
    :param is_force_log: Forcibly recorded in a journal.
    """
    global CONFIG

    if CONFIG:
        if get_debug_mode() or is_force_print:
            print_color_txt('SERVICE. ' + message, CYAN_COLOR_TEXT)
        if get_log_mode() or is_force_log:
            logging.debug('SERVICE. ' + message)
    else:
        print_color_txt(NOT_INIT_LOG_SYS_MSG, PURPLE_COLOR_TEXT)
        print_color_txt('SERVICE. ' + message, CYAN_COLOR_TEXT)
