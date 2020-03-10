#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support for access to metadata of system resources through a point.
"""

from ..util import global_func
from ..util import log_func

from ..passport import passport
from ..object import object_context

__version__ = (0, 0, 0, 1)


class iqMetaDotUseProto(object):
    """
    Support class for access to metadata.
    """
    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        if default_passport:
            self._cur_passport = default_passport
        else:
            self._cur_passport = passport.iqPassport()

    def create(self, parent=None, *arg, **kwarg):
        """
        Create selected object.
        """
        kernel = global_func.getKernel()
        if kernel:
            if 'context' in kwarg:
                if isinstance(kwarg['context'], dict):
                    context = object_context.iqContext(kernel=kernel)
                    context.update(kwarg['context'])
                else:
                    context = kwarg['context']
                del kwarg['context']
            else:
                context = object_context.iqContext(kernel=kernel)
            return kernel.createObject(psp=self.passport(), parent=parent, context=context, *arg, **kwarg)
        else:
            log_func.error(u'Kernel object not defined')
        return None

    def get(self, parent=None, *arg, **kwarg):
        """
        Get an object.
        """
        kernel = global_func.getKernel()
        if kernel:
            psp = self.passport()
            obj = kernel.findObject(psp)
            if obj:
                return obj

            if 'context' in kwarg:
                if isinstance(kwarg['context'], dict):
                    context = object_context.iqContext(kernel=kernel)
                    context.update(kwarg['context'])
                else:
                    context = kwarg['context']
                del kwarg['context']
            else:
                context = object_context.iqContext(kernel=kernel)
            return kernel.createObject(psp=self.passport(), parent=parent, context=context, *arg, **kwarg)
        else:
            log_func.error(u'Kernel object not defined')
        return None

    def passport(self):
        """
        Getting a passport of the selected object.
        """
        return self._cur_passport


class iqObjectDotUse(iqMetaDotUseProto):
    """
    Metadata Description Class.
    To access meta descriptions through the dot.
    """
    THIS_PRJ = passport.DEFAULT_THIS_PROJECT_NAME

    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        iqMetaDotUseProto.__init__(self, default_passport)

    def __getattribute__(self, attribute_name):
        """
        Support for access to meta descriptions through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            

        prj = iqPrjDotUse(object.__getattribute__(self, '_cur_passport'))

        if attribute_name == object.__getattribute__(self, 'THIS_PRJ'):
            prj._cur_passport.prj = global_func.getProjectName()
        else:
            prj._cur_passport.prj = attribute_name
            
        return prj


class iqPrjDotUse(iqMetaDotUseProto):
    """
    Class of the project. 
    To access meta descriptions through the dot.
    """
    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        iqMetaDotUseProto.__init__(self, default_passport)

    def __getattribute__(self, attribute_name):
        """
        Support for access to meta descriptions through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        res_name = iqResNameDotUse(object.__getattribute__(self, '_cur_passport'))
        
        res_name._cur_passport.module = attribute_name
        return res_name


class iqResNameDotUse(iqMetaDotUseProto):
    """
    The resource name class.
    To access meta descriptions through the dot.
    """
    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        iqMetaDotUseProto.__init__(self, default_passport)

    def __getattribute__(self, attribute_name):
        """
        Support for access to meta descriptions through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        obj_type = iqObjTypeDotUse(object.__getattribute__(self, '_cur_passport'))
        
        obj_type._cur_passport.typename = attribute_name
            
        return obj_type


class iqObjTypeDotUse(iqMetaDotUseProto):
    """
    The type class of the object.
    To access meta descriptions through the dot.
    """
    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        iqMetaDotUseProto.__init__(self, default_passport)

    def __getattribute__(self, attribute_name):
        """
        Support for access to meta descriptions through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        obj_name = iqObjNameDotUse(object.__getattribute__(self, '_cur_passport'))
        obj_name._cur_passport.name = attribute_name
        return obj_name


class iqObjNameDotUse(iqMetaDotUseProto):
    """
    The class of the name of the object.
    To access meta descriptions through the dot.
    """
    def __init__(self, default_passport=None):
        """
        Constructor.
        """
        iqMetaDotUseProto.__init__(self, default_passport)
