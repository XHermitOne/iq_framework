#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reference data object component.
"""

import gettext

from ...components import data_navigator

from . import spc
from . import ref_object
from ...util import log_func
from ...util import lang_func
from ...util import global_func

from ...role import component as role

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

EDIT_PERMISSION = dict(name='edit_ref_objects', description=_('Can edit ref objects'), type='DATA')
NEW_PERMISSION = dict(name='new_ref_objects', description=_('Can add new ref objects'), type='DATA')
DEL_PERMISSION = dict(name='del_ref_objects', description=_('Can delete ref objects'), type='DATA')
ACTIVE_PERMISSION = dict(name='active_ref_objects', description=_('Can activate/deactivate ref objects'), type='DATA')
CHANGE_PERMISSION = dict(name='change_ref_objects', description=_('Can edit records/change ref objects'), type='DATA')

role.addPermision(**EDIT_PERMISSION)
role.addPermision(**NEW_PERMISSION)
role.addPermision(**DEL_PERMISSION)
role.addPermision(**ACTIVE_PERMISSION)
role.addPermision(**CHANGE_PERMISSION)


class iqDataRefObject(ref_object.iqRefObjectManager, data_navigator.COMPONENT):
    """
    Reference data object component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        data_navigator.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        ref_object.iqRefObjectManager.__init__(self, *args, **kwargs)

        # Cache cod len
        self._cod_len = None

    def getCodLen(self):
        """
        Get list of level code lengths.
        """
        if self._cod_len is not None:
            return self._cod_len

        self._cod_len = ()
        cod_len_value = self.getAttribute('cod_len')
        if cod_len_value:
            try:
                if isinstance(cod_len_value, int):
                    self._cod_len = (cod_len_value, )
                elif isinstance(cod_len_value, list):
                    self._cod_len = tuple(cod_len_value)
                elif isinstance(cod_len_value, tuple):
                    self._cod_len = cod_len_value
                else:
                    log_func.warning(u'Error type cod len <%s> in ref object <%s>' % (type(cod_len_value),
                                                                                    self.getName()))
            except:
                log_func.fatal(u'Error level code lengths format <%s>' % cod_len)
        return self._cod_len

    def getLevelLabels(self):
        """
        Get level label list.
        """
        level_count = self.getLevelCount()
        labels = self.getAttribute('level_labels')
        labels = list(labels) + [u''] * (level_count-len(labels)) if labels else [u''] * level_count
        return tuple(labels)

    def test(self):
        """
        Object test function.

        :return: True/False.
        """
        if global_func.isWXEngine():
            import wx
            app = wx.GetApp()
            parent = app.GetTopWindow() if app else None
            return self.edit(parent=parent)
        return False


COMPONENT = iqDataRefObject
