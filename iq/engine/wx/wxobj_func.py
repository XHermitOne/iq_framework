#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Additional functions for working with wx objects.
"""

import wx


__version__ = (0, 0, 0, 1)


def isSameWxObject(wx_obj1, wx_obj2):
    """
    Check for the same object.

    :param wx_obj1: The first object to compare.
    :param wx_obj2: The second object to compare.
    :return: If this is the same object, then True otherwise False.
    """
    if issubclass(wx_obj1.__class__, wx.Object) and issubclass(wx_obj2.__class__, wx.Object):
        # Heir comparison wx.Object
        return wx_obj1.IsSameAs(wx_obj2)
    elif 'Swig' in wx_obj1.__str__() and 'Swig' in wx_obj2.__str__():
        # Not all wxPython classes inherit from wx.Object
        # So just check the string representation of the objects
        return wx_obj1.__str__() == wx_obj2.__str__()
    # Just checking objects as python
    return wx_obj1 == wx_obj2


def isWxObjectInList(wx_obj, wx_obj_list):
    """
    Check if wx object is in the list.

    :param wx_obj: wx object.
    :param wx_obj_list: Object list.
    :return: True/False.
    """
    return bool([obj for obj in wx_obj_list if isSameWxObject(wx_obj, obj)])


def getIndexWxObjectInList(wx_obj, wx_obj_list):
    """
    Get the index of the wx object in the list.

    :param wx_obj: wx object.
    :param wx_obj_list: Object list.
    :return: The index of the object in the list, if present
         or -1 if it is not present.
    """
    for i, obj in enumerate(wx_obj_list):
        if isSameWxObject(wx_obj, obj):
            return i
    return -1


def isWxDeadObject(wx_object):
    """
    Checking if the WX object is a deleted / destroyed Destroy method.

    :param wx_object: WX object.
    :return: True/False.
    """
    if wx_object is None:
        return True
    if not issubclass(wx_object.__class__, wx.Object):
        # If the class is not a descendant of wx.Object, then there is no need to check
        return False
    return not wx_object  # avoid a PyDeadObject error
