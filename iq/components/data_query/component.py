#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data query component.
"""

from ... import object

from . import spc
from . import query

from ...dialog import dlg_func
from ...util import lang_func

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext


class iqDataQuery(query.iqDBQuery, object.iqObject):
    """
    Data query component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        query.iqDBQuery.__init__(self, *args, **kwargs)

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


COMPONENT = iqDataQuery
