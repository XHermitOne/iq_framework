#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migrate wxFormBuilder project files.
"""

import sys
import os
import os.path

from ..util import log_func

from . import migrate_py

__version__ = (0, 0, 0, 1)

MIGRATE_REPLACES = ()


def migrateFBP(fbp_filename, *args, **kwargs):
    """
    Make wxFormBuilder project module migration replacements.

    :param fbp_filename: Python file path.
    :return: True/False.
    """
    if not os.path.exists(fbp_filename) or not os.path.isfile(fbp_filename):
        log_func.error(u'wxFormBuilder project file <%s> not found' % fbp_filename)
        return False

    result = migrate_py.migrateTxtFile(fbp_filename, migrate_replaces=MIGRATE_REPLACES,
                                       *args, **kwargs)
    if result:
        log_func.info(u'Migration wxFormBuilder project file <%s> ... OK' % fbp_filename)
    else:
        log_func.error(u'Migration wxFormBuilder project file <%s> ... FAIL' % fbp_filename)
    return result


if __name__ == '__main__':
    migrateFBP(*sys.argv[1:])
