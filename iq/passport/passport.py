#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Passport - Structure identifying the program object.

The composition of the passport includes:
    type - Object Type Name
    name - Object Name
    module - Object Module file name
    guid - The unique identifier of the object in memory.
"""

import os.path

from ..util import file_func
from ..util import global_func
from ..util import res_func
from ..util import spc_func

__version__ = (0, 0, 0, 1)


PASSPORT_STR_DELIM = '.'
DEFAULT_THIS_PROJECT_NAME = 'THIS'


class iqPassport(object):
    """
    Passport - Structure identifying the program object.
    """
    def __init__(self, prj=None, module=None, typename=None, name=None, guid=None):
        """
        Constructor.

        :param prj: Project name.
        :param module: Object module file name.
        :param typename: Object type name.
        :param name: Object name.
        :param guid: The unique identifier of the object in memory.
        """
        self.prj = prj
        self.module = module
        self.typename = typename
        self.name = name
        self.guid = guid

    def set(self, prj=None, typename=None, name=None, module=None, guid=None):
        """
        Set passport.

        :param prj: Project name.
        :param module: Object module file name.
        :param typename: Object type name.
        :param name: Object name.
        :param guid: The unique identifier of the object in memory.
        """
        self.prj = prj
        self.module = module
        self.typename = typename
        self.name = name
        self.guid = guid
        return self

    def to_str(self):
        """
        Convert to string.

        :return: Passport as string.
        """
        return '%s.%s.%s.%s%s' % (str(self.prj) if self.prj else 'THIS',
                                  str(self.module),
                                  str(self.typename),
                                  str(self.name),
                                  '.%s' % str(self.guid) if self.guid else '')

    def from_str(self, passport=None):
        """
        Set passport from string.

        :param passport: Passport as string.
        :return:
        """
        if not isinstance(passport, str):
            assert u'Error passport as string'

        passport_tuple = tuple(passport.split(PASSPORT_STR_DELIM))
        self.from_tuple(passport_tuple)
        return self

    def to_dict(self):
        """
        Convert to dictionary.

        :return: Passport as dictionary.
        """
        return dict(prj=self.prj, module=self.module,
                    type=self.typename, name=self.name, guid=self.guid)

    def to_tuple(self):
        """
        Convert to tuple.

        :return: Passport as tuple.
        """
        return self.prj, self.module, self.typename, self.name, self.guid

    def from_dict(self, passport=None):
        """
        Set passport from dictionary.

        :param passport: Passport as dictionary.
        """
        if not isinstance(passport, dict):
            assert u'Error passport as dictionary'

        self.prj = passport.get('prj', None)
        self.module = passport.get('module', None)
        self.typename = passport.get('type', None)
        self.name = passport.get('name', None)
        self.guid = passport.get('guid', None)
        return self

    def from_tuple(self, passport=None):
        """
        Set passport from tuple.

        :param passport: Passport as tuple.
        """
        if not isinstance(passport, tuple):
            assert u'Error passport as tuple'

        if len(passport) not in (4, 5):
            assert u'Error length passport as tuple'

        self.prj = passport[0]
        self.module = passport[1]
        self.typename = passport[2]
        self.name = passport[3]
        self.guid = passport[4] if len(passport) == 5 else None
        return self

    def is_passport(self, passport=None):
        """
        Check whether the structure is a passport.

        :param passport: Passport as not known structure.
        :return: True - this is a passport / False - no it's not a passport.
        """
        if isinstance(passport, dict):
            return True
        elif isinstance(passport, tuple) and len(passport) in (4, 5):
            return True
        elif issubclass(passport.__class__, self.__class__):
            return True
        return False

    def same_passport(self, passport=None, compare_guid=False):
        """
        Passport сomparison.

        :param passport: Passport as not known structure.
        :param compare_guid: Compare GUID?
        :return: True - Same passport / False - Different passports.
        """
        if not self.is_passport(passport=passport):
            return False

        compare = [False]
        if isinstance(passport, dict):
            compare = [self.prj == passport.get('prj', None),
                       self.module == passport.get('module', None),
                       self.typename == passport.get('type', None),
                       self.name == passport.get('name', None)]
            if compare_guid:
                compare.append(self.guid == passport.get('guid', None))
        elif isinstance(passport, tuple) and len(passport) >= 3:
            compare = [self.prj == passport[0],
                       self.module == passport[1],
                       self.typename == passport[2],
                       self.name == passport[3]]
            if compare_guid:
                compare.append(self.guid == passport[4])
        return all(compare)

    def findResourceFilename(self, passport=None, find_path=None):
        """
        Find resource file by passport.

        :param passport: Object passport.
        :param find_path: Directory path to search.
            If None then get project path.
        :return: Resource filename or None if error.
        """
        passport = self.set_from(passport)

        if find_path is None:
            prj_name = global_func.getProjectName() if not passport.prj or passport.prj == DEFAULT_THIS_PROJECT_NAME else passport.prj
            prj_path = os.path.join(file_func.getFrameworkPath(), prj_name)
            find_path = prj_path

        file_names = file_func.getFileNames(find_path)
        res_filename = file_func.setFilenameExt(passport.module, res_func.RESOURCE_FILE_EXT)
        if res_filename in file_names:
            return os.path.join(find_path, res_filename)
        else:
            dir_paths = file_func.getDirectoryPaths(find_path)
            for dir_path in dir_paths:
                find_res_filename = self.findResourceFilename(passport, find_path=dir_path)
                if find_res_filename:
                    return find_res_filename
        return None

    def findObjResource(self, passport=None):
        """
        Find object resource by passport.

        :param passport: Object passport.
        :return: Object resource or None if not found.
        """
        passport = self.set_from(passport)

        res_filename = self.findResourceFilename(passport=passport)
        if res_filename:
            resource = res_func.loadRuntimeResource(res_filename)
            return spc_func.findObjResource(resource,
                                            object_type=passport.typename,
                                            object_name=passport.name,
                                            object_guid=passport.guid)
        return None

    def set_from(self, passport=None):
        """
        Set passport.

        :param passport: Passport data.
        :return: Self passport.
        """
        if passport is None:
            passport = self
        elif isinstance(passport, iqPassport):
            pass
        elif isinstance(passport, str):
            passport = self.from_str(passport)
        elif isinstance(passport, dict):
            passport = self.from_dict(passport)
        elif isinstance(passport, (list, tuple)):
            passport = self.from_tuple(passport)
        return passport
