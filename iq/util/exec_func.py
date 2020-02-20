#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Execute functions module.
"""

import os
import uuid

from . import log_func

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
