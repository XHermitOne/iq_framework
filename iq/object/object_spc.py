#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Object specification module.
"""

import os.path

from ..util import file_func
from ..util import py_func
from ..util import spc_func

from ..editor import property_editor_id

__version__ = (0, 0, 1, 1)


def genModule(module_filename=None, resource=None):
    """
    Generate object module.

    :param module_filename: Module filename
    :param resource: Resource dictionary.
    :return: True/False.
    """
    package_path = os.path.dirname(module_filename)
    py_modulename = file_func.setFilenameExt(os.path.basename(module_filename), '.py')
    module_doc = resource.get(spc_func.DESCRIPTION_ATTR_NAME, u'') if resource else u''
    return py_func.createPyModule(package_path=package_path, py_modulename=py_modulename, rewrite=True, module_doc=module_doc)


OBJECT_SPC = {
    'name': 'default',
    'type': 'iqObjectProto',
    'description': '',
    'activate': True,
    'guid': None,
    'module': None,

    '_children_': [],

    '__icon__': None,
    '__gen_module__': genModule,
    '__doc__': None,
    '__help__': {
        'name': u'Object name',
        'type': u'Object type',
        'description': u'Description',
        'activate': u'Activate trigger',
        'guid': u'Global object identifier',
        'module': u'Resource python module',
    },
    '__edit__': {
        'name': property_editor_id.STRING_EDITOR,
        'type': property_editor_id.READONLY_EDITOR,
        'description': property_editor_id.TEXT_EDITOR,
        'activate': property_editor_id.CHECKBOX_EDITOR,
        'guid': property_editor_id.READONLY_EDITOR,
        'module': property_editor_id.READONLY_EDITOR,
    },
    '__content__': (),

    '__test__': None,       # Test function
    '__design__': None,     # Design function
}
