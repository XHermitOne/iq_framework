#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User functions module for working with INI files.

ATTENTION! In the INI file, the parameter names are written in lowercase
and the section names in the upper.
"""

import os
import os.path

from . import log_func

try:
    import configparser
except ImportError:
    log_func.error('Import error configparser', is_force_print=True)

__version__ = (0, 0, 0, 1)

INI_FILE_EXT = '.ini'
DEFAULT_ENCODE = 'utf-8'


def loadParamINI(ini_filename, section_name, param_name):
    """
    Reading the parameter from the settings file.

    :type ini_filename: C{string}
    :param ini_filename: Full name of the settings file.
    :type section_name: C{string}
    :param section_name: Section name.
    :type param_name: C{string}
    :param param_name: The name of the parameter.
    :return: Returns the value of the parameter or None (if there is no parameter or error).
    """
    try:
        param = None
        ini_parser = configparser.ConfigParser()
        ini_parser.read(ini_filename)
        if ini_parser.has_section(section_name) and ini_parser.has_option(section_name, param_name):
            param = ini_parser.get(section_name, param_name)
        return param
    except:
        log_func.fatal(u'Error loading parameter [%s.%s] from INI file <%s>' % (section_name, param_name, ini_filename))
    return None


def loadParamINIValue(*args, **kwargs):
    """
    Reading the parameter from the settings file.

    :return: An attempt is made to convert from a return string to a real type by means of <eval>.
        If an error occurs during the conversion, then a string is returned.
    """
    param = loadParamINI(*args, **kwargs)
    try:
        value = eval(param)
    except:
        value = param
    return value


def saveParamINI(ini_filename, section_name, param_name, param_value):
    """
    Writing a parameter to the settings file.

    :type ini_filename: C{string}
    :param ini_filename: The full name of the settings file.
    :type section_name: C{string}
    :param section_name: Section name.
    :type param_name: C{string}
    :param param_name: Parameter name.
    :param param_value: Parameter value.
    :return: Returns the result of the operation True/False.
    """
    ini_file = None
    try:
        ini_file_name = os.path.split(ini_filename)
        path = ini_file_name[0]
        # base_filename = ini_file_name[1]
        if not os.path.isdir(path):
            os.makedirs(path)

        # If there is no ini file, then _create it
        if not os.path.isfile(ini_filename):
            ini_file = open(ini_filename, 'wt')
            ini_file.write('')
            ini_file.close()
            
        # Create configuration object
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # If there is no such section, then _create it.
        if not ini_parser.has_section(section_name):
            ini_parser.add_section(section_name)

        if not isinstance(param_value, str):
            param_value = str(param_value)
        ini_parser.set(section_name, param_name, param_value)

        # Save and close file
        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        return True
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'Error saving parameter [%s.%s] in the INI file <%s>' % (section_name, param_name, ini_filename))
    return False


def delParamINI(ini_filename, section_name, param_name):
    """
    Remove parameter from configuration file section.

    :type ini_filename: C{string}
    :param ini_filename: The full name of the settings file.
    :type section_name: C{string}
    :param section_name: Section name.
    :type param_name: C{string}
    :param param_name: Parameter name.
    :return: Returns the result of the operation True/False.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log_func.warning(u'INI file <%s> not found' % ini_filename)
            return False
            
        # Create configuration object
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        # If there is no such section
        if not ini_parser.has_section(section_name):
            log_func.warning(u'Section [%s] does not exist in the file <%s>' % (section_name, ini_filename))
            return False

        ini_parser.remove_option(section_name, param_name)

        # Save and close file
        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()

        return True
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'Error deleting parameter [%s.%s] from INI file <%s>' % (section_name, param_name, ini_filename))
    return False


def getParamCountINI(ini_filename, section_name):
    """
    Number of parameters in the section.

    :type ini_filename: C{string}
    :param ini_filename: Full name of the settings file.
    :type section_name: C{string}
    :param section_name: Section Name.
    :return: Returns the quantities of the parameters in the section or -1 in case of an error.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log_func.warning(u'INI file <%s> not found' % ini_filename)
            return 0
            
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        if not ini_parser.has_section(section_name):
            log_func.warning(u'Section [%s] does not exist in the file <%s>' % (section_name, ini_filename))
            return 0
        return len(ini_parser.options(section_name))
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'INI file <%s>. Error determining the number of section parameters [%s]' % (ini_filename, section_name))
    return -1


def getParamNamesINI(ini_filename, section_name):
    """
    Parameter names in the section.

    :type ini_filename: C{string}
    :param ini_filename: Full name of the settings file.
    :type section_name: C{string}
    :param section_name: Section name.
    :return: Returns a list of parameter names in a section or None in case of an error.
    """
    ini_file = None
    try:
        if not os.path.isfile(ini_filename):
            log_func.warning(u'INI file <%s> not found' % ini_filename)
            return None
            
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        if not ini_parser.has_section(section_name):
            log_func.warning(u'Section [%s] does not exist in the file <%s>' % (section_name, ini_filename))
            return []
        return ini_parser.options(section_name)
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'INI file <%s>. Error defining section parameter names [%s]' % (ini_filename, section_name))
    return None


def INI2Dict(ini_filename):
    """
    Presentation of the contents of an INI file as a dictionary.

    :type ini_filename: C{string}
    :param ini_filename: Full name of the settings file.
    :return: Filled dictionary or None in case of error.
    """
    ini_file = None
    try:
        if not os.path.exists(ini_filename):
            log_func.warning(u'INI file <%s> not found' % ini_filename)
            return None
            
        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()
        
        ini_dict = {}
        sections = ini_parser.sections()
        for section in sections:
            params = ini_parser.options(section)
            ini_dict[section] = {}
            for param in params:
                param_str = ini_parser.get(section, param)
                try:
                    # Perhaps in the form of a parameter is recorded a dictionary / list / None / number, etc.
                    param_value = eval(param_str)
                except:
                    # No, it's a string.
                    param_value = param_str
                ini_dict[section][param] = param_value
        
        return ini_dict
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'Error converting INI file <%s> to dictionary' % ini_filename)
    return None


def Dict2INI(src_dictionary, ini_filename, rewrite=False):
    """
    View / write dictionary as INI file.

    :type src_dictionary: C{dictionary}
    :param src_dictionary: Source dictionary.
    :type ini_filename: C{string}
    :param ini_filename: Full name of the settings file.
    :param rewrite: Overwrite fully existing INI file?
    :return: Returns the result of saving True/False.
    """
    ini_file = None
    try:
        if not src_dictionary:
            log_func.warning(u'No dictionary defined for saving to INI file. <%s>' % src_dictionary)
            return False

        ini_file_name = os.path.split(ini_filename)
        path = ini_file_name[0]
        if not os.path.isdir(path):
            os.makedirs(path)

        if not os.path.exists(ini_filename) or rewrite:
            ini_file = open(ini_filename, 'wt')
            ini_file.write('')
            ini_file.close()

        ini_parser = configparser.ConfigParser()
        ini_file = open(ini_filename, 'rt')
        ini_parser.readfp(ini_file)
        ini_file.close()

        for section in src_dictionary.keys():
            section_str = str(section)
            if not ini_parser.has_section(section_str):
                ini_parser.add_section(section_str)

            for param in src_dictionary[section].keys():
                ini_parser.set(section_str, str(param), str(src_dictionary[section][param]))

        ini_file = open(ini_filename, 'wt')
        ini_parser.write(ini_file)
        ini_file.close()
        
        return True
    except:
        if ini_file:
            ini_file.close()
        log_func.fatal(u'Error saving dictionary in INI file <%s>' % ini_filename)
    return False
