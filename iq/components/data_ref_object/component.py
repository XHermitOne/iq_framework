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

from ...role import component as role

__version__ = (0, 0, 0, 1)

_ = gettext.gettext

EDIT_PERMISSION = dict(name='edit_ref_objects', description=_('Can edit ref objects'), type='DATA')
role.addPermision(**EDIT_PERMISSION)


class iqDataRefObject(ref_object.iqRefObjectManager, data_navigator.COMPONENT):
    """
    Reference data object component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        data_navigator.COMPONENT.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)
        ref_object.iqRefObjectManager.__init__(self, *args, **kwargs)

    def getCodLen(self):
        """
        Get list of level code lengths.
        """
        cod_len = tuple()
        cod_len_value = self.getAttribute('cod_len')
        if cod_len_value:
            try:
                if isinstance(cod_len_value, int):
                    cod_len = (cod_len_value, )
                elif isinstance(cod_len_value, list):
                    cod_len = tuple(cod_len_value)
                elif isinstance(cod_len_value, tuple):
                    cod_len = cod_len_value
                else:
                    log_func.error(u'Error type cod len <%s> in ref object <%s>' % (type(cod_len_value),
                                                                                    self.getName()))
            except:
                log_func.fatal(u'Error level code lengths format <%s>' % cod_len)
        return cod_len


COMPONENT = iqDataRefObject
