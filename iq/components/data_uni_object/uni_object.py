#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object manager.
"""

import sqlalchemy.sql

from ..data_navigator import model_navigator

from ...util import log_func
from ...util import global_func

__version__ = (0, 0, 0, 1)

DEFAULT_GUID_COL_NAME = 'guid'
DEFAULT_NAME_COL_NAME = 'name'
DEFAULT_NUM_COL_NAME = 'num'
DEFAULT_ACTIVE_COL_NAME = 'activate'


class iqUniObjectManager(model_navigator.iqModelNavigatorManager):
    """
    Unique data object manager.
    """
    def __init__(self, model=None, *args, **kwargs):
        """
        Constructor.

        :param model: Model.
        """
        model_navigator.iqModelNavigatorManager.__init__(self, model=model)

    def getGuidColumnName(self):
        """
        Get GUID column name.
        """
        return DEFAULT_GUID_COL_NAME

    def getNameColumnName(self):
        """
        Get name column name.
        """
        return DEFAULT_NAME_COL_NAME

    def getNumColumnName(self):
        """
        Get num column name.
        """
        return DEFAULT_NUM_COL_NAME

    def getActiveColumnName(self):
        """
        Get active column name.
        """
        return DEFAULT_ACTIVE_COL_NAME

    def clear(self):
        """
        Clear unique data object tables.

        :return: True/False.
        """
        try:
            self.getModelQuery().delete(synchronize_session=False)
            self.getScheme().getSession().commit()
            log_func.info(u'Clear unique data object <%s>' % self.getName())
            return True
        except:
            self.getScheme().getSession().rollback()
            log_func.fatal(u'Error clear unique data object <%s>' % self.getName())
        return False

    def getRecByGuid(self, guid):
        """
        Get record by guid.

        :param guid: Unique data GUID.
        :return: Record dictionary or None if error.
        """
        try:
            model = self.getModel()
            records = self.getModelQuery().filter(getattr(model, self.getGuidColumnName()) == guid)
            if records.count():
                # Presentation of query result in the form of a dictionary
                return records.first().__dict__
            else:
                log_func.warning(u'Unique data guid <%s> not found in <%s>' % (guid, self.getName()))
        except:
            log_func.fatal(u'Error get unique data object <%s> record by guid' % self.getName())
        return False

    def getDataObjectRec(self, value):
        """
        Get data object record by value.

        :param value: Unique data GUID.
        :return: Record dictionary or None if error.
        """
        return self.getRecByGuid(guid=value)

    def isEmpty(self):
        """
        Is the ref object empty?

        :return: True/False.
        """
        try:
            rec_count = self.getModelQuery().count()
            # log_func.debug(u'Check empty ref object <%s>' % rec_count)
            return not bool(rec_count)
        except:
            log_func.fatal(u'Error check empty unique object <%s>' % self.getName())
        return None

    def hasGuid(self, guid):
        """
        Is there such code in the unique object?

        :param guid: Unique object GUID.
        :return: True/False.
        """
        try:
            model = self.getModel()
            rec_count = self.getModelQuery().filter(getattr(model, self.getGuidColumnName()) == guid).count()
            return bool(rec_count)
        except:
            log_func.fatal(u'Error check GUID unique object <%s>' % self.getName())
        return None

