#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base object class module.
"""

import os
import os.path

from . import object_context
from ..util import global_func
from ..util import spc_func
from ..util import log_func
from ..util import file_func
from ..util import imp_func
from ..util import py_func
from ..util import id_func

from .. import passport

__version__ = (0, 0, 2, 1)


class iqObject(object):
    """
    Base object class.
    """
    def __init__(self, parent=None, resource=None, spc=None, context=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param spc: Component specification.
        :param context: Context dictionary.
        :param args:
        :param kwargs:
        """
        self._parent = parent
        self._resource = spc_func.fillResourceBySpc(resource=resource, spc=spc)

        default_psp = dict(prj=global_func.getProjectName(),
                           module=self.getName(),
                           type=self.getType(),
                           name=self.getName())
        self._passport = passport.iqPassport().setAsDict(default_psp)

        self._children = None

        self._context = self.createContext(context)

    def destroy(self):
        """
        Destructor function.
        """
        pass

    def getName(self):
        """
        Object name.
        """
        res = self.getResource()
        if isinstance(res, dict):
            return res.get('name', u'Unknown')
        return u'Unknown'

    def getType(self):
        """
        Object type.
        """
        res = self.getResource()
        if isinstance(res, dict):
            return res.get('type', u'Unknown')
        return u'Unknown'

    def getGUID(self):
        """
        Object resource GUID.
        """
        res = self.getResource()
        if isinstance(res, dict):
            return res.get('guid', id_func.NONE_GUID)
        return id_func.NONE_GUID

    def isActivate(self):
        """
        Is activate object?
        :return: True/False.
        """
        return self.getAttribute('activate')

    def getDescription(self):
        """
        Object description.
        """
        res = self.getResource()
        if isinstance(res, dict):
            return res.get('description', u'')
        return u''

    def setPassport(self, psp=None):
        """
        Set object passport.

        :param psp: Object passport in any form.
        :return: Passport object.
        """
        self._passport = passport.iqPassport().setAsAny(psp)
        return self._passport

    def getPassport(self):
        """
        Get object passport.
        """
        return self._passport

    def newPassport(self):
        """
        Create new passport object.

        :return: Passport object.
        """
        return passport.iqPassport()

    def getParent(self):
        """
        Get parent object.
        """
        return self._parent

    def getResource(self):
        """
        Get object resource dictionary.
        """
        return self._resource

    def getModuleFilename(self):
        """
        Get resource python module filename by passport.

        :return: Resource python module filename or None if file not found.
        """
        psp = self.getPassport()
        res_filename = psp.findResourceFilename()
        if res_filename:
            module_filename = file_func.setFilenameExt(filename=res_filename, ext='.py')
            if os.path.exists(module_filename):
                return module_filename
        #     else:
        #         log_func.warning(u'Resource python module <%s> not found' % module_filename)
        # else:
        #     log_func.warning(u'Not define resource file of object <%s : %s>' % (self.getName(), self.getType()))
        return None

    def getModule(self, module_filename=None):
        """
        Get resource python module object.

        :param module_filename: Resource python module filename.
        :return: Module object or None if error.
        """
        if module_filename is None:
            module_filename = self.getModuleFilename()
        if module_filename and os.path.exists(module_filename):
            module = imp_func.importPyModule(import_name=self.getName(),
                                             import_filename=module_filename)
            return module
        return None

    def getContext(self):
        """
        Get context object.
        """
        if self._context:
            # Automatically add an object pointer to the context
            self._context.update(dict(self=self))
        return self._context

    def createContext(self, context=None):
        """
        Create object context.

        :param context: Context dictionary.
        :return: Context.
        """
        self._context = None
        if context is None:
            self._context = object_context.iqContext(root_obj=self,
                                                     kernel=self.getKernel())
        elif isinstance(context, dict):
            self._context = object_context.iqContext(root_obj=self,
                                                     kernel=self.getKernel())
            self._context.update(context)
        elif isinstance(context, object_context.iqContext):
            self._context = context

        if self._context:
            # Add resource module name space
            module = self.getModule()
            if module:
                module_dict = {name: getattr(module, name) for name in dir(module)}
                self._context.update(module_dict)
        return self._context

    def getKernel(self):
        """
        Get kernel object.
        """
        return self._context.getKernel() if self._context else global_func.getKernel()

    def getAttribute(self, attribute_name):
        """
        Get attribute from resource.

        :param attribute_name: Attribute name.
        :return: Attribute value.
        """
        value = self._resource.get(attribute_name, None) if self._resource else None
        return value

    def isAttributeValue(self, attribute_name):
        """
        Defined attribute value?

        :param attribute_name: Attribute name.
        :return: True/False.
        """
        attr_value = self.getAttribute(attribute_name)
        if isinstance(attr_value, str):
            return attr_value.strip() not in ('None', '')
        return attr_value is not None

    def getChildren(self):
        """
        Get children objects.
        """
        if self._children is None:
            self._children = self.createChildren()
        return self._children

    def hasChildren(self):
        """
        Has children objects?

        :return: True/False.
        """
        return bool(self._children)

    def createChildren(self):
        """
        Create children objects.

        :return: Children list or None if error.
        """
        try:
            res_children = self._resource.get(spc_func.CHILDREN_ATTR_NAME, list())
            kernel = self.getKernel()
            context = self.getContext()

            # Create only activated children
            self._children = [kernel.createByResource(parent=self,
                                                      resource=res_child,
                                                      context=context) for res_child in res_children if res_child.get('activate', True)]
            return self._children
        except:
            log_func.fatal(u'Error create children obj object <%s : %s>' % (self.getName(), self.getType()))
        return list()

    def hasChild(self, name):
        """
        Is there a child with that name?

        :param name: Child object name.
        :return: True/False.
        """
        res_children = self._resource.get(spc_func.CHILDREN_ATTR_NAME, list())
        return name in [res_child.get('name', None) for res_child in res_children]

    def getChild(self, name):
        """
        Get child object by name.

        :param name: Child object name.
        :return: Child object or None if not found.
        """
        children = self.getChildren()

        for child in children:
            if name == child.getName():
                return child

        log_func.warning(u'Child <%s> not found in <%s : %s>' % (name, self.getName(), self.getType()))
        return None

    def findChild(self, name):
        """
        Find child object recursively by name.

        :param name: Child object name.
        :return: Child object or None if not found.
        """
        children = self.getChildren()

        for child in children:
            if name == child.getName():
                return child

        for child in children:
            if child.hasChildren():
                find_child = child.findChild(name)
                if find_child:
                    return find_child

        return None

    def filterChildrenByClass(self, child_class):
        """
        Filter child list by class.

        :param child_class: Child class.
        :return: Child list of child class.
        """
        children = self.getChildren()
        return [child for child in children if issubclass(child.__class__, child_class)]

    def test(self):
        """
        Test object.

        :return: True/False.
        """
        log_func.warning(u'Not defined test function for component <%s : %s>' % (self.getName(), self.getType()))
        return False
