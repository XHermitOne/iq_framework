#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support for access to local design configuration through a point.

Project locals are stored in the *.ini project file:
$HOME/.iq/<Project Dir>/<Project Name>.ini
"""

import os
import os.path

from iq.util import file_func
from iq.util import global_func
from iq.util import ini_func
from iq.util import log_func
from iq.util import exec_func

from iq.passport import passport

__version__ = (0, 0, 0, 1)


class iqLocalsDotUseProto(object):
    """
    Project locals access support class.
    """
    def __init__(self, default_locals=None):
        """
        Constructor.

        :param default_locals: Point-by-point locals list.
            The list consists of 3 items.:
            0 - project name.
            1 - section name.
            2 - parameter name.
        """
        if default_locals:
            self._cur_locals_list = default_locals
        else:
            self._cur_locals_list = [None, None, None]
        
    def _getINIFilename(self):
        """
        Determine the full name of the locals file from the project name.
        """
        prj_profile_path = file_func.getProjectProfilePath()
        if prj_profile_path:
            ini_filename = os.path.join(prj_profile_path, self._cur_locals_list[0] + '.ini')
        else:
            prj_name = self._cur_locals_list[0]
            profile_path = file_func.getProfilePath()
            ini_filename = os.path.join(profile_path, prj_name, '%s.ini' % prj_name)
        return ini_filename
    
    def get(self):
        """
        Value retrieval function.
        """
        return None
    
    def set(self, value):
        """
        Value save function.

        :param value: Value.
        """
        return None


class iqLocalsDotUse(iqLocalsDotUseProto):
    """
    Class for the description of project locals.
    To access the project locals through the point.
    """
    THIS_PRJ = passport.DEFAULT_THIS_PROJECT_NAME

    def __init__(self, default_locals=None):
        """
        Constructor.
        """
        iqLocalsDotUseProto.__init__(self, default_locals)

    def __getattribute__(self, attribute_name):
        """
        Support for access to project locals through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            

        prj = iqPrjDotUse(object.__getattribute__(self, '_cur_locals_list'))

        if attribute_name == object.__getattribute__(self, 'THIS_PRJ'):
            prj._cur_locals_list[0] = global_func.getProjectName()
        else:
            prj._cur_locals_list[-1] = attribute_name
            
        return prj


class iqPrjDotUse(iqLocalsDotUseProto):
    """
    Class of the project. To access the project locals through the point.
    """
    def __init__(self, default_locals=None):
        """
        Constructor.
        """
        iqLocalsDotUseProto.__init__(self, default_locals)

    def __getattribute__(self, attribute_name):
        """
        Support for access to sections of the configuration file through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        section = iqSectionDotUse(object.__getattribute__(self, '_cur_locals_list'))
        section._cur_locals_list[1] = attribute_name
        return section

    def get(self):
        """
        The function of getting the value.
        """
        ini_filename = self._getINIFilename()
        return ini_func.INI2Dict(ini_filename)
    
    def set(self, value):
        """
        The function of saving the value.

        :param value: Value.
        """
        if isinstance(value, dict):
            ini_filename = self._getINIFilename()
            return ini_func.Dict2INI(value, ini_filename, True)
        return None

    def edit(self):
        """
        Start editing the INI locals file.
        """
        ini_filename = self._getINIFilename()
        if os.path.exists(ini_filename):
            cmd = 'gedit %s &' % ini_filename
            exec_func.execSystemCommand(cmd)
        else:
            log_func.warning(u'INI file <%s> not found' % ini_filename)


class iqSectionDotUse(iqLocalsDotUseProto):
    """
    The section class of the project setup file.
    To access the project locals through the point.
    """
    def __init__(self, default_locals=None):
        """
        Constructor.
        """
        iqLocalsDotUseProto.__init__(self, default_locals)

    def __getattribute__(self, attribute_name):
        """
        Support access to locals file locals through point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        param = iqParamDotUse(object.__getattribute__(self, '_cur_locals_list'))
        param._cur_locals_list[2] = attribute_name
        return param

    def get(self):
        """
        The function of getting the value.
        """
        ini_filename = self._getINIFilename()
        locals_dict = ini_func.INI2Dict(ini_filename)
        if self._cur_locals_list[1] in locals_dict:
            return locals_dict[self._cur_locals_list[1]]
        return None
    
    def set(self, value):
        """
        The function of saving the value.

        :param value: Value.
        """
        if isinstance(value, dict):
            ini_filename = self._getINIFilename()
            locals_dict = ini_func.INI2Dict(ini_filename)
            locals_dict[self._cur_locals_list[1]] = value
            return ini_func.Dict2INI(locals_dict, ini_filename, True)
        return None


class iqParamDotUse(iqLocalsDotUseProto):
    """
    Project setup file parameter class.
    To access the project locals through the point.
    """
    def __init__(self, default_locals=None):
        """
        Конструктор.
        """
        iqLocalsDotUseProto.__init__(self, default_locals)

    def get(self):
        """
        The function of getting the value.
        """
        ini_filename = self._getINIFilename()
        value = ini_func.loadParamINI(ini_filename, self._cur_locals_list[1], self._cur_locals_list[2])
        value = u'' if value is None else value
        return value

    def set(self, value):
        """
        The function of saving the value.

        :param value: Value.
        """
        ini_filename = self._getINIFilename()
        return ini_func.saveParamINI(ini_filename, self._cur_locals_list[1], self._cur_locals_list[2], value)

    def value(self):
        """
        Get the value.
        An attempt is made to convert the type.

        :return:
        """
        str_value = self.get()
        try:
            value = eval(str_value)
        except:
            value = str_value
        return value
