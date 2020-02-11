#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specification functions.
"""

import copy

from . import log_func

from .. import components

__version__ = (0, 0, 0, 1)

SYS_ATTR_SIGN = '__'
CHILDREN_ATTR_NAME = '_children_'

ICON_ATTR_NAME = '__icon__'
PARENT_ATTR_NAME = '__parent__'
EDIT_ATTR_NAME = '__edit__'
HELP_ATTR_NAME = '__help__'
DOC_ATTR_NAME = '__doc__'
CONTENT_ATTR_NAME = '__content__'

TEST_FUNC_ATTR_NAME = '__test__'
DESIGN_FUNC_ATTR_NAME = '__design__'

BASIC_ATTRIBUTES = ('name', 'type', 'description', 'activate', 'guid')
ALL_BASIC_ATTRIBUTES = list(BASIC_ATTRIBUTES) + [CHILDREN_ATTR_NAME]


def fillSpcByParent(spc):
    """
    Fill component specification by __parent__.

    :param spc: Component specification dictionary.
    :return:
    """
    if PARENT_ATTR_NAME in spc and isinstance(spc[PARENT_ATTR_NAME], dict):
        spc = fillResourceBySpc(resource=spc, spc=spc[PARENT_ATTR_NAME])
    return spc


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
        component_type = resource.get('type', None)
        if component_type:
            spc = getSpcByType(component_type)
        if not spc:
            log_func.warning(u'Not define component specification <%s>' % component_type)

    try:
        spc = fillSpcByParent(spc)

        for attr_name in list(spc.keys()):
            # log_func.debug(u'Attr <%s> Resource %s Specification %s' % (attr_name, resource, spc))
            if attr_name not in resource and attr_name != PARENT_ATTR_NAME:
                if attr_name.startswith(SYS_ATTR_SIGN):
                    resource[attr_name] = spc[attr_name]
                else:
                    if isinstance(spc[attr_name], list) and attr_name in resource:
                        resource[attr_name] += copy.deepcopy(spc[attr_name])
                    elif isinstance(spc[attr_name], list) and attr_name not in resource:
                        resource[attr_name] = copy.deepcopy(spc[attr_name])
                    elif isinstance(spc[attr_name], dict) and attr_name in resource:
                        resource[attr_name].update(copy.deepcopy(spc[attr_name]))
                    elif isinstance(spc[attr_name], dict) and attr_name not in resource:
                        resource[attr_name] = copy.deepcopy(spc[attr_name])
                    else:
                        resource[attr_name] = spc[attr_name]

        if CHILDREN_ATTR_NAME in resource:
            children = resource[CHILDREN_ATTR_NAME]
            resource[CHILDREN_ATTR_NAME] = [fillResourceBySpc(resource=child) for child in children]

        if PARENT_ATTR_NAME in resource:
            del resource[PARENT_ATTR_NAME]
        # log_func.debug(u'Resource %s Specification %s' % (resource, spc))
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


def getResourceRootComponentType(resource):
    """
    Get resource root component type.

    :param resource: Resource data structure.
    :return: resource root component type name or None if error.
    """
    if isinstance(resource, dict):
        return resource.get('type', None)
    else:
        log_func.error(u'Resource type error')
    return None


def getSpcByType(component_type):
    """
    Get component specification by component type.

    :param component_type: Component type.
    :return: Component specification or None if error.
    """
    return components.findComponentSpc(component_type=component_type)
