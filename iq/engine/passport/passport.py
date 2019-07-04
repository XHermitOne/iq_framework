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

__version__ = (0, 0, 0, 1)


class iqPassport(object):
    """
    Passport - Structure identifying the program object.
    """
    def __init__(self, type=None, name=None, module=None, guid=None):
        """
        Constructor.
        @param type: Object Type Name.
        @param name: Object Name.
        @param module: Object Module file name.
        @param guid: The unique identifier of the object in memory.
        """
        self.type = type
        self.name = name
        self.module = module
        self.guid = guid

    def set(self, type=None, name=None, module=None, guid=None):
        """
        Set passport.
        @param type: Object Type Name.
        @param name: Object Name.
        @param module: Object Module file name.
        @param guid: The unique identifier of the object in memory.
        """
        self.type = type
        self.name = name
        self.module = module
        self.guid = guid

    def to_dict(self):
        """
        Convert to dictionary.
        @return: Passport as dictionary.
        """
        return dict(type=self.type, name=self.name, module=self.module, guid=self.guid)

    def to_tuple(self):
        """
        Convert to tuple.
        @return: Passport as tuple.
        """
        return self.type, self.name, self.module, self.guid

    def from_dict(self, passport=None):
        """
        Set passport from dictionary.
        @param passport: Passport as dictionary.
        """
        if not isinstance(passport, dict):
            assert u'Error passport as dictionary'

        self.type = passport.get('type', None)
        self.name = passport.get('name', None)
        self.module = passport.get('module', None)
        self.guid = passport.get('guid', None)

    def from_tuple(self, passport=None):
        """
        Set passport from tuple.
        @param passport: Passport as tuple.
        """
        if not isinstance(passport, tuple):
            assert u'Error passport as tuple'

        if len(passport) != 4:
            assert u'Error length passport as tuple'

        self.type = passport[0]
        self.name = passport[1]
        self.module = passport[2]
        self.guid = passport[3]

    def is_passport(self, passport=None):
        """
        Check whether the structure is a passport.
        @param passport: Passport as not known structure.
        @return: True - this is a passport / False - no it's not a passport.
        """
        if isinstance(passport, dict):
            return True
        elif isinstance(passport, tuple) and len(passport) == 4:
            return True
        elif issubclass(passport.__class__, self.__class__):
            return True
        return False

    def same_passport(self, passport=None, compare_guid=False):
        """
        Passport сomparison.
        @param passport: Passport as not known structure.
        @param compare_guid: Compare GUID?
        @return: True - Same passport / False - Different passports.
        """
        if not self.is_passport(passport=passport):
            return False

        compare = [False]
        if isinstance(passport, dict):
            compare = [self.type == passport.get('type', None),
                       self.name == passport.get('name', None),
                       self.module == passport.get('module', None)]
            if compare_guid:
                compare.append(self.guid == passport.get('guid', None))
        elif isinstance(passport, tuple) and len(passport) >= 3:
            compare = [self.type == passport[0],
                       self.name == passport[1],
                       self.module == passport[2]]
            if compare_guid:
                compare.append(self.guid == passport[3])
        return all(compare)

