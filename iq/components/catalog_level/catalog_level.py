#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Catalog level class module.
"""

__version__ = (0, 0, 0, 1)

# Default level folder name
DEFAULT_LEVEL_FOLDER_NAME = 'unknown'


class iqCatalogLevelProto(object):
    """
    Catalog level prototype class.

    self._get_folder_name_func(obj) - External definition function
         name of the level folder by the object placed in the directory.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._get_folder_name_func = None

    def getFolderName(self, obj):
        """
        Get level folder name by catalogable object.

        :param obj: Catalogable object.
        :return: Folder name.
        """
        if self._get_folder_name_func:
            return self._get_folder_name_func(obj)
        if hasattr(self, 'name'):
            # If a level name is specified, then it is the default folder name
            return self.name
        return DEFAULT_LEVEL_FOLDER_NAME
