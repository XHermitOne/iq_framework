#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Display control manager on geo-maps.
Implemented on the basis 2GIS.
API documentation 2GIS https://api.2gis.ru/doc/maps/ru/quickstart/.

Spots, markers, coverage circles, etc. can serve as an indicator.

Yandex is used as a system for determining geolocation by address.
"""

from . import map_indicator

from . import double_gis

__version__ = (0, 0, 0, 1)


class iq2GISMapIndicatorManagerProto(map_indicator.iqMapIndicatorManagerProto):
    """
    2GIS map indicator manager.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        map_indicator.iqMapIndicatorManagerProto.__init__(self, *args, **kwargs)

        self.setRendering(double_gis)
