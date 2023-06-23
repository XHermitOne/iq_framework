#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine choice manager.
"""

from ..data_engine import db_engine

from ...util import global_func
from ...util import log_func
from ...util import lang_func
from ...util import id_func

from ...dialog import dlg_func

from ...engine import stored_manager

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqDBEngineChoiceManager(db_engine.iqDBEngineManager,
                              stored_manager.iqStoredManager):
    """
    DB engine choice manager.
    """
    def __init__(self):
        """
        Constructor.
        """
        db_engine.iqDBEngineManager.__init__(self)

        self._filename = None
        self._data = None

        # Internal values
        self._description = ''
        self._dialect = None
        self._driver = None
        self._host = None
        self._port = None
        self._db_name = None
        self._username = None
        self._password = None
        self._db_filename = None
        self._echo = False
        self._convert_unicode = False
        self._charset = None

    def getData(self):
        """
        Get database engine data.
        """
        if self._data is None:
            filename = self.getFilename()
            self._data = self.loadCustomData(save_filename=filename)
        return self._data

    def selectDB(self, parent=None):
        """
        Select DB.

        :param parent: Parent form.
        :return: Self or None if error.
        """
        if global_func.isWXEngine():
            from . import select_dbengine_dialog
            select_dbengine_dialog.openSelectDBEngineDialog(parent=parent, manager=self)
            return self
        else:
            log_func.warning(u'Not supported engine <%s> for selection database engine' % global_func.getEngineType())

        return None

    def newDB(self, parent=None):
        """
        New DB.

        :param parent: Parent form.
        :return: Self or None if error.
        """
        if self._data is None:
            self._data = dict(records=list())

        new_db = dict(guid=id_func.genGUID())

        if global_func.isWXEngine():
            from . import edit_dbengine_dialog
            result = edit_dbengine_dialog.openNewDBEngineDialog(parent=parent)
            if result is not None:
                new_db.update(result)
                self._data['records'].append(new_db)
                # Update internal values
                self.updateValues(**new_db)
                return self
        return None

    def deleteDB(self, parent=None, db_guid=None):
        """
        Delete DB.

        :param parent: Parent form.
        :param db_guid: Deleted database GUID.
        :return: Self or None if error.
        """
        if db_guid is None:
            log_func.warning(u'Not defined database engine GUID for delete')
            return None

        try:
            data = self.getData()
            records = data['records'] if data else list()
            find_db_record = [record for record in records if record['guid'] == db_guid]
            if not find_db_record:
                log_func.warning(u'Not found database engine <%s>' % db_guid)
                return None
            db_record = find_db_record[0]
            db_description = db_record.get('description', '')
            del_answer = dlg_func.openAskBox(title=_('DELETE'),
                                             prompt_text=_('Delete database') + (' <%s>?' % db_description),
                                             parent=parent)
            if del_answer:
                db_guids = [record['guid'] for record in records]
                i_del = db_guids.index(db_guid)
                del_record = data['records'].pop(i_del)
                # Update internal values
                self.updateValues(**del_record)
                return self
        except:
            log_func.fatal(u'Error delete database engine <%s>' % db_guid)
        return None

    def editDB(self, parent=None, db_guid=None):
        """
        Edit DB.

        :param parent: Parent form.
        :param db_guid: Edited database GUID.
        :return: Self or None if error.
        """
        if self._data is None:
            self._data = dict(records=list())

        find_db_record = [record for record in self._data['records'] if record['guid'] == db_guid]
        if not find_db_record:
            log_func.warning(u'Not found <%s> database engine for edit' % db_guid)
            return None

        edit_db = find_db_record[0]

        if global_func.isWXEngine():
            from . import edit_dbengine_dialog
            result = edit_dbengine_dialog.openEditDBEngineDialog(parent=parent, db_record=edit_db)
            if result is not None:
                edit_db.update(result)
                db_guids = [record['guid'] for record in self._data['records']]
                i_edit = db_guids.index(db_guid)
                self._data['records'][i_edit] = edit_db
                # Update internal values
                self.updateValues(**edit_db)
                return self
        return None

    def getFilename(self):
        """
        Get data filename.
        """
        if self._filename is None:
            self._filename = self.genCustomDataFilename()
        return self._filename

    def getDescription(self):
        """
        Get description.

        :return:
        """
        return self._description

    def getDialect(self):
        """
        Get database type/dialect.

        :return:
        """
        return self._dialect

    def getDriver(self):
        """
        Get database driver.

        :return:
        """
        return self._driver

    def getHost(self):
        """
        Get database host.

        :return:
        """
        return self._host

    def getPort(self):
        """
        Get port.

        :return:
        """
        return self._port

    def getDBName(self):
        """
        Get database name.

        :return:
        """
        return self._db_name

    def getUsername(self):
        """
        Get database username.

        :return:
        """
        return self._username

    def getPassword(self):
        """
        Get user password.

        :return:
        """
        return self._password

    def getDBFilename(self):
        """
        Get database filename (for SQLite).

        :return:
        """
        return self._db_filename

    def isEcho(self):
        """
        Echo debug information?
        """
        return self._echo

    def isConvertUnicode(self):
        """
        """
        return self._convert_unicode

    def getCharset(self):
        """
        Get charset.
        """
        return self._charset

    def updateValues(self, **values):
        """
        Set internal values.
        """
        self._description = values.get('description', '')
        self._dialect = values.get('dialect', None)
        self._driver = values.get('driver', None)
        self._host = values.get('host', None)
        self._port = values.get('port', None)
        self._db_name = values.get('db_name', None)
        self._username = values.get('username', None)
        self._password = values.get('password', None)
        self._db_filename = values.get('db_filename', None)
        self._echo = values.get('echo', False)
        self._convert_unicode = values.get('convert_unicode', False)
        self._charset = values.get('charset', None)

    def save(self):
        """
        Save data.
        """
        return self.saveCustomData(save_filename=self.getFilename(),
                                   save_data=self.getData())
