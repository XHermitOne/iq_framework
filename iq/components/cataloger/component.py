#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cataloger component.
"""

import os
import os.path

from ... import object

from . import spc
from . import cataloger

from ...util import log_func
from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqCataloger(cataloger.iqCatalogerProto, object.iqObject):
    """
    Cataloger component.
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

        cataloger.iqCatalogerProto.__init__(self)

        self.createChildren()

        # List of physical directory levels
        self.physic_catalog = self.getChildren()

        if self.isPutPhysicFunc():
            self._put_physic_func = self.putPhysicFunc
        if self.isGetPhysicFunc():
            self._get_physic_func = self.getPhysicFunc

        # Define the physical directory location folder
        self.physic_catalog_folder = self.getFolder()

    def getFolder(self):
        """
        Location path.
        """
        folder = self.getAttribute('folder')

        if folder and os.path.isabs(folder) and not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except OSError:
                log_func.fatal(u'Error create cataloger folder <%s>' % self.getName())
        return folder

    def isPutPhysicFunc(self):
        """
        Is the location function in the cataloger defined?

        :return: True/False.
        """
        return self.isAttributeValue('put_physic_func')

    def isGetPhysicFunc(self):
        """
        Defined function to get an object from the cataloguer?

        :return: True/False.
        """
        return self.isAttributeValue('get_physic_func')

    def putPhysicFunc(self, obj, physic_path):
        """
        The function of placing an object in a physical directory.

        :param obj: Catalogable object in physic catalog.
        :param physic_path: Object path in physic catalog.
        :return: True/False.
        """
        context = self.getContext()
        context['OBJ'] = obj
        context['PHYSIC_PATH'] = physic_path
        context['PATH'] = physic_path
        function_body = self.getAttribute('put_physic_func')
        result = exec_func.execTxtFunction(function=function_body, context=context)
        if result:
            return result
        else:
            log_func.error(u'Cataloger <%s>. Error put object to physic catalog. Path <%s>' % (self.getName(),
                                                                                               physic_path))
        return False

    def getPhysicFunc(self, physic_path):
        """
        The function of obtaining an object from a physical directory.

        :param physic_path: Object path in physic catalog.
        :return: Object/File name in physic catalog.
        """
        context = self.getContext()
        context['PHYSIC_PATH'] = physic_path
        context['PATH'] = physic_path

        function_body = self.getAttribute('get_physic_func')
        result = exec_func.execTxtFunction(function=function_body, context=context)
        if result:
            return result
        else:
            log_func.error(u'Cataloger <%s>. Error get object from physic catalog. Path <%s>' % (self.getName(),
                                                                                                 physic_path))
        return None


COMPONENT = iqCataloger
