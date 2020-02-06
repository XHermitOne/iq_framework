#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python script generate functions.
"""

import os.path

from . import txtfile_func
from . import log_func

__version__ = (0, 0, 0, 1)


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
            log_func.fatal(u'Create directory <%s> error' % package_path)
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
