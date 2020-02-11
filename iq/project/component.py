#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project manager component.
"""

from .. import object

from . import spc
from . import prj

__version__ = (0, 0, 0, 1)


class iqProject(object.iqObject, prj.iqProjectManager):
    """
    Project manager component.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standart component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        object.iqObject.__init__(parent=parent, resource=resource, spc=spc.SPC, context=context)
        prj.iqProjectManager.__init__(self, *args, **kwargs)

COMPONENT = iqProject