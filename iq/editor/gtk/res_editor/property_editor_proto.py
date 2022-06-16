#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Property editor abstract class.
"""

__version__ = (0, 0, 0, 1)


class iqPropertyEditorProto(object):
    """
    Property editor abstract class.
    """
    def __init__(self, label='', value=None, choices=None, default=None):
        """
        Constructor.

        :param label: Property label.
        :param value: Property value.
        :param choices: Property choices for selection.
        :param default: Property default value.
        """
        self.label = label
        self.value = value
        self.choices = choices
        self.default = default
        self.help_string = None

    def setHelpString(self, help_string):
        """
        Set help string.

        :param help_string: Help string.
        """
        self.help_string = help_string
