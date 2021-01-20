#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data engine component.
"""

from ... import object

from . import spc
from . import db_engine

from ...dialog import dlg_func
from ...util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqDataEngine(db_engine.iqDBEngineManager, object.iqObject):
    """
    Data engine component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        db_engine.iqDBEngineManager.__init__(self, *args, **kwargs)

    def test(self):
        """
        Object test function.

        :return: True/False.
        """
        check_connection = self.checkConnection()
        if check_connection:
            dlg_func.openMsgBox(_(u'MESSAGE'),
                                _(u'Database connection established') + u' <%s>' % self.getDBUrl())
            return True
        else:
            dlg_func.openErrBox(_(u'ERROR'),
                                _(u'Database connection not established') + u' <%s>' % self.getDBUrl())
        return False

    def getDialect(self):
        """
        Get database type/dialect.

        :return:
        """
        return self.getAttribute('dialect')

    def getDriver(self):
        """
        Get database driver.

        :return:
        """
        return self.getAttribute('driver')

    def getHost(self):
        """
        Get database host.

        :return:
        """
        return self.getAttribute('host')

    def getPort(self):
        """
        Get port.

        :return:
        """
        return self.getAttribute('port')

    def getDBName(self):
        """
        Get database name.

        :return:
        """
        return self.getAttribute('db_name')

    def getUsername(self):
        """
        Get database username.

        :return:
        """
        return self.getAttribute('username')

    def getPassword(self):
        """
        Get user password.

        :return:
        """
        return self.getAttribute('password')

    def getCharset(self):
        """
        Get DB code page.

        :return:
        """
        charset = self.getAttribute('charset')
        return db_engine.ENCODING2CHARSET.get(charset, charset)

COMPONENT = iqDataEngine
