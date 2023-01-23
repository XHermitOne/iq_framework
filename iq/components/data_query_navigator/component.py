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
from ...util import exec_func

from ..wx_filterchoicectrl import filter_convert

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

    def getQueryWhere(self):
        """
        Get WHERE section.
        """
        function_body = self.getAttribute('get_where')

        if function_body:
            context = self.getContext()
            context['self'] = self
            rec_filter = self.getRecFilter()
            context['REC_FILTER'] = rec_filter
            where = filter_convert.convertFilterWhereSection2PgSQLWhereSection(rec_filter)
            context['WHERE'] = where
            return exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)
        return None

    def getQueryOrderBy(self):
        """
        Get ORDER BY section.
        """
        function_body = self.getAttribute('get_order_by')

        if function_body:
            context = self.getContext()
            context['self'] = self
            context['ORDER_BY'] = self.getOrderBy()
            return exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)
        return None

    def getQueryLimit(self):
        """
        Get LIMIT section.
        """
        function_body = self.getAttribute('get_limit')

        if function_body:
            context = self.getContext()
            context['self'] = self
            context['LIMIT'] = self.getLimit()
            return exec_func.execTxtFunction(function=function_body, context=context, show_debug=True)
        return None


COMPONENT = iqDataQueryNavigator
