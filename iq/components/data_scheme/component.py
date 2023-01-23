#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme component.
"""

from ... import object

from . import spc
from . import scheme

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqDataScheme(scheme.iqSchemeManager, object.iqObject):
    """
    Data scheme component.
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

    def getDBEngine(self):
        """
        Get database engine.

        :return: DB engine object or None if error.
        """
        psp = self.getAttribute('db_engine')
        if psp:
            kernel = self.getKernel()
            return kernel.getObject(psp, register=True)
        else:
            log_func.warning(u'Not define DB engine in data scheme <%s>' % self.getName())
        return None


COMPONENT = iqDataScheme
