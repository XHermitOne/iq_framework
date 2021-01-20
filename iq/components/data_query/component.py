#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query component.
"""

from ... import object

from . import spc
from . import query

from ...dialog import dlg_func
from ...util import log_func
from ...util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqDataQuery(query.iqDBQuery, object.iqObject):
    """
    Data query component.
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
        query.iqDBQuery.__init__(self, *args, **kwargs)

    def getDBPsp(self):
        """
        Get database engine passport.

        :return: DB engine passport or None if error.
        """
        return self.getAttribute('db_engine')

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

    def getSQLText(self):
        """
        Get SQL query text.

        :return: SQL query text or None if error.
        """
        return self.getAttribute('sql_txt')

    def test(self):
        """
        Object test function.

        :return: True/False.
        """
        from . import view_sql_query_dlg

        db = self.getDBEngine()
        sql_txt = self.getSQLText()
        return view_sql_query_dlg.viewSQLQueryDlg(parent=None, db=db, sql_txt=sql_txt)


COMPONENT = iqDataQuery
