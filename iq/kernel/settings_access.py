#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support for access to system design configuration through a point.

Project settings are stored in the * .ini project file:
<Framework path>/<Project Dir>/<Project Name>.ini
"""

import os
import os.path

from iq.util import file_func
from iq.util import global_func
from iq.util import ini_func
from iq.util import log_func
from iq.util import exec_func

from iq.passport import passport

__version__ = (0, 1, 2, 1)


class iqSettingsDotUseProto(object):
    """
    Project settings access support class.
    """
    def __init__(self, default_settings=None):
        """
        Constructor.

        :param default_settings: Point-by-point settings list.
            The list consists of 3 items.:
            0 - project name.
            1 - section name.
            2 - parameter name.
        """
        # log_func.debug(u'Default settings: %s' % default_settings)
        if default_settings:
            self._cur_settings_list = default_settings
        else:
            self._cur_settings_list = [None, None, None]
        
    def _getINIFilename(self):
        """
        Determine the full name of the settings file from the project name.
        """
        prj_name = self._cur_settings_list[0]
        root_path = file_func.getFrameworkPath()
        # log_func.debug(u'Project path <%s>. Project name <%s>' % (prj_path, prj_name))
        if root_path:
            ini_filename = os.path.join(root_path, prj_name, prj_name + '.ini')
        else:
            ini_filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                        prj_name, '%s.ini' % prj_name)
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


class iqSettingsDotUse(iqSettingsDotUseProto):
    """
    Class for the description of project settings.
    To access the project settings through the point.
    """
    THIS_PRJ = passport.DEFAULT_THIS_PROJECT_NAME

    def __init__(self, default_settings=None):
        """
        Constructor.
        """
        iqSettingsDotUseProto.__init__(self, default_settings)

    def __getattribute__(self, attribute_name):
        """
        Support for access to project settings through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            

        prj = iqPrjDotUse(object.__getattribute__(self, '_cur_settings_list'))
        # log_func.debug(u'Settings. Attribute name: %s. Current settings list %s' % (attribute_name, prj._cur_settings_list))
        if attribute_name == object.__getattribute__(self, 'THIS_PRJ'):
            prj._cur_settings_list[0] = global_func.getProjectName()
        else:
            prj._cur_settings_list[0] = attribute_name
            
        return prj


class iqPrjDotUse(iqSettingsDotUseProto):
    """
    Class of the project. To access the project settings through the point.
    """
    def __init__(self, default_settings=None):
        """
        Constructor.
        """
        iqSettingsDotUseProto.__init__(self, default_settings)

    def __getattribute__(self, attribute_name):
        """
        Support for access to sections of the configuration file through the point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        section = iqSectionDotUse(object.__getattribute__(self, '_cur_settings_list'))
        section._cur_settings_list[1] = attribute_name
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
        Start editing the INI settings file.
        """
        ini_filename = self._getINIFilename()
        if os.path.exists(ini_filename):
            cmd = 'gedit %s &' % ini_filename
            exec_func.execSystemCommand(cmd)
        else:
            log_func.warning(u'INI file <%s> not found' % ini_filename)

    def find_section(self, section_name):
        """
        Find section in INI settings file by name.

        :param section_name: Search section name.
        :return: Section dictionary or None if it not found.
        """
        ini_filename = self._getINIFilename()
        ini_dict = ini_func.INI2Dict(ini_filename)
        return ini_dict.get(section_name, None)

    def set_param(self, section_name, param_name, value):
        """
        Set parameter value.

        :param section_name: Section name.
        :param param_name: Prameter name.
        :param value: Parameter value.
        :return: True/False.
        """
        ini_filename = self._getINIFilename()
        return ini_func.saveParamINI(ini_filename=ini_filename,
                                     section_name=section_name,
                                     param_name=param_name,
                                     param_value=value)


class iqSectionDotUse(iqSettingsDotUseProto):
    """
    The section class of the project setup file.
    To access the project settings through the point.
    """
    def __init__(self, default_settings=None):
        """
        Constructor.
        """
        iqSettingsDotUseProto.__init__(self, default_settings)

    def __getattribute__(self, attribute_name):
        """
        Support access to settings file settings through point.
        """
        try:
            return object.__getattribute__(self, attribute_name)
        except AttributeError:
            pass            
            
        param = iqParamDotUse(object.__getattribute__(self, '_cur_settings_list'))
        param._cur_settings_list[2] = attribute_name
        return param

    def get(self):
        """
        The function of getting the value.
        """
        ini_filename = self._getINIFilename()
        settings_dict = ini_func.INI2Dict(ini_filename)
        if self._cur_settings_list[1] in settings_dict:
            return settings_dict[self._cur_settings_list[1]]
        return None
    
    def set(self, value):
        """
        The function of saving the value.

        :param value: Value.
        """
        if isinstance(value, dict):
            ini_filename = self._getINIFilename()
            settings_dict = ini_func.INI2Dict(ini_filename)
            settings_dict[self._cur_settings_list[1]] = value
            return ini_func.Dict2INI(settings_dict, ini_filename, True)
        return None

    def find_param(self, param_name):
        """
        Find parameter in section by name.

        :param param_name: Search parameter name.
        :return: Parameter value or None if it not found.
        """
        ini_filename = self._getINIFilename()
        settings_dict = ini_func.INI2Dict(ini_filename)
        if self._cur_settings_list[1] in settings_dict:
            return settings_dict[self._cur_settings_list[1]].get(param_name, None)
        return None


class iqParamDotUse(iqSettingsDotUseProto):
    """
    Project setup file parameter class.
    To access the project settings through the point.
    """
    def __init__(self, default_settings=None):
        """
        Конструктор.
        """
        iqSettingsDotUseProto.__init__(self, default_settings)

    def get(self):
        """
        The function of getting the value.
        """
        ini_filename = self._getINIFilename()
        value = ini_func.loadParamINI(ini_filename, self._cur_settings_list[1], self._cur_settings_list[2])
        value = u'' if value is None else value
        return value

    def set(self, value):
        """
        The function of saving the value.

        :param value: Value.
        """
        ini_filename = self._getINIFilename()
        return ini_func.saveParamINI(ini_filename, self._cur_settings_list[1], self._cur_settings_list[2], value)

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
