#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object component.
"""

from ...components import data_navigator

from . import ref_object
from ...util import log_func

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

    def getCodLen(self):
        """
        Get list of level code lengths.
        """
        cod_len = self.getAttribute('cod_len')
        if cod_len:
            try:
                print(cod_len)
            except:
                log_func.fatal(u'Error level code lengths format <%s>' % cod_len)
        return ()


COMPONENT = iqDataRefObject
