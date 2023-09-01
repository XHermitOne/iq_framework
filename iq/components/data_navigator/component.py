#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data model navigator component.
"""

from ... import object

from . import spc
from . import model_navigator
from ..data_scheme import scheme as scheme_module

from ...util import log_func

__version__ = (0, 0, 3, 2)


class iqDataNavigator(model_navigator.iqModelNavigatorManager, object.iqObject):
    """
    Data model navigator component.
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
        model_navigator.iqModelNavigatorManager.__init__(self, *args, **kwargs)

        self.setReadOnly(readonly=self.getAttribute('readonly'))

    def getModelPsp(self):
        """
        Get model passport.
        """
        model_psp = self.getAttribute('model')
        return model_psp

    def getScheme(self):
        """
        Get scheme object by model.

        :return: Data scheme object or None if error.
        """
        model_psp = self.getModelPsp()

        if not model_psp:
            log_func.error(u'Not define model in <%s : %s>' % (self.getName(), self.getType()))
            return None

        psp = self.newPassport().setAsStr(model_psp)
        psp.typename = None
        psp.name = None
        scheme = self.getKernel().getObject(psp=psp, register=True)
        return scheme if issubclass(scheme.__class__, scheme_module.iqSchemeManager) else None

    def createModel(self):
        """
        Create sqlalchemy model object.

        :return: Model or None if error.
        """
        model_psp = self.getModelPsp()

        if not model_psp:
            log_func.warning(u'Not define model in <%s : %s>' % (self.getName(), self.getType()))
            return None

        model_name = self.newPassport().setAsStr(model_psp).name

        scheme = self.getScheme()
        if scheme:
            return scheme.getModel(model_name)
        else:
            log_func.warning(u'Error create data scheme object')
        return None

    def getModelObj(self):
        """
        Get model resource object.
        """
        model_psp = self.getModelPsp()

        if not model_psp:
            log_func.warning(u'Not define model in <%s : %s>' % (self.getName(), self.getType()))
            return None
        model_obj = self.getKernel().createByPsp(psp=model_psp)
        return model_obj

    def _updateLinkDataDataset(self, dataset, columns=None):
        """
        Update dataset by link object data

        :param dataset: Dataset list.
        :param columns: Column object list.
        :return: Updated dataset.
        """
        if columns is None:
            columns = self.getModelObj().getChildren()
        return model_navigator.iqModelNavigatorManager._updateLinkDataDataset(self, dataset=dataset, columns=columns)

    def _updateLinkDataRecord(self, record, columns=None):
        """
        Update record by link object data

        :param record: Record dictionary.
        :param columns: Column object list.
        :return: Updated record dictionary.
        """
        if columns is None:
            columns = self.getModelObj().getChildren()
        return model_navigator.iqModelNavigatorManager._updateLinkDataRecord(self, record=record, columns=columns)


COMPONENT = iqDataNavigator
