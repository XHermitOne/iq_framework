#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text generate function by context.
"""

import jinja2

from ..util import log_func

__version__ = (0, 0, 0, 1)


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

