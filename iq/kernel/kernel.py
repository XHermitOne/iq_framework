#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kernel - general dispatcher of all program objects.
"""

import sys
import os.path

from .. import config
from ..util import global_func
from ..util import log_func
from ..util import res_func
from .. import components

from ..passport import passport
from .. import project

__version__ = (0, 0, 0, 1)

RUNTIME_MODE_STATE = 'runtime'
EDITOR_MODE_STATE = 'editor'
RESOURCE_EDITOR_MODE_STATE = 'resource_editor'

DEFAULT_RETURN_CODE = 0


class iqKernel(object):
    """
    Kernel - general dispatcher of all program objects.
    """
    def __init__(self, project_name=None, *args, **kwargs):
        """
        Constructor.
        """
        self.setProject(project_name)

        # Is running state?
        self.is_running = False

        # Component cache
        self._components = components.getComponents()

        # Program object cache
        self._object_cache = dict()

        # Application object
        # self.app = None
        #
        # self.app_return_code = 0

    def setProject(self, project_name=None):
        """
        Set current project_name.

        :param project_name: Project name.
        :return: True/False.
        """
        global_func.setProjectName(project_name)
        return True

    def start(self, mode=None, project_name=None, username=None, password=None):
        """
        Start program.

        :param mode: Startup mode (runtime, editor).
            If not defined, it is taken from the configuration file.
        :param project_name: Project name.
            If not defined, it is taken from the configuration file.
        :param username: User name.
        :param password: User password.
        :return: True/False.
        """
        if isinstance(mode, str):
            global_func.setRuntimeMode(mode == RUNTIME_MODE_STATE)
        if isinstance(project_name, str):
            global_func.setProjectName(project_name)

        try:
            prj_psp = passport.iqPassport(prj=project_name, module=project_name,
                                          typename=project.COMPONENT_TYPE, name=project_name)
            log_func.debug(u'Project passport <%s>' % prj_psp.getAsStr())
            prj = self.createObject(psp=prj_psp, parent=self)

            config.set_cfg_param('PROJECT', prj)
            return prj.start(username, password)
        except:
            log_func.fatal(u'Start programm error')
        return False

    def stop(self):
        """
        Stop programm.

        :return: True/False
        """
        prj = global_func.getProject()
        if prj:
            prj.stop()

        sys.exit(DEFAULT_RETURN_CODE)

    def _createByResource(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Create object by resource.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        obj = None
        try:
            component_type = resource.get('type', None)
            if not component_type:
                log_func.error(u'Not define component type in resource %s' % resource)
            else:
                component_class = self._components.get(component_type, None)
                if not component_class:
                    log_func.error(u'Component <%s> not registered' % component_type)
                else:
                    try:
                        obj = component_class(parent, resource, context, *args, **kwargs)
                    except:
                        log_func.fatal(u'Create object error. Component <%s>' % component_type)
                        obj = None
        except:
            log_func.fatal(u'Create object by resource error')
        return obj

    def _createByResFile(self, parent=None, res_filename=None, context=None, *args, **kwargs):
        """
        Create object by resource file.

        :param parent: Parent object.
        :param res_filename: Resource filename.
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        resource = res_func.loadRuntimeResource(res_filename)
        return self._createByResource(parent=parent, resource=resource,
                                      context=context, *args, **kwargs)

    def _createByPsp(self, parent=None, psp=None, context=None, *args, **kwargs):
        """
        Create object by resource file.

        :param parent: Parent object.
        :param psp: Object passport.
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        resource = passport.iqPassport().findObjResource(passport=psp)
        if resource:
            return self._createByResource(parent=parent, resource=resource,
                                          context=context, *args, **kwargs)
        return None

    def _create(self, parent=None, object_data=None, context=None, *args, **kwargs):
        """
        Create object.

        :param parent: Parent object.
        :param object_data: Object data (passport, resource or resource filename).
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        psp = passport.iqPassport()
        if psp.isPassport(object_data):
            return self._createByPsp(parent=parent, psp=psp, context=context, *args, **kwargs)
        elif isinstance(object_data, str) and os.path.isfile(object_data):
            return self._createByResFile(parent=parent, res_filename=object_data, context=context, *args, **kwargs)
        elif isinstance(object_data, dict):
            return self._createByResource(parent=parent, resource=object_data, context=context, *args, **kwargs)
        return None

    def findObject(self, psp, compare_guid=False):
        """
        Find object in object cache.

        :param psp: Object passport.
        :param compare_guid: Compare GUID?
        :return: Registered object or None if not found.
        """
        obj_psp = passport.iqPassport().setAsAny(psp)
        for psp_tuple in list(self._object_cache.keys()):
            if obj_psp.isSamePassport(psp_tuple, compare_guid=compare_guid):
                return self._object_cache[psp_tuple]
        return None

    def getObject(self, psp, compare_guid=False, *args, **kwargs):
        """
        Find an object in the cache, or if it is not registered, _create.

        :param psp: Object passport.
        :param compare_guid: Compare GUID?
        :return: Registered object or None if error.
        """
        find_obj = self.findObject(psp, compare_guid=compare_guid)
        if find_obj:
            return find_obj

        return self.createObject(psp=psp, *args, **kwargs)

    def createObject(self, psp, *args, **kwargs):
        """
        Create object by passport.

        :param psp: Object passport.
        :return: Registered object or None if error.
        """
        obj = self._createByPsp(psp=psp, *args, **kwargs)
        self._object_cache[psp] = obj
        return obj


def initSettings():
    """
    Project settings saved to file INI.
    """
    if config.get_cfg_param('SETTINGS') is None:
        from ..engine import settings_access
        config.set_cfg_param('SETTINGS',
                             settings_access.iqSettingsDotUse())
    return config.get_cfg_param('SETTINGS')


def initObjects():
    """
    Access to project objects.
    """
    if config.get_cfg_param('OBJECTS') is None:
        from ..engine import objects_access
        config.set_cfg_param('OBJECTS',
                             objects_access.iqObjectDotUse())
    return config.get_cfg_param('OBJECTS')


def createKernel():
    """
    Create kernel object.

    :return: Kernel object.
    """
    kernel = iqKernel()
    config.set_cfg_param('KERNEL', kernel)

    initSettings()
    initObjects()

    return kernel
