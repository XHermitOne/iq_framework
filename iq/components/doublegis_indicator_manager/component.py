#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2GIS map indicator manager component.
"""

from ... import object
# from ... import passport

from . import spc

# from ...util import log_func

from . import double_gis_map_indicator_manager

__version__ = (0, 0, 0, 1)


class iqDoubleGISMapIndicatorManager(double_gis_map_indicator_manager.iq2GISMapIndicatorManagerProto,
                                     object.iqObject):
    """
    2GIS map indicator manager.
    """
    def __init__(self, parent=None, resource=None, context=None, *args, **kwargs):
        """
        Standard component constructor.

        :param parent: Parent object.
        :param resource: Object resource dictionary.
        :param context: Context dictionary.
        """
        component_spc = kwargs['spc'] if 'spc' in kwargs else spc.SPC
        object.iqObject.__init__(self, parent=parent, resource=resource, spc=component_spc, context=context)

        double_gis_map_indicator_manager.iq2GISMapIndicatorManagerProto.__init__(self)


COMPONENT = iqDoubleGISMapIndicatorManager
