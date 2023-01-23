#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cataloger manager class.
"""

import os
import os.path
import shutil

from ...util import log_func
from ..catalog_level import catalog_level as catalog_level_proto

__version__ = (0, 0, 0, 1)


class iqCatalogerProto(object):
    """
    Cataloger prototype class.

    self.physic_catalog - List of physical directory levels
    self.logic_catalogs - Dictionary of logical directory structures:
        {
        'logic catalog name': [physical directory level index list],
        ...
        }

    The default directory is stored in the usual folder-file structure
    on the disk, but in order to be able to change the storage,
    let’s say the directory has these functions:
    self._put_physic_func(obj, physic_path) - Overridden function of placing an object in a physical directory
    self._get_physic_func(physic_path) - Overridden function to get an object from a physical directory
    self.physic_catalog_folder - Physical directory location folder
    """

    def __init__(self):
        """
        Constructor.
        """
        # List of physical directory levels
        self.physic_catalog = list()

        self.logic_catalogs = dict()

        self._put_physic_func = None
        self._get_physic_func = None

        # Physical directory location folder
        self.physic_catalog_folder = None

        # The last item to be cataloged
        self.last_catalog_objpath = None

    def getLastObjPath(self):
        """
        Get last item to be cataloged.
        """
        return self.last_catalog_objpath

    def addPhysicCatalogLevel(self, catalog_level):
        """
        Add to the cataloger the level of the physical catalog.

        :param catalog_level: Catalog level object.
        :return: True/False
        """
        if not issubclass(catalog_level.__class__,
                          catalog_level_proto.iqCatalogLevelProto):
            log_func.warning(u'Object <%s> not catalog level')
            return False
        if self.physic_catalog is None:
            self.physic_catalog = list()
        self.physic_catalog_func.append(catalog_level)
        return True

    def addLogicCatalogSeries(self, logic_catalog_name, *index_series):
        """
        Add logic catalogs.

        :param logic_catalog_name: Logic catalog name.
        :param index_series: The sequence of indices of the levels of the physical catalog.
        :return: True/False
        """
        # Checking input types
        check_arg = min([isinstance(idx, int) for idx in index_series])
        if not check_arg:
            log_func.warning(u'Not valid indexes type')
            return False

        if self.logic_catalogs is None:
            self.logic_catalogs = list()

        # Indices should not be repeated
        index_series = tuple([idx for i, idx in enumerate(index_series) if idx not in index_series[i+1:]])
        self.logic_catalogs[logic_catalog_name] = index_series
        return True

    def putObject(self, obj, do_remove=False):
        """
        Place an object in a catalog.
        Placement is made according to the characteristics of the object
        at the levels of the physical catalog.

        :param obj: Catalogable object.
        :param do_remove: Transfer object?
        :return: True/False.
        """
        phys_path = list()
        for level in self.physic_catalog:
            folder_name = level.getFolderName(obj)
            phys_path.append(folder_name)

        return self.putObjPath(obj, phys_path, do_remove=do_remove)

    def logic2physicPath(self, logic_path, logic_catalog_name):
        """
        Convert logical path to physical.

        :param logic_path: Logic path.
        :param logic_catalog_name: Logic catalog name.
        :return: List of folder names of the physical path or None if error.
        """
        logic_series = self.logic_catalogs.get(logic_catalog_name, None)
        if logic_series is None:
            log_func.warning(u'Not define logic catalog series <%s>' % logic_catalog_name)
            return None
        if len(logic_path) != len(logic_series):
            log_func.warning(u'Path does not match logic catalog series')
            return None

        phys_path = [None] * len(self.physic_catalog)
        for i, idx in enumerate(logic_series):
            phys_path[idx] = logic_path[i]
        return phys_path

    def putObjPath(self, obj, path, logic_catalog_name=None, do_remove=False):
        """
        Placing an object in a directory along a path.

        :param obj: Catalogable object.
        :param path: Catalog path for placement.
            Catalog path - list of folder names.
        :param logic_catalog_name: The name of the logical directory,
            if the placement is made by the logical directory.
            If None, then we believe that the placement is made according
            to the physical catalog.
        :param do_remove: Transfer object?
        :return: True/False.
        """
        phys_path = path
        if logic_catalog_name:
            phys_path = self.logic2physicPath(path, logic_catalog_name)
            if phys_path is None:
                return False

        return self.putObjPhysicPath(obj, phys_path, do_remove=do_remove)

    def putObjPhysicPath(self, obj, physic_path, do_remove=False):
        """
        Placing an object in a physical directory along a physical path.

        :param obj: Catalogable object.
        :param physic_path: The physical path in the physical directory.
            Directory path - a list of folder names.
        :param do_remove: Transfer object?
        :return: True/False.
        """
        self.last_catalog_objpath = None

        if self._put_physic_func:
            # If an external function is defined, then pass control to it
            return self._put_physic_func(obj, physic_path)

        if self.physic_catalog_folder is None:
            log_func.warning(u'The catalog folder for the cataloger physical directory is not defined')
            return False
        real_path = os.path.join(self.physic_catalog_folder, *physic_path)

        if isinstance(obj, str):
            # If the object is a string, then we assume that this is the file name
            if not os.path.exists(obj):
                log_func.warning(u'File <%s> not found for catalogization' % obj)
                return False
            filename = os.path.join(real_path, os.path.basename(obj))
            log_func.debug(u'Copy file <%s> to folder <%s>' % (obj, real_path))
            try:
                if not os.path.exists(real_path):
                    os.makedirs(real_path)
                if os.path.exists(filename) and not os.path.samefile(obj, filename):
                    # Delete if such a file already exists in the directory
                    log_func.warning(u'File <%s> exists in catalog. File will be deleted' % filename)
                    os.remove(filename)
                if not os.path.exists(filename) or not os.path.samefile(obj, filename):
                    shutil.copyfile(obj, filename)
                    log_func.info(u'Copy <%s> -> <%s> ... ok' % (obj, filename))

                    if do_remove:
                        try:
                            log_func.info(u'Delete file <%s>' % obj)
                            os.remove(obj)
                        except:
                            log_func.fatal(u'Error delete file <%s>' % obj)
                else:
                    log_func.warning(u'Error copy file <%s> -> <%s>' % (obj, filename))

                self.last_catalog_objpath = filename
            except:
                log_func.fatal(u'Error copy file <%s> to <%s>' % (obj, filename))
                return False
            return True
        else:
            log_func.warning(u'Unsupported catalogable object type <%s>' % type(obj))
        return False

    def getObject(self, path, logic_catalog_name=None):
        """
        Get an object along the path.

        :param path: Object path.
        :param logic_catalog_name: The name of the logical directory,
            if the placement is made by the logical directory.
            If None, then we believe that the placement is made according
            to the physical catalog.
        :return: Object/Filename in physic catalog.
        """
        if logic_catalog_name:
            path = self.logic2physicPath(path, logic_catalog_name)
        return self.getObjPhysicPath(path)

    def getObjPhysicPath(self, physic_path):
        """
        Get object by path in physic catalog.

        :return: Object/Filename in physic catalog.
        """
        if self._get_physic_func:
            # If an external function is defined, then pass control to it
            return self._get_physic_func(physic_path)

        # The path of the physical directory, just get the path to the file and return it
        real_path = os.path.join(*physic_path)
        if not os.path.exists(real_path):
            # We warn that there is no such object, but we return the real way
            log_func.warning(u'Object <%s> not found in physic catalog' % real_path)
        return real_path
