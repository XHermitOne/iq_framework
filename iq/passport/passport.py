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
from ..util import log_func

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

    def __str__(self):
        return self.getAsStr()

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

    def getAsStr(self):
        """
        Convert to string.

        :return: Passport as string.
        """
        return '%s.%s.%s.%s%s' % (str(self.prj) if self.prj else 'THIS',
                                  str(self.module),
                                  str(self.typename),
                                  str(self.name),
                                  '.%s' % str(self.guid) if self.guid else '')

    def setAsStr(self, passport=None):
        """
        Set passport from string.

        :param passport: Passport as string.
        :return:
        """
        assert (isinstance(passport, str) and self.isPassport(passport)), u'Error passport as string'

        passport_tuple = tuple(passport.split(PASSPORT_STR_DELIM))
        # log_func.debug(u'Passport as tuple %s : %s' % (str(passport_tuple), self.isPassport(passport)))
        self.setAsTuple(passport_tuple)
        return self

    def getAsDict(self):
        """
        Convert to dictionary.

        :return: Passport as dictionary.
        """
        return dict(prj=self.prj, module=self.module,
                    type=self.typename, name=self.name, guid=self.guid)

    def setAsDict(self, passport=None):
        """
        Set passport from dictionary.

        :param passport: Passport as dictionary.
        """
        assert (isinstance(passport, dict) and self.isPassport(passport)), u'Error passport as dictionary'

        self.prj = passport.get('prj', None)
        self.module = passport.get('module', None)
        self.typename = passport.get('type', None)
        self.name = passport.get('name', None)
        self.guid = passport.get('guid', None)
        return self

    def getAsTuple(self):
        """
        Convert to tuple.

        :return: Passport as tuple.
        """
        return self.prj, self.module, self.typename, self.name, self.guid

    def setAsTuple(self, passport=None):
        """
        Set passport from tuple.

        :param passport: Passport as tuple.
        """
        assert (isinstance(passport, tuple) and self.isPassport(passport)), u'Error passport as tuple'

        assert (len(passport) in (4, 5)), u'Error length passport as tuple'

        self.prj = passport[0]
        self.module = passport[1]
        self.typename = passport[2]
        self.name = passport[3]
        self.guid = passport[4] if len(passport) == 5 else None
        return self

    def isPassport(self, passport=None):
        """
        Check whether the structure is a passport.

        :param passport: Passport as not known structure.
        :return: True - this is a passport / False - no it's not a passport.
        """
        if isinstance(passport, dict):
            return True
        elif isinstance(passport, tuple) and len(passport) in (4, 5):
            return True
        elif isinstance(passport, str) and len(passport.split(PASSPORT_STR_DELIM)) in (4, 5):
            return True
        elif issubclass(passport.__class__, self.__class__):
            return True
        return False

    def isSamePassport(self, passport=None, compare_guid=False):
        """
        Passport сomparison.

        :param passport: Passport as not known structure.
        :param compare_guid: Compare GUID?
        :return: True - Same passport / False - Different passports.
        """
        if not self.isPassport(passport=passport):
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
        passport = self.setAsAny(passport)

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
        log_func.error(u'Resource file <%s> not found in %s' % (res_filename, file_names))
        return None

    def findObjResource(self, passport=None):
        """
        Find object resource by passport.

        :param passport: Object passport.
        :return: Object resource or None if not found.
        """
        passport = self.setAsAny(passport)

        res_filename = self.findResourceFilename(passport=passport)
        if res_filename:
            resource = res_func.loadRuntimeResource(res_filename)
            obj_resource = spc_func.findObjResource(resource,
                                                    object_type=passport.typename,
                                                    object_name=passport.name,
                                                    object_guid=passport.guid)
            if not obj_resource:
                log_func.error(u'Object <%s> not found in resource' % str(passport))
            return obj_resource
        else:
            log_func.error(u'Resource file <%s> not found' % str(passport))
        return None

    def setAsAny(self, passport=None):
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
            passport = self.setAsStr(passport)
        elif isinstance(passport, dict):
            passport = self.setAsDict(passport)
        elif isinstance(passport, (list, tuple)):
            passport = self.setAsTuple(passport)
        return passport
