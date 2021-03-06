#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object manager.
"""

import sqlalchemy.sql

from ..data_navigator import model_navigator

from ...util import log_func
from ...util import lang_func
from ...util import id_func
from ...dialog import dlg_func

from ..wx_filterchoicectrl import filter_convert

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

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

        # Current filter data
        self._filter = None

    def setFilter(self, filter_data=None):
        """
        Set current filter data.

        :param filter_data: Filter data.
            If None then not filtered.
        :return: True/False.
        """
        self._filter = filter_data

    def getFilterData(self):
        """
        Get current filter data.
        """
        return self._filter

    def filterDataset(self, filter_data=None, limit=None, sort_columns=None):
        """
        Get filtered dataset.

        :param filter_data: Filter data.
        :param limit: Record number limit.
        :param sort_columns: Sort columns names.
        :return: Dataset.
        """
        if filter_data:
            self.setFilter(filter_data)

        try:
            if self._filter:
                model = self.getModel()
                query = self.getModelQuery()
                sql_filter = filter_convert.convertFilter2SQLAlchemyQuery(filter_data=self._filter,
                                                                          model=model,
                                                                          query=query,
                                                                          limit=limit,
                                                                          order_by=sort_columns)
                # Execute SQL
                try:
                    records = sql_filter.all()
                    log_func.debug(u'Filter uni object <%s>:\n%s\nRecord count [%d]' % (self.getName(), str(sql_filter), len(records)))
                except:
                    log_func.fatal(u'Error execute SQL filter <%s>' % str(sql_filter))
                    records = list()

                self.__dataset__ = [vars(record) for record in records]
                self.__dataset__ = self._updateLinkDataDataset(self.__dataset__)
            return self.getDataset()
        except:
            log_func.fatal(u'Error filter dataset unic object <%s>' % self.getName())
        return list()

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

    def newRec(self, record):
        """
        Create new record.

        :param record: Record dictionary.
        :return: New model object or None if error.
        """
        if not record.get(DEFAULT_GUID_COL_NAME, None):
            record[DEFAULT_GUID_COL_NAME] = id_func.genGUID()
        return model_navigator.iqModelNavigatorManager.newRec(self, record=record)

    def save(self, guid=None, save_record=None):
        """
        Save object by GUID.

        :param guid: GUID object.
        :param save_record: Save record dictionary.
        :return: True/False.
        """
        if guid is None:
            log_func.warning(u'Not define unic object GUID for save')
            return False
        log_func.debug(u'Save unic object <%s>' % guid)
        return self.saveRec(id=guid, record=save_record,
                            id_field=DEFAULT_GUID_COL_NAME)

    def delete(self, guid=None, ask=True):
        """
        Delete object by GUID.

        :param guid: GUID object.
        :param ask: Ask user to delete?
        :return: True/False.
        """
        if guid is None:
            log_func.warning(u'Not define unic object GUID for delete')
            return False

        can_delete = dlg_func.openAskBox(title=_('DELETE'),
                                         prompt_text=_(u'Confirm deletion')) if ask else True
        if can_delete:
            return self.deleteRec(id=guid, id_field=DEFAULT_GUID_COL_NAME)
        return False
