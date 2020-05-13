#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Catalog level component.
"""

from ... import object

from . import spc
from . import catalog_level

from ...util import log_func
from ...util import exec_func

__version__ = (0, 0, 0, 1)


class iqCatalogLevel(catalog_level.iqCatalogLevelProto, object.iqObject):
    """
    Catalog level component.
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

        catalog_level.iqCatalogLevelProto.__init__(self)

        if self.isGetFolderNameFunc():
            self._get_folder_name_func = self.getFolderNameFunc
        else:
            log_func.warning(u'Not defined  function to determine the directory level folder name <%s>' % self.getName())
            self._get_folder_name_func = None

    def isGetFolderNameFunc(self):
        """
        Defined function to get the name of the folder location of the object?

        :return: True/False.
        """
        return self.isAttributeValue('get_folder_name')

    def getFolderNameFunc(self, obj):
        """
        The function of obtaining the folder name of the location of the object by the object itself.

        :param obj: Catalogable object.
        :return: Folder name.
        """
        context = self.getContext()
        context['OBJ'] = obj
        function_body = self.getAttribute('get_folder_name')
        result = exec_func.execTxtFunction(function=function_body, context=context)
        if result:
            log_func.debug(u'Allocation folder <%s>' % result)
            return result
        else:
            log_func.error(u'Cataloger. Error define folder name by catalog level <%s>' % self.getName())
        return self.getName()


COMPONENT = iqCatalogLevel
