#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specification functions.
"""

import copy

from . import log_func

__version__ = (0, 0, 0, 1)

CHILDREN_ATTR_NAME = '_children_'
PARENT_ATTR_NAME = '__parent__'
SYS_ATTR_SIGN = '__'


def fillResourceBySpc(resource=None, spc=None):
    """
    Add resource with specification attributes.

    :param resource: Resource dictionary.
    :param spc: Specification dictionary.
    :return: Qualified resource filled or None if error.
    """
    if resource is None:
        resource = dict()

    if spc is None:
        spc = dict()

    try:
        for attr_name in list(spc.keys()):
            if attr_name == PARENT_ATTR_NAME and isinstance(spc[PARENT_ATTR_NAME], dict):
                resource = fillResourceBySpc(resource=resource, spc=spc[PARENT_ATTR_NAME])
            elif attr_name not in resource and attr_name != PARENT_ATTR_NAME:
                if attr_name.startswith(SYS_ATTR_SIGN):
                    resource[attr_name] = spc[attr_name]
                else:
                    if isinstance(spc[attr_name], (list, dict)):
                        resource[attr_name] = copy.deepcopy(spc[attr_name])
                    else:
                        resource[attr_name] = spc[attr_name]
        return resource
    except:
        log_func.fatal(u'Add resource with specification attributes error')
    return None


def clearResourceFromSpc(resource=None):
    """
    Clear resource from specification attributes.

    :return: Purified resource from specification attributes or None if error.
    """
    if resource is None:
        resource = dict()

    dst_resource = dict()
    try:
        for attr_name in list(resource.keys()):
            if not attr_name.startswith(SYS_ATTR_SIGN) and attr_name != CHILDREN_ATTR_NAME:
                dst_resource[attr_name] = resource[attr_name]
            elif attr_name == CHILDREN_ATTR_NAME:
                dst_resource[attr_name] = list()
                for child_resource in resource[attr_name]:
                    dst_resource[attr_name].append(clearResourceFromSpc(resource=child_resource))
        return dst_resource
    except:
        log_func.fatal(u'Clear resource from specification attributes error')
    return None
