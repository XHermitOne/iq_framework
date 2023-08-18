#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object manager.
"""

import copy
import operator
import sqlalchemy.sql

from ..data_navigator import model_navigator

from ...util import log_func
from ...util import global_func
from ...util import lock_func
from ...util import lang_func

from ...dialog import dlg_func

from ...components.data_column import column_types

__version__ = (0, 0, 4, 1)

_ = lang_func.getTranslation().gettext

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

        # Internal object data cache
        self.__cache__ = dict()

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

    def getCache(self):
        """
        Cache ref object data?
        :return: True/False.
        """
        return False

    def clearCache(self):
        """
        Clear internal ref object data cache.
        """
        self.__cache__.clear()

    def getRecByCod(self, cod):
        """
        Get record by cod.

        :param cod: Reference data code.
        :return: Record dictionary or None if error.
        """
        is_cache = self.getCache()
        if is_cache and cod in self.__cache__:
            return self.__cache__[cod]

        record = self.getRecByColValue(column_name=self.getCodColumnName(),
                                       column_value=cod)
        if is_cache:
            self.__cache__[cod] = record
        return record

    def getRecByColValue(self, column_name=None, column_value=None):
        """
        Get first record by column value.

        :param column_name: Column name.
            If None then get cod column name.
        :param column_value: Column value.
        :return: Record dictionary or None if error.
        """
        if column_name is None:
            column_name = self.getCodColumnName()

        filter_data = {column_name: column_value}
        records = self.searchRecsByColValues(**filter_data)
        result = records[0] if records else None
        if records and len(records) > 1:
            log_func.warning(u'Found several records by column <%s> value <%s>' % (column_name, str(column_value)))
            # for rec in records:
            #     print(rec[self.getCodColumnName()], rec[self.getNameColumnName()], rec)
        if result is None:
            log_func.warning(u'Not found record by column <%s> value <%s>' % (column_name, str(column_value)))
        return result

    def getCodByColValue(self, column_name=None, column_value=None):
        """
        Get first cod by column value.

        :param column_name: Column name.
            If None then get cod column name.
        :param column_value: Column value.
        :return: Record dictionary or None if error.
        """
        rec = self.getRecByColValue(column_name=column_name, column_value=column_value)
        if rec:
            return rec.get(self.getCodColumnName(), None)
        return None

    def searchRecsByColValues(self, **column_values):
        """
        Get records by column values.

        :param column_values: Column value data:
            {
            'column name': column value,
            ...
            }
        :return: Record dictionary list or None if error.
        """
        if not column_values:
            log_func.warning(u'Not define column values for search in <%s>' % self.getName())
            return None

        model = self.getModel()
        transaction = self.startTransaction()
        recordset = None
        try:
            filter_data = [getattr(model, column_name) == value for column_name, value in column_values.items()]
            query = transaction.query(model).filter(*filter_data)

            if self.existsQuery(query):
                # Presentation of query result in the form of a dictionary
                records = query.all()
                recordset = [vars(record) for record in records]
            else:
                log_func.warning(u'Reference data columns %s not found in <%s>' % (column_values,
                                                                                   self.getName()))

        except:
            log_func.fatal(u'Error get reference data records by column values %s in <%s>' % (column_values,
                                                                                              self.getName()))
        self.stopTransaction(transaction)
        return recordset

    def searchRecsByColContent(self, column_name=None, search_text=None,
                               case_sensitive=False, do_sort=True,
                               order_by=None,
                               only_first=False):
        """
        Get records by column contained.

        :param column_name: Column name.
            If None then get cod column name.
        :param search_text: Search content text.
        :param case_sensitive: Case sensitive?
        :param do_sort: Sort result list by column.
        :param order_by: Sort column name list.
        :param only_first: Get only first record.
        :return: Record dictionary list or None if error.
        """
        if not search_text:
            log_func.warning(u'Not define column search text in <%s>' % self.getName())
            return None

        if column_name is None:
            column_name = self.getCodColumnName()

        model = self.getModel()
        transaction = self.startTransaction()
        result = None
        try:
            search_expression = '%' + search_text + '%'
            if case_sensitive:
                filter_data = [getattr(model, column_name).like(search_expression)]
            else:
                filter_data = [getattr(model, column_name).ilike(search_expression)]

            query = transaction.query(model).filter(*filter_data)
            if do_sort:
                if not isinstance(order_by, (list, tuple)):
                    query = query.order_by(getattr(model, column_name))
                else:
                    order_by_data = [getattr(model, col_name) for col_name in order_by]
                    query = query.order_by(*order_by_data)

            # if query.count():
            if self.existsQuery(query):
                if not only_first:
                    # Presentation of query result in the form of a dictionary
                    records = query.all()
                    result = [vars(record) for record in records]
                else:
                    record = query.one()
                    result = [vars(record)]
            else:
                log_func.warning(u'Reference data column <%s : %s> not found in <%s>' % (column_name,
                                                                                         search_text,
                                                                                         self.getName()))
        except:
            log_func.fatal(u'Error get reference data records by column content <%s : \'%s\'> in <%s>' % (column_name,
                                                                                                          search_text,
                                                                                                          self.getName()))
        self.stopTransaction(transaction)
        return result

    def searchCodes(self, **column_values):
        """
        Search codes by column values.

        :param column_values: Column values dictionary.
            For example:
                {
                    'name': u'Name',
                    'alter_id': 'Alter ID',
                    ...
                }
            The search is made for exact comparison by <AND>.
        :return: The list of found codes that match the desired value.
            Or None if error.
        """
        search_records = self.searchRecsByColValues(**column_values)
        cod_column_name = self.getCodColumnName()
        return [record.get(cod_column_name, None)for record in search_records] if search_records is not None else list()

    def findRecByColContent(self, column_name=None, search_text=None,
                            case_sensitive=False, do_sort=True):
        """
        :param column_name: Column name.
            If None then get cod column name.
        :param search_text: Search content text.
        :param case_sensitive: Case sensitive?
        :param do_sort: Sort result list by column.
        :return: Record dictionary or None if not found.
        """
        if not search_text:
            log_func.warning(u'Not define column find text in <%s>' % self.getName())
            return None

        if column_name is None:
            column_name = self.getCodColumnName()

        records = self.searchRecsByColContent(column_name=column_name, search_text=search_text,
                                              case_sensitive=case_sensitive, do_sort=do_sort,
                                              only_first=True)
        return records[0] if records else None

    def searchCodesByColValue(self, search_value, search_colname=None,
                              sort_columns=None, reverse=False):
        """
        Search codes by column value.

        :param search_value: Search value.
        :param search_colname: Search column name.
            If None then get name column.
        :param sort_columns: Sort order as column name list or
            column name if sort by one column.
        :param reverse: Reverse sort?
        :return: Code list or empty list if not found.
        """
        if search_colname is None:
            search_colname = self.getNameColumnName()
        if isinstance(sort_columns, str):
            sort_columns = (sort_columns, )

        model = self.getModel()
        transaction = self.startTransaction()
        result = list()
        try:
            column_type = model.__table__.columns[search_colname].type
            column = getattr(model, search_colname)

            query = None
            if column_type.__class__ in column_types.SQLALCHEMY_TEXT_TYPES:
                search_like = '%%%s%%' % search_value
                query = transaction.query(model).filter(column.ilike(search_like))
            elif column_type.__class__ in column_types.SQLALCHEMY_INT_TYPES:
                num_value = int(search_value)
                query = transaction.query(model).filter(column == num_value)
            elif column_type.__class__ in column_types.SQLALCHEMY_FLOAT_TYPES:
                num_value = float(search_value)
                query = transaction.query(model).filter(column == num_value)
            elif column_type.__class__ in column_types.SQLALCHEMY_DATETIME_TYPES or column_type in column_types.SQLALCHEMY_DATE_TYPES:
                # dt_value = datetimefunc.strDateTime2Date(search_value)
                query = transaction.query(model).filter(column == search_value)
            else:
                log_func.warning(u'Find by column type <%s : %s> not supported' % (search_colname,
                                                                                   column_type.__class__.__name__))

            if query is not None and sort_columns:
                if isinstance(sort_columns, (list, tuple)):
                    query = query.order_by(*[
                            getattr(model, col_name) if not reverse else getattr(model, col_name).desc() for
                            col_name in sort_columns])
                else:
                    log_func.warning(u'Error ORDER BY columns type <%s>' % type(sort_columns))

            records = None if query is None else query.all()

            if records:
                result = [record.cod for record in records]
        except:
            log_func.fatal(u'Error search codes by column <%s> value <%s>' % (search_colname, search_value))
        self.stopTransaction(transaction)
        return result

    def getColumnValues(self, cod, *column_names):
        """
        Get column values by cod.

        :param cod: Reference data code.
        :param column_names: Column names.
            If not defined then get column 'name'.
        :return: Column dictionary:
            {
            'column_name': Column value if activate,
            ...
            }
            or None if error.
        """
        if not column_names:
            column_names = (self.getNameColumnName(), )

        rec = self.getRecByCod(cod)
        if rec:
            activate = rec.get(self.getActiveColumnName(), False)
            if activate:
                for column_name in column_names:
                    if column_name not in rec:
                        log_func.warning(u'Column <%s> not define in ref object <%s>' % (column_name, self.getName()))

                return {column_name: rec.get(column_name, None) for column_name in column_names}
            else:
                log_func.warning(u'Ref object <%s> cod <%s> not activate' % (self.getName(), cod))
        return None

    def getColumnValue(self, cod, column_name):
        """
        Get column value by cod.

        :param cod: Reference data code.
        :param column_name: Column name.
            If not defined then get column 'name'.
        :return: Column value if activate,
            or None if error.
        """
        values = self.getColumnValues(cod, column_name)
        return values.get(column_name, None) if values else None

    def getColumnNameValue(self, cod):
        """
        Get column name value by cod.

        :param cod: Reference data code.
        :return: Column 'name' value if cod activate or None.
        """
        column_name = self.getNameColumnName()
        column_values = self.getColumnValues(cod, column_name)
        return column_values.get(column_name, None)

    def getDataObjectRec(self, value):
        """
        Get data object record by value.

        :param value: Reference data code.
        :return: Record dictionary or None if error.
        """
        return self.getRecByCod(cod=value)

    def isEmpty(self):
        """
        Is the ref object empty?

        :return: True/False.
        """
        model = self.getModel()
        transaction = self.startTransaction()
        result = None
        try:
            query = transaction.query(model)
            result = not self.existsQuery(query)
        except:
            log_func.fatal(u'Error check empty ref object <%s>' % self.getName())
        self.stopTransaction(transaction)
        return result

    def hasCod(self, cod):
        """
        Is there such code in the ref object?

        :param cod: Code.
        :return: True/False.
        """
        model = self.getModel()
        transaction = self.startTransaction()
        result = None
        try:
            query = transaction.query(model).filter(getattr(model, self.getCodColumnName()) == cod)
            result = self.existsQuery(query)
        except:
            log_func.fatal(u'Error check code <%s> ref object <%s>' % (cod, self.getName()))

        self.stopTransaction(transaction)
        return result

    def hasName(self, name):
        """
        Is there such name in the ref object?

        :param name: Name.
        :return: True/False.
        """
        model = self.getModel()
        transaction = self.startTransaction()
        result = None
        try:
            query = transaction.query(model).filter(getattr(model, self.getNameColumnName()) == name)
            result = self.existsQuery(query)
        except:
            log_func.fatal(u'Error check name <%s> ref object <%s>' % (name, self.getName()))

        self.stopTransaction(transaction)
        return result

    def getCodLen(self):
        """
        Get list of level code lengths.
        """
        return ()

    def getLevelCodLen(self, level=0):
        """
        Get level cod length.

        :param level: Level index.
        :return: Level cod length or -1 if error.
        """
        cod_len = self.getCodLen()
        if cod_len and (0 <= level < len(cod_len)):
            return cod_len[level]
        else:
            log_func.warning(u'Not valid level index [%s]' % level)
        return -1

    def getCodAsTuple(self, cod):
        """
        Get ref object cod as tuple.

        :param cod: Code as string.
        :return: Code as tuple.
        """
        cod_len = self.getCodLen()
        if cod_len:
            cod_tuple = tuple([cod[sum(cod_len[:i]):sum(cod_len[:i+1])] for i in range(len(cod_len))])
        else:
            cod_tuple = (cod,)
        return cod_tuple

    def getLevelCount(self):
        """
        Get level number.
        """
        cod_len = self.getCodLen()
        return len(cod_len) if cod_len else 0

    def getLevelRecsByCod(self, parent_cod=None):
        """
        Get level records by code.

        :param parent_cod: Parent level code. If None then get root level.
        :return: Record list or None if error.
        """
        cod_len = self.getCodLen()
        model = self.getModel()
        transaction = self.startTransaction()
        recordset = None
        try:
            records = list()
            if not cod_len:
                records = transaction.query(model).all()
            elif cod_len and parent_cod is None:
                level_cod_len = cod_len[0]
                cod_column = getattr(model, self.getCodColumnName())
                records = transaction.query(model).filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len).all()
            elif cod_len and parent_cod:
                cod_len_list = list(cod_len) + [0]
                parent_cod_len = len(parent_cod)
                level_subcod_len = cod_len_list[[sum(cod_len_list[:i]) for i, sub_cod in enumerate(cod_len_list)].index(parent_cod_len)]
                if level_subcod_len:
                    level_cod_len = parent_cod_len + level_subcod_len
                    cod_column = getattr(model, self.getCodColumnName())
                    records = transaction.query(model).filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len,
                                                              cod_column.like(parent_cod + '%')).all()
            else:
                log_func.warning(u'Not supported getting level records in <%s>' % self.getName())

            recordset = [vars(record) for record in records]
        except:
            log_func.fatal(u'Error get level data ref object <%s>' % self.getName())
        self.stopTransaction(transaction)
        return recordset

    def hasChildrenCodes(self, parent_cod=None):
        """
        Does the code have child subcodes?

        :param parent_cod: Code.
        :return: True/False.
        """
        cod_len = self.getCodLen()

        model = self.getModel()
        transaction = self.startTransaction()
        record_exists = None
        try:
            if not cod_len:
                record_exists = self.existsQuery(transaction.query(model))
            elif cod_len and parent_cod is None:
                level_cod_len = cod_len[0]
                cod_column = getattr(model, self.getCodColumnName())
                record_exists = self.existsQuery(transaction.query(model).filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len))
            elif cod_len and parent_cod:
                cod_len_list = list(cod_len) + [0]
                parent_cod_len = len(parent_cod)
                level_subcod_len = cod_len_list[[sum(cod_len_list[:i]) for i, sub_cod in enumerate(cod_len_list)].index(parent_cod_len)]
                if level_subcod_len:
                    level_cod_len = parent_cod_len + level_subcod_len
                    cod_column = getattr(model, self.getCodColumnName())
                    record_exists = self.existsQuery(transaction.query(model).filter(sqlalchemy.sql.func.length(cod_column) == level_cod_len,
                                                                                     cod_column.like(parent_cod + '%')))
            else:
                log_func.warning(u'Not supported getting level record count in <%s>' % self.getName())
                record_exists = False

            # log_func.debug(u'Record count <%s : %s>' % (parent_cod, record_count))
        except:
            log_func.fatal(u'Error get level data ref object <%s>' % self.getName())
        self.stopTransaction(transaction)
        return record_exists

    def canEdit(self):
        """
        Checking the possibility of editing the reference object.

        :return: True - The user registered in the program can edit the directory,
            False - Can not.
        """
        user = global_func.getUser()
        return user.isPermission('edit_ref_objects')

    def edit(self, parent=None):
        """
        Edit ref object.

        :param parent: Parent window.
        :return: True/False.
        """
        lock_name = self.getName()
        if lock_func.isLockObj(lock_name):
            lock_computer = lock_func.getLockComputerObj(lock_name)
            lock_username = lock_func.getLockUsernameObj(lock_name)
            lock_msg = _('Editing locked by user ') + lock_username + _(' Computer ') + lock_computer
            dlg_func.openWarningBox(_('ATTENTION'), lock_msg)
            return False

        if global_func.isWXEngine():
            lock_func.lockObj(lock_name)

            from . import wx_editdlg
            result = wx_editdlg.editRefObjDlg(parent=parent, ref_obj=self)

            lock_func.unLockObj(lock_name)
            return result
        else:
            log_func.warning(u'Not support edit ref object. Engine <%s>' % global_func.getEngineType())
        return False

    def choiceCod(self, parent=None, view_fields=None, search_fields=None,
                  clear_cache=False):
        """
        Choice ref object item.

        :param parent: Parent window.
        :param view_fields: List of displayed fields.
        :param search_fields: List of fields to search.
        :param clear_cache: Clear cache?
        :return: Selected cod.
        """
        selected_record = self.choiceRecord(parent=parent,
                                            view_fields=view_fields,
                                            search_fields=search_fields)
        return selected_record.get(self.getCodColumnName(), None) if isinstance(selected_record, dict) else None

    def choiceRecord(self, parent=None, view_fields=None, search_fields=None,
                     clear_cache=False):
        """
        Choice ref object item record.

        :param parent: Parent window.
        :param view_fields: List of displayed fields.
        :param search_fields: List of fields to search.
        :param clear_cache: Clear cache?
        :return: Selected record or None if error.
        """
        try:
            if global_func.isWXEngine():
                from . import wx_choicetreedlg
                selected_record = wx_choicetreedlg.choiceRefObjRecDlg(parent=parent,
                                                                      ref_obj=self,
                                                                      fields=view_fields,
                                                                      search_fields=search_fields,
                                                                      clear_cache=clear_cache)
                return selected_record
            else:
                log_func.warning(u'Not support choice ref object. Engine <%s>' % global_func.getEngineType())
        except:
            log_func.fatal(u'Error choice ref object item <%s>' % self.getName())
        return None

    choice = choiceRecord

    def checkCodes(self, parent=None, view_fields=None, search_fields=None,
                   clear_cache=False):
        """
        Check ref object items.

        :param parent: Parent window.
        :param view_fields: List of displayed fields.
        :param search_fields: List of fields to search.
        :param clear_cache: Clear cache?
        :return: Selected codes.
        """
        selected_records = self.checkRecords(parent=parent,
                                             view_fields=view_fields,
                                             search_fields=search_fields)
        return [selected_record.get(self.getCodColumnName(), None) for selected_record in selected_records] if isinstance(selected_records, (tuple, list)) else None

    def checkRecords(self, parent=None, view_fields=None, search_fields=None,
                     clear_cache=False):
        """
        Check ref object item records.

        :param parent: Parent window.
        :param view_fields: List of displayed fields.
        :param search_fields: List of fields to search.
        :param clear_cache: Clear cache?
        :return: Selected records or None if error.
        """
        try:
            if global_func.isWXEngine():
                from ..wx_refobjmultiplecheckcomboctrl import wx_checktreedlg
                selected_records = wx_checktreedlg.checkRefObjRecsDlg(parent=parent,
                                                                      ref_obj=self,
                                                                      fields=view_fields,
                                                                      search_fields=search_fields,
                                                                      clear_cache=clear_cache)
                return selected_records
            else:
                log_func.warning(u'Not support check ref objects. Engine <%s>' % global_func.getEngineType())
        except:
            log_func.fatal(u'Error check ref objects item <%s>' % self.getName())
        return None

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
            # log_func.debug(u'Save. Update record. Code <%s>' % cod)
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
            log_func.debug(u'Save. Add record. Code <%s>' % cod)
            new_record = copy.deepcopy(record)
            new_record[self.getCodColumnName()] = cod
            return self.addRec(record=new_record)
        return False

    def delRecByCod(self, cod):
        """
        Delete record by code.

        :param cod: Code.
        :return: True/False.
        """
        return self.deleteRec(id=cod, id_field=self.getCodColumnName())

    def isChildrenCodes(self, cod):
        """
        Does the above code have sublevel subcodes?

        :param cod: Ref object code.
        """
        recs = self.getLevelRecsByCod(cod)
        return bool(recs)

    def getChildrenCodes(self, cod=None):
        """
        Get children codes.

        :param cod: Ref object code.
        :return: Get children codes list as tuple.
        """
        recs = self.getLevelRecsByCod(cod)
        return [rec.get(self.getCodColumnName(), None) for rec in recs] if recs else tuple()

    def isParentLevelCod(self, cod):
        """
        Is it a parent level code?

        :param cod: Code.
        :return: True/False.
        """
        cod_tuple = tuple([subcod for subcod in self.getCodAsTuple(cod) if subcod])
        # log_func.debug(u'Cod tuple %s' % str(cod_tuple))
        return len(cod_tuple) < self.getLevelCount()

    def isGrandParentLevelCod(self, cod):
        """
        Is it a grandparent level code?

        :param cod: Code.
        :return: True/False.
        """
        cod_tuple = tuple([subcod for subcod in self.getCodAsTuple(cod) if subcod])
        return len(cod_tuple) < (self.getLevelCount() - 1)
