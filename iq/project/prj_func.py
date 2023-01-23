#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project functions.
"""

import os
import os.path

from ..util import file_func
from ..util import imp_func

__version__ = (0, 0, 0, 1)

NOT_PROJECT_NAMES = ('iq', 'locale', 'ide')


def getProjectNames():
    """
    Get all project names in framework.

    :return: Project names list.
    """
    framework_path = file_func.getFrameworkPath()

    prj_paths = [os.path.join(framework_path, dirname) for dirname in os.listdir(framework_path) if dirname not in file_func.HIDDEN_DIRNAMES and dirname not in NOT_PROJECT_NAMES]
    prj_paths = [dirpath for dirpath in prj_paths if os.path.isdir(dirpath)]
    prj_names = [os.path.basename(dirpath) for dirpath in prj_paths]
    return prj_names


def getProjectDescriptions():
    """
    Get all project descriptions in framework.

    :return: Dictionary:
        {
        'project1 name': u'Project description',
        ...
        }
    """
    framework_path = file_func.getFrameworkPath()

    prj_paths = [os.path.join(framework_path, dirname) for dirname in os.listdir(framework_path) if dirname not in file_func.HIDDEN_DIRNAMES and dirname not in NOT_PROJECT_NAMES]
    prj_paths = [dirpath for dirpath in prj_paths if os.path.isdir(dirpath)]

    prj_descriptions = dict()
    for dirpath in prj_paths:
        prj_name = os.path.basename(dirpath)
        pkg = imp_func.importPyModule(import_name='prj_package',
                                      import_filename=dirpath,
                                      reimport=True)
        try:
            prj_description = pkg.__doc__.strip().splitlines()[0]
        except:
            prj_description = u''
        prj_descriptions[prj_name] = prj_description

    return prj_descriptions
