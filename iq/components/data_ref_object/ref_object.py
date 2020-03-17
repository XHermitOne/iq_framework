#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object manager.
"""

# import sqlalchemy

from ..data_navigator import model_navigator

from ...util import log_func

__version__ = (0, 0, 0, 1)

DEFAULT_COD_COL_NAME = 'cod'
DEFAULT_NAME_COL_NAME = 'name'
DEFAULT_ACTIVE_COL_NAME = 'activate'


class iqRefObjectManager(model_navigator.iqModelNavigatorManager):
    """
    Reference data object manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        model_navigator.iqModelNavigatorManager.__init__(self, model=model)

    def getCodColumnName(self):
        """
        Get cod column name.
        """
        return DEFAULT_COD_COL_NAME

    def getNameColumnName(self):
        """
        Get name column name.
        """
        return DEFAULT_NAME_COL_NAME

    def getActiveColumnName(self):
        """
        Get active column name.
        """
        return DEFAULT_ACTIVE_COL_NAME

    def clear(self):
        """
        Clear reference data object tables.

        :return: True/False.
        """
        try:
            self.getModelQuery().delete(synchronize_session=False)
            self.getScheme().getSession().commit()
            log_func.info(u'Clear reference data object <%s>' % self.getName())
            return True
        except:
            self.getScheme().getSession().rollback()
            log_func.fatal(u'Error clear reference data object <%s>' % self.getName())
        return False

    def getRecByCod(self, cod):
        """
        Get record by cod.

        :param cod: Reference data code.
        :return: Record dictionary or None if error.
        """
        try:
            model = self.getModel()
            records = self.getModelQuery().filter(getattr(model, self.getCodColumnName()) == cod)
            if records.count():
                # Presentation of query result in the form of a dictionary
                return records.first().__dict__
            else:
                log_func.warning(u'Reference data code <%s> not found in <%s>' % (cod, self.getName()))
        except:
            log_func.fatal(u'Error get reference data object <%s> record by code' % self.getName())
        return False

