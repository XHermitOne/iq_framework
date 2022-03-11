#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query dataset navigator component.
"""

from ... import object

from . import spc
from . import query_navigator
# from ..data_scheme import scheme as scheme_module

from ...passport import passport
from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqDataQueryNavigator(query_navigator.iqQueryNavigatorManager, object.iqObject):
    """
    Data query dataset navigator component.
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
        query_navigator.iqQueryNavigatorManager.__init__(self, *args, **kwargs)

        # Set query object
        query_psp = self.getQueryPsp()
        if query_psp:
            query = self.getKernel().getObject(psp=query_psp)
            self.setQuery(query)

    def getQueryPsp(self):
        """
        Get query passport.
        """
        query_psp = self.getAttribute('query')
        if passport.isPassport(query_psp):
            return query_psp
        else:
            log_func.warning(u'<%s> object. <%s> component. Not define query' % (self.getName(), self.__class__.__name__))

    def getQueryWhereName(self):
        """
        Get records filter name in Query expression WHERE section.
        """
        return self.getAttribute('where_name')

    def getQueryOrderByName(self):
        """
        Sorting name in Query expression ORDER BY section.
        """
        return self.getAttribute('order_by_name')

    def getQueryLimitName(self):
        """
        Limiting name in Query expression LIMIT section.
        """
        return self.getAttribute('limit_name')


COMPONENT = iqDataQueryNavigator
