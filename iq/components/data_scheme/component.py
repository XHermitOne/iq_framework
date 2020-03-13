#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme component.
"""

from ... import object

from . import spc
from . import scheme

__version__ = (0, 0, 0, 1)


class iqDataScheme(scheme.iqSchemeManager, object.iqObject):
    """
    Data scheme component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=spc.SPC, context=context)
        scheme.iqSchemeManager.__init__(self, *args, **kwargs)

    def getDBEngine(self):
        """
        Get database engine.

        :return:
        """
        psp = self.getAttribute('db_engine')
        kernel = self.getKernel()
        return kernel.getObject(psp)


COMPONENT = iqDataScheme
