#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text generate function by context.
"""

import re
import jinja2

from ..util import log_func
from ..util import global_func

__version__ = (0, 0, 0, 1)

REPLACE_NAME_START = u'{{'
REPLACE_NAME_END = u'}}'

VAR_PATTERN = r'(\{\{.*?\}\})'


def generate(text_template, context=None):
    """
    Generate text by context.

    :param text_template: Template text.
    :param context. Context dictionary.
    :return: Generated text or None if error.
    """
    if context is None:
        context = dict()

    try:
        template = jinja2.Template(text_template)
        result_txt = template.render(**context)
        return result_txt
    except:
        log_func.fatal(u'Error generate text <%s>' % text_template)
    return None


def isGenered(txt):
    """
    Checking if the text is generated.
         Those. whether it contains the necessary replacements.

    :param txt: Text.
    :return: True - there are replacements, False - no replacements.
    """
    if not isinstance(txt, str):
        return False

    if isinstance(txt, bytes):
        txt = txt.decode(global_func.getDefaultEncoding())
    return REPLACE_NAME_START in txt and REPLACE_NAME_END in txt


def getReplaceNames(txt):
    """
    Get replacement names.

    :param txt: Text.
    :return: Replacentent name list.
    """
    if txt is None:
        log_func.warning(u'Not define text for replacements')
        return list()

    try:
        replaces = re.findall(VAR_PATTERN, txt)
        return [replace_name[len(REPLACE_NAME_START):-len(REPLACE_NAME_END)].strip() for replace_name in replaces]
    except:
        log_func.fatal(u'Error get replacement names from text\n<%s>' % txt)
    return list()

