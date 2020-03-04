#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mnemoscheme component.
"""

from ... import object

from . import spc
from . import mnemoscheme

__version__ = (0, 0, 0, 1)


class iqMnemoScheme(object.iqObject, mnemoscheme.iqMnemoSchemeManager):
    """
    Mnemoscheme component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        mnemoscheme.iqMnemoSchemeManager.__init__(self, *args, **kwargs)


COMPONENT = iqMnemoScheme
