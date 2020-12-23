#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unique data object component.
"""

import gettext

from ...components import data_navigator

from . import spc
from . import uni_object
from ...util import log_func
from ...util import lang_func

from ...role import component as role

__version__ = (0, 0, 0, 1)

_ = lang_func.getTranslation().gettext

EDIT_PERMISSION = dict(name='edit_uni_objects', description=_('Can edit uni objects'), type='DATA')
NEW_PERMISSION = dict(name='new_uni_objects', description=_('Can add new uni objects'), type='DATA')
DEL_PERMISSION = dict(name='del_uni_objects', description=_('Can delete uni objects'), type='DATA')
ACTIVE_PERMISSION = dict(name='active_uni_objects', description=_('Can activate/deactivate uni objects'), type='DATA')
CHANGE_PERMISSION = dict(name='change_uni_objects', description=_('Can edit records/change uni objects'), type='DATA')

role.addPermision(**EDIT_PERMISSION)
role.addPermision(**NEW_PERMISSION)
role.addPermision(**DEL_PERMISSION)
role.addPermision(**ACTIVE_PERMISSION)
role.addPermision(**CHANGE_PERMISSION)


class iqDataUniObject(uni_object.iqUniObjectManager, data_navigator.COMPONENT):
    """
    Unique data object component.
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
        uni_object.iqUniObjectManager.__init__(self, *args, **kwargs)


COMPONENT = iqDataUniObject
