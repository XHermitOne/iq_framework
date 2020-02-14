#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data scheme manager.
"""

from ...util import log_func
from ...util import imp_func

from . import scheme_module_generator

__version__ = (0, 0, 0, 1)


class iqSchemeManager(scheme_module_generator.iqSchemeModuleGenerator):
    """
    Data scheme manager.
    """
    def getDBEngine(self):
        """
        Get database engine.

        :return:
        """
        return None

    def getModule(self, module_filename=None):
        """
        Get module object.

        :param module_filename: Module filename.
            If None then generate module filename.
        :return: Module object if None if error.
        """
        if module_filename is None:
            module_filename = self.genModuleFilename()
        if not self.existsModule(module_filename):
            self.genModule(module_filename)

        if self.existsModule(module_filename):
            return imp_func.loadPyModule(name=self.getName(),
                                         path=module_filename)
        else:
            log_func.error(u'Scheme <%s> module <%s> not exists' % (self.getName(), module_filename))
        return None

    def getModel(self, model_name):
        """
        Get model class object.

        :param model_name: Model name.
        :return: Model class object or None if error.
        """
        module = self.getModule()
        if module and hasattr(module, model_name):
            return getattr(module, model_name)
        else:
            log_func.error(u'Model <%s> not find in module <%s>' % (model_name, module.__file__))
        return None
