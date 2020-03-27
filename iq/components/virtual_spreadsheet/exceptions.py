#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exceptions used in VirtualExcel.
"""

__version__ = (0, 0, 0, 1)


class iqMergeCellError(Exception):
    """
    Error accessing the forbidden area of the merged cell.
    """
    def __init__(self, args=None, user=None):
        self.args = args


class iqCellAddressInvalidError(Exception):
    """
    Invalid cell address error.
    """
    def __init__(self, args=None, user=None):
        self.args = args
