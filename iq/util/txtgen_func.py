#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text generate function by context.
"""

import os
import os.path
import re
import jinja2

from ..util import log_func
from ..util import global_func
from ..util import file_func

__version__ = (0, 1, 1, 1)

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


def generateTextFile(template_filename, output_filename, context=None, encoding='utf-8'):
    """
    Generate text file by template file.

    :param template_filename: Template text filename.
    :param output_filename: Result filename.
    :param context: Context dictionary.
    :param encoding: Result file code page.
    :return: True/False.
    """
    template_file = None
    output_file = None

    template_filename = os.path.abspath(template_filename)
    if not os.path.exists(template_filename):
        log_func.warning(u'Template file <%s> not found' % template_filename)
        return False

    # Read template
    try:
        template_file = open(template_filename, 'rt')
        template_txt = template_file.read()
        template_file.close()
    except:
        if template_file:
            template_file.close()
        log_func.fatal(u'Error read template file <%s>' % template_filename)
        return False

    # Generate text
    gen_txt = generate(template_txt, context)

    # Write output file
    output_filename = os.path.abspath(output_filename)
    try:
        output_path = os.path.dirname(output_filename)
        if not os.path.exists(output_path):
            file_func.createDir(output_path)

        output_file = open(output_filename, 'wt+', encoding=encoding)
        output_file.write(gen_txt)
        output_file.close()
        return os.path.exists(output_filename)
    except:
        if output_file:
            output_file.close()
        log_func.fatal(u'Error generate file <%s> by template <%s>' % (output_filename, template_filename))
    return False
