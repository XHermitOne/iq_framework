#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Accumulate registry component.
"""

from ... import object

from . import spc
from . import acc_registry

from ...util import log_func

from .. import data_column

__version__ = (0, 0, 0, 1)


REQUISITE_VAL_TYPE_TRANSLATE = dict(Text='text',
                                    Integer='int',
                                    Float='float',
                                    DateTime='datetime')


class iqDataAccumulateRegistry(acc_registry.iqAccRegistry, object.iqObject):
    """
    Accumulate registry component.
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

        db = self.getDB()
        db_url = db.getDBUrl() if db else None
        if not db_url:
            log_func.error(u'DB URL not defined for accumulate registry <%s>' % self.getName())
        acc_registry.iqAccRegistry.__init__(self, db_url=db_url,
                                            operation_table_name=self.getOperationTabName(),
                                            result_table_name=self.getResultTabName())

        self.createChildren()

        dimension_requisite_names = self.getDimensionRequisiteNames()
        dimension_requisites = [requisite for requisite in self.getChildrenRequisites() if
                                requisite.name in dimension_requisite_names]
        for requisite in dimension_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.addDimensionRequisite(requisite_name, requisite_type)

        resource_requisite_names = self.getResourceRequisiteNames()
        resource_requisites = [requisite for requisite in self.getChildrenRequisites() if
                               requisite.name in resource_requisite_names]
        for requisite in resource_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.addResourceRequisite(requisite_name, requisite_type)

        extended_requisite_names = self.getExtendedRequisiteNames()
        extended_requisites = [requisite for requisite in self.getChildrenRequisites() if
                               requisite.name in extended_requisite_names]
        for requisite in extended_requisites:
            requisite_name = requisite.name
            requisite_type = REQUISITE_VAL_TYPE_TRANSLATE.get(requisite.getTypeValue(), 'text')
            self.addExtendedRequisite(requisite_name, requisite_type)

    def getDBPsp(self):
        """
        Get database.
        """
        return self.getAttribute('db_engine')

    def getDB(self):
        """
        Get database object.
        """
        db_psp = self.getDBPsp()
        db = None
        if db_psp:
            db = self.getKernel().createByPsp(db_psp)
        return db

    def getChildrenRequisites(self):
        """
        Get children requisites.
        """
        return [child for child in self.getChildren() if issubclass(child.__class__, data_column.COMPONENT)]

    def getOperationTabName(self):
        """
        Get operation table name.
        """
        return self.getAttribute('operation_table')

    def getResultTabName(self):
        """
        Get result table name.
        """
        return self.getAttribute('result_table')

    def getDimensionRequisiteNames(self):
        """
        Get dimension requisite names.
        """
        return self.getAttribute('dimension_requisites')

    def getResourceRequisiteNames(self):
        """
        Get resource requisite names.
        """
        return self.getAttribute('resource_requisites')

    def getExtendedRequisiteNames(self):
        """
        Get extended requisite names.
        """
        used_requisite_names = self.getDimensionRequisiteNames() + self.getResourceRequisiteNames()
        return [requisite.name for requisite in self.getChildrenRequisites() if requisite.name not in used_requisite_names]


COMPONENT = iqDataAccumulateRegistry
