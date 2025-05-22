#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug mode functions.
"""

import sys

try:
    import rich.console
except ImportError:
    print(u'Not found rich library. Install: pip3 install rich')
    sys.exit(1)

from . import global_func

__version__ = (0, 1, 1, 1)


CONSOLE = rich.console.Console()
EXCEPTION_EXTRA_LINE_COUNT = 8


def printStyledText(text, style=None):
    """
    Print styled text in console.

    :param text: Text.
    :param style: Text style.
    """
    if not isinstance(text, str):
        text = str(text)

    CONSOLE.print(text, style=style)


def debug(message=u'', is_force_print=False):
    """
    Print debug message.

    :param message: Message text.
    :param is_force_print: Forcibly display.
    """
    if not isinstance(message, str):
        message = str(message)

    if global_func.isDebugMode() or is_force_print:
        printStyledText(message, style='blue')


def info(message=u'', is_force_print=False):
    """
    Print information message.

    :param message: Message text.
    :param is_force_print: Forcibly display.
    """
    if not isinstance(message, str):
        message = str(message)

    if global_func.isDebugMode() or is_force_print:
        printStyledText(message, style='green')


def warning(message=u'', is_force_print=False):
    """
    Print warning message.

    :param message: Message text.
    :param is_force_print: Forcibly display.
    """
    if not isinstance(message, str):
        message = str(message)

    if global_func.isDebugMode() or is_force_print:
        printStyledText(message, style='yellow')


def error(message=u'', is_force_print=False):
    """
    Print error message.

    :param message: Message text.
    :param is_force_print: Forcibly display.
    """
    if not isinstance(message, str):
        message = str(message)

    if global_func.isDebugMode() or is_force_print:
        printStyledText(message, style='red')


def fatal(message=u'', is_force_print=False):
    """
    Print exception.

    :param message: Message text.
    :param is_force_print: Forcibly display.
    """
    if global_func.isDebugMode() or is_force_print:
        error(message, is_force_print=is_force_print)
        CONSOLE.print_exception(extra_lines=EXCEPTION_EXTRA_LINE_COUNT, show_locals=True)
