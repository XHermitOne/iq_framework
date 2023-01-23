#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Column types constants.
"""

import sqlalchemy.types

__version__ = (0, 0, 0, 1)


SQLALCHEMY_TEXT_TYPES = (sqlalchemy.types.Text,
                         sqlalchemy.types.TEXT,
                         sqlalchemy.types.UnicodeText,
                         )

SQLALCHEMY_FLOAT_TYPES = (sqlalchemy.types.Float,
                          sqlalchemy.types.FLOAT,
                          sqlalchemy.types.DECIMAL,
                          )

SQLALCHEMY_INT_TYPES = (sqlalchemy.types.Integer,
                        sqlalchemy.types.INTEGER,
                        sqlalchemy.types.BigInteger,
                        sqlalchemy.types.SmallInteger,
                        sqlalchemy.types.BIGINT,
                        sqlalchemy.types.SMALLINT,
                        )

SQLALCHEMY_DATE_TYPES = (sqlalchemy.types.Date,
                         sqlalchemy.types.DATE,
                         )

SQLALCHEMY_DATETIME_TYPES = (sqlalchemy.types.DateTime,
                             sqlalchemy.types.DATETIME,
                             )
