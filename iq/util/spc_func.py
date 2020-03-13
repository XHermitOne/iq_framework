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
GEN_MODULE_FUNC_ATTR_NAME = '__gen_module__'

BASIC_ATTRIBUTES = ('name', 'type', 'description', 'activate', 'guid', 'module')
ALL_BASIC_ATTRIBUTES = list(BASIC_ATTRIBUTES) + [CHILDREN_ATTR_NAME]


def fillAllResourcesBySpc(resource=None):
    """
    Add all object resources with specification attributes.

    :param resource: Resource dictionary.
    :return: Qualified resource filled or None if error.
    """
    resource = fillResourceBySpc(resource)
    if CHILDREN_ATTR_NAME in resource:
        for i, child_resource in enumerate(resource[CHILDREN_ATTR_NAME]):
            resource[CHILDREN_ATTR_NAME][i] = fillAllResourcesBySpc(child_resource)
    return resource


def fillSpcByParent(spc):
    """
    Add specification with parent specification attributes.

    :param spc: Component specification.
    :return: Qualified component specification filled or None if error.
    """
    if PARENT_ATTR_NAME in spc and isinstance(spc[PARENT_ATTR_NAME], dict):
        spc = fillResourceBySpc(spc, spc[PARENT_ATTR_NAME])
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
        if PARENT_ATTR_NAME in spc and isinstance(spc[PARENT_ATTR_NAME], dict):
            spc = fillResourceBySpc(spc, spc[PARENT_ATTR_NAME])

        for attr_name in spc.keys():
            if (attr_name in (EDIT_ATTR_NAME, HELP_ATTR_NAME) and attr_name in resource and
               isinstance(resource[attr_name], dict) and isinstance(spc[attr_name], dict)):
                for attr in spc[attr_name].keys():
                    if attr not in resource[attr_name]:
                        resource[attr_name][attr] = spc[attr_name][attr]

            elif attr_name not in resource and attr_name != PARENT_ATTR_NAME:
                if isinstance(spc[attr_name], (list, dict)):
                    resource[attr_name] = copy.deepcopy(spc[attr_name])
                else:
                    resource[attr_name] = spc[attr_name]
    except:
        log_func.fatal('Error add resource with specification attributes')

    return resource


def clearAllResourcesFromSpc(resource=None):
    """
    Clear resource from specification attributes.

    :return: Purified resource from specification attributes or None if error.
    """
    resource = clearResourceFromSpc(resource)
    if CHILDREN_ATTR_NAME in resource:
        for i, child_resource in enumerate(resource[CHILDREN_ATTR_NAME]):
            resource[CHILDREN_ATTR_NAME][i] = clearAllResourcesFromSpc(child_resource)
    return resource


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
        log_func.fatal(u'Error clear resource from specification attributes')
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
        log_func.error(u'Error resource type')
    return None


def getSpcByType(component_type):
    """
    Get component specification by component type.

    :param component_type: Component type.
    :return: Component specification or None if error.
    """
    return components.findComponentSpc(component_type=component_type)


def findObjResource(resource, object_type=None, object_name=None, object_guid=None):
    """
    Find object resource in parent resource by type, name and guid.

    :param resource: Parent object resource.
    :param object_type: Object type.
        If None then not searched.
    :param object_name: Object name.
        If None then not searched.
    :param object_guid:
        If None then not searched.
    :return: Object resource or None if not found.
    """
    if object_type is None:
        return resource

    resource_type = resource.get('type', None)
    resource_name = resource.get('name', None)
    resource_guid = resource.get('guid', None)

    find_resource = None
    if object_type and resource_type == object_type:
        find_resource = resource
    if find_resource:
        if object_name:
            find_resource = resource if resource_name == object_name else None
    if find_resource:
        if object_guid:
            find_resource = resource if resource_guid == object_guid else None
    if find_resource:
        return find_resource
    else:
        children = resource.get(CHILDREN_ATTR_NAME, list())
        for child_resource in children:
            find_resource = findObjResource(child_resource, object_type, object_name, object_guid)
            if find_resource:
                break
    return find_resource
