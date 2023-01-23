#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pandas DataFrame functions.
"""

import sqlalchemy

from . import log_func

__version__ = (0, 0, 0, 1)


def dataframe2sql(dataframe, db_url, table_name, rewrite=True):
    """
    Convert a pandas DataFrame to SQL table.

    :param dataframe: Pandas DataFrame object.
    :param db_url: Database URL.
    :param table_name: Destination table name.
    :param rewrite: Rewrite destination table?
        If False then append to destination table.
    :return: True/False.
    """
    try:
        db_engine = sqlalchemy.create_engine(db_url, echo=False)
        dataframe.to_sql(table_name, con=db_engine,
                         if_exists='replace' if rewrite else 'append')
        return True
    except:
        log_func.fatal(u'Error convert DataFrame to SQL table <%s : %s>' % (db_url, table_name))
    return False
