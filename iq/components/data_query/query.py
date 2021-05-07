#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query component.
"""

from ...util import log_func
from ...util import txtgen_func

from ..data_model import data_object
__version__ = (0, 0, 1, 1)


class iqDBQuery(data_object.iqDataObjectProto):
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

        full_sql_txt = txtgen_func.generate(sql_txt, variables)
        log_func.debug(u'Execute SQL:\n%s' % full_sql_txt)
        try:
            if full_sql_txt:
                return db.executeSQL(full_sql_txt)
        except:
            log_func.fatal(u'Error execute query <%s>' % full_sql_txt)
        return None

    def genSQLText(self, **variables):
        """
        Generate SQL query text.

        :param variables: SQL query variables.
        :return: SQL query text or None if error.
        """
        sql_txt = self.getSQLText()

        if not sql_txt:
            log_func.warning(u'Empty SQL text for generation in <%s>' % self.getName())
            return None

        try:
            full_sql_txt = txtgen_func.generate(sql_txt, variables)
            return full_sql_txt
        except:
            log_func.fatal(u'Error generate SQL query <%s>' % sql_txt)
        return None

    def getDataset(self, *args, **kwargs):
        """
        Get dataset.

        :return: Record dictionary list.
        """
        records = self.execute(**kwargs)
        if records is not None:
            return records
        return list()
