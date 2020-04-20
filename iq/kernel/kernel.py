#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kernel - general dispatcher of all program objects.
"""

import os.path

from .. import global_data
from ..util import global_func
from ..util import log_func
from ..util import res_func
from .. import components

from ..passport import passport
from .. import project

from . import objects_access, settings_access

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
        log_func.info(u'Set project <%s>' % project_name)
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
            prj = self.createObject(psp=prj_psp, parent=self, register=True)

            global_data.setGlobal('PROJECT', prj)
            result = prj.start(username, password)
            return result
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

        # Clear cache
        log_func.info(u'Clear object cache')
        self.printObjCache()
        for psp, obj in self._object_cache.items():
            if hasattr(obj, 'destroy'):
                try:
                    obj.destroy()
                except:
                    log_func.fatal(u'Error destroy object <%s>' % psp)

    def createByResource(self, parent=None, resource=None, context=None, *args, **kwargs):
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

    def createByResFile(self, parent=None, res_filename=None, context=None, *args, **kwargs):
        """
        Create object by resource file.

        :param parent: Parent object.
        :param res_filename: Resource filename.
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        resource = res_func.loadRuntimeResource(res_filename)
        obj = self.createByResource(parent=parent, resource=resource,
                                    context=context, *args, **kwargs)
        # Set passport
        psp = obj.getPassport()
        psp.module = os.path.splitext(os.path.basename(res_filename))[0]
        obj.setPassport(psp)
        return obj

    def createByPsp(self, parent=None, psp=None, context=None, *args, **kwargs):
        """
        Create object by resource file.

        :param parent: Parent object.
        :param psp: Object passport.
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        resource = passport.iqPassport().findObjResource(passport=psp)
        if resource:
            obj = self.createByResource(parent=parent, resource=resource,
                                        context=context, *args, **kwargs)
            # Set passport
            if obj:
                obj.setPassport(psp)
            return obj
        else:
            log_func.error(u'Resource <%s> not found' % str(psp))
        return None

    def create(self, parent=None, object_data=None, context=None, *args, **kwargs):
        """
        Create object.

        :param parent: Parent object.
        :param object_data: Object data (passport, resource or resource filename).
        :param context: Context dictionary.
        :return: New object or None if error.
        """
        psp = passport.iqPassport()
        if psp.isPassport(object_data):
            return self.createByPsp(parent=parent, psp=psp, context=context, *args, **kwargs)
        elif isinstance(object_data, str) and os.path.isfile(object_data):
            return self.createByResFile(parent=parent, res_filename=object_data, context=context, *args, **kwargs)
        elif isinstance(object_data, dict):
            return self.createByResource(parent=parent, resource=object_data, context=context, *args, **kwargs)
        return None

    def findObject(self, psp, compare_guid=False):
        """
        Find object in object cache.

        :param psp: Object passport.
        :param compare_guid: Compare GUID?
        :return: Registered object or None if not found.
        """
        obj_psp = passport.iqPassport().setAsAny(psp)
        for cache_psp in self._object_cache.keys():
            if obj_psp.isSamePassport(cache_psp, compare_guid=compare_guid):
                return self._object_cache[cache_psp]
        # log_func.debug(u'KERNEL. Object <%s> not found' % str(psp))
        return None

    def getObject(self, psp, compare_guid=False, register=True, *args, **kwargs):
        """
        Find an object in the cache, or if it is not registered, create.

        :param psp: Object passport.
        :param compare_guid: Compare GUID?
        :param register: Register in object cache.
        :return: Registered object or None if error.
        """
        if not psp:
            log_func.error(u'KERNEL. Not define object passport for getting')
            return None

        find_obj = self.findObject(psp, compare_guid=compare_guid)
        if find_obj:
            return find_obj

        return self.createObject(psp=psp, register=register, *args, **kwargs)

    def createObject(self, psp, register=False, *args, **kwargs):
        """
        Create object by passport.

        :param psp: Object passport.
        :param register: Register in object cache.
        :return: Registered object or None if error.
        """
        if not psp:
            log_func.error(u'KERNEL. Not define object passport for create')
            return None

        obj = self.createByPsp(psp=psp, *args, **kwargs)
        # log_func.info(u'Create object <%s : %s>' % (str(psp), str(obj)))
        if register:
            self._object_cache[psp] = obj
        return obj

    def printObjCache(self):
        """
        Print object cache.

        :return: True/False.
        """
        log_func.info(u'KERNEL. Object cache:')
        try:
            for psp, obj in self._object_cache.items():
                log_func.info(u'\t%s\t=\t%s' % (str(psp), str(obj)))
            return True
        except:
            log_func.fatal(u'Error print object cache')
        return False

    @property
    def obj(self):
        """
        Create an object access object by point.

        :return:
        """
        return objects_access.iqObjectDotUse()

    @property
    def settings(self):
        """
        Create an settings access object by point.

        :return:
        """
        return settings_access.iqSettingsDotUse()


def createKernel():
    """
    Create kernel object.

    :return: Kernel object.
    """
    kernel = iqKernel()
    global_data.setGlobal('KERNEL', kernel)

    import iq
    iq.KERNEL = kernel
    log_func.info(u'Create KERNEL object')
    return kernel
