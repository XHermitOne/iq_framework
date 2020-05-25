#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Numerator component.
"""

from ... import object

from . import spc
from . import numerator

from ...util import log_func
from ...util import dt_func

__version__ = (0, 0, 0, 1)


class iqNumerator(numerator.iqNumeratorProto, object.iqObject):
    """
    Numerator component.
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

        numerator.iqNumeratorProto.__init__(db_url=self.getDBUrl(),
                                            numerator_table_name=self.getTabName(),
                                            num_code_format=self.getNumCodeFormat(),
                                            check_unique=self.getCheckUnique())

    def getDB(self):
        """
        Database engine object.
        """
        db_psp = self.getAttribute('db_engine')
        db = None
        if db_psp:
            db = self.getKernel().get(db_psp)
        else:
            log_func.error(u'Not define DB engine in <%s>' % self.getName())
        return db

    def getDBUrl(self):
        """
        Get database URL / connection string.
        """
        db = self.getDB()
        if db:
            return db.getURL()
        return None

    def getTabName(self):
        """
        Numerator table name.
        """
        return self.getAttribute('num_tabname')

    def getNumCodeFormat(self):
        """
        Get number-code format.
        The numbering code format can contain all temporary formats,
        and
             <%N> - the identifier number of the row of the numbering table.
             <%E> - additional parameters passed to the function
                    generating code as additional arguments.
        """
        return self.getAttribute('num_code_fmt')

    def getCheckUnique(self):
        """
        Check the uniqueness of the generated code number?
        """
        return self.getAttribute('check_unique')

    def getUseSysDT(self):
        """
        Use system date-time?
        """
        return self.getAttribute('use_sys_dt')

    def getActualYear(self):
        """
        Get actual year for define maximal counter.

        :return: Actual year.
        """
        if self.getUseSysDT():
            return dt_func.getNowYear()

        operate_year = dt_func.getOperateYear()
        return operate_year if operate_year else dt_func.getNowYear()


COMPONENT = iqNumerator
