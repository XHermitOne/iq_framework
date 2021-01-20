#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query component.
"""

from ...util import log_func
from ...util import txtgen_func

__version__ = (0, 0, 0, 1)


class iqDBQuery(object):
    """
    Database query class.
    """
    def __init__(self):
        """
        Constructor.
        """
        pass

    def getDBEngine(self):
        """
        Get database engine.

        :return: DB engine object or None if error.
        """
        log_func.error(u'Not define getDBEngine method in <%s>' % self.__class__.__name__)
        return None

    def getSQLText(self):
        """
        Get SQL query text.

        :return: SQL query text or None if error.
        """
        log_func.error(u'Not define getSQLText method in <%s>' % self.__class__.__name__)
        return None

    def execute(self, **variables):
        """
        Execute query.

        :param variables: SQL query variables.
        :return: Execute query result or None if error.
        """
        db = self.getDBEngine()
        sql_txt = self.getSQLText()

        if not db or not sql_txt:
            return None

        try:
            full_sql_txt = txtgen_func.generate(sql_txt, variables)
            if full_sql_txt:
                return db.executeSQL(full_sql_txt)
        except:
            log_func.fatal(u'Error execute query <%s>' % sql_txt)
        return None
