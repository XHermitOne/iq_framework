#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
New resource dialog class module.
"""

from . import new_resource_dlg

from ....util import log_func

__version__ = (0, 0, 0, 1)


class iqNewResourceDialog(new_resource_dlg.iqNewResourceDialogProto):
    """
    New resource dialog class module.
    """
    def __init__(self, parent=None, *args, **kwargs):
        """
        Constructor.

        :param parent: Parent window object.
        """
        new_resource_dlg.iqNewResourceDialogProto.__init__(self, parent=parent)


def createNewResource(component_spc=None, component_name=None, res_filename=None):
    """
    Create new resource.

    :param component_spc: Resource component specification.
    :param component_name: Component name.
    :param res_filename: Resource filename.
    :return: True/False.
    """
    try:
        return True
    except:
        log_func.fatal(u'Create new resource error')
    return False
