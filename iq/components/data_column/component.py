#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data column component.
"""

from ... import object

from . import spc
from . import column

from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqDataColumn(column.iqColumnManager, object.iqObject):
    """
    Data column component.
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
        column.iqColumnManager.__init__(self, *args, **kwargs)

        self.link_obj = None

    def getFieldType(self):
        """
        Get column type.
        """
        return self.getAttribute('field_type')

    def getLinkPsp(self):
        """
        Get link data object passport.
        """
        return self.getAttribute('link')

    def getLinkDataObj(self):
        """
        Get link data object.

        :return: Link data object or None if error.
        """
        if self.link_obj is None:
            link_psp = self.getLinkPsp()
            if link_psp:
                self.link_obj = self.getKernel().createByPsp(psp=link_psp)
            else:
                log_func.error(u'Not define link object in column <%s>' % self.getName())
        return self.link_obj

    def getFilterFuncs(self):
        """
        Список функций фильтрации.
        """
        from ..wx_filterchoicectrl import filter_builder_env

        link_psp = self.getLinkPsp()

        if not link_psp:
            field_type = self.getFieldType()
            req_type = filter_builder_env.DB_FLD_TYPE2REQUISITE_TYPE.get(field_type)
            return filter_builder_env.DEFAULT_FUNCS.get(req_type)
        else:
            funcs = filter_builder_env.DEFAULT_FUNCS.get(filter_builder_env.REQUISITE_TYPE_REF)

            # Change link with ref object in extension editor
            for func_body in filter_builder_env.DEFAULT_ENV_REF_FUNCS.values():
                func_body['args'][0]['ext_kwargs']['component'] = {'link_psp': link_psp}

            return funcs


COMPONENT = iqDataColumn
