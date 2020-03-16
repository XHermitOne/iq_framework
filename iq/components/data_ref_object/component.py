#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object component.
"""

from ...components import data_navigator

# from . import spc
from . import ref_object
# from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqDataRefObject(ref_object.iqRefObjectManager, data_navigator.COMPONENT):
    """
    Reference data object component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        data_navigator.COMPONENT.__init__(self, parent=parent, resource=resource, context=context)
        ref_object.iqRefObjectManager.__init__(self, *args, **kwargs)

    def getCodColumnName(self):
        """
        Get cod column name.
        """
        return self.getAttribute('cod_column')

    def getNameColumnName(self):
        """
        Get name column name.
        """
        return self.getAttribute('name_column')

    def getActiveColumnName(self):
        """
        Get active column name.
        """
        return self.getAttribute('active_column')


COMPONENT = iqDataRefObject
