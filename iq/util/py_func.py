#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python script generate functions.
"""

import os.path

from . import txtfile_func
from . import log_func
from . import file_func

__version__ = (0, 0, 1, 1)


PYTHON_FILE_EXT = '.py'

INIT_PY_FILENAME = '__init__.py'

DEFAULT_PY_FMT = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
%s.
\"\"\"

__version__ = (0, 0, 0, 1)
'''


def getInitPyFilename(package_path):
    """
    Get __init__.py full filename.

    :param package_path: Package path.
    :return: __init__.py full filename.
    """
    return os.path.join(package_path, INIT_PY_FILENAME)


def isFolderPyPackage(folder_path):
    """
    Is the folder a Python package?

    :param folder_path: Folder path.
    :return: True/False.
    """
    init_py_filename = getInitPyFilename(folder_path)
    return os.path.exists(init_py_filename)


def createPyModule(package_path, py_modulename=None, py_file_body=None, rewrite=False, module_doc=u''):
    """
    Create py_modulename.py python module file.

    :param package_path: Package path.
    :param py_modulename: Module filename.
    :param py_file_body: Text python module file.
        If None then write default python file text.
    :param rewrite: Rewrite file if it exists?
    :param module_doc: Module documentation.
    :return: True/False.
    """
    if not package_path:
        log_func.warning(u'Not define package path for create python file')
        return False

    if py_file_body is None:
        py_file_body = DEFAULT_PY_FMT % module_doc

    if not os.path.exists(package_path):
        try:
            os.makedirs(package_path)
        except OSError:
            log_func.fatal(u'Error create directory <%s>' % package_path)
            return False

    py_filename = os.path.join(package_path, py_modulename)
    return txtfile_func.saveTextFile(py_filename, py_file_body, rewrite=rewrite)


def createInitModule(package_path, init_file_body=None, rewrite=False, module_doc=u''):
    """
    Create __init__.py python module file.

    :param package_path: Package path.
    :param init_file_body: Text __init__.py.
        If None then write default __init__.py file text.
    :param rewrite: Rewrite file if it exists?
    :param module_doc: Module documentation.
    :return: True/False.
    """
    return createPyModule(package_path=package_path, py_modulename=INIT_PY_FILENAME,
                          py_file_body=init_file_body, rewrite=rewrite, module_doc=module_doc)


def createPackage(package_path, module_doc=u''):
    """
    Create python package.

    :param package_path: Package path.
    :param module_doc: Init module documentation.
    :return: True/False.
    """
    return createInitModule(package_path, module_doc=module_doc)


def isPythonFile(filename):
    """
    Check if the file is python module.

    :param filename: Checked file path.
    :return: True/False.
    """
    return file_func.isFilenameExt(filename, PYTHON_FILE_EXT)


def isPyFileSignature(py_filename, signature):
    """
    Is there a signature in the python file?

    :param py_filename: Python file path.
    :param signature: Signature text.
    :return: True/False.
    """
    if not isPythonFile(py_filename):
        log_func.warning(u'File <%s> is not python module' % py_filename)
        return False

    py_file = None
    try:
        py_file = open(py_filename, 'rt')
        text = py_file.read()
        py_file.close()
        return text.find(signature) != -1
    except:
        log_func.fatal(u'Error searching signature <%s> in python file <%s>.' % (signature, py_filename))
        if py_file:
            py_file.close()
    return False
