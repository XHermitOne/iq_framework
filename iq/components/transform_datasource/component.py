#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transformation table data component.
"""

from ... import object

from . import spc
from . import transform_datasource_proto

# from ...dialog import dlg_func
from ...util import log_func

__version__ = (0, 0, 0, 1)


class iqTransformDataSource(transform_datasource_proto.iqTransformDataSourceProto,
                            object.iqObject):
    """
    Transformation table data component class.
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
        transform_datasource_proto.iqTransformDataSourceProto.__init__(self, *args, **kwargs)

    def getTabDataSourcePsp(self):
        """
        Get table datasource object passport.

        :return: Table datasource object passport or None if error.
        """
        return self.getAttribute('tab_datasource')

    def getTabDataSource(self):
        """
        Get table datasource object.

        :return: Table datasource object or None if error.
        """
        psp = self.getTabDataSourcePsp()
        if psp:
            kernel = self.getKernel()
            return kernel.getObject(psp, register=True)
        else:
            log_func.warning(u'Not define table datasource in transform datasource <%s>' % self.getName())
        return None

COMPONENT = iqTransformDataSource
