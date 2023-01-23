#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Virtual spreadsheet component.
"""

from ... import object

from . import spc

from ...util import log_func

from . import v_spreadsheet

__version__ = (0, 0, 0, 1)


class iqVirtualSpreadsheet(v_spreadsheet.iqVSpreadsheet, object.iqObject):
    """
    Virtual spreadsheet component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        v_spreadsheet.iqVSpreadsheet.__init__(self, *args, **kwargs)


COMPONENT = iqVirtualSpreadsheet
