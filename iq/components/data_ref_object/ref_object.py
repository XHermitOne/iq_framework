#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object manager.
"""

import copy
import sqlalchemy.sql

from ..data_navigator import model_navigator

from ...util import log_func
from ...util import global_func

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
        return None

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
            log_func.fatal(u'Error check empty ref object <%s>' % self.getName())
        return None

    def hasCod(self, cod):
        """
        Is there such code in the ref object?

        :param cod: Code.
        :return: True/False.
        """
        try:
            model = self.getModel()
            rec_count = self.getModelQuery().filter(getattr(model, self.getCodColumnName()) == cod).count()
            return bool(rec_count)
        except:
            log_func.fatal(u'Error check code ref object <%s>' % self.getName())
        return None

    def getCodLen(self):
        """
        Get list of level code lengths.
        """
        return ()

    def getLevelRecsByCod(self, parent_cod=None):
        """
        Get level records by code.

        :param parent_cod: Parent level code. If None then get root level.
        :return: Record list or None if error.
        """
        try:
            cod_len = self.getCodLen()

            model = self.getModel()

            records = list()
            if not cod_len:
                records = self.getModelQuery().all()
            elif cod_len and parent_cod is None:
                level_cod_len = cod_len[0]
                cod_column = getattr(model, self.getCodColumnName())
                records = self.getModelQuery().filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len)
            elif cod_len and parent_cod:
                cod_len_list = list(cod_len) + [0]
                parent_cod_len = len(parent_cod)
                level_subcod_len = cod_len_list[[sum(cod_len_list[:i]) for i, sub_cod in enumerate(cod_len_list)].index(parent_cod_len)]
                if level_subcod_len:
                    level_cod_len = parent_cod_len + level_subcod_len
                    cod_column = getattr(model, self.getCodColumnName())
                    records = self.getModelQuery().filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len,
                                                          cod_column.like(parent_cod + '%'))
            else:
                log_func.error(u'Not supported getting level records in <%s>' % self.getName())

            return [vars(record) for record in records]
        except:
            log_func.fatal(u'Error get level data ref object <%s>' % self.getName())
        return None

    def hasChildrenCodes(self, parent_cod=None):
        """
        Does the code have child subcodes?

        :param parent_cod: Code.
        :return: True/False.
        """
        try:
            cod_len = self.getCodLen()

            model = self.getModel()

            record_count = 0
            if not cod_len:
                record_count = self.getModelQuery().count()
            elif cod_len and parent_cod is None:
                level_cod_len = cod_len[0]
                cod_column = getattr(model, self.getCodColumnName())
                record_count = self.getModelQuery().filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len).count()
            elif cod_len and parent_cod:
                cod_len_list = list(cod_len) + [0]
                parent_cod_len = len(parent_cod)
                level_subcod_len = cod_len_list[[sum(cod_len_list[:i]) for i, sub_cod in enumerate(cod_len_list)].index(parent_cod_len)]
                if level_subcod_len:
                    level_cod_len = parent_cod_len + level_subcod_len
                    cod_column = getattr(model, self.getCodColumnName())
                    record_count = self.getModelQuery().filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len,
                                                               cod_column.like(parent_cod + '%')).count()
            else:
                log_func.error(u'Not supported getting level record count in <%s>' % self.getName())

            # log_func.debug(u'Record count <%s : %s>' % (parent_cod, record_count))
            return bool(record_count)
        except:
            log_func.fatal(u'Error get level data ref object <%s>' % self.getName())
        return None

    def edit(self, parent=None):
        """
        Edit ref object.

        :param parent: Parent window.
        :return: True/False.
        """
        if global_func.isWXEngine():
            from . import wx_editdlg
            return wx_editdlg.editRefObjDlg(parent=parent, ref_obj=self)
        else:
            log_func.error(u'Not support edit ref object. Engine <%s>' % global_func.getEngineType())
        return False

    def isActive(self, cod):
        """
        Is active code?

        :param cod: Code.
        :return: True/False.
        """
        rec = self.getRecByCod(cod)
        return rec.get(self.getActiveColumnName(), False) if rec else False

    def getLevelIdxByCod(self, cod):
        """
        Get level index by cod.

        :param cod: Code.
        :return: Level index or -1 if error.
        """
        cod_len_tuple = self.getCodLen()
        for i, level_cod_len in enumerate(cod_len_tuple):
            if len(cod) == sum(cod_len_tuple[:i+1]):
                return i
        return -1

    def save(self, cod, **record):
        """
        Save ref object record by cod.
        If there is such a code, then the values are overwritten.
        Otherwise, a new entry is added.

        :param cod: Code.
        :param record: Record data.
        :return: True/False.
        """
        if self.hasCod(cod):
            cod_col_name = self.getCodColumnName()
            model = self.getModel()
            find_cod_param = [getattr(model, cod_col_name) == cod]
            find_rec = self.findRec(*find_cod_param)
            find_id = find_rec.get('id', None)
            # log_func.debug(u'Find ID %d' % find_id)
            if find_id:
                return self.saveRec(id=find_id, record=record)
            else:
                log_func.warning(u'Record not found fo cod <%s>' % cod)
        else:
            new_record = copy.deepcopy(record)
            new_record[self.getCodColumnName()] = cod
            return self.addRec(record=new_record)
        return False
