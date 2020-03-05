#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python script generate functions.
"""

import os.path

from . import txtfile_func
from . import log_func
from . import file_func

__version__ = (0, 0, 0, 1)


PYTHON_FILE_EXT = '.py'

INIT_PY_FILENAME = '__init__.py'

DEFAULT_INIT_PY = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
.
\"\"\"

__version__ = (0, 0, 0, 1)
'''


def createInitModule(package_path, init_file_body=None):
    """
    Create __init__.py python module file.

    :param package_path: Package path.
    :param init_file_body: Text __init__.py.
        If None then write default __init__.py file text.
    :return: True/False.
    """
    if not package_path:
        log_func.warning(u'Not define package path for create __init__.py file')
        return False

    if init_file_body is None:
        init_file_body = DEFAULT_INIT_PY

    if not os.path.exists(package_path):
        try:
            os.makedirs(package_path)
        except OSError:
            log_func.fatal(u'Error create directory <%s>' % package_path)
            return False

    init_py_filename = os.path.join(package_path, INIT_PY_FILENAME)
    return txtfile_func.saveTextFile(init_py_filename, init_file_body)


def createPackage(package_path):
    """
    Create python package.

    :param package_path: Package path.
    :return: True/False.
    """
    return createInitModule(package_path)


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
